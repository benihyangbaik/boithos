from unidecode import unidecode
from collections import OrderedDict


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
# FIXME: Some/on of these are unidecoded as &quot;
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
        v = v.lower()
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
