import yaml

from mprequest.util import DictBacked
from nurpg.document.model import Character, Item, RuleReferences


def load_character(input, model):
    value = yaml.load(input)
    char_content = DictBacked(value['character'], strict=False)

    # Copy contents over
    character = Character(
        name=char_content.name,
        aspect_points=char_content.aspect_points,
        starting_funds=char_content.starting_funds,
        model=model)

    # Look up aspects
    for aspect_ref in char_content.aspects:
        character.add_aspect(aspect_ref.name, aspect_ref)

    # Look up items
    for item_ref in char_content.items:
        character.add_item(item_ref.name, item_ref)

    # Finish building the character model
    character.load(model)

    # Check the character then return it
    character.check(model)
    return character
