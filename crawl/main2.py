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


class AspectManager(object):

    def __init__(self, descriptors):
        self.aspects = dict()
        self.descriptors = descriptors

    def add_aspect(self, aspect):
        self.aspects[aspect.name] = aspect

    def cost(self, aspect_name):
        aspect = self.aspects[aspect_name]

        base_cost = aspect.cost(self.descriptors)
        full_cost = base_cost

        for requirement in aspect.requirements:
            _, req_cost = self.cost(requirement.name)
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


def assemble_descriptor(feature_xml):
    name = feature_xml.attrib['descriptor']
    feature = feature_xml.attrib.get('value')

    desc = Descriptor(name, feature)

    for detail_xml in feature_xml:
        desc.add_detail(detail_xml)

    return desc


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
        self.name = name
        self.type = item_type
        self.descriptors = list()

    def add_feature(self, feature_xml):
        self.descriptors.append(assemble_descriptor(feature_xml))

    def cost(self, descriptor_manager):
        cost = 0
        for descriptor in self.descriptors:
            cost += descriptor_manager.get_feature(
                descriptor.name, descriptor.feature)

        return cost


def format_aspect(aspect, aspects):
    base_cost, full_cost = aspects.cost(aspect.name)

    output = '### {}\n'.format(aspect.name)
    output += '{}'.format(aspect.text)
    output += 'Aspect Point Cost: **{} AP**\n<br />'.format(base_cost)
    output += 'Capstone Cost: **{} AP**\n'.format(full_cost)
    output += '\n'

    for req in aspect.requirements:
        output += 'Requires: **[{}](#{})**<br />'.format(
            req.name,
            req.name.lower().replace(' ', '-'))

    output += '\n'

    if len(aspect.descriptors) > 0:
        output += '#### Details\n'
        
        for descriptor in aspect.descriptors:
            details = ''
    
            for detail in descriptor.details:
                if detail.type == 'targets':
                    details += '\t* Applies to: **{}**\n'.format(detail.value)
    
                elif detail.type == 'energy_type':
                    details += '\t* Magic Energy Type: **{}**\n'.format(detail.value)
    
                elif detail.type == 'base_difficulty':
                    details += '\t* Base Difficulty: **{}**\n'.format(detail.value)
                    
                elif detail.type == 'inherits_from':
                    details += '\t* Inherits Modifiers from: **{}**\n'.format(detail.value)
    
                elif detail.type == 'limit':
                    details += '\t* Limited: **{}**\n'.format(detail.value)
    
                else:
                    details += '\t* {}: {}\n'.format(detail.type, detail.value)
    
            output += '* {}'.format(descriptor.name)
    
            if descriptor.feature is not None:
                output += ': {}'.format(descriptor.feature)
                
            elif descriptor.name == 'Skill Check':
                output += ': {}'.format(aspect.name)
    
            output += '\n'
    
            if len(details) > 0:
                output += details

    return output


def sanitize_text(text):
    output = ''
    for line in text.split('\n'):
        output += '{}\n'.format(line.strip())
    return output


#
eq_tree = etree.parse('core.xml')
root = eq_tree.getroot()

if root.tag != 'document':
    raise Exception('Expected document tag at top-level.')


descriptors = DescriptorManager()
aspects = AspectManager(descriptors)

for element in root:
    if element.tag == 'descriptors':
        for descdef_xml in element:
            descriptors.add_descdef(descdef_xml)

        break

for element in root:
    if element.tag == 'descriptors':
        continue

    elif element.tag == 'items':
        # print('\nItems\n')

        for item_xml in element:
            item = Item(
                item_xml.attrib['name'],
                item_xml.attrib['type'])

            for feature_xml in item_xml:
                item.add_feature(feature_xml)

            # print('Item {} costs {} AP.'.format(item.name, item.cost(descriptors)))

    elif element.tag == 'aspects':
        print('\n## Aspects\n')

        for aspect_xml in element:
            aspect = Aspect(
                aspect_xml.attrib['name'])

            for part in aspect_xml:
                if part.tag == 'feature':
                    aspect.add_feature(part)

                elif part.tag == 'requires':
                    aspect.add_requirement(part)

                elif part.tag == 'text':
                    aspect.text = sanitize_text(part.text)

                else:
                    Exception('Unexpected element: {}'.format(part.tag))

            aspects.add_aspect(aspect)

        for _, aspect in sorted(aspects.aspects.items()):
            print('{}\n\n'.format(format_aspect(aspect, aspects)))

    else:
        raise Exception('Unexpected element: {}'.format(element.tag))
