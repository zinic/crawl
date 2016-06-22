#!/usr/bin/env python

import sys
import argparse
import datetime

import crawl.html as html


def new_argparser():
    argparser = argparse.ArgumentParser(
        prog='crawl',
        description='Doc Manager for The Crawl')

    argparser.add_argument(
        '-v', '--version',
        action='version',
        version='0.1')

    subparsers = argparser.add_subparsers(
        dest='command',
        title='Commands',
        help='Commands')

    format_parser = subparsers.add_parser(
        'format',
        help='Initializes a restore of a backup')

    format_parser.add_argument(
        'target',
        nargs=1,
        help='Target path to restore to')

    return argparser


def parse_args():
    argparser = new_argparser()

    if len(sys.argv) <= 1:
        argparser.print_help()
        sys.exit(1)

    return argparser.parse_args()


def read_file(path):
    with open(path, 'r') as fin:
        for line in fin.readlines():
            for part in line.split():
                yield part
            yield '\n'


def main():
    args = parse_args()

    target_path = args.target[0]
    doc = parse(read_file(target_path))

    with open('output.html', 'w') as fout:
        fout.write(str(
            html.html(
                html.head(
                    html.title('TODO')),

                html.body(
                    doc_to_html(doc)))))


def is_directive(token):
    return token.startswith('@')


N_ROOT = 'root'
N_CONTENTS = 'root'
N_TEXT = 'text'
N_DATE = 'date'
N_SECTION = 'section'

C_CONTENTS = '@toc'
C_DATE = '@date'
C_DICE = '@dice'
C_SECTION = '@section'
C_TITLE = '@title'
C_END = '@end'


def read_directive(root, tokens, directive):
    if directive == C_SECTION:
        read_section(root, tokens)

    elif directive == C_DATE:
        root.date()

    elif directive == C_CONTENTS:
        root.contents()

    else:
        raise Exception('Unknown directive: {}'.format(directive))


def read_section(root, tokens):
    title = tokens.next()
    section_node = root.section(title)

    text = ''
    token = tokens.next()
    while token != C_END:
        # Check if this is an additiona directive
        if is_directive(token):
            # Dump accumulated text
            if len(text) > 0:
                section_node.text(text)
                text = ''

            read_directive(section_node, tokens, token)

        else:
            text += ' {}'.format(token)

        token = tokens.next()


def parse(tokens):
    parser = Parser()

    for token in tokens:
        while parser.next(token) == REPLAY:
            pass

    return parser._doc


REPLAY = True
CONSUME = None

START = 'start'
NEXT_DIRECTIVE = 'next_directive'
SECTION_START = 'section_start'
SECTION_TITLE = 'section_title'
SECTION_CONTENT = 'section_content'


def ignore_newline(delegate):
    def _before(self, token):
        if token == '\n':
            return CONSUME
        else:
            return delegate(self, token)

    return _before


class Parser(object):

    def __init__(self):
        self._doc = Root()
        self._doc_stack = [self._doc]

        self._state = START
        self._buffer = list()

    @property
    def _current(self):
        return self._doc_stack[len(self._doc_stack) - 1]

    def _hold(self, token):
        self._buffer.append(token)

    def _holding(self):
        return len(self._buffer) > 0

    def _release(self):
        content = ' '.join(self._buffer).strip()
        self._buffer = list()

        return content

    def _ascend(self):
        self._doc_stack.pop()

    def _descend(self, node):
        self._current.add(node)
        self._doc_stack.append(node)

    def next(self, token):
        print('{}: {}'.format(self._state, token))
        return getattr(self, self._state)(token)

    def start(self, token):
        self._state = NEXT_DIRECTIVE
        return REPLAY

    @ignore_newline
    def next_directive(self, token):
        if token == C_SECTION:
            self._state = SECTION_START

        elif token == C_DATE:
            pass

        elif token == C_CONTENTS:
            pass

        elif token == C_END:
            self._ascend()

            if isinstance(self._current, Section):
                self._state = SECTION_CONTENT

        else:
            raise Exception('Unknown directive: {}'.format(token))

    @ignore_newline
    def section_start(self, token):
        # Current node is now the section
        self._descend(Section())

        if token == C_TITLE:
            self._state = SECTION_TITLE

        else:
            self._state = SECTION_CONTENT

    def section_title(self, token):
        if token == C_END:
            self._state = SECTION_CONTENT
            self._current.title = self._release()

        else:
            self._hold(token)

    def section_content(self, token):
        if is_directive(token):
            if self._holding():
                text = Text(self._release())
                self._current.add(text)

            self._state = NEXT_DIRECTIVE
            return REPLAY

        else:
            self._hold(token)
            return CONSUME


class Component(object):

    def __init__(self):
        self.components = list()

    def add(self, component):
        self.components.append(component)


class Root(Component):

    def __init__(self):
        super(Root, self).__init__()


class Section(Component):

    def __init__(self, title=''):
        super(Section, self).__init__()
        self.title = title


class Text(Component):

    def __init__(self, content=''):
        super(Text, self).__init__()
        self.content = content


def doc_to_html(root):
    html_div = html.div()

    for c in root.components:
        if isinstance(c, Section):
            element = html_div.add(
                html.div(
                    html.span(c.title)
                ))

            element.add(doc_to_html(c))

        elif isinstance(c, Text):
            text = html_div.add(html.p())
            for line in c.content.split('\n'):
                text.add(line)
                text.add(html.br())

    return html_div


if __name__ == '__main__':
    main()
