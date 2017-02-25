import re
import math
import collections

import nurpg.formulas as formulas

DICE_REGEX = re.compile('[\d]+d[\d]+')


class OptionPositionInfo(object):
    def __init__(self, option, range_value, position):
        self.option = option
        self.range_value = range_value
        self.position = position

    def format_name(self):
        option_name = self.option.name

        matched = dict()
        if '{range_value}' in option_name:
            is_prefix = option_name.startswith('{range_value}')

            value = self.range_value
            if self.range_value < 0 and is_prefix is False:
                value = int(math.fabs(value))
            elif self.range_value > 0 and is_prefix is True:
                value = '+{}'.format(value)

            matched['range_value'] = value

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
        cost = option_info.range_value
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

            # Set the definition iteration num
            env_copy['i'] = option_info.range_value

            # This is so nasty...
            cost = eval(formula.equation, env_copy)

            # Return as a formula result
            return RuleOption(option_info.format_name(), int(cost))

        if formula.function == 'damage_cost':
            return self.calculate_damage_cost(option_info)

        raise Exception('Unknown formula => {}::{}'.format(formula.type, formula.function))


def iterate_options(rule_xml):
    # Positions start at 1
    i = 1

    # Iterate through the defined options
    for option in rule_xml.options:
        # Values start with the position of the option
        values = [i]

        # Values may have a short-hand notation to generate additional options in a range
        if option.range is not None:
            start, end = [int(v) for v in option.range.split(',')]
            values = range(start, end + 1)

        for r in values:
            i += 1

            # By default we always skip and value that resolves its range to 0
            if r == 0:
                continue

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
        for rule in aspect.selected_rules(self):
            cost_ref = AspectCostReference(rule.definition.name, rule.option.name, rule.option.cost)
            cost_bd.cost_elements.append(cost_ref)

        return cost_bd

    def aspect(self, name):
        return self._aspects[name]

    def aspects(self):
        return [self._aspects[k] for k in sorted(self._aspects.keys())]

    def rule(self, name):
        return self._rules[name]

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
        self.modifiers = list()
        self.text = text
        self.options = collections.OrderedDict()

    def add_modifier(self, modifier_target):
        self.modifiers.append(modifier_target)

    @classmethod
    def from_xml(cls, option_generator, rule_xml, formula_xml):
        rule = cls(rule_xml.name, rule_xml.category, rule_xml.text)
        for modifier_xml in rule_xml.modifiers:
            rule.add_modifier(modifier_xml.ref)

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
            if not aspect.has_rule(required_rule):
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

        self._rule_references = list()
        self._predefined_rules = list()

    def add_predefined_rule(self, rule):
        self._predefined_rules.append(rule)

    def selected_rules(self, model):
        rules = [rf.realize(model) for rf in self._rule_references]
        for predefined in self._predefined_rules:
            rules.append(RuleSelection(predefined, predefined.name))
        return rules

    def has_rule(self, rule_name):
        for rf in self._rule_references:
            if rf.rule_name == rule_name:
                return True
        return False

    @classmethod
    def from_xml(cls, aspect_xml):
        aspect = cls(aspect_xml.name, aspect_xml.template, aspect_xml.text)

        for aspect_requirement_xml in aspect_xml.requirements:
            aspect.requirements.append(aspect_requirement_xml.name)

        for rule_ref_xml in aspect_xml.rules:
            aspect._rule_references.append(RuleReference(rule_ref_xml.ref, rule_ref_xml.value))

        return aspect


class CoreAspect(Aspect):
    @classmethod
    def define(cls, name, categroy, text):
        core_aspect = Aspect(name, categroy, text)
        core_aspect_rule = Rule(name, categroy, text)
        core_aspect_rule.options[name] = RuleOption(name, 0)
        core_aspect_rule.add_modifier(name)
        core_aspect.add_predefined_rule(core_aspect_rule)

        return core_aspect

    @classmethod
    def Strength(cls):
        return cls.define('Strength', 'core', 'Strength Core')

    @classmethod
    def Mobility(cls):
        return cls.define('Mobility', 'core', 'Mobility Core')

    @classmethod
    def Intelligence(cls):
        return cls.define('Intelligence', 'core', 'Intelligence Core')


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
    def __init__(self, rule_name, option):
        self.rule_name = rule_name
        self.option = option

    def realize(self, model):
        return RuleSelection(model.rule(self.rule_name), self.option)


class RuleSelection(object):
    def __init__(self, definition, target_option):
        self.definition = definition
        self._target_option = target_option

    @property
    def option(self):
        target = self._target_option if self._target_option is not None else self.definition.name
        try:
            return self.definition.options[target]
        except Exception:
            print(target)
            print(self.definition.name)
            print(self.definition.options)
            raise


class AspectCostReference(object):
    def __init__(self, rule_name, option_name, cost):
        self.rule_name = rule_name
        self.option_name = option_name
        self.cost = cost


class CharacterCheckException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class Character(object):
    def __init__(self, name, aspect_points):
        self.aspects = {
            'Strength': CoreAspect.Strength(),
            'Intelligence': CoreAspect.Intelligence(),
            'Mobility': CoreAspect.Mobility(),
        }

        self.name = name
        self.health_pool = 6
        self.aspect_points = aspect_points

    def stats(self, model):
        stats = dict()
        for aspect in self.aspects.values():
            for rule in aspect.selected_rules(model):
                for modifier in rule.definition.modifiers:
                    stats[modifier] = 0
        return stats

    def check(self, model):
        ap_total = 0
        for aspect in self.aspects.values():
            ap_total += model.ap_cost_breakdown(aspect).total

            for requirement_ref in aspect.requirements:
                if requirement_ref not in self.aspects:
                    raise CharacterCheckException(
                        'Character aspect {} is missing requirement {}.'.format(aspect.name, requirement_ref))

        if ap_total > self.aspect_points:
            raise CharacterCheckException(
                'Character build requires {} aspect points but only has {} AP allotted.'.format(
                    ap_total, self.aspect_points))
