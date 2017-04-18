from .model import GameModel
from .xml_backend import load
from .yaml_backend import load_character, write_yaml
from .yaml_backend import load_game_module as load_document_yaml


def load_document_xml(path):
    with open(path, 'r') as fin:
        document_node = load(fin)
        return GameModel(document_node)
