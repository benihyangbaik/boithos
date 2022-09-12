# TODO: Deal with verse ranges.

from subprocess import run
from threading import Thread
import os
import shutil
import sys

import prepare_corpora as pc

# Tokenization and BPE data compression scripts.
SCRIPTS = '../../lib/mosesdecoder/scripts'
TOKENIZER = SCRIPTS + '/tokenizer/tokenizer.perl'
CLEAN = SCRIPTS + '/training/clean-corpus-n.perl'
BPE_SCRIPT = 'subword-nmt'

# Tokenization and BPE data compression variables.
BPE_TOKENS = 45000
CLEAN_RATIO = 1.5

# Tokenization and BPE temporary results.
PREP = 'bible.prep'
TMP = PREP + '/tmp'
BPE_CODE = PREP + '/code'

# starts with * = unidecode
CORPUS = [
    "*grcgrcbrenttisch", "indindags", "aazaaz", "pmyPMY",
    "tgltglulb", "*tonton", "iloiloulb", "ifkifk", "ifaifa",
    "ifbifb", "hlthltmcsb", "hlthltthb", "alpalpNT", "amkamk",
    "blzblzNT", "*ptuptu", "beubeu", "rowrow", "nfanfa", "frdfrd",
    "*hvnhvn", "heghegNTpo", "kjekjeNT", "mknmkn", "llgllg",
    "lexlex", "ayzAYZ", "mqjmqjNT", "nbqnbq", "nxlnxl", "*uryury",
    "rgurgu", "sluslu", "setset", "tettet", "txqtxq", "kklkkl",
    "yvayvaNT", "*jvnjvnNT", "bjnbjn", "zlmzlmKSZI", "agnagn",
    "ifyify", "agtagt", "dgcdgc", "duoduo", "*attatt", "abpABP",
    "sgbsgb", "blxblx", "xsbxsb", "*sblsbl", "ifuifu", "zypzypNT",
    "csycsy",
]

TRAIN_DATAS = {
    'bjnbjn': 'RUT',  # Banjar, Malaysia
    'indindags': 'MAT',  # Indonesia
    'jvnjvnNT': 'ROM',  # Carribean Java
    # 'kjekjeNT': '1JN',  # Kisar Island, Maluku Barat Daya
    # 'lexlex': '1PE',  # Leti and Babar Islands, Maluku
    'uryury': '2TH',  # Orya, Papua
}

TRANS_RAW = [
    'indindags', 'jvnjvnNT',
    # 'kjekjeNT', 'lexlex',
    'uryury', 'bjnbjn',
]

SRC_TOKEN_EXTRA_WEIGHT = 2
TARGET_EXTRA_PASSES = 2
TARGETS = list(TRAIN_DATAS)

SRC = 'grcgrcbrenttisch'

GLOSSARIES = ['TGT_' + m.lstrip('*') for m in CORPUS] + ['TGT_TEMPLATE']


def apply_bpe(fname):
    with open(TMP + '/' + fname) as inf:
        with open(PREP + '/' + fname, 'w') as outf:
            CMD = ([BPE_SCRIPT, 'apply-bpe', '--glossaries'] +
                   GLOSSARIES + ['-c', BPE_CODE] + ['--vocabulary', TMP +
                                                    '/bpe.vocab.both',
                                                    '--vocabulary-threshold',
                                                    '50'])
            run(CMD, stdin=inf, stdout=outf, check=True)


def initial_checks():
    srcnames = [x.lstrip('*') for x in CORPUS]
    assert SRC in srcnames
    assert not (set(TRAIN_DATAS) - set(srcnames)), (set(TRAIN_DATAS) -
                                                    set(srcnames))
    assert not (set(TARGETS) - set(srcnames)), (set(TARGETS) - set(srcnames))

    shutil.rmtree(PREP, ignore_errors=True)
    os.mkdir(PREP)
    os.mkdir(TMP)

    # Check if tokenizer dependency exists.
    if not os.path.exists('../../lib/mosesdecoder'):
        print('ERROR: Directory "mosesdecoder" does not exist.',
              file=sys.stderr)
        print('Did you forget to run install_dependencies.sh?',
              file=sys.stderr)
        sys.exit(1)

    # Check if corpus exists.
    if not os.path.exists('../../corpus'):
        print('ERROR: Directory "corpus" does not exist.', file=sys.stderr)
        print('Did you forget to run install_dependencies.sh?',
              file=sys.stderr)
        sys.exit(1)


def load_sources():
    print('Loading sources...')
    train_corpus = {}
    valid_corpus = {}
    for s in CORPUS:
        print(s, end=' ', flush=True)
        decode = False
        if s[0] == '*':
            decode = True
            s = s[1:]
        train_corpora = pc.load_source_file(s, toascii=decode)
        if s in TRAIN_DATAS:
            valid_corpora, train_corpora = pc.split_at_key(TRAIN_DATAS[s],
                                                           train_corpora)
            valid_corpus[s] = valid_corpora
        train_corpus[s] = train_corpora
    return train_corpus, valid_corpus


