import io


def write_line(line, output):
    output.write('{}\n'.format(line))


def format_character(char, model, output):
    write_line('## Character Sheet', output)
    write_line('### Details', output)
    write_line('**Name:** {}'.format(char.name), output)

    ap_total = 0
    aspect_list = io.StringIO()
    for aspect_ref in char.aspects:
        aspect = model.aspect(aspect_ref)
        aspect_cost = model.ap_cost_breakdown(aspect)

        ap_total += aspect_cost.total

        write_line('##### {}'.format(aspect.name), aspect_list)
        write_line('* Aspect Point Cost: **{} AP**'.format(aspect_cost.total), aspect_list)

    write_line('### Aspects', output)
    write_line('#### AP Required: {}'.format(ap_total), output)
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
