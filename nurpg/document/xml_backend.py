import xml.etree.ElementTree as etree

DOCUMENT_TAG = 'document'
FORMULAS_TAG = 'formulas'
RULES_TAG = 'rules'
TEMPLATES_TAG = 'templates'
ASPECTS_TAG = 'aspects'
RULE_OPTION_TAG = 'option'


def load(fd):
    return load_as(fd, DocumentNode)


def load_as(fd, cls):
    core_tree = etree.parse(fd)
    root = core_tree.getroot()

    return cls(root)


def sanitize_text(text):
    output = ''
    for line in text.strip().splitlines():
        output += '{}\n'.format(line.strip())
    return output


class DocumentCheckError(Exception):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg

    def __repr__(self):
        return self._msg


class XMLNode(object):
    def __init__(self, xml):
        self._xml = xml

    def text(self):
        return sanitize_text(self._xml.text)

    def tag(self):
        return self._xml.tag

    def node(self, tag):
        results = self.each_node(search=tag)
        return results[0] if len(results) > 0 else None

    def each_node(self, search=None):
        results = list()
        for node in self._xml:
            if search is not None and search == node.tag:
                wrapped = XMLNode(node)
                results.append(wrapped)

        return results

    def has_node(self, name):
        return self.node(name) is not None

    def attr(self, name, default=None):
        return self._xml.attrib.get(name, default)

    def has_attr(self, name):
        return name in self._xml.attrib

    def __getattr__(self, name):
        return self._xml.attrib.get(name, None)


class XMLBacked(object):
    def __init__(self, xml):
        self._xml = xml if isinstance(xml, XMLNode) else XMLNode(xml)

    @property
    def text(self):
        text_xml = self._xml.node('text')
        if text_xml is not None:
            return sanitize_text(text_xml.text())
        return ''

    def _wrap(self, tag, wrapper_cls):
        return wrapper_cls(self._xml.node(tag))

    def _wrap_each(self, tag, wrapper_cls):
        return [wrapper_cls(n) for n in self._xml.each_node(tag)]

    def _wrap_set(self, set_name, tag, wrapper_cls):
        set_node = self._xml.node(set_name)
        return [wrapper_cls(n) for n in set_node.each_node(tag)]

    def __getattr__(self, item):
        return self._xml.attr(item)


def find_node(nodes, name, attribute='name'):
    for node in nodes:
        if node._xml.attr(attribute) == name:
            return node
    return None


class DocumentNode(XMLBacked):
    def items(self):
        return self._xml.node('items')

    def resources(self):
        return self._xml.node('resources')

    def formulas(self):
        return self._xml.node('formulas')

    def rules(self):
        return self._xml.node('rules')

    def templates(self):
        return self._xml.node('templates')

    def aspects(self):
        return self._xml.node('aspects')
