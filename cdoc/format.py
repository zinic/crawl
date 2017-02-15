def write_line(line, output):
    output.write('{}\n'.format(line))


def format_rules(model, output):
    write_line('## Rules', output)

    for rule in model.rules:
        write_line('#### Rule: {}'.format(rule.name), output)

        if rule.text is not None:
            write_line(rule.text, output)

        for option_name in rule.options:
            option = rule.options[option_name]
            write_line('* **{}**\n\t* Aspect Point Cost: {}\n'.format(option.name, option.cost), output)


def format_aspects(model, output):
    write_line('## Aspects', output)

    for aspect in model.aspects:
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
                cost_element.rule_name, cost_element.cost, cost_element.option_name)
            ap_cost += cost_element.cost

        write_line('Aspect Point Cost: {}'.format(ap_cost), output)
        write_line('#### Details\n{}'.format(cost_breakdown), output)


def format_markdown(model):
    with open('output.md', 'w') as output:
        write_line('# Crawl Aspect Document', output)
        format_rules(model, output)
        format_aspects(model, output)
