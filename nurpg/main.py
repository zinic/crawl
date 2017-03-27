import sys

from nurpg.document import load_document_yaml, load_character
from nurpg.format import *


def read_character(path, model):
    with open(path, 'r') as fin:
        return load_character(fin, model)


def main():
    target = 'document'
    if len(sys.argv) > 1:
        target = sys.argv[1]

    # Run default sanity checks
    model = load_document_yaml('core_module.yaml')
    model.check()

    if target == 'document':
        with open('core_module.md', 'w') as output:
            # Write as markdown
            format_markdown(model, output)

    elif target == 'character':
        char = read_character(sys.argv[2], model)

        for failure in char.check(model):
            print(failure)

        with open('character.md', 'w') as fout:
            format_character(char, model, fout)


if __name__ == '__main__':
    main()
