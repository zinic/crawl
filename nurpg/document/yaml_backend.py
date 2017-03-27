import collections

from ruamel import yaml
from mprequest.util import DictBacked

from nurpg.document.model import Character, Item, Aspect, Model, CharacterCheckException


class UnsortableList(list):
    def sort(self, *args, **kwargs):
        pass


def represent_ordered_dicts(dumper, data):
    items_list = data.items()
    data.items = lambda: UnsortableList(items_list)

    return dumper.represent_dict(data)


def represent_strings(dumper, data):
    scalar = dumper.represent_str(data)

    if dumper.simple_key_context is not True:
        scalar.style = '|' if len(data) > 80 else '"'

    return scalar


def wrap_scalar_style(dumper_cls):
    original_func = dumper_cls.choose_scalar_style

    def _wrapped(self):
        # Keys are never styled
        if self.simple_key_context:
            return None

        return original_func(self)

    dumper_cls.choose_scalar_style = _wrapped


def configure_dumper():
    yaml.SafeDumper.add_representer(str, represent_strings)
    yaml.SafeDumper.add_representer(collections.OrderedDict, represent_ordered_dicts)

    wrap_scalar_style(yaml.SafeDumper)


def write_yaml(output, model):
    configure_dumper()

    stream = yaml.dump(model.to_dict(), Dumper=yaml.SafeDumper, default_flow_style=False, indent=2)
    output.write(stream.replace('\n- ', '\n\n- '))


def load_yaml_model(yaml_path):
    root_yaml = None
    with open(yaml_path, 'r') as fin:
        root_yaml = yaml.load(fin, Loader=yaml.SafeLoader)

    return Model.from_yaml(DictBacked(root_yaml))


def load_character(input, model):
    value = yaml.load(input, Loader=yaml.SafeLoader)
    version = float(value.get('version', '0.1'))

    char_yaml = DictBacked(value['character'], strict=False)

    # Copy contents over
    character = Character(
        name=char_yaml.name,
        aspect_points=char_yaml.aspect_points,
        starting_funds=char_yaml.starting_funds,
        model=model)

    # Manage the character's wallet
    if char_yaml.wallet is not None:
        if char_yaml.wallet.spent is not None:
            # Calc spent first
            for amount in char_yaml.wallet.spent:
                character.spend_monetary_funds(amount)

        if char_yaml.wallet.recieved is not None:
            # Calc recieved next
            for amount in char_yaml.wallet.recieved:
                character.add_monetary_funds(amount)

    # Look up aspects
    if char_yaml.aspects is not None:
        if version > 0.2:
            for aspect_yaml in char_yaml.aspects:
                aspect = None
                if aspect_yaml.reference is not None:
                    aspect = model.aspect(aspect_yaml.reference)
                elif aspect_yaml.name is not None:
                    aspect = Aspect.from_yaml(aspect_yaml)
                else:
                    raise CharacterCheckException('Aspect must have a non-empty reference or name.')

                character.add_aspect(aspect)
        else:
            for aspect_yaml in char_yaml.aspects:
                if model.has_aspect(aspect_yaml.name):
                    character.add_aspect(model.aspect(aspect_yaml.name))
                else:
                    character.add_aspect(Aspect.from_yaml(aspect_yaml))

    # Look up items
    if char_yaml.items is not None:
        if version > 0.2:
            for item_yaml in char_yaml.items:
                if item_yaml.free is None:
                    raise CharacterCheckException(
                        'Item {} must specify whether or not it is free.'.format(item_yaml.name))

                item = None
                if item_yaml.reference is not None:
                    # Try to load the item from the model if it's a ref
                    item = model.item(item_yaml.reference)
                    item.free = item_yaml.free.lower() == 'yes'

                elif item_yaml.name is not None:
                    # If the model doesn't have the item, maybe the player specified details inline
                    item = Item.from_yaml(item_yaml)
                else:
                    raise CharacterCheckException('Item must have a non-empty reference or name.')

                character.add_item(item)
        else:
            for item_yaml in char_yaml.items:
                if model.has_item(item_yaml.name):
                    character.add_item(model.item(item_yaml.name))
                else:
                    character.add_item(Item.from_yaml(item_yaml))

    # Finish building the character model
    character.load(model)

    # Check the character then return it
    return character
