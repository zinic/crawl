import datetime

import xml.etree.ElementTree as etree
import crawl.html as html


S_START = 'start'
S_DOCUMENT = 'document'
S_SECTION = 'section'


class Handler(object):

    def __init__(self):
        self._doc = Document()
        self._work_stack = list()

    def handle(self, tree):
        element = tree.getroot()

        if element.tag == 'document':
            self.in_document(element)

        else:
            raise Exception('Expected document tag at top-level.')

    def in_document(self, element):
        for c in element:
            if c.tag == 'title':
                self._doc.title = Text(c)

            elif c.tag == 'date':
                self._doc.date = datetime.datetime.now()

            elif c.tag == 'section':
                self._doc.add_section(self.in_section(c))

    def in_section(self, element):
        section = Section()

        for c in element:
            if c.tag == 'title':
                section.title = Text(c)

            elif c.tag == 'content':
                section.content = Content(c)

            elif c.tag == 'section':
                section.add_section(self.in_section(c))

        return section


class Document(object):

    def __init__(self):
        self.title = None
        self.date = None
        self.sections = list()

    def add_section(self, section):
        self.sections.append(section)

    def to_html(self):
        doc = html.html(
            html.head(
                html.title(self.title)))

        body = doc.add(html.body(
            html.div(
                html.span(self.date))))

        work_stack = [s for s in self.sections]
        while len(work_stack) > 0:
            section = work_stack.pop()
            section_div = body.add(html.div())

            section_div.add(html.span(
                section.title))

            section_div.add(html.p(
                section.content))

            for c in reversed(section.sections):
                work_stack.insert(0, c)

        return doc


class Section(object):

    def __init__(self):
        self.title = None
        self.content = None
        self.sections = list()

    def add_section(self, section):
        self.sections.append(section)


class TextObject(object):

    def __init__(self, text=''):
        self.text = text

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.text


class Text(TextObject):

    def __init__(self, element):
        super(Text, self).__init__(' '.join(element.itertext()))


class Content(TextObject):

    def __init__(self, element):
        super(Content, self).__init__(' '.join(element.itertext()))


tree = etree.parse('core.xml')
handler = Handler()
handler.handle(tree)

print(handler._doc.to_html())
#print(ht)
