import yaml

from mprequest.util import DictBacked
from nurpg.document.model import Character, Item, RuleReferences


def load_character(input, model):
    value = yaml.load(input)
    char_content = DictBacked(value['character'], strict=False)

    # Copy contents over
    character = Character(
        name=char_content.name,
        aspect_points=char_content.aspect_points)

    # Look up aspects
    for aspect_ref in char_content.aspects:
        character.aspects[aspect_ref] = model.aspect(aspect_ref)

    # Look up items
    for item_name in char_content.items:
        # Try to load the item from our model first
        model_item = model.item(item_name)
        if model_item is None:
            # If the model doesn't have the item, maybe the player specified details inline
            model_item = Item.from_yaml(item_name, char_content.items[item_name])

        character.items[item_name] = model_item

    # Finish building the character model
    character.load(model)

    # Check the character then return it
    character.check(model)
    return character
