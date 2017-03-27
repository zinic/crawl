import io


def write_line(line, output):
    output.write('{}\n'.format(line))


def format_character_aspect(char_aspect, model, output):
    if char_aspect.origin == 'character':
        format_aspect(char_aspect.definition, model, output)
        return

    aspect = char_aspect.definition
    write_line('### {}'.format(aspect.name), output)

    if aspect.text is not None:
        write_line(aspect.text, output)

    write_line('', output)

    write_line('Aspect Point Cost: Provided by Item', output)


def format_character(character, model, output):
    core_aspects = io.StringIO()
    aspect_list = io.StringIO()
    for char_aspect in character.aspects:
        buffer = aspect_list if char_aspect.origin != 'core' else core_aspects
        format_character_aspect(char_aspect, model, buffer)

    # Write the character header
    write_line('# {}'.format(character.name), output)

    write_line('## Details', output)
    write_line('### Aspect Points', output)
    write_line('* AP Total: {}'.format(character.aspect_points), output)
    write_line('* AP Spent: {}'.format(character.aspect_points_spent), output)
    write_line('* AP Available: {}'.format(character.aspect_points - character.aspect_points_spent), output)

    write_line('### Monetary Funds', output)
    write_line('* Starting Funds: $$ {}'.format(character.monetary_funds_start), output)
    write_line('* <span style="color: green;">Funds Gained: $$ {}</span>'.format(character.monetary_funds), output)
    write_line('* <span style="color: red;">Funds Spent: $$ {}</span>'.format(character.monetary_funds_spent), output)
    write_line('* Funds Available: $$ {}'.format(character.monetary_funds - character.monetary_funds_spent), output)

    write_line('## Resources', output)
    for name in sorted(character.resources.keys()):
        if name == 'Monetary Funds':
            continue

        resource = character.resources[name]
        write_line('* **{}:** {}'.format(name, resource), output)

    write_line('## Skill Stats', output)

    for name in sorted(character.skills.keys()):
        skill = character.skills[name]
        write_line('* **{}**\n\t* {}\n\t* Modifier: {}'.format(
            skill.name,
            skill.difficulty,
            '+{}'.format(skill.modifier) if skill.modifier > 0 else skill.modifier), output)

    write_line('## Aspect List', output)

    # write_line('### Core Aspects', output)
    # write_line(core_aspects.getvalue(), output)

    write_line(aspect_list.getvalue(), output)

    write_line('## Character Inventory', output)
    for item in character.items:
        format_item(item, model, output)


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

        write_line('* **{}**\n\t* Aspect Point Cost: {}\n'.format(option.name, option.ap_cost), output)
        if option.text is not None:
            write_line('\n{}\n'.format(option.text), output)


def name_to_anchor(name):
    return '#{}'.format(
        name.lower().replace(' ', '-'))


def format_aspect(aspect, model, output):
    write_line('### {}'.format(aspect.name), output)

    if aspect.text is not None:
        write_line(aspect.text, output)

    for requirement in aspect.requirements:
        write_line('Requires: **[{}]({})**\n'.format(requirement, name_to_anchor(requirement)), output)

    write_line('', output)

    ap_cost = 0
    cost_breakdown = ''

    if aspect.template != 'core':
        for cost_element in model.aspect_cost_breakdown(aspect).cost_elements:
            modifier_output = ''
            if cost_element.modifiers is not None and len(cost_element.modifiers) > 0:
                modifier_output = ' ({})'.format(', '.join(cost_element.modifiers))

            cost_breakdown += '* {} (**{} AP**): {}{}\n'.format(
                cost_element.name, cost_element.ap_cost, cost_element.option.name, modifier_output)
            ap_cost += cost_element.ap_cost

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
    cost_breakdown = ''
    for cost_element in model.item_cost_breakdown(item).cost_elements:
        cost_breakdown += '* {}: {} (**$$ {}**)\n'.format(
            cost_element.name, cost_element.option.name, cost_element.monetary_cost)
        total_cost += cost_element.monetary_cost

    write_line('\nMonetary Value: $${}'.format(total_cost), output)
    write_line('#### Details'.format(), output)

    if item.wearable is not None:
        write_line('Worn on Item Slot: **{}**'.format(item.wearable.slot), output)

    write_line(cost_breakdown, output)


def format_items(model, output):
    write_line('## Items', output)

    for item in model.items():
        format_item(item, model, output)


def format_markdown(model, output):
    write_line('# Crawl Aspect Document', output)
    format_rules(model, output)
    format_aspects(model, output)
    format_items(model, output)
