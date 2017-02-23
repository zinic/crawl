import yaml

from nurpg.util import DictBacked
from nurpg.document.model import Character


def load_character(input, model):
    value = yaml.load(input)
    char_content = DictBacked(value['character'])

    # Copy contents over
    character = Character(
        name=char_content.name,
        aspect_points=char_content.aspect_points)

    # Look up aspects
    for aspect_ref in char_content.aspects:
        character.aspects[aspect_ref] = model.aspect(aspect_ref)

    # Check the character first then return it
    character.check(model)
    return character
