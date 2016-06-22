import xml.etree.ElementTree as etree

tree = etree.parse('core.txt')

element_stack = [ce for ce in tree.getroot()]

while len(element_stack) > 0:
    next_element = element_stack.pop()

    for ce in next_element:
        element_stack.append(ce)

    print(next_element)


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
