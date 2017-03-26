from ruamel import yaml
from mprequest.util import DictBacked

from nurpg.document.model import Character, Item, Aspect, Model


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
    wrap_scalar_style(yaml.SafeDumper)


def write_yaml(output, model):
    configure_dumper()

    stream = yaml.dump(model.to_dict(), Dumper=yaml.SafeDumper, default_flow_style=False)
    output.write(stream.replace('\n- ', '\n\n- '))


def load_yaml_model(yaml_path):
    root_yaml = None
    with open(yaml_path, 'r') as fin:
        root_yaml = yaml.load(fin, Loader=yaml.SafeLoader)

    return Model.from_yaml(DictBacked(root_yaml))


def load_character(input, model):
    value = yaml.load(input, Loader=yaml.SafeLoader)
    # version = value.get('version', '0.1')

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
