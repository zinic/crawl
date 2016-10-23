from crawl.util import sanitize_text
from crawl.formulas import get_formula


def find_child(parent_xml, tag):
    for child in parent_xml:
        if child.tag == tag:
            return child
    return None


def assemble_descriptor(effect_xml):
    name = effect_xml.attrib['descriptor']
    effect = effect_xml.attrib.get('value')

    desc = AspectEffect(name, effect)

    for detail_xml in effect_xml:
        desc.add_detail(detail_xml)

    return desc


class DocumentManager(object):
    
    def __init__(self):
        self.items = ItemManager()
        self.aspects = AspectManager()
        self.effects = DescriptorManager()

    def item_cost(self, name):
        return self.items.cost(name, self.aspects, self.effects)

    def aspect_cost(self, name):
        return self.aspects.cost(name, self.effects)


class ItemManager(object):
    
    def __init__(self):
        self.items = dict()

    def add_item(self, item_xml):
        item = Item(
            item_xml.attrib['name'],
            item_xml.attrib['type'])

        flat_cost = item_xml.attrib.get('cost')
        if flat_cost is not None:
            item.cost = flat_cost

        else:
            for part_xml in item_xml:
                if part_xml.tag == 'effect':
                    item.add_effect(part_xml)
                    
                elif part_xml.tag == 'text':
                    item.text = sanitize_text(part_xml.text)
                    
                elif part_xml.tag == 'grants':
                    item.add_grant(part_xml)
                    
                else:
                    raise Exception('Unexpected element: {}'.format(part_xml.tag))

        self.items[item.name] = item

    def cost(self, item_name, aspects, descriptors):
        item = self.items[item_name]
        return item.ap_cost(descriptors)


class AspectManager(object):

    def __init__(self):
        self.aspects = dict()

    def add_aspect(self, aspect):
        self.aspects[aspect.name] = aspect

    def cost(self, aspect_name, descriptors):
        aspect = self.aspects[aspect_name]

        base_cost = aspect.cost(descriptors)
        full_cost = base_cost

        for requirement in aspect.requirements:
            _, req_cost = self.cost(requirement.name, descriptors)
            full_cost += req_cost

        return base_cost, full_cost


class DescriptorManager(object):

    def __init__(self):
        self.effects = dict()

    def add_descdef(self, desdef_xml):
        name = desdef_xml.attrib['name']
        
        desdef = Descriptor(name)

        text_xml = find_child(desdef_xml, 'text')
        if text_xml is not None:
            desdef.text = sanitize_text(text_xml.text)
        
        if 'formula' in desdef_xml.attrib:
            desdef.formula = desdef_xml.attrib['formula']

            for entry_xml in desdef_xml:
                if entry_xml.tag == 'example':
                    desdef.add_example(entry_xml)     

        elif 'cost' in desdef_xml.attrib:
            desdef.cost = int(desdef_xml.attrib['cost'])

        else:
            for entry_xml in desdef_xml:
                if entry_xml.tag == 'value':
                    desdef.add_effect(entry_xml)

        self.effects[name] = desdef

    def get_effect(self, mod_name, effect_name):
        
        try:
            desdef = self.effects[mod_name]
            if len(desdef.entries) > 0:
                return int(desdef.entries[effect_name])
        except:
            print('Unable to find {} for effect {}'.format(mod_name, effect_name))
            return -1
        
        if desdef.formula != None:
            return get_formula(desdef.formula)(effect_name)

        else:
            return desdef.cost


class Descriptor(object):

    def __init__(self, name):
        self.name = name
        self.entries = dict()
        self.examples = list()
        self.formula = None
        self.cost = None
        self.text = None

    def add_example(self, example_xml):
        self.examples.append(example_xml.attrib['value'])

    def add_effect(self, entry_xml):
        effect_name = entry_xml.attrib['name']
        self.entries[effect_name] = entry_xml.attrib['cost']


class Detail(object):

    def __init__(self, detail_type, value):
        self.type = detail_type
        self.value = value


class AspectEffect(object):

    def __init__(self, name, effect=None):
        self.name = name
        self.effect = effect

        self.details = list()

    def add_detail(self, detail_xml):
        self.details.append(Detail(
            detail_xml.attrib['type'],
            detail_xml.attrib.get('value')))


class Requirement(object):

    def __init__(self, name):
        self.name = name


class Aspect(object):

    def __init__(self, name):
        self.name = name
        self.text = ''
        self.effects = list()
        self.requirements = list()

    def add_effect(self, effect_xml):
        self.effects.append(assemble_descriptor(effect_xml))

    def add_requirement(self, req_xml):
        self.requirements.append(Requirement(
            req_xml.attrib['name']))

    def cost(self, descriptor_manager):
        print('Calculating th ecost of: {}'.format(self.name))
        
        cost = 0
        for descriptor in self.effects:
            unit_cost = descriptor_manager.get_effect(
                descriptor.name, descriptor.effect)
            cost += unit_cost
            
            print('Cost of descriptor {} at {} is {} - Total is now: {}'.format(descriptor.name, descriptor.effect, unit_cost, cost))

        return cost if cost != 0 else 1


class Item(object):

    def __init__(self, name, item_type):
        self.text = ''
        self.name = name
        self.type = item_type
        self.cost = None
        self.grants = list()
        self.effects = list()

    def add_effect(self, effect_xml):
        self.effects.append(assemble_descriptor(effect_xml))

    def add_grant(self, grant_xml):
        self.grants.append(grant_xml.attrib['aspect'])

    def ap_cost(self, descriptor_manager):
        cost = 0
        for descriptor in self.effects:
            cost += descriptor_manager.get_effect(
                descriptor.name, descriptor.effect)

        return cost
