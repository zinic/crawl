import sys
import yaml

from cdoc.format import *
from cdoc.document import load_document
from cdoc.util import DictBacked


def load_character(path):
    with open(path, 'r') as fin:
        return DictBacked(yaml.load(fin)['character'])


def main():
    target = 'document'
    if len(sys.argv) > 1:
        target = sys.argv[1]

    # Run default sanity checks
    document = load_document('template.xml')
    document.check()

    if target == 'document':
        # Write as markdown
        format_markdown(document)

    elif target == 'character':
        char = load_character(sys.argv[2])
        with open('character.md', 'w') as fout:
            format_character(char, document, fout)



if __name__ == '__main__':
    main()
