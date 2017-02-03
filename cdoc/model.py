DOCUMENT_TAG = 'document'
FORMULAS_TAG = 'formulas'
RULES_TAG = 'rules'
TEMPLATES_TAG = 'templates'
ASPECTS_TAG = 'aspects'
RULE_OPTION_TAG = 'option'


def sanitize_text(text):
    output = ''
    for line in text.split('\n'):
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

    def each_node(self, search=None):
        for node_xml in self._xml:
            if search is None or search == node_xml.tag:
                yield XMLNode(node_xml)

    def node(self, name):
        # Find the first and return it
        for node in self.each_node(name):
            return node
        return None

    def has_node(self, name):
        return self.node(name) is not None

    def attr(self, name, default=None):
        return self._xml.attrib.get(name, default)

    def has_attr(self, name):
        return name in self._xml.attrib

    def cls_wrap(self, cls):
        return cls(self._xml)

    def __getattr__(self, name):
        return self._xml.attrib[name]


class Document(XMLNode):
    def formulas(self):
        formulas_node = self.node(FORMULAS_TAG)
        return [n.cls_wrap(RuleFormula) for n in formulas_node.each_node('formula')]

    def rules(self):
        rules_node = self.node(RULES_TAG)
        return [n.cls_wrap(Rule) for n in rules_node.each_node('rule')]

    def templates(self):
        return self.node(TEMPLATES_TAG)

    def aspects(self):
        return self.node(ASPECTS_TAG)

    def check(self):
        if self.tag() != DOCUMENT_TAG:
            raise DocumentCheckError('Expected document tag at XML top-level')

        for expected in (RULES_TAG, TEMPLATES_TAG, ASPECTS_TAG,):
            if self.node(expected) is None:
                raise DocumentCheckError('Expected {} in document but found no matching XML node.'.format(
                    expected))


class Rule(XMLNode):
    def formula(self):
        return self.node('formula').cls_wrap(RuleFormula)

    def options(self):
        return [n.cls_wrap(RuleOption) for n in self.each_node('option')]


class RuleOption(XMLNode):
    pass


class RuleFormula(XMLNode):
    def argument(self, name, default=None, arg_type=str):
        for argument in self.arguments():
            if argument.name == name:
                return arg_type(argument.value) if argument.has_attr('value') else arg_type(argument.name)
        return default

    def arguments(self):
        return [n.cls_wrap(RuleFormulaArgument) for n in self.each_node('argument')]


class RuleFormulaArgument(XMLNode):
    pass
