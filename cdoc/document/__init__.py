from .model import Model
from .xml import load


def load_document(path):
    with open(path, 'r') as fin:
        document_node = load(fin)
        return Model(document_node)
