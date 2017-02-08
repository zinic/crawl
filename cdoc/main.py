import re
import sys
import math
import xml.etree.ElementTree as etree

from cdoc.formulas import *
from cdoc.model import *


def formula_absolute(rule):
    default_cost = rule.formula().argument('cost', 0)

    results = list()
    for option in rule.options():
        cost = option.attr('cost', default_cost)
        results.append('{}: {}'.format(option.name, cost))
    return results


# Costs start at 4 and go up from there by 2
def damage_value_cost(dmg):
    return dmg


class OptionPositionInfo(object):
    def __init__(self, option, range_name, position):
        self.option = option
        self.range_name = range_name
        self.position = position

    def format_name(self):
        option_name = self.option.name

        matched = dict()
        if '{rn}' in option_name:
            matched['rn'] = self.range_name

        if '{position}' in option_name:
            matched['position'] = self.position

        return option_name.format(**matched)


def iterate_options(rule):
    i = 0

    # Process args first
    for argument in rule.formula.arguments:
        if argument.name == 'Basic Start':
            i = 1
        elif argument.name == 'Easy Start':
            i = 2
        elif argument.name == 'Normal Start':
            i = 3
        elif argument.name == 'Hard Start':
            i = 5
        elif argument.name == 'Heroic Start':
            i = 8

    for option in rule.options:
        values = [i]

        if option.range is not None:
            start, end = [int(v) for v in option.range.split(',')]
            if start < end:
                values = range(start, end + 1)
            else:
                values = reversed(range(end, start + 1))

        for r in values:
            i += 1
            yield OptionPositionInfo(option, r, i)


DICE_REGEX = re.compile('[\d]+d[\d]+')


def formula_damage_cost(rule):
    for op_info in iterate_options(rule):
        cost = damage_value_cost(op_info.position)
        formatted_name = op_info.format_name()

        if DICE_REGEX.match(formatted_name):
            # Figure out the number of dice and number of sides
            num_dice, sides = [int(v) for v in formatted_name.split('d')]

            # Cost is number of dice + damage value
            cost = num_dice - 1 + damage_value_cost(num_dice * sides)

        yield formatted_name, cost


class FormulaContext():
    def __init__(self, model):
        self._model = model
        self._provided = {
            'absolute': formula_absolute,
            'damage_cost': formula_damage_cost,
        }

    def calc_provided(self, rule, formula):
        real_func = self._provided[formula.function]
        return real_func(rule)

    @classmethod
    def calc_custom(cls, rule, formula):
        # Set up the globals
        env = {
            'abs': math.fabs,
            'pow': math.pow,
            'fib': Fibonacci(1000),
        }

        for op_info in iterate_options(rule):
            # Increase the rule iteration num and overwrite it in the eval env
            env['i'] = op_info.position

            # Run the calc - this is so nasty
            cost = eval(formula.equation, env)

            # Yield the result
            yield op_info.format_name(), int(cost)

    def cost_of(self, rule, target):
        for name, cost in self.calc(rule):
            if name == target:
                return cost
        raise Exception('Unable to find cost for rule {} targeting {}'.format(rule.name, target))

    def calc(self, rule):
        fref = rule.formula.ref
        formula = self._model.formula(fref)

        cost_filter = lambda c: c
        for argument in rule.formula.arguments:
            if argument.name == 'Returns AP':
                cost_filter = lambda c: -1 * c

        if formula.type == 'custom':
            for name, cost in self.calc_custom(rule, formula):
                yield name, cost_filter(cost)

        elif formula.type == 'provided':
            for name, cost in self.calc_provided(rule, formula):
                yield name, cost_filter(cost)


def write_line(line, output):
    output.write('{}\n'.format(line))


def format_rules(model, output):
    formula_ctx = FormulaContext(model)

    write_line('## Rules', output)

    for rule in model.rules():
        write_line('#### Rule: {}'.format(rule.name), output)

        if rule.text is not None:
            write_line(rule.text, output)

        for name, cost in formula_ctx.calc(rule):
            write_line('* **{}**\n\t* Aspect Point Cost: {}\n'.format(name, cost), output)


def iterate_costs(model, aspect):
    formula_ctx = FormulaContext(model)

    for aspect_rule in aspect.rules:
        rule = model.rule(aspect_rule.ref)

        if rule is None:
            raise Exception('Rule {} does not exist'.format(aspect_rule.ref))

        ap_cost = formula_ctx.cost_of(rule, aspect_rule.value)

        yield aspect_rule, ap_cost


def format_aspects(model, output):
    write_line('## Aspects', output)

    for aspect in model.aspects():
        write_line('### {}'.format(aspect.name), output)

        if aspect.text is not None:
            write_line(aspect.text, output)

        for requirement in aspect.requirements:
            write_line('Requires: **[{}](#)**\n'.format(requirement.name), output)

        write_line('', output)

        ap_cost = 0
        cost_breakdown = ''
        for rule, cost in iterate_costs(model, aspect):
            cost_breakdown += '* {} (**{} AP**): {}\n'.format(rule.ref, cost, rule.value)
            ap_cost += cost

        write_line('Aspect Point Cost: {}'.format(ap_cost), output)
        write_line('#### Details\n{}'.format(cost_breakdown), output)


def format_markdown(model):
    with open('output.md', 'w') as output:
        write_line('# Crawl Aspect Document', output)
        format_rules(model, output)
        format_aspects(model, output)

    for aspect in model.aspects():
        template = model.template(aspect.template)

        if template is not None:
            template.validate(aspect)


def main():
    rule_filter = ''

    if len(sys.argv) > 1:
        rule_filter = sys.argv[1].lower()

    # Process the doc
    core_tree = etree.parse('template.xml')
    root = core_tree.getroot()

    model = Document(root)
    model.check()

    format_markdown(model)

    print('OK')


if __name__ == '__main__':
    main()
