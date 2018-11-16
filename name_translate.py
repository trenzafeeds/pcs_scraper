"""
Translates name strings into acceptable PCS names
"""

import sys
from unidecode import unidecode

def name_translate(name):

    return name.replace(' ', '-').lower()

def main():
    if len(sys.argv) > 1:
        name_to_translate = unicode("")
        for i in xrange(1, len(sys.argv)):
            name_to_translate += unidecode(unicode(sys.argv[i], 'utf-8'))
            if i != (len(sys.argv) - 1):
                name_to_translate += unicode(" ")
        print name_translate(name_to_translate)
    else:
        pass

main()
