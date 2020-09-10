# -*- coding: utf-8 -*-
import os
import re
import codecs
import sys
import argparse

from glob import glob


def main():
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=__doc__)
    parser.add_argument("input", help="naver news directory")
    parser.add_argument("output", help="clean naver news directory")
    args = parser.parse_args()

    fnames = glob(args.input + '/*/wiki*')
    with codecs.open(args.output, 'w', encoding='utf-8', errors='ignore') as fout:
        for fname in fnames:
            with codecs.open(fname, 'r', encoding='utf-8', errors='ignore') as fin:
                text = re.sub('\n\n\n', '@@SPACE', fin.read())
                text = re.sub('[\n]+', ' ', text)
                text = re.sub('(@@SPACE)+', '\n', text)
                text = re.sub('[\n]+', '\n', text)
                fout.write(text + '\n')


if __name__ == '__main__':
    main()
