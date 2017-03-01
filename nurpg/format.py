import io


def write_line(line, output):
    output.write('{}\n'.format(line))


def format_character(char, model, output):
    ap_total = 0
    core_aspects = io.StringIO()
    aspect_list = io.StringIO()
    for aspect in char.aspects.values():
        if aspect.template != 'core':
            ap_total += model.aspect_cost_breakdown(aspect.name).ap_total
            format_aspect(aspect, model, aspect_list)
        else:
            format_aspect(aspect, model, core_aspects)

    write_line('# {}'.format(char.name), output)

    write_line('## Details', output)
    write_line('* AP Total: {}'.format(char.aspect_points), output)
    write_line('* AP Spent: {}'.format(ap_total), output)
    write_line('* AP Available: {}'.format(char.aspect_points - ap_total), output)

    write_line('## Resources', output)
    for name in sorted(char.resources.keys()):
        value = char.resources[name]
        write_line('* **{}:** {}'.format(name, value), output)

    write_line('## Skill Stats', output)

    for name in sorted(char.skills.keys()):
        skill = char.skills[name]
        write_line('* **{}**\n\t* {}\n\t* Modifier: {}'.format(
            skill.name,
            skill.difficulty,
            '+{}'.format(skill.modifier) if skill.modifier > 0 else skill.modifier), output)

    write_line('## Aspect List', output)

    # write_line('### Core Aspects', output)
    # write_line(core_aspects.getvalue(), output)

    write_line(aspect_list.getvalue(), output)


def format_rules(model, output):
    write_line('## Rules', output)

    write_line('### Universal Rules', output)
    write_line('Universal rules may apply to anything in a game universe.', output)

    for rule in model.rules(cat_filter='all'):
        format_rule(rule, output)

    write_line('### Item Rules', output)
    write_line('Rules that apply to items only.', output)

    for rule in model.rules(cat_filter='item'):
        format_rule(rule, output)

    write_line('### Charcater Rules', output)
    write_line('Rules that apply to characters only.', output)

    for rule in model.rules(cat_filter='character'):
        format_rule(rule, output)


def format_rule(rule, output):
    write_line('#### Rule: {}'.format(rule.name), output)

    if rule.text is not None:
        write_line(rule.text, output)

    for option_name in rule.options:
        option = rule.options[option_name]
        write_line('* **{}**\n\t* Aspect Point Cost: {}\n'.format(option.name, option.cost), output)


def format_aspect_name(name):
    return name.replace(' ', '_')


def format_aspect(aspect, model, output):
    write_line('### {}'.format(aspect.name), output)

    if aspect.text is not None:
        write_line(aspect.text, output)

    for requirement in aspect.requirements:
        write_line('Requires: **[{}](#)**\n'.format(requirement), output)

    write_line('', output)

    ap_cost = 0
    cost_breakdown = ''
    for cost_element in model.aspect_cost_breakdown(aspect.name).cost_elements:
        cost_breakdown += '* {} (**{} AP**): {}\n'.format(
            cost_element.name, cost_element.cost, cost_element.option.name)
        ap_cost += cost_element.cost

    write_line('Aspect Point Cost: {}'.format(ap_cost), output)
    write_line('#### Details\n{}'.format(cost_breakdown), output)


def format_aspects(model, output):
    write_line('## Aspects', output)

    for aspect in model.aspects():
        format_aspect(aspect, model, output)


def format_item(item, model, output):
    write_line('### {}'.format(item.name), output)

    if item.text is not None:
        write_line(item.text, output)

    total_cost = 0
    grants_breakdown = ''
    for grant in item.grants:
        grant_cost = model.aspect_cost_breakdown(grant).ap_total
        total_cost += grant_cost

        grants_breakdown += '* {} (**{} AP**)'.format(grant, grant_cost)

    cost_breakdown = ''
    for cost_element in model.item_cost_breakdown(item.name).cost_elements:
        cost_breakdown += '* {} (**{} AP**)\n'.format(
            cost_element.name, cost_element.cost)
        total_cost += cost_element.cost

    write_line('Monetary Cost: $${}'.format(total_cost * 100), output)
    write_line('#### Details'.format(), output)

    if item.wearable is not None:
        write_line('Worn on Item Slot: **{}**'.format(item.wearable.slot), output)

    write_line(cost_breakdown, output)

def format_items(model, output):
    write_line('## Items', output)

    for item in model.items():
        format_item(item, model, output)


def format_markdown(model):
    with open('output.md', 'w') as output:
        write_line('# Crawl Aspect Document', output)
        format_rules(model, output)
        format_aspects(model, output)
        format_items(model, output)
