import traceback
import os
import falcon
import io
import waitress

from nurpg.document import load_document
from nurpg.document.model import Aspect
from nurpg.document.xml_backend import load_as, XMLBacked
from nurpg.document.yaml_backend import load_character
from nurpg.format import format_aspect, format_character


def _rel_load(target):
    path = os.path.join(os.path.dirname(__file__), target)

    with open(path, 'r') as fin:
        return fin.read()


class UIResource(object):
    HTML = _rel_load('index.html')

    def on_get(self, req, resp):
        resp.set_header('Content-Type', 'text/html')
        resp.body = _rel_load('index.html')


class AspectFormatResource(object):
    def __init__(self, doc):
        self._doc = doc

    def on_post(self, req, resp):
        resp.set_header('Content-Type', 'text/markdown')

        try:
            aspect_xml = load_as(req.stream, XMLBacked)
            aspect_model = Aspect.from_xml(aspect_xml)

            buffer = io.StringIO()
            format_aspect(aspect_model, self._doc, buffer)
            resp.body = buffer.getvalue()
            buffer.close()
        except Exception as ex:
            resp.body = '### General Error\n\n{}'.format(ex)


class CharacterFormatResource(object):
    def __init__(self, doc):
        self._doc = doc

    def on_post(self, req, resp):
        resp.set_header('Content-Type', 'text/markdown')

        try:
            character = load_character(req.stream, self._doc)

            buffer = io.StringIO()
            format_character(character, self._doc, buffer)
            resp.body = buffer.getvalue()
            buffer.close()
        except Exception as ex:
            traceback.print_exc()
            resp.body = '### General Error\n\n{}'.format(ex)


def main():
    document = load_document('template.xml')

    api = falcon.API()
    api.add_route('/ui', UIResource())
    api.add_route('/format/aspect', AspectFormatResource(document))
    api.add_route('/format/character', CharacterFormatResource(document))

    waitress.serve(api, host='0.0.0.0', port=8080)


if __name__ == "__main__":
    main()
