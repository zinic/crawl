import sys
import datetime
import xml.etree.ElementTree as etree

from crawl.model import *
from crawl.util import sanitize_text
from crawl.formulas import get_formula


SKILL_CHECK_DESC = 'Skill Check'
BASE_DIFFICULTY_DESC = 'Base Difficulty'
ACTION_POINT_COST_DESC = 'Action Point Cost'

def check_aspect(aspect):
    is_skill = False
    has_action_cost = False
    has_difficulty = False

    for descriptor in aspect.descriptors:
        if descriptor.name == SKILL_CHECK_DESC:
            is_skill = True
        elif descriptor.name == BASE_DIFFICULTY_DESC:
            has_difficulty = True
        elif descriptor.name == ACTION_POINT_COST_DESC:
            has_action_cost = True

    if is_skill:
        if not has_action_cost:
            print('Aspect {} has a skill check but no associated action point cost.'.format(aspect.name))

        if not has_difficulty:
            print('Aspect {} has a skill check but no associated base difficulty.'.format(aspect.name))


def format_descriptor(descriptor):
    output = '#### {}\n'.format(descriptor.name)
    
    if descriptor.text is not None:
        output += '{}\n\n'.format(descriptor.text)
    
    if descriptor.cost is not None:
        output += '* Aspect Point Cost: {}'.format(descriptor.cost)
    
    elif descriptor.formula is not None:
        output += '* Formula: {}\n\n'.format(descriptor.formula)
        
        output += '**Examples**\n\n'
        for example in descriptor.examples:
            output += '* **{}**\n\t* Aspect Point Cost: {}\n'.format(
                example, get_formula(descriptor.formula)(example))
    
    else:
        for name, value in descriptor.entries.items():
            output += '* **{}**\n\t* Aspect Point Cost: {}\n'.format(name, value)

    return '{}<br /><br />\n'.format(output)


def format_item(item, model):
    cost = model.item_cost(item.name)
    
    for grant in item.grants:
        base_cost, full_cost = model.aspect_cost(grant)
        cost += full_cost
    
    output = '#### {}\n'.format(item.name)
    output += '{}'.format(item.text)
    output += 'Monetary Cost: **{} $$**\n<br />'.format(cost * 120)
    output += '\n'
    
    for grant in item.grants:
        output += 'Grants Aspect: **[{}](#{})**<br />'.format(
            grant,
            grant.lower().replace(' ', '-'))
    
    output += '\n'
    
    if len(item.descriptors) > 0:
        output += '#### Details\n'

        for descriptor in item.descriptors:
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
                output += ': {}'.format(item.name)

            output += '\n'

            if len(details) > 0:
                output += details
    
    return '{}<br /><br />\n'.format(output)


def format_aspect(aspect, model):
    base_cost, full_cost = model.aspect_cost(aspect.name)

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

    return '{}<br /><br />\n'.format(output)


def process_document(root):
    model = DocumentManager()

    if root.tag != 'document':
        raise Exception('Expected document tag at top-level.')

    # Sort out the elements in the document
    descriptors_xml = None
    items_xml = None
    aspects_xml = None
    
    for element in root:
        if element.tag == 'descriptors':
            descriptors_xml = element
        elif element.tag == 'items':
            items_xml = element
        elif element.tag == 'aspects':
            aspects_xml = element
        elif element.tag == 'templates':
            pass
        else:
            raise Exception('Unexpected element: {}'.format(element.tag))

    # Process.descriptors first
    for descdef_xml in descriptors_xml:
        model.descriptors.add_descdef(descdef_xml)

    # Next process items
    for item_xml in items_xml:
        model.items.add_item(item_xml)

    # Lastly process aspects
    for aspect_xml in aspects_xml:
        aspect = Aspect(
            aspect_xml.attrib['name'])

        for part_xml in aspect_xml:
            if part_xml.tag == 'feature':
                aspect.add_feature(part_xml)

            elif part_xml.tag == 'requires':
                aspect.add_requirement(part_xml)

            elif part_xml.tag == 'text':
                aspect.text = sanitize_text(part_xml.text)

            else:
                raise Exception('Unexpected element: {}'.format(part_xml.tag))

        model.aspects.add_aspect(aspect)

    return model


def main():
    do_check = False

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == '--check':
                do_check = True

    # Process the doc
    core_tree = etree.parse('core.xml')
    root = core_tree.getroot()

    model = process_document(root)

    with open('out.md', 'w') as fout:
        fout.write('# The Crawl Aspect Document\n\n')
        fout.write('## Components\n')
        
        for name, descriptor in sorted(model.descriptors.descriptors.items()):
            fout.write('{}\n\n'.format(format_descriptor(descriptor)))
        
        fout.write('## Items\n')

        for _, item in sorted(model.items.items.items()):
            fout.write('{}\n\n'.format(format_item(item, model)))

        fout.write('## Aspects\n')

        for _, aspect in sorted(model.aspects.aspects.items()):
            if do_check:
                check_aspect(aspect)

            fout.write('{}\n\n'.format(format_aspect(aspect, model)))


if __name__ == '__main__':
    main()
