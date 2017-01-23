import math
import sys
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
    return int((dmg - 4) / 2)


def formula_damage_cost(rule):
    results = list()
    for option in rule.options():
        roll = option.name
        num, die = [int(v) for v in roll.split('d')]
        cost = num + damage_value_cost(num * die)

        results.append('{}: {}'.format(option.name, cost))
    return results


class FormulaDefinition(object):
    def __init__(self):
        pass


class FormulaRepo(NamedRepo):
    def __init__(self):
        self._provided = {
            'absolute': formula_absolute,
            'damage_cost': formula_damage_cost
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

        # Track results
        results = list()
        i = rule.formula().argument('start', 0, int)

        for option in rule.options():
            # Increase the rule iteration num and overwrite it in the eval env
            i += 1
            env['i'] = i

            # Run the calc - this is so nasty
            cost = eval(formula.equation, env)
            results.append('{}: {}'.format(option.name, int(cost)))

        return results

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
        rule_filter = sys.argv[1]

    # Process the doc
    core_tree = etree.parse('template.xml')
    root = core_tree.getroot()

    model = Document(root)
    model.check()

    formula_defs = load_formulas(model)
    rule_defs = load_rules(model)

    for rule in rule_defs.values():
        if rule_filter is not None and rule_filter not in rule.name:
            continue

        if not rule.has_node('formula'):
            print('Rule {} has no formula!'.format(rule.name))
            continue

        results = formula_defs.calc(rule)
        if results is not None:
            print('Rule: {}'.format(rule.name))
            for result in results:
                print('\t{}'.format(result))

    print('OK')


if __name__ == '__main__':
    main()