# TODO: Sockeye has a way to add prefixes, might it be better than adding it
#       manually? Try this after finding out if we proceed with Sockeye or no
#       on step two on the research.
def generate_training_data(src_corpora, train_corpus):
    print("Generating training data...")
    src_data = []
    tgt_data = []
    for tgt_corpora in train_corpus:
        passes = 1
        if tgt_corpora in TARGETS:
            passes += TARGET_EXTRA_PASSES
        for i in range(passes):
            for src_line, tgt_line in pc.gen_trans(src_corpora,
                                                   train_corpus[tgt_corpora]):
                src_data.append('TGT_' + tgt_corpora + ' ' + src_line)
                tgt_data.append(tgt_line)
    return src_data, tgt_data


def generate_validation_data(src_corpora, valid_corpus):
    print("Generating validation data...")
    valid_src_data = []
    valid_tgt_data = []
    for tgt_corpora in valid_corpus:
        for src_line, tgt_line in pc.gen_trans(src_corpora,
                                               valid_corpus[tgt_corpora]):
            valid_src_data.append('TGT_' + tgt_corpora + ' ' + src_line)
            valid_tgt_data.append(tgt_line)
    return valid_src_data, valid_tgt_data


def tokenize_data(src_data, tgt_data, valid_src_data, valid_tgt_data,
                  src_corpora):
    print('Tokenizing training data...')
    # TODO: Find out what is this for other than target code name removal.
    with open(TMP + '/protect', 'w') as f:
        print('TGT_[a-zA-Z0-9]+', file=f)

    # For BPE, learn source language only 1+SRC_TOKEN_EXTRA_WEIGHT times.
    with open(TMP + '/src-once', 'w') as f:
        for i in range(1+SRC_TOKEN_EXTRA_WEIGHT):
            print('\n'.join(src_corpora.values()), file=f)

    # Create a file for the source exactly once.
    src_template = ['TGT_TEMPLATE ' + x for x in src_corpora.values()]

    # Tokenize the data.
    for data, fname in [(src_data, 'train.src'), (tgt_data, 'train.tgt'),
                        (valid_src_data, 'valid.src'), (valid_tgt_data,
                                                        'valid.tgt'),
                        (src_template, 'src-template')]:
        CMD = ['perl', TOKENIZER, '-time', '-q', '-threads', '8', '-protected',
               TMP+'/protect', '-l', 'nosuchlanguage']
        with open(TMP + '/' + fname, 'w') as f:
            run(CMD, input='\n'.join(data), stdout=f, check=True,
                encoding='utf-8')

    # Clean the tokenized data?
    for s, d in [('train', 'train.clean'), ('valid', 'valid.clean')]:
        CMD = ['perl', CLEAN, '-ratio', str(CLEAN_RATIO), TMP+'/'+s, 'src',
               'tgt', TMP + '/' + d, '1', '175']
        run(CMD, check=True)

    run('cat {tmp}/src-once {tmp}/train.tgt >{tmp}/train.both'.format(tmp=TMP),
        shell=True, check=True)


# Learn BPE and vocabulary from the training data and apply BPE
# to the training data, validation data, and untranslated data.
def learn_and_apply_bpe():
    print('Learning BPE and vocabulary...')
    CMD = [BPE_SCRIPT, 'learn-joint-bpe-and-vocab', '-i', TMP +
           '/train.both', '-s', str(BPE_TOKENS), '-o', BPE_CODE,
           '--write-vocabulary', TMP + '/bpe.vocab.both']
    run(CMD, check=True)

    print('Applying BPE to:')
    threads = []
    for line in ('src', 'tgt'):
        for s in ('train', 'valid'):
            fname = s + '.' + line
            print('- ' + fname)
            th = Thread(target=apply_bpe, args=[fname])
            th.start()
            threads.append(th)

    print('- src-template')
    th = Thread(target=apply_bpe, args=['src-template'])
    th.start()
    threads.append(th)

    print('On separate threads ...')

    for t in threads:
        t.join()


def main():
    initial_checks()

    train_corpus, valid_corpus = load_sources()
    print()

    src_corpora = train_corpus[SRC]
    del train_corpus[SRC]

    src_data, tgt_data = generate_training_data(src_corpora, train_corpus)
    valid_src_data, valid_tgt_data = generate_validation_data(src_corpora,
                                                              valid_corpus)
    tokenize_data(src_data, tgt_data, valid_src_data, valid_tgt_data,
                  src_corpora)

    learn_and_apply_bpe()

    # TODO: Remove the lines already translated in the target
    #       language.
    print('Preparing source templates for each target language...')
    for trans in TRANS_RAW:
        fname = PREP + '/src.' + trans + '.txt'
        shutil.copy(PREP + '/src-template', fname)
        new_lines = []
        with open(fname) as f:
            for line in f.readlines():
                new_lines.append(line.strip().replace("TEMPLATE", trans))
        with open(fname, 'w') as f:
            f.write('\n'.join(new_lines))

    # FIXME proper test set
    shutil.copy(PREP + '/valid.src', PREP + '/test.src')
    shutil.copy(PREP + '/valid.tgt', PREP + '/test.tgt')


if __name__ == '__main__':
    main()
