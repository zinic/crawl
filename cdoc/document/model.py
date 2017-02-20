import re
import math
import collections

import cdoc.formulas as formulas

DICE_REGEX = re.compile('[\d]+d[\d]+')


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


class OptionGenerator(object):
    def __init__(self):
        self._env = {
            'abs': math.fabs,
            'pow': math.pow,
            'fib': formulas.generate_fibonacci(1000),
        }

    @classmethod
    def calculate_damage_cost(cls, option_info):
        cost = option_info.position
        formatted_name = option_info.format_name()

        # Check if the damage is defined as a dice roll
        if DICE_REGEX.match(formatted_name):
            # Figure out the number of dice and number of sides
            num_dice, sides = [int(v) for v in formatted_name.split('d')]

            # Cost is number of dice + damage value
            cost = num_dice - 1 + num_dice * sides

        return RuleOption(formatted_name, int(cost))

    def calculate_option(self, formula, option_info):
        if formula.type == 'custom':
            # Copy the environment every time
            env_copy = self._env.copy()

            # Set the rule iteration num
            env_copy['i'] = option_info.position

            # This is so nasty...
            cost = eval(formula.equation, env_copy)

            # Return as a formula result
            return RuleOption(option_info.format_name(), int(cost))

        if formula.function == 'damage_cost':
            return self.calculate_damage_cost(option_info)

        raise Exception('Unknown formula => {}::{}'.format(formula.type, formula.function))


def iterate_options(rule_xml):
    i = 0
    for option in rule_xml.options:
        values = [i]

        # Values may have a short-hand notation to generate additional options in a range
        if option.range is not None:
            start, end = [int(v) for v in option.range.split(',')]
            if start < end:
                values = range(start, end + 1)
            else:
                values = reversed(range(end, start + 1))

        for r in values:
            i += 1
            yield OptionPositionInfo(option, r, i)


class Model(object):
    def __init__(self, document):
        self._document = document

        self._rules = dict()
        self._templates = dict()
        self._aspects = dict()

        self._generate(document)

    def check(self):
        for rule in self.rules():
            if rule.category is None:
                raise Exception('Rule "{}" is lacking a category.'.format(rule.name))

        for aspect in self.aspects():
            # Templates are not required for all aspects yet
            if aspect.template is not None:
                template = self._templates[aspect.template]
                template.validate_aspect(aspect)

            cost_breakdown = self.lookup_ap_cost_breakdown(aspect.name)
            if cost_breakdown.total <= 0:
                raise Exception('Aspect {} has an invalid AP cost of: {}'.format(
                    aspect.name, cost_breakdown.total))

    def _generate(self, document):
        option_generator = OptionGenerator()

        for rule_xml in document.rules():
            rule = Rule.from_xml(option_generator, rule_xml, document.formula(rule_xml.formula.ref))
            self._rules[rule.name] = rule

        for template_xml in document.templates():
            template = Template.from_xml(template_xml)
            self._templates[template.name] = template

        for aspect_xml in document.aspects():
            aspect = Aspect.from_xml(aspect_xml)
            self._aspects[aspect.name] = aspect

    def lookup_ap_cost_breakdown(self, name):
        return self.ap_cost_breakdown(self._aspects[name])

    def ap_cost_breakdown(self, aspect):
        cost_bd = AspectCostBreakdown()
        for rule_ref in aspect.rule_references:
            rule = self._rules[rule_ref.rule_name]

            # Since many rules only have one option of the same name, I made this a bit easier
            option_target = rule_ref.option if rule_ref.option is not None else rule_ref.rule_name
            option = rule.options[option_target]

            cost_ref = AspectCostReference(rule.name, option.name, option.cost)
            cost_bd.cost_elements.append(cost_ref)

        return cost_bd

    def aspects(self):
        return [self._aspects[k] for k in sorted(self._aspects.keys())]

    def rules(self, cat_filter=None):
        rules = list()

        for key in sorted(self._rules):
            rule = self._rules[key]

            if cat_filter is not None and rule.category != cat_filter:
                continue

            rules.append(rule)

        return rules


class Rule(object):
    def __init__(self, name, category, text):
        self.name = name
        self.category = category
        self.text = text
        self.options = collections.OrderedDict()

    @classmethod
    def from_xml(cls, option_generator, rule_xml, formula_xml):
        rule = cls(rule_xml.name, rule_xml.category, rule_xml.text)
        for option_info in iterate_options(rule_xml):
            calculated_option = option_generator.calculate_option(formula_xml, option_info)
            rule.options[calculated_option.name] = calculated_option

        return rule


class RuleOption(object):
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


class Template(object):
    def __init__(self, name):
        self.name = name
        self.requirements = list()

    def validate_aspect(self, aspect):
        for required_rule in self.requirements:
            aspect_rule_ref = aspect.rule_reference(required_rule)

            if aspect_rule_ref is None:
                raise Exception(
                    'Aspect {} does not conform to template {}.\nAspect is missing: {}'.format(
                        aspect.name, self.name, required_rule))

    @classmethod
    def from_xml(cls, template_xml):
        template = cls(template_xml.name)

        for template_requirement_xml in template_xml.requirements:
            template.requirements.append(template_requirement_xml.rule)

        return template


class Aspect(object):
    def __init__(self, name, template, text):
        self.name = name
        self.template = template
        self.text = text
        self.requirements = list()
        self.rule_references = list()

    def rule_reference(self, rule_name):
        for rule_ref in self.rule_references:
            if rule_ref.rule_name == rule_name:
                return rule_ref
        return None

    @classmethod
    def from_xml(cls, aspect_xml):
        aspect = cls(aspect_xml.name, aspect_xml.template, aspect_xml.text)

        for aspect_requirement_xml in aspect_xml.requirements:
            aspect.requirements.append(aspect_requirement_xml.name)

        for rule_ref_xml in aspect_xml.rules:
            aspect.rule_references.append(RuleReference(rule_ref_xml.ref, rule_ref_xml.value))

        return aspect


class AspectCostBreakdown(object):
    def __init__(self):
        self.cost_elements = list()

    @property
    def total(self):
        ap_cost = 0
        for cost_element in self.cost_elements:
            ap_cost += cost_element.cost

        return ap_cost


class RuleReference(object):
    def __init__(self, rule_name, value):
        self.rule_name = rule_name
        self.option = value


class AspectCostReference(object):
    def __init__(self, rule_name, option_name, cost):
        self.rule_name = rule_name
        self.option_name = option_name
        self.cost = cost
