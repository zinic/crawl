_HTML_ELEMENT_NAMES = [
    'html',
    'head',
    'title',
    'base',
    'link',
    'meta',
    'style',
    'script',
    'noscript',
    'template',
    'body',
    'section',
    'nav',
    'article',
    'aside',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'header',
    'footer',
    'address',
    'main',
    'p',
    'hr',
    'pre',
    'blockquote',
    'ol',
    'ul',
    'li',
    'dl',
    'dt',
    'dd',
    'figure',
    'figcaption',
    'div',
    'a',
    'em',
    'strong',
    'small',
    's',
    'cite',
    'q',
    'dfn',
    'abbr',
    'data',
    'time',
    'code',
    'var',
    'samp',
    'kbd',
    'sub',
    'sup',
    'i',
    'b',
    'u',
    'mark',
    'ruby',
    'rt',
    'rp',
    'bdi',
    'bdo',
    'span',
    'br',
    'wbr',
    'ins',
    'del',
    'img',
    'iframe',
    'embed',
    'object',
    'param',
    'video',
    'audio',
    'source',
    'track',
    'canvas',
    'map',
    'area',
    'svg',
    'math',
    'tabe',
    'caption',
    'colgroup',
    'col',
    'tbody',
    'thead',
    'tfoot',
    'tr',
    'td',
    'th',
    'form',
    'fieldset',
    'legend',
    'label',
    'input',
    'button',
    'select',
    'datalist',
    'optgroup',
    'option',
    'textarea',
    'keygen',
    'output',
    'progress',
    'meter',
    'details',
    'summary',
    'menuitem',
    'menu',
]


_HTML_SHORT_TAG_TEMPLATE = '<{name} />'
_HTML_TAG_TEMPLATE = '<{name}{attributes}>{content}</{name}>'


class XMLAttributes(object):

    def __init__(self, attributes=None):
        self._attributes = dict() if attributes is None else attributes

    def size(self):
        return len(self._attributes)

    def get(self, key):
        return self._attributes[key]

    def set(self, key, value):
        self._attributes[key] = value

    def remove(self, key):
        del self._attributes[key]

    def __str__(self):
        output = ' ' if len(self._attributes) > 0 else ''

        for k, v in self._attributes.items():
            output += '{}="{}"'.format(k, v)

        return output

    def __repr__(self):
        return str(self)


class XMLElement(object):

    def __init__(self, name, attributes, contents):
        self.name = name
        self.contents = contents
        self.attributes = XMLAttributes(attributes)

    @classmethod
    def NewElementType(cls, name):
        def _new_element(*contents):
            attributes = None
            elements = list()

            for c in contents:
                if type(c) is dict:
                    attributes = c
                else:
                    elements.append(c)

            if attributes is None:
                attributes = dict()

            return XMLElement(name, attributes, elements)
        return _new_element

    def add(self, content):
        self.contents.append(content)
        return content

    def __str__(self):
        # Simple tags get collapsed
        if len(self.contents) == 0 and self.attributes.size() == 0:
            return _HTML_SHORT_TAG_TEMPLATE.format(
                name=self.name)

        # Complex tags require more work
        content = ''
        for c in self.contents:
            content += str(c)

        return _HTML_TAG_TEMPLATE.format(
            name=self.name,
            attributes=self.attributes,
            content=content)

    def __repr__(self):
        return str(self)


# Init our tag functions
for tag_name in _HTML_ELEMENT_NAMES:
    vars()[tag_name] = XMLElement.NewElementType(tag_name)
