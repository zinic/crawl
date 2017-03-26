from .model import Model
from .xml_backend import load
from .yaml_backend import load_character, write_yaml
from .yaml_backend import load_yaml_model as load_document_yaml


def load_document_xml(path):
    with open(path, 'r') as fin:
        document_node = load(fin)
        return Model(document_node)
