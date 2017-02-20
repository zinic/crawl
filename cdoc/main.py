from cdoc.format import format_markdown
from cdoc.document import load_document


def main():
    document = load_document('template.xml')

    # Run default sanity checks
    document.check()

    # Write as markdown
    format_markdown(document)


if __name__ == '__main__':
    main()
