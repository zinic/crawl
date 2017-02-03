import re
import sys
import math
import xml.etree.ElementTree as etree

from cdoc.formulas import *
from cdoc.model import *


class NamedRepo(dict):
    def register(self, k, v):
        self[k] = v


class RuleRepo(NamedRepo):
    pass


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
        self.range_name =range_name
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
    for argument in rule.formula().arguments():
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

    for option in rule.options():
        values = [i]

        if option.has_attr('name-range'):
            start, end = [int(v) for v in option.attr('name-range').split(',')]
            if start < end:
                values = range(start, end + 1)
            else:
                values = reversed(range(end, start + 1))

        for r in values:
            i += 1
            yield OptionPositionInfo(option, r, i)


DICE_REGEX = re.compile('[\d]+d[\d]+')


def formula_damage_cost(rule):
    cost_filter = lambda c: c
    for argument in rule.formula().arguments():
        if argument == 'Returns AP':
            cost_filter = lambda c: -1 * c

    for op_info in iterate_options(rule):
        cost = damage_value_cost(op_info.position)
        formatted_name = op_info.format_name()

        if DICE_REGEX.match(formatted_name):
            # Figure out the number of dice and number of sides
            num_dice, sides = [int(v) for v in formatted_name.split('d')]

            # Cost is number of dice + damage value
            cost = num_dice - 1 + damage_value_cost(num_dice * sides)

        yield formatted_name, cost_filter(cost)


class FormulaDefinition(object):
    def __init__(self):
        pass


class FormulaRepo(NamedRepo):
    def __init__(self):
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

    def calc(self, rule):
        fref = rule.formula()
        if fref.has_attr('ref'):
            formula = self[fref.ref]

            if formula.type == 'custom':
                return self.calc_custom(rule, formula)
            elif formula.type == 'provided':
                return self.calc_provided(rule, formula)

        else:
            print('Formula definition for {} has no ref!'.format(rule.name))


def load_rules(model):
    repo = RuleRepo()

    for rule in model.rules():
        repo.register(rule.name, rule)

    return repo


def load_formulas(model):
    repo = FormulaRepo()

    for formula in model.formulas():
        repo.register(formula.id, formula)

    return repo


def main():
    rule_filter = ''

    if len(sys.argv) > 1:
        rule_filter = sys.argv[1].lower()

    # Process the doc
    core_tree = etree.parse('template.xml')
    root = core_tree.getroot()

    model = Document(root)
    model.check()

    formula_defs = load_formulas(model)
    rule_defs = load_rules(model)

    for rule in rule_defs.values():
        if rule_filter is not None and rule_filter not in rule.name.lower():
            continue

        if not rule.has_node('formula'):
            print('Rule {} has no formula!'.format(rule.name))
            continue

        results = formula_defs.calc(rule)
        if results is not None:
            print('Rule: {}'.format(rule.name))
            for name, cost in results:
                if rule.formula().argument('Returns AP', False, bool) is True:
                    cost *= -1

                print('\t{}: {} AP'.format(name, cost))

    print('OK')


if __name__ == '__main__':
    main()
