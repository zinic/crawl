import xml.etree.ElementTree as etree

from cdoc.format import format_markdown
from cdoc.model import Document
from cdoc.view import Model


def main():
    # Process the doc
    core_tree = etree.parse('template.xml')
    root = core_tree.getroot()

    # Create the document object
    document = Document(root)

    # Translate into our model
    model = Model(document)

    # Run default sanity checks
    model.check()

    # Write as markdown
    format_markdown(model)

    print('OK')


if __name__ == '__main__':
    main()
