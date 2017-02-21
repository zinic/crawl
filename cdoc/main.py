import sys

from cdoc.document import load_document, load_character
from cdoc.format import *


def read_character(path, model):
    with open(path, 'r') as fin:
        return load_character(fin, model)


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
        char = read_character(sys.argv[2], document)

        with open('character.md', 'w') as fout:
            format_character(char, document, fout)


if __name__ == '__main__':
    main()
