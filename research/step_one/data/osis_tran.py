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

RM_CHARS = '¶'
REPL_CHARS = {
    '»': '"',
    '«': '"',
    '„': '"',
    '“': '"',
    '”': '"',
    '’': "'"
}

# Catch whole OSIS verse
RE = re.compile(r'<verse osisID="([^"]+)">(.*)</verse>')
RE_NT_ONLY = re.compile(r'<verse osisID="([{}][^"]+)">(.*)</verse>'.format(''.join(['|' + m for m in NT_OSIS_ABBREVIATION])[1:]))
RE_OT_ONLY = re.compile(r'<verse osisID="([{}][^"]+)">(.*)</verse>'.format(''.join(['|' + m for m in OT_OSIS_ABBREVIATION])[1:]))

# Catch OSIS note tag
REF_RE = re.compile(r'<note.*\/note>')

# Catch ther OSIS tag and white spaces
TAG_RE = re.compile(r'<[^<>]+>')
SPACE_RE = re.compile(r' +')

# Catch some weird Strong's numbers that's where it shouldn't be in ByzMT
BYZ_RE = re.compile(r'\d{4}')

def load_osis_str(inp, toascii=False, isall=False, isbyz=False):
    inp = inp.split('\n')
    dic = OrderedDict()
    for i, line in enumerate(inp):
        line = line.strip()
        if not line or line.startswith('$'):
            continue
        r = RE.match(line)
        if isall:
            if isall == "NT":
                r = RE_NT_ONLY.match(line)
            elif isall == "OT":
                r = RE_OT_ONLY.match(line)
        # assert r, line
        if not r:
            continue
        key = r.group(1)
        v = r.group(2).strip()
        for c in RM_CHARS:
            v = v.replace(c, '')
        for r, t in REPL_CHARS.items():
            v = v.replace(r, t)
        v = REF_RE.sub(' ', v.strip())
        v = TAG_RE.sub(' ', v.strip())
        v = SPACE_RE.sub(' ', v)
        if isbyz:
            v = BYZ_RE.sub('', v)
        v = v.lower()
        if toascii:
            v = unidecode(v)
        dic[key] = v
    return dic


def load_osis_file(fname, **kwargs):
    with open(fname) as f:
        data = f.read()
    return load_osis_str(data, **kwargs)


def load_osis_module(modname, **kwargs):
    # r = subprocess.run(['mod2imp', modname, '-r', 'OSIS'], check=True,
    #                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    #                    encoding='utf-8')
    r = subprocess.run(['mod2osis', modname], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                       encoding='utf-8')
    return load_osis_str(r.stdout, **kwargs)


def gen_trans(src, tgt):
    for key in tgt:
        if key in src:
            yield src[key], tgt[key]


def split_at_key(split_key, od):
    lo = OrderedDict()
    hi = OrderedDict()
    tgt = lo
    for key, v in od.items():
        if key.startswith(split_key):
            tgt = hi
        tgt[key] = v
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
