import sys
import re
from unidecode import unidecode
from collections import OrderedDict

import subprocess

OT_OSIS_ABBREVIATION = [
    'Gen', 'Exod', 'Lev', 'Nuv', 'Deut', 'Josh', 'Judg', 'Ruth', '1Sam',
    '2Sam', '1Kgs', '2Kgs', '1Chr', '2Chr', 'Ezra', 'Neh', 'Esth', 'Job',
    'Ps', 'Prov', 'Eccl', 'Song', 'Isa', 'Jer', 'Lam', 'Ezek', 'Dan',
    'Hos', 'Joel', 'Amos', 'Obad', 'Jonah', 'Mic', 'Nah', 'Hab', 'Zeph',
    'Hag', 'Zech', 'Mal',
]

NT_OSIS_ABBREVIATION = [
    'Matt', 'Mark', 'Luke', 'John', 'Acts', 'Rom', '1Cor', '2Cor', 'Gal',
    'Eph', 'Phil', 'Col', '1Thess', '2Thess', '1Tim', '2Tim', 'Titus',
    'Phlm', 'Heb', 'Jas', '1Pet', '2Pet', '1John', '2John', '3John',
    'Jud', 'Rev'
]

PATH_TO_SOURCE = '../../corpus/'
REF_FILE = PATH_TO_SOURCE + 'modvref.txt'

RM_CHARS = ['¶']
REPL_CHARS = {
    '»': '"',
    '«': '"',
    '„': '"',
    '“': '"',
    '”': '"',
    '’': "'"
}

def load_source_str(data, ref, toascii=False, isall=False, isbyz=False):
    data = data.split('\n')
    ref = ref.split('\n')
    dic = OrderedDict()
    for i, (v, k) in enumerate(zip(data, ref)):
        v = v.strip()
        if not k or not v:
            continue
        for c in RM_CHARS:
            v = v.replace(c, '')
        for r, t in REPL_CHARS.items():
            v = v.replace(r, t)
        if toascii:
            v = unidecode(v)
        dic[k] = v
    return dic


def load_source_file(fname, **kwargs):
    fname = PATH_TO_SOURCE + fname + ".txt"
    with open(fname) as f:
        data = f.read()
    with open(REF_FILE) as f:
        ref = f.read()
    return load_source_str(data, ref, **kwargs)


def gen_trans(src, tgt):
    for key in tgt:
        if key in src:
            yield src[key], tgt[key]


def split_at_key(split_key, od):
    lo = OrderedDict()
    hi = OrderedDict()
    tgt = lo
    for k, v in od.items():
        if k.startswith(split_key):
            tgt = hi
        tgt[k] = v
    return lo, hi


def main():
    TAG = sys.argv[1].upper()
    SRC_OSIS = sys.argv[2]
    TGT_OSIS = sys.argv[3]
    OUT_SRC = sys.argv[4]
    OUT_TGT = sys.argv[5]

    src = load_osis_file(SRC_OSIS, toascii=True)
    tgt = load_osis_file(TGT_OSIS)

    with open(OUT_SRC, 'w') as out_src:
        with open(OUT_TGT, 'w') as out_tgt:
            for srcv, tgtv in gen_trans(src, tgt):
                print('TGT_'+TAG + ' ' + srcv, file=out_src)
                print(tgtv, file=out_tgt)


if __name__ == '__main__':
    main()
