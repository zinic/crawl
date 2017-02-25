import io


def write_line(line, output):
    output.write('{}\n'.format(line))


def format_character(char, model, output):
    ap_total = 0
    core_aspects = io.StringIO()
    aspect_list = io.StringIO()
    for aspect in char.aspects.values():
        if aspect.template != 'core':
            ap_total += model.ap_cost_breakdown(aspect).total
            format_aspect(aspect, model, aspect_list)
        else:
            format_aspect(aspect, model, core_aspects)

    write_line('# {}'.format(char.name), output)
    write_line('## Stats', output)

    for stat_name, value in char.stats(model).items():
        write_line('* **{}**: {}'.format(stat_name, value), output)

    write_line('## Details', output)
    write_line('* AP Total: {}'.format(char.aspect_points), output)
    write_line('* AP Spent: {}'.format(ap_total), output)
    write_line('* AP Available: {}'.format(char.aspect_points - ap_total), output)

    write_line('## Aspect List', output)

    # write_line('### Core Aspects', output)
    # write_line(core_aspects.getvalue(), output)

    write_line('### Aspects', output)
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
    for cost_element in model.ap_cost_breakdown(aspect).cost_elements:
        cost_breakdown += '* {} (**{} AP**): {}\n'.format(
            cost_element.rule_name, cost_element.cost, cost_element.option_name)
        ap_cost += cost_element.cost

    write_line('Aspect Point Cost: {}'.format(ap_cost), output)
    write_line('#### Details\n{}'.format(cost_breakdown), output)


def format_aspects(model, output):
    write_line('## Aspects', output)

    for aspect in model.aspects():
        format_aspect(aspect, model, output)


def format_markdown(model):
    with open('output.md', 'w') as output:
        write_line('# Crawl Aspect Document', output)
        format_rules(model, output)
        format_aspects(model, output)
