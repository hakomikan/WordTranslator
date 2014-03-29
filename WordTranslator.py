import codecs

def MaxLengthWord(wordList):
    """
    >>> MaxLengthWord(["aaa","bbbbb"])
    'bbbbb'
    """
    return max(wordList, key=lambda x:len(x))

def ReplaceWord(src, replaceWords):
    """
    >>> ReplaceWord("SmallBed",{"Bed":"Couch","SmallBed":"BabyBed"})
    ('BabyBed', [])
    >>> ReplaceWord("ASmallBed",{"Bed":"Couch","SmallBed":"BabyBed","A":"The"})
    ('TheBabyBed', [])
    >>> ReplaceWord("TheSmallBed",{"Bed":"Couch","SmallBed":"BabyBed"})
    ('TheBabyBed', ['The'])
    """
    if src == "":
        return ("", [])

    untranslatedWords = []
    matchedWords = [ x for x in replaceWords.keys() if x in src ]

    if len(matchedWords) == 0:
        return (src, [src])

    replaceWord = MaxLengthWord(matchedWords)
    untranslatedWords = src.split(replaceWord)
    retranslatedWords = [list(y) for y in zip(*[ReplaceWord(x,replaceWords) for x in untranslatedWords])]
    untranslatedWords = sum(retranslatedWords[1],[])
    retranslatedWords = retranslatedWords[0]

    return (replaceWords[replaceWord].join(retranslatedWords), untranslatedWords)

def FindDuplication(dct):
    """
    >>> FindDuplication({"A":"C", "B":"C"})
    {'C': ['A', 'B']}
    """
    from collections import defaultdict
    ret = {}
    for k,v in dct.items():
        ret[v] = ret.get(v,[]) + [k]
    for k in [ x for x in ret.keys() ]:
        if len(ret[k]) <= 1:
            del ret[k]
        else:
            ret[k].sort()
    return ret

def TranslateWords(
    sourceWords,
    replaceWords,
    duplicatableWords={},
    untranslationWords={}
    ) -> ('translatedWords',
          'untranslatedWords',
          'duplicatedWords'):

    translatedWords = {}
    untranslatedWords = []
    duplicatedWords = {}

    for src in sourceWords:
        translatedWords[src], currentUntranslatedWords = ReplaceWord(src, replaceWords)
        if currentUntranslatedWords:
            untranslatedWords.append(currentUntranslatedWords)

    duplicatedWords = FindDuplication(translatedWords)
    duplicatedWords = dict( (k,v) for k,v in duplicatedWords.items() if k not in duplicatableWords )

    untranslatedWords = [ x for x in untranslatedWords if x not in untranslationWords ]

    return (translatedWords,
            duplicatedWords,
            untranslatedWords)

import begin
import yaml
import codecs
import sys

Encoding = None

def OpenOutputStream(filename):
    if filename == "-":
        sys.stdout.close = lambda: None
        return sys.stdout
    else:
        print(filename)
        return codecs.open(filename, "w", Encoding)

def OpenInputStream(filename):
    if filename == "-":
        return sys.stdin
    else:
        return codecs.open(filename, "r", Encoding)

def ReadYaml(filename):
    with OpenInputStream(filename) as f:
        return yaml.load(f.read())

def WriteYaml(filename, data):
    f = OpenOutputStream(filename)
    f.write(
        yaml.safe_dump(
            data,
            allow_unicode=True,
            default_flow_style=False))

def ReadList(filename):
    with OpenInputStream(filename) as f:
        return [x.strip() for x in f.readlines()]

def WriteList(filename, lst):
    with OpenOutputStream(filename) as f:
        for x in lst:
            print(x, file=f)

@begin.start(short_args=False)
def main(source_words = "-",
         replace_words = None,
         ignore_duplication = None,
         ignore_untranslation = None,
         output = "-",
         output_duplicated = "-",
         output_untranslated = "-",
         encoding = "utf-8"):

    global Encoding
    Encoding = encoding

    sourceWords = ReadList(source_words)
    replaceWords = ReadYaml(replace_words)
    duplicatableWords = ReadList(ignore_duplication)
    untranslationWords = ReadList(ignore_untranslation)

    replacedWords, duplicatedWords, untranslatedWords = TranslateWords(sourceWords, replaceWords, duplicatableWords, untranslationWords)

    WriteYaml(output, replacedWords)

    if duplicatedWords:
        print("{0} duplicated words:".format(len(duplicatedWords)), file=sys.stdout)
        WriteList(output_duplicated, duplicatedWords)

    if untranslatedWords:
        print("{0} untranslated words:".format(len(untranslatedWords)), file=sys.stdout)
        WriteList(output_untranslated, untranslatedWords)

    if len(duplicatedWords) != 0 or len(untranslatedWords) != 0:
        sys.exit(1)
