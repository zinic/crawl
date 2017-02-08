DOCUMENT_TAG = 'document'
FORMULAS_TAG = 'formulas'
RULES_TAG = 'rules'
TEMPLATES_TAG = 'templates'
ASPECTS_TAG = 'aspects'
RULE_OPTION_TAG = 'option'


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


class XMLBacked(object):
    def __init__(self, xml):
        self._xml = xml if isinstance(xml, XMLNode) else XMLNode(xml)

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


class Document(XMLBacked):
    def formula(self, name):
        return find_node(self.formulas(), name)

    def formulas(self):
        return self._wrap_set('formulas', 'formula', Formula)

    def rule(self, name):
        return find_node(self.rules(), name)

    def rules(self):
        return self._wrap_set('rules', 'rule', Rule)

    def template(self, name):
        return find_node(self.templates(), name)

    def templates(self):
        return self._wrap_set('templates', 'template', Template)

    def aspect(self, name):
        return find_node(self.aspects(), name)

    def aspects(self):
        return self._wrap_set('aspects', 'aspect', Aspect)

    def check(self):
        if self._xml.tag() != DOCUMENT_TAG:
            raise DocumentCheckError('Expected document tag at XML top-level')

        for expected in (RULES_TAG, TEMPLATES_TAG, ASPECTS_TAG,):
            if self._xml.node(expected) is None:
                raise DocumentCheckError('Expected {} in document but found no matching XML node.'.format(
                    expected))

        for rule in self.rules():
            if rule.category is None:
                raise DocumentCheckError('Rule "{}" is lacking a category.'.format(rule.name))


class Formula(XMLBacked):
    pass


class Rule(XMLBacked):
    @property
    def formula(self):
        return self._wrap('formula', RuleFormula)

    @property
    def options(self):
        return self._wrap_each('option', RuleOption)


class RuleFormula(XMLBacked):
    @property
    def arguments(self):
        return self._wrap_each('argument', RuleFormulaArgument)


class RuleFormulaArgument(XMLBacked):
    pass


class RuleOption(XMLBacked):
    pass


class Template(XMLBacked):
    def validate(self, aspect):
        for requirement in self.requirements:
            aspect_rule = aspect.rule(requirement.rule)

            if aspect_rule is None:
                raise DocumentCheckError('Aspect {} does not conform to template {}'.format(aspect.name, self.name))

    @property
    def requirements(self):
        return self._wrap_each('requires', TemplateRequirement)


class TemplateRequirement(XMLBacked):
    pass


class Aspect(XMLBacked):
    @property
    def text(self):
        text_xml = self._xml.node('text')
        if text_xml is not None:
            return text_xml.text()
        return ''

    def rule(self, name):
        return find_node(self.rules, name, attribute='ref')

    @property
    def rules(self):
        return self._wrap_each('rule', AspectRule)

    @property
    def requirements(self):
        return self._wrap_each('requires', AspectRequirement)


class AspectRule(XMLBacked):
    pass


class AspectRequirement(XMLBacked):
    pass
