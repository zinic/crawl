import sys

from nurpg.document import load_document_xml, load_document_yaml, load_character, write_yaml
from nurpg.format import *


def read_character(path, model):
    with open(path, 'r') as fin:
        return load_character(fin, model)


def main():
    target = 'document'
    if len(sys.argv) > 1:
        target = sys.argv[1]

    # Run default sanity checks
    document = load_document_xml('template.xml')
    document.check()

    if target == 'document':
        # Write as markdown
        format_markdown(document)

    elif target == 'character':
        char = read_character(sys.argv[2], document)

        for failure in char.check(document):
            print(failure)

        with open('character.md', 'w') as fout:
            format_character(char, document, fout)

    elif target == 'reverse_rebuild':
        with open('output.yaml', 'w') as fout:
            write_yaml(fout, document)

    elif target == 'test_yaml':
        document = load_document_yaml(sys.argv[2])

        # Write as markdown
        format_markdown(document)

if __name__ == '__main__':
    main()
