import datetime

import xml.etree.ElementTree as etree
import crawl.html as html


# Costs start at 4 and go up from there by 2
def damage_value_cost(dmg):
    return (dmg - 4) / 2


# cost = number of dice + damage value cost
def damage_cost(value):
    num_st, die_st = value.split('d')

    num = int(num_st)
    die = int(die_st)

    damage_value = num * die
    return num + damage_value_cost(damage_value)


def damage_resistance_cost(value):
    return 100


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


class ItemDescriptor(object):

    def __init__(self, name, feature, feature_type):
        self.name = name
        self.feature = feature
        self.feature_type = feature_type


class Item(object):

    def __init__(self, name, item_type):
        self.name = name
        self.type = item_type
        self.descriptors = list()

    def add_feature(self, feature_xml):
        self.descriptors.append(ItemDescriptor(
            feature_xml.attrib['descriptor'],
            feature_xml.attrib['value'],
            feature_xml.attrib.get('type')))

    def cost(self, descriptor_manager):
        cost = 0
        for descriptor in self.descriptors:
            cost += descriptor_manager.get_feature(
                descriptor.name, descriptor.feature)

        return cost


#
eq_tree = etree.parse('equipment.xml')
root = eq_tree.getroot()

if root.tag != 'document':
    raise Exception('Expected document tag at top-level.')


descriptors = DescriptorManager()

for element in root:
    if element.tag == 'descriptors':
        for descdef_xml in element:
            descriptors.add_descdef(descdef_xml)

        break

for element in root:
    if element.tag == 'descriptors':
        continue

    elif element.tag == 'items':
        for item_xml in element:
            item = Item(
                item_xml.attrib['name'],
                item_xml.attrib['type'])

            for feature_xml in item_xml:
                item.add_feature(feature_xml)

            print('Item {} costs {} AP.'.format(item.name, item.cost(descriptors)))
        
    else:
        raise Exception('Unexpected element: {}'.format(element.tag))
