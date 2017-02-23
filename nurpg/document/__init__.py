from .model import Model
from .xml_backend import load
from .yaml_backend import load_character


def load_document(path):
    with open(path, 'r') as fin:
        document_node = load(fin)
        return Model(document_node)
