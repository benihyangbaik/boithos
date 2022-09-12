import os
import sys
import argparse
from utoken import detokenize

CORPUS_DIR = '../corpus'
REF_FILE = CORPUS_DIR + '/modvref.txt'

REV_UNIDECODE = {
    '&quot;': '"',
}


def main() -> None:
    # Check if corpus exists.
    if not os.path.exists(CORPUS_DIR):
        print('ERROR: Directory "corpus" does not exist.', file=sys.stderr)
        print('Did you forget to run install_dependencies.sh?',
              file=sys.stderr)
        sys.exit(1)

    parser = argparse.ArgumentParser(description='Detokenize and add verse '
                                     'references', allow_abbrev=True)
    parser.add_argument('--language-code', required=True, type=str, help='The '
                        'language code according to ISO 639-3')
    parser.add_argument('--input', required=True, type=str, help='Input file')
    parser.add_argument('--output', required=True, type=str, help='Output '
                        'file')
    args = parser.parse_args()

    detok = detokenize.Detokenizer(lang_code=args.language_code)
    print(detok.detokenize_string(''))

    new_lines = []
    with open(args.input) as df:
        with open(REF_FILE) as rf:
            for (dl, rl) in zip(df.readlines(), rf.readlines()):
                for r, t in REV_UNIDECODE.items():
                    dl = dl.replace(r, t)
                rl = rl.replace('\n', '')
                dl = dl.replace('\n', '')
                new_lines.append(f"{rl} {detok.detokenize_string(dl)}")

    with open(args.output, 'w') as f:
        f.write('\n'.join(new_lines))


if __name__ == '__main__':
    main()
