import yaml

from mprequest.util import DictBacked
from nurpg.document.model import Character, Item, RuleReferences, Aspect


def load_character(input, model):
    value = yaml.load(input)
    version = value.get('version', '0.1')

    char_content = DictBacked(value['character'], strict=False)

    # Copy contents over
    character = Character(
        name=char_content.name,
        aspect_points=char_content.aspect_points,
        starting_funds=char_content.starting_funds,
        model=model)

    # Look up aspects
    if char_content.aspects is not None:
        for aspect_yaml in char_content.aspects:
            aspect = model.aspect(aspect_yaml.name)
            if aspect is None:
                aspect = Aspect.from_yaml(aspect_yaml)

            character.add_aspect(aspect)

    # Look up items
    if char_content.items is not None:
        for item_ref in char_content.items:
            # Try to load the item from the model first
            item = model.item(item_ref.name)
            if item is None:
                # If the model doesn't have the item, maybe the player specified details inline
                item = Item.from_yaml(item_ref)

            character.add_item(item)

    # Finish building the character model
    character.load(model)

    # Check the character then return it
    return character
