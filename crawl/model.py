from crawl.formulas import *


def assemble_descriptor(feature_xml):
    name = feature_xml.attrib['descriptor']
    feature = feature_xml.attrib.get('value')

    desc = Descriptor(name, feature)

    for detail_xml in feature_xml:
        desc.add_detail(detail_xml)

    return desc


class DocumentManager(object):
    
    def __init__(self):
        self.items = ItemManager()
        self.aspects = AspectManager()
        self.descriptors = DescriptorManager()

    def item_cost(self, name):
        return self.items.cost(name, self.aspects, self.descriptors)

    def aspect_cost(self, name):
        return self.aspects.cost(name, self.descriptors)


class ItemManager(object):
    
    def __init__(self):
        self.items = dict()

    def add(self, item):
        self.items[item.name] = item

    def cost(self, item_name, aspects, descriptors):
        item = self.items[item_name]
        return item.cost(descriptors)


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
        self.definitions = dict()

    def add_descdef(self, descdef_xml):
        moddef_name = descdef_xml.attrib['name']
        moddef = ModifierDefinition(moddef_name)

        if 'formula' in descdef_xml.attrib:
            moddef.formula = descdef_xml.attrib['formula']

        elif 'cost' in descdef_xml.attrib:
            moddef.cost = int(descdef_xml.attrib['cost'])

        else:
            for entry_xml in descdef_xml:
                if entry_xml.tag != 'feature':
                    raise Exception('Unexpected element {}'.format(entry_xml.tag))

                moddef.add_entry(entry_xml)

        self.definitions[moddef_name] = moddef

    def get_feature(self, mod_name, feature_name):
        moddef = self.definitions[mod_name]

        if len(moddef.entries) > 0:
            return int(moddef.entries[feature_name])

        if moddef.formula != None:
            return globals()[moddef.formula](feature_name)

        else:
            return moddef.cost


class ModifierDefinition(object):

    def __init__(self, name):
        self.name = name
        self.entries = dict()

        self.formula = None
        self.cost = 0

    def add_entry(self, entry_xml):
        feature_name = entry_xml.attrib['name']
        self.entries[feature_name] = entry_xml.attrib['cost']


class Detail(object):

    def __init__(self, detail_type, value):
        self.type = detail_type
        self.value = value


class Descriptor(object):

    def __init__(self, name, feature=None):
        self.name = name
        self.feature = feature

        self.details = list()

    def add_detail(self, detail_xml):
        self.details.append(Detail(
            detail_xml.attrib['type'],
            detail_xml.attrib['value']))


class Requirement(object):

    def __init__(self, name):
        self.name = name


class Aspect(object):

    def __init__(self, name):
        self.name = name
        self.text = ''
        self.descriptors = list()
        self.requirements = list()

    def add_feature(self, feature_xml):
        self.descriptors.append(assemble_descriptor(feature_xml))

    def add_requirement(self, req_xml):
        self.requirements.append(Requirement(
            req_xml.attrib['name']))

    def cost(self, descriptor_manager):
        cost = 0
        for descriptor in self.descriptors:
            cost += descriptor_manager.get_feature(
                descriptor.name, descriptor.feature)

        return cost if cost != 0 else 1


class Item(object):

    def __init__(self, name, item_type):
        self.text = ''
        self.name = name
        self.type = item_type
        self.grants = list()
        self.descriptors = list()

    def add_feature(self, feature_xml):
        self.descriptors.append(assemble_descriptor(feature_xml))

    def add_grant(self, grant_xml):
        self.grants.append(grant_xml.attrib['aspect'])

    def cost(self, descriptor_manager):
        cost = 0
        for descriptor in self.descriptors:
            cost += descriptor_manager.get_feature(
                descriptor.name, descriptor.feature)

        return cost
