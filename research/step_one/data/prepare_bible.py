# TODO: Deal with verse ranges.
# TODO: Use tuple instead of list and NamedTuple instead of dict for ensuring
# the correct tracing, as suggested here:
# [INFO:sockeye.checkpoint_decoder] Created CheckpointDecoder(max_input_len=-1, beam_size=5, num_sentences=500)
# /home/user/Desktop/Repositories/proyek/benihyangbaik/boithos/research/env/step_one/lib64/python3.10/site-packages/torch/jit/_trace.py:958:
# TracerWarning: Encountering a list at the output of the tracer might cause
# the trace to be incorrect, this is only valid if the container structure does
# not change based on the module's inputs. Consider using a constant container
# instead (e.g. for `list`, use a `tuple` instead. for `dict`, use a
# `NamedTuple` instead). If you absolutely need this and know the side effects,
# pass strict=False to trace() to allow this behavior.

from unidecode import unidecode
from collections import OrderedDict
from subprocess import run
from threading import Thread
import os
import shutil
import sys

import prepare_corpora

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
SOURCES = [
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
    'bjnbjn': 'RUT', # Banjar, Malaysia
    'indindags': 'MAT', # Indonesia
    'jvnjvnNT': 'ROM', # Carribean Java
    # 'kjekjeNT': '1JN', # Kisar Island, Maluku Barat Daya
    # 'lexlex': '1PE', # Leti and Babar Islands, Maluku
    'uryury': '2TH', # Orya, Papua
}

TRANS_RAW = [
    'indindags', 'jvnjvnNT',
    # 'kjekjeNT', 'lexlex',
    'uryury', 'bjnbjn',
]

SRC_TOKEN_EXTRA_WEIGHT = 2
TARGET_EXTRA_PASSES = 2
TARGETS = list(TRAIN_DATAS)

SRC='grcgrcbrenttisch'

GLOSSARIES = ['TGT_' + m.lstrip('*') for m in SOURCES] + ['TGT_TEMPLATE']

def apply_bpe(fname):
    with open(TMP + '/' + fname) as inf:
        with open(PREP + '/' + fname, 'w') as outf:
            CMD = ([BPE_SCRIPT, 'apply-bpe', '--glossaries'] +
                   GLOSSARIES + ['-c', BPE_CODE] + ['--vocabulary', TMP +
                                                    '/bpe.vocab.both',
                                                    '--vocabulary-threshold',
                                                    '50'])
            run(CMD, stdin=inf, stdout=outf, check=True)


def main():
    srcnames = [x.lstrip('*') for x in SOURCES]
    assert SRC in srcnames
    assert not (set(TRAIN_DATAS) - set(srcnames)), (set(TRAIN_DATAS) - set(srcnames))
    assert not (set(TARGETS) - set(srcnames)), (set(TARGETS) - set(srcnames))

    shutil.rmtree(PREP, ignore_errors=True)
    os.mkdir(PREP)
    os.mkdir(TMP)

    # Check if tokenizer dependency exists.
    if not os.path.exists('../../lib/mosesdecoder'):
        print('ERROR: Directory "mosesdecoder" does not exist.', file=sys.stderr)
        print('Did you forget to run install_dependencies.sh?', file=sys.stderr)
        sys.exit(1)

    # Check if corpus exists.
    if not os.path.exists('../../corpus/grcgrcbrenttisch.txt'):
        print('ERROR: Corpora "grcgrcbrenttisch.txt" does not exist.', file=sys.stderr)
        print('Did you forget to run install_dependencies.sh?', file=sys.stderr)
        sys.exit(1)

    # Load sources to train_mods and valid_mods object.
    train_mods = {}
    valid_mods = {}
    print('Loading sources...')
    for s in SOURCES:
        print(s, end=' ', flush=True)
        decode = False
        if s[0] == '*':
            decode = True
            s = s[1:]
        train_mod = prepare_corpora.load_source_file(s, toascii=decode)
        # print(train_mod)
        if s in TRAIN_DATAS:
            valid_mod, train_mod = prepare_corpora.split_at_key(TRAIN_DATAS[s], train_mod)
            # print("valid mod")
            # print(valid_mod)
            valid_mods[s] = valid_mod
        train_mods[s] = train_mod
    print()

    src_mod = train_mods[SRC]
    del train_mods[SRC]

    print("Generating training data...")
    src_data = []
    tgt_data = []
    for tgt_mod in train_mods:
        passes = 1
        if tgt_mod in TARGETS:
            passes += TARGET_EXTRA_PASSES
        for i in range(passes):
            for src_line, tgt_line in prepare_corpora.gen_trans(src_mod, train_mods[tgt_mod]):
                src_data.append('TGT_' + tgt_mod + ' ' + src_line)
                tgt_data.append(tgt_line)

    print("Generating validation data...")
    valid_src_data = []
    valid_tgt_data = []
    for tgt_mod in valid_mods:
        for src_line, tgt_line in prepare_corpora.gen_trans(src_mod, valid_mods[tgt_mod]):
            valid_src_data.append('TGT_' + tgt_mod + ' ' + src_line)
            valid_tgt_data.append(tgt_line)

    print('Preprocessing training data...')
    # TODO: Find out what is this for other than target code name removal.
    with open(TMP + '/protect', 'w') as f:
        print('TGT_[a-zA-Z0-9]+', file=f)

    # For BPE, learn source language only 1+SRC_TOKEN_EXTRA_WEIGHT times.
    with open(TMP + '/src-once', 'w') as f:
        for i in range(1+SRC_TOKEN_EXTRA_WEIGHT):
            print('\n'.join(src_mod.values()), file=f)

    # Also create a file for the source exactly once - it's useful down the road
    src_template = ['TGT_TEMPLATE ' + x for x in src_mod.values()]

    # Tokenize the data.
    for data, fname in [(src_data, 'train.src'), (tgt_data, 'train.tgt'),
                        (valid_src_data, 'valid.src'), (valid_tgt_data,
                                                        'valid.tgt'),
                        (src_template, 'src-template')]:
        CMD = ['perl', TOKENIZER, '-time', '-q', '-threads', '8', '-protected',
               TMP+'/protect', '-l', 'nosuchlanguage']
        with open(TMP + '/' + fname, 'w') as f:
            run(CMD, input='\n'.join(data), stdout=f, check=True, encoding='utf-8')

    # Clean the tokenized data?
    for s, d in [('train', 'train.clean'), ('valid', 'valid.clean')]:
        CMD = ['perl', CLEAN, '-ratio', str(CLEAN_RATIO), TMP+'/'+s, 'src', 'tgt',
               TMP + '/' + d, '1', '175']
        run(CMD, check=True)

    run('cat {tmp}/src-once {tmp}/train.tgt >{tmp}/train.both'.format(tmp=TMP),
        shell=True, check=True)

    print('Learning BPE and vocabulary...')
    CMD = [BPE_SCRIPT, 'learn-joint-bpe-and-vocab', '-i', TMP +
           '/train.both', '-s', str(BPE_TOKENS), '-o', BPE_CODE,
           '--write-vocabulary', TMP + '/bpe.vocab.both']
    run(CMD, check=True)

    print('Applying BPE to:')
    threads = []
    for l in ('src', 'tgt'):
        for s in ('train', 'valid'):
            fname = s + '.' + l
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

    # FIXME proper test set
    shutil.copy(PREP + '/valid.src', PREP + '/test.src')
    shutil.copy(PREP + '/valid.tgt', PREP + '/test.tgt')


if __name__ == '__main__':
    main()
