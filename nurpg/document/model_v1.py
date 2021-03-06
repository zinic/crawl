import math

import collections
import re
from mprequest.util import ListBacked

import nurpg.formulas as formulas

DICE_REGEX = re.compile('[\d]+d[\d]+')


class FormulaDefinition(object):
    def __init__(self, name, backend_type, equation, provided_func_ref):
        self.name = name
        self.type = backend_type
        self.equation = equation
        self.provided_func_ref = provided_func_ref

    def to_dict(self):
        root = collections.OrderedDict()
        root['name'] = self.name
        root['type'] = self.type
        root['equation'] = self.equation

        if self.provided_func_ref is not None:
            root['provided_function'] = self.provided_func_ref

        return root

    @classmethod
    def from_yaml(cls, formula_yaml):
        return cls(formula_yaml.name, formula_yaml.type, formula_yaml.equation, formula_yaml.provided_function)

    @classmethod
    def from_xml(cls, formula_xml):
        return cls(formula_xml.name, formula_xml.type, formula_xml.equation, formula_xml.function)


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
    def calculate_damage_cost(cls, info):
        cost = info.range_value
        formatted_name = info.format_name()

        # Check if the damage is defined as a dice roll
        if DICE_REGEX.match(formatted_name):
            # Figure out the number of dice and number of sides
            num_dice, sides = [int(v) for v in formatted_name.split('d')]

            # Cost is number of dice + damage value
            cost = num_dice - 1 + num_dice * sides

        return APCostElement(formatted_name, int(cost), info.option.text())

    def calculate_option(self, formula, info):
        if formula.type == 'custom':
            # Copy the environment every time
            env_copy = self._env.copy()

            # Set the definition iteration num
            env_copy['i'] = info.range_value

            # This is so nasty...
            cost = eval(formula.equation, env_copy)

            # Return as a formula result
            return APCostElement(info.format_name(), int(cost), info.option.text())

        if formula.provided_func_ref == 'damage_cost':
            return self.calculate_damage_cost(info)

        if formula.provided_func_ref == 'dr_cost':
            cost_element = self.calculate_damage_cost(info)
            cost_element.ap_cost *= 2
            return cost_element

        raise Exception('Unknown formula => {}::{}'.format(formula.type, formula.provided_func_ref))


def generate_options(rule_xml):
    options = list()

    # Positions start at 1
    i = 1

    # Iterate through the defined options
    option_nodes = rule_xml.each_node('option')

    if len(option_nodes) == 0:
        # If there are no options specified then return only one option with the same
        # name as the rule itself
        return [OptionPositionInfo(rule_xml, 0, 1)]

    for option_xml in option_nodes:
        # Values start with the position of the option
        values = [i]

        # Values may have a short-hand notation to generate additional options in a range
        if option_xml.range is not None:
            start, end = [int(v) for v in option_xml.range.split(',')]
            values = range(start, end + 1)

        for r in values:
            i += 1

            # By default we always skip and value that resolves its range to 0
            if r == 0:
                continue

            options.append(OptionPositionInfo(option_xml, r, i))

    return options


class OptionGeneratorYAML(object):
    def __init__(self):
        self._env = {
            'abs': math.fabs,
            'pow': math.pow,
            'fib': formulas.generate_fibonacci(1000),
        }

    @classmethod
    def calculate_damage_cost(cls, info):
        cost = info.range_value
        formatted_name = info.format_name()

        # Check if the damage is defined as a dice roll
        if DICE_REGEX.match(formatted_name):
            # Figure out the number of dice and number of sides
            num_dice, sides = [int(v) for v in formatted_name.split('d')]

            # Cost is number of dice + damage value
            cost = num_dice - 1 + num_dice * sides

        return APCostElement(formatted_name, int(cost), info.option.text)

    def calculate_option(self, formula, info):
        if formula.type == 'custom':
            # Copy the environment every time
            env_copy = self._env.copy()

            # Set the definition iteration num
            env_copy['i'] = info.range_value

            # This is so nasty...
            cost = eval(formula.equation, env_copy)

            # Return as a formula result
            return APCostElement(info.format_name(), int(cost), info.option.text)

        if formula.provided_func_ref == 'damage_cost':
            return self.calculate_damage_cost(info)

        if formula.provided_func_ref == 'dr_cost':
            cost_element = self.calculate_damage_cost(info)
            cost_element.ap_cost *= 2
            return cost_element

        raise Exception('Unknown formula => {}::{}'.format(formula.type, formula.provided_func_ref))


def generate_options_yaml(rule_yaml):
    options = list()

    # Positions start at 1
    i = 1

    # Iterate through the defined options
    option_nodes = rule_yaml.options

    if option_nodes is None or len(option_nodes) == 0:
        # If there are no options specified then return only one option with the same
        # name as the rule itself
        return [OptionPositionInfo(rule_yaml, 0, 1)]

    for option_yaml in option_nodes:
        # Values start with the position of the option
        values = [i]

        # Values may have a short-hand notation to generate additional options in a range
        if option_yaml.range is not None:
            start, end = [int(v) for v in option_yaml.range.split(',')]
            values = range(start, end + 1)

        for r in values:
            i += 1

            # By default we always skip and value that resolves its range to 0
            if r == 0:
                continue

            options.append(OptionPositionInfo(option_yaml, r, i))

    return options


class Model(object):
    def __init__(self, document):
        self._document = document

        self._resources = dict()
        self._formulas = dict()
        self._rules = dict()
        self._templates = dict()
        self._aspects = dict()
        self._items = dict()

        if document is not None:
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

            cost_breakdown = self.lookup_aspect_cost_breakdown(aspect.name)
            if cost_breakdown.ap_total <= 0:
                raise Exception('Aspect {} has an invalid AP ap_cost of: {}'.format(
                    aspect.name, cost_breakdown.ap_total))

    def to_dict(self):
        root = collections.OrderedDict()

        formulas = list()
        for formula in self._formulas.values():
            formulas.append(formula.to_dict())
        root['formulas'] = formulas

        templates = list()
        for template in self._templates.values():
            templates.append(template.to_dict())
        root['templates'] = templates

        rules = list()
        for rule in self._rules.values():
            rules.append(rule.to_dict())
        root['rules'] = rules

        resources = list()
        for resource in self._resources.values():
            resources.append(resource.to_dict())
        root['resources'] = resources

        aspects = list()
        for aspect in self._aspects.values():
            aspects.append(aspect.to_dict())
        root['aspects'] = aspects

        items = list()
        for item in self._items.values():
            items.append(item.to_dict())
        root['items'] = items

        return root

    @classmethod
    def from_yaml(cls, root):
        model = cls(None)
        option_generator = OptionGeneratorYAML()

        if root.formulas is not None:
            for formula_def_yaml in root.formulas:
                model._formulas[formula_def_yaml.name] = FormulaDefinition.from_yaml(formula_def_yaml)

        if root.rules is not None:
            for rule_def_yaml in root.rules:
                formula = model._formulas[rule_def_yaml.formula.ref]
                model._rules[rule_def_yaml.name] = Rule.from_yaml(option_generator, rule_def_yaml, formula)

        if root.resources is not None:
            for resource_def_yaml in root.resources:
                model._resources[resource_def_yaml.name] = Resource.from_yaml(resource_def_yaml)

        if root.templates is not None:
            for template_def_yaml in root.templates:
                model._templates[template_def_yaml.name] = Template.from_yaml(template_def_yaml)

        if root.aspects is not None:
            for aspect_def_yaml in root.aspects:
                model._aspects[aspect_def_yaml.name] = Aspect.from_yaml(aspect_def_yaml)

        if root.items is not None:
            for item_def_yaml in root.items:
                model._items[item_def_yaml.name] = Item.from_yaml(item_def_yaml)

        return model

    def _generate(self, document):
        option_generator = OptionGenerator()

        for formula_xml in document.formulas().each_node('formula'):
            formula = FormulaDefinition.from_xml(formula_xml)
            self._formulas[formula.name] = formula

        for rule_xml in document.rules().each_node('rule'):
            formula_ref = rule_xml.node('formula').ref
            formula = self._formulas[formula_ref]

            rule = Rule.from_xml(option_generator, rule_xml, formula)
            self._rules[rule.name] = rule

        for resource_xml in document.resources().each_node('resource'):
            resource = Resource.from_xml(resource_xml)
            self._resources[resource.name] = resource

        for template_xml in document.templates().each_node('template'):
            template = Template.from_xml(template_xml)
            self._templates[template.name] = template

        for aspect_xml in document.aspects().each_node('aspect'):
            aspect = Aspect.from_xml(aspect_xml)
            self._aspects[aspect.name] = aspect

        for item_xml in document.items().each_node('item'):
            item = Item.from_xml(item_xml)
            self._items[item.name] = item

    def lookup_item_cost_breakdown(self, name):
        return self.item_cost_breakdown(self._items[name])

    def item_cost_breakdown(self, item):
        cost_bd = RuleCostBreakdown()

        for aspect_ref in item.grants:
            aspect_cost_bd = self.lookup_aspect_cost_breakdown(aspect_ref)
            cost_bd.cost_elements.append(
                APCostElement(aspect_ref, aspect_cost_bd.ap_total, 'Granted by item.'))

        for rule in item.rules.realize(self):
            cost_bd.cost_elements.append(rule)

        return cost_bd

    def aspect_cost_breakdown(self, aspect):
        cost_bd = RuleCostBreakdown()
        for rule in aspect.selected_rules(self):
            cost_bd.cost_elements.append(rule)

        return cost_bd

    def lookup_aspect_cost_breakdown(self, name):
        return self.aspect_cost_breakdown(self._aspects[name])

    def resources(self):
        return [self._resources[k] for k in sorted(self._resources.keys())]

    def aspect(self, name, default=None):
        return self._aspects.get(name, default)

    def aspects(self):
        return [self._aspects[k] for k in sorted(self._aspects.keys())]

    def item(self, name, default=None):
        return self._items.get(name, default)

    def items(self):
        return [self._items[k] for k in sorted(self._items.keys())]

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


class Resource(object):
    def __init__(self, name, starting_value, unit=None):
        self.name = name
        self.unit = unit
        self.starting_value = starting_value

    def to_dict(self):
        root = collections.OrderedDict()
        root['name'] = self.name

        if self.unit is not None and self.unit != '':
            root['unit'] = self.unit

        root['starting_value'] = self.starting_value

        return root

    @classmethod
    def from_yaml(cls, resource_yaml):
        return cls(resource_yaml.name, int(resource_yaml.starting_value))

    @classmethod
    def from_xml(cls, resource_xml):
        return Resource(resource_xml.name, int(resource_xml.starting_value))


class RuleOption(object):
    def __init__(self, name, range=None, text=None):
        self.name = name
        self.range = range
        self.text = text

    def to_dict(self):
        root = collections.OrderedDict()
        root['name'] = self.name

        if self.text is not None and self.text != '':
            root['text'] = self.text

        if self.range is not None and self.range != '':
            root['range'] = self.range

        return root


class RuleFormulaReference(object):
    def __init__(self, ref):
        self.ref = ref

    def to_dict(self):
        root = collections.OrderedDict()
        root['ref'] = self.ref
        return root


class Rule(object):
    def __init__(self, name, category, text):
        self.name = name
        self.category = category
        self.text = text

        self.formula_ref = None
        self.modifiers = list()
        self.option_definitions = list()
        self.options = collections.OrderedDict()

    def to_dict(self):
        root = collections.OrderedDict()

        root['name'] = self.name
        root['formula'] = self.formula_ref.to_dict()

        if self.category is not None:
            root['category'] = self.category

        if self.text is not None and self.text != '':
            root['text'] = self.text

        if len(self.modifiers) > 0:
            root['modifies'] = self.modifiers

        options = list()
        for option_def in self.option_definitions:
            options.append(option_def.to_dict())

        if len(options) > 0:
            root['options'] = options

        return root

    @classmethod
    def from_yaml(cls, option_generator, rule_def_yaml, related_formula):
        rule = cls(rule_def_yaml.name, rule_def_yaml.category, rule_def_yaml.text)

        """
        rules:
          - name: Testing Rule
            modifies:
              - Target
        """

        if rule_def_yaml.modifies is not None and len(rule_def_yaml.modifies) > 0:
            for modifier_target in rule_def_yaml.modifies:
                rule.modifiers.append(modifier_target)

        if rule_def_yaml.options is not None and len(rule_def_yaml.options) > 0:
            for option_yaml in rule_def_yaml.options:
                rule.option_definitions.append(
                    RuleOption(option_yaml.name, option_yaml.range))

        rule.formula_ref = RuleFormulaReference(rule_def_yaml.formula.ref)

        for option_info in generate_options_yaml(rule_def_yaml):
            calculated_option = option_generator.calculate_option(related_formula, option_info)
            rule.options[calculated_option.name] = calculated_option

        return rule

    @classmethod
    def from_xml(cls, option_generator, rule_xml, formula_xml):
        rule = cls(rule_xml.name, rule_xml.category, rule_xml.text())

        for modifier_xml in rule_xml.each_node('modifier'):
            rule.modifiers.append(modifier_xml.ref)

        option_nodes = rule_xml.each_node('option')
        if len(option_nodes) == 0:
            # If there are no options specified then return only one option with the same
            # name as the rule itself
            rule.option_definitions.append(
                RuleOption(rule_xml.name))
        else:
            for option_xml in option_nodes:
                rule.option_definitions.append(
                    RuleOption(option_xml.name, option_xml.range, option_xml.text()))

        formula_ref_xml = rule_xml.node('formula')
        rule.formula_ref = RuleFormulaReference(formula_ref_xml.ref)

        for option_info in generate_options(rule_xml):
            calculated_option = option_generator.calculate_option(formula_xml, option_info)
            rule.options[calculated_option.name] = calculated_option

        return rule


class APCostElementOption(object):
    def __init__(self):
        self.name = ''


class APCostElement(object):
    def __init__(self, name, ap_cost, text):
        self.name = name
        self.ap_cost = ap_cost
        self.text = text
        self.option = APCostElementOption()
        self.modifeirs = None

    @property
    def monetary_cost(self):
        return self.ap_cost * 100


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

    def to_dict(self):
        root = collections.OrderedDict()
        root['name'] = self.name

        if len(self.requirements) > 0:
            root['requirements'] = self.requirements

        return root

    @classmethod
    def from_yaml(cls, template_yaml):
        template = cls(template_yaml.name)

        if template_yaml.requirements is not None and len(template_yaml.requirements) > 0:
            for template_requirement in template_yaml.requirements:
                template.requirements.append(template_requirement)

        return template

    @classmethod
    def from_xml(cls, template_xml):
        template = cls(template_xml.name)

        for template_requirement_xml in template_xml.each_node('requires'):
            template.requirements.append(template_requirement_xml.rule)

        return template


class Skill(object):
    def __init__(self, name, skill_type):
        self.name = name
        self.type = skill_type
        self.inheritance = list()

    def inherits_from(self, ref):
        self.inheritance.append(ref)

    def to_dict(self):
        root = collections.OrderedDict()
        root['name'] = self.name
        root['type'] = self.type

        if len(self.inheritance) > 0:
            root['inherits_from'] = self.inheritance

        return root

    @classmethod
    def from_yaml(cls, name, skill_yaml):
        skill = cls(name, skill_yaml.type)
        if skill_yaml.inherits is not None:
            for inheritance in skill_yaml.inherits:
                skill.inherits_from(inheritance)
        return skill

    @classmethod
    def from_xml(cls, name, skill_xml):
        skill = cls(name, skill_xml.type)
        for inherits_xml in skill_xml.each_node('inherits'):
            skill.inherits_from(inherits_xml.from_ref)
        return skill


class Item(object):
    def __init__(self, name, text=None):
        self.name = name
        self.text = text

        self.rules = RuleReferences()
        self.grants = list()
        self.wearable = None

    def to_dict(self):
        root = collections.OrderedDict()
        root['name'] = self.name

        if self.text is not None and self.text != '':
            root['text'] = self.text

        if len(self.rules) > 0:
            root['rules'] = self.rules.to_dict()

        if len(self.grants) > 0:
            root['grants'] = self.grants

        if self.wearable is not None:
            root['wearable'] = self.wearable.to_dict()

        return root

    @classmethod
    def from_yaml(cls, item_yaml):
        item = cls(item_yaml.name, item_yaml.text)

        if item_yaml.rules is not None:
            item.rules = RuleReferences.from_yaml(item_yaml.rules)

        if item_yaml.grants is not None:
            for aspect_ref in item_yaml.grants:
                item.grants.append(aspect_ref)

        if item_yaml.wearable is not None:
            item.wearable = ItemSlotAssignment(item_yaml.wearable.slot)

        return item

    @classmethod
    def from_xml(cls, item_xml):
        item = cls(item_xml.name, item_xml.text())
        item.rules = RuleReferences.from_xml(item_xml)

        for grants_xml in item_xml.each_node('grants'):
            item.grants.append(grants_xml.ref)

        item_slot_xml = item_xml.node('wearable')
        if item_slot_xml is not None:
            item.wearable = ItemSlotAssignment(item_slot_xml.slot)

        return item


class ItemSlotAssignment(object):
    def __init__(self, slot):
        self.slot = slot

    def to_dict(self):
        return {
            'slot': self.slot
        }


class Aspect(object):
    SKILL_REQUIREMENTS = [
        'Energy Point Cost',
        'Failure Chance'
    ]

    def __init__(self, name, template, text):
        self.name = name
        self.template = template
        self.text = text
        self.skill = None
        self.rules = RuleReferences()
        self.requirements = list()

        self._predefined_rules = list()

    def has_skill(self):
        return self.skill is not None

    def add_predefined_rule(self, rule):
        self._predefined_rules.append(rule)

    def selected_rule(self, name, model):
        for rule in self.selected_rules(model):
            if rule.definition.name == name:
                return rule
        return None

    def selected_rules(self, model):
        rules = self.rules.realize(model)
        for predefined in self._predefined_rules:
            rules.append(RuleSelection(predefined, list(), predefined.name))

        return rules

    def has_rule(self, rule_name):
        return self.rules.has_ref_to(rule_name)

    def check(self, model):
        failures = list()
        requirements = Aspect.SKILL_REQUIREMENTS.copy()

        if self.skill is not None:
            for rule in self.selected_rules(model):
                if rule.name in requirements:
                    requirements.remove(rule.name)

            if len(requirements) > 0:
                failures.append(
                    CharacterCheckException('Aspect {} grants a skill but is missing the required rules: {}'.format(
                        self.name,
                        ', '.join(requirements))))

        return failures

    def to_dict(self):
        root = collections.OrderedDict()
        root['name'] = self.name

        if self.template is not None and self.template != '':
            root['template'] = self.template

        if self.text is not None and self.text != '':
            root['text'] = self.text

        if len(self.rules) > 0:
            root['rules'] = self.rules.to_dict()

        if self.skill is not None:
            root['skill'] = self.skill.to_dict()

        if len(self.requirements) > 0:
            root['requires'] = self.requirements

        return root

    @classmethod
    def from_yaml(cls, aspect_yaml):
        aspect = cls(aspect_yaml.name, aspect_yaml.template, aspect_yaml.text)

        if aspect_yaml.rules is not None:
            aspect.rules = RuleReferences.from_yaml(aspect_yaml.rules)

        if aspect_yaml.skill is not None:
            aspect.skill = Skill.from_yaml(aspect_yaml.name, aspect_yaml.skill)

        if aspect_yaml.requires is not None:
            for requirement in aspect_yaml.requires:
                aspect.requirements.append(requirement)

        return aspect

    @classmethod
    def from_xml(cls, aspect_xml):
        aspect = cls(aspect_xml.name, aspect_xml.template, aspect_xml.text())
        aspect.rules = RuleReferences.from_xml(aspect_xml)

        aspect_skill_xml = aspect_xml.node('skill')
        if aspect_skill_xml is not None:
            aspect.skill = Skill.from_xml(aspect_xml.name, aspect_skill_xml)

        for aspect_requirement_xml in aspect_xml.each_node('requires'):
            aspect.requirements.append(aspect_requirement_xml.name)

        return aspect


class CoreAspect(Aspect):
    @classmethod
    def define(cls, name, categroy, text):
        core_aspect = Aspect(name, categroy, text)
        core_aspect.template = 'core'
        core_aspect_rule = Rule(name, categroy, text)
        core_aspect_rule.category = 'core'
        core_aspect_rule.options[name] = APCostElement(name, 0, 'Core Aspect Rule')
        core_aspect.add_predefined_rule(core_aspect_rule)

        core_aspect_skill = Skill(name, 'Core Aspect')
        core_aspect_skill.type = 'core'
        core_aspect.skill = core_aspect_skill

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


class RuleCostBreakdown(object):
    def __init__(self):
        self.cost_elements = list()

    @property
    def monetary_total(self):
        return self.ap_total * 100

    @property
    def ap_total(self):
        ap_cost = 0
        for cost_element in self.cost_elements:
            ap_cost += cost_element.ap_cost

        return ap_cost

    def __str__(self):
        rep = ''
        for cost_element in self.cost_elements:
            rep += '* {} ({}AP)'.format(cost_element.option, cost_element.ap_cost)
        return rep


class RuleReferences(object):
    def __init__(self):
        self._references = list()

    def __len__(self):
        return len(self._references)

    def has_ref_to(self, rule_name):
        for rf in self._references:
            if rf.rule_name == rule_name:
                return True
        return False

    def add(self, rule_ref):
        self._references.append(rule_ref)

    def realize(self, model):
        return [rr.realize(model) for rr in self._references]

    def to_dict(self):
        root = list()
        for rref in self._references:
            root.append(rref.to_dict())

        return root

    @classmethod
    def from_yaml(cls, rrefs_yaml):
        rrefs = cls()
        if isinstance(rrefs_yaml, ListBacked):
            for rref_yaml in rrefs_yaml:
                rrefs.add(RuleReference.from_yaml(rref_yaml))
        else:
            # This is for version 0.1 of the chracter YAML
            for name in rrefs_yaml:
                rrefs.add(RuleReference(name, rrefs_yaml[name]))

        return rrefs

    @classmethod
    def from_xml(cls, rref_parent_xml):
        rrefs = cls()
        for rref_xml in rref_parent_xml.each_node('rule'):
            rrefs.add(RuleReference.from_xml(rref_xml))

        return rrefs


class RuleReference(object):
    def __init__(self, rule_name, option):
        self.rule_name = rule_name
        self.option = option
        self.modifiers = list()

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)

    def realize(self, model):
        rule = model.rule(self.rule_name)

        rule_modifiers = list()
        rule_modifiers.extend(self.modifiers)
        rule_modifiers.extend(rule.modifiers)

        return RuleSelection(rule, rule_modifiers, self.option)

    def to_dict(self):
        root = collections.OrderedDict()
        root['name'] = self.rule_name

        if self.option is not None and self.option != self.rule_name:
            root['option'] = self.option

        if len(self.modifiers) > 0:
            root['modifies'] = self.modifiers

        return root

    @classmethod
    def from_yaml(cls, rule_ref_yaml):
        rref = cls(rule_ref_yaml.name, rule_ref_yaml.option)

        if rule_ref_yaml.modifies is not None:
            for rref_modifier_target in rule_ref_yaml.modifies:
                rref.add_modifier(rref_modifier_target)
        return rref

    @classmethod
    def from_xml(cls, rule_ref_xml):
        rref = cls(rule_ref_xml.ref, rule_ref_xml.value)
        for rr_modifier_xml in rule_ref_xml.each_node('modifier'):
            rref.add_modifier(rr_modifier_xml.ref)
        return rref


class RuleSelection(object):
    def __init__(self, definition, modifiers, target_option):
        self.definition = definition
        self.modifiers = modifiers
        self._target_option = target_option

    @property
    def name(self):
        return self.definition.name

    @property
    def monetary_cost(self):
        return self.option.ap_cost * 100

    @property
    def ap_cost(self):
        return self.option.ap_cost

    @property
    def option(self):
        # If there is no option specified then assume that the name of the rule def will suffice
        target = self._target_option if self._target_option is not None else self.definition.name
        return self.definition.options[target]


class CharacterCheckException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


MODIFIER_EXTRACTION_RE = re.compile('(?:[$\s]+)?([+-]?[\d]+).*')


def extract_numeric_modifier(modifier):
    match = MODIFIER_EXTRACTION_RE.match(modifier)
    if match is not None:
        return int(match.group(1))

    raise Exception('Unable to extract a numeric modifier value from modifier: {}'.format(modifier))


class CharacterAspect(object):
    def __init__(self, aspect, origin):
        self.definition = aspect
        self.origin = origin


class Character(object):
    def __init__(self, name, aspect_points, starting_funds, model):
        self.name = name
        self.aspect_points = aspect_points
        self.aspect_points_spent = 0
        self.monetary_funds_start = starting_funds if starting_funds is not None else 0
        self.monetary_funds_spent = 0

        self.resources = dict()
        self.skills = dict()

        self._model = model
        self._items = list()
        self._aspects = list()

        self._load()

    def _load(self):
        # Load core aspects
        self._aspects.extend([
            CharacterAspect(CoreAspect.Strength(), 'core'),
            CharacterAspect(CoreAspect.Intelligence(), 'core'),
            CharacterAspect(CoreAspect.Mobility(), 'core')
        ])

        # Load resources
        for resource in self._model.resources():
            self.resources[resource.name] = resource.starting_value

    @property
    def monetary_funds(self):
        return self.resources['Monetary Funds'] + self.monetary_funds_start

    @property
    def items(self):
        return sorted(self._items, key=lambda i: i.name)

    @property
    def aspects(self):
        aspects = self._aspects.copy()
        aspects.extend(self._item_granted_aspects())
        return sorted(aspects, key=lambda ca: ca.definition.name)

    def has_aspect(self, ref):
        for char_aspect in self._aspects:
            if char_aspect.definition.name == ref:
                return True
        return False

    def add_aspect(self, aspect):
        # Wrap the aspect and add information as to where
        # it was sourced from. Assign the aspect to us after
        self._aspects.append(CharacterAspect(aspect, 'character'))

    def _item_granted_aspects(self):
        aspects = list()
        for item in self._items:
            # Check if the item grants any aspects and add them
            if item.grants is not None:
                for grant_ref in item.grants:
                    if not self.has_aspect(grant_ref):
                        ig_aspect = CharacterAspect(self._model.aspect(grant_ref), 'item')
                        aspects.append(ig_aspect)
        return aspects

    def define_skill(self, aspect):
        # print('Defining skill {}.'.format(aspect.skill.name))

        skill = CharacterSkill(aspect.skill)

        failure_chance = aspect.selected_rule('Failure Chance', self._model)
        if failure_chance is not None:
            skill.difficulty = failure_chance.option.name
        else:
            skill.difficulty = 'Difficulty: GM Specified'

        self.skills[aspect.skill.name] = skill

    def add_item(self, item):
        # Assign the item to us
        self._items.append(item)

    def load(self, model):
        # Process all the aspects for skills first
        for char_aspect in self.aspects:
            # If the aspect describes a skill, process it
            if char_aspect.definition.has_skill():
                self.define_skill(char_aspect.definition)

        # Process costs and modifiers
        for char_aspect in self.aspects:
            aspect = char_aspect.definition

            # Record the costs of all non-core and non-item aspects
            if char_aspect.origin != 'core' and char_aspect.origin != 'item':
                self.aspect_points_spent += model.aspect_cost_breakdown(aspect).ap_total

            # Resolve all aspect assigned modifiers and apply them
            for rule_selection in aspect.selected_rules(model):
                for modifier in rule_selection.modifiers:
                    modifier_value = extract_numeric_modifier(rule_selection.option.name)

                    # Check first if a resource matches the name
                    resource = self.resources.get(modifier)
                    if resource is not None:
                        self.resources[modifier] = resource + modifier_value
                        continue

                    # Check if a skill matches the name
                    skill = self.skills[modifier]
                    modifier_value = extract_numeric_modifier(rule_selection.option.name)
                    skill.modifier += modifier_value

        # Resolve all item assigned modifiers and apply them
        for item in self.items:
            self.monetary_funds_spent += model.item_cost_breakdown(item).monetary_total

            for rule_selection in item.rules.realize(model):
                for modifier in rule_selection.modifiers:
                    modifier_value = extract_numeric_modifier(rule_selection.option.name)

                    # Check first if a resource matches the name
                    resource = self.resources.get(modifier)
                    if resource is not None:
                        self.resources[modifier] = resource + modifier_value
                        continue

                    # Check if a skill matches the name
                    skill = self.skills[modifier]
                    modifier_value = extract_numeric_modifier(rule_selection.option.name)
                    skill.modifier += modifier_value

        skills_remaining = list()
        skills_remaining.extend(self.skills.keys())

        skills_complete = list()
        while len(skills_remaining) > 0:
            delete_list = list()
            for skill_name in skills_remaining:
                skill = self.skills[skill_name]

                # print('Processing skill modifiers for {}'.format(skill_name))

                incomplete = False
                if len(skill.definition.inheritance) > 0:
                    for inherits_from in skill.definition.inheritance:
                        if inherits_from not in skills_complete:
                            # print('Skill {} reqires skill {} to be complete still.'.format(skill_name, inherits_from))
                            incomplete = True
                            break

                        donor_skill = self.skills[inherits_from]
                        skill.modifier += donor_skill.modifier

                        # print('Skill {} inherited {} from skill {}.'.format(skill_name, donor_skill.modifier, inherits_from))

                if incomplete is False:
                    # We're done with the skill here
                    skills_complete.append(skill_name)
                    delete_list.append(skill_name)

            if len(delete_list) == 0:
                raise Exception('Skill dependency tree broken')

            for skill_name in delete_list:
                # print('Removing {}'.format(skill_name))
                skills_remaining.remove(skill_name)

    def check(self, model):
        failures = list()

        for char_aspect in self.aspects:
            if char_aspect.origin == 'core':
                continue

            aspect = char_aspect.definition

            # Run the aspect's own check first
            failures.extend(aspect.check(model))

            # Figure out if we satisfy all required aspects
            for requirement_ref in aspect.requirements:
                if self.has_aspect(requirement_ref) is False:
                    failures.append(CharacterCheckException(
                        'Character aspect {} is missing requirement {}.'.format(aspect.name, requirement_ref)))

        if self.aspect_points_spent > self.aspect_points:
            failures.append(CharacterCheckException(
                'Character build requires {} aspect points but only has {} AP allotted.'.format(
                    self.aspect_points_spent, self.aspect_points)))

        # TODO: This might be dangerous later since the resources are defined by the model
        total_funds = self.resources['Monetary Funds'] + self.monetary_funds_start
        if self.monetary_funds_spent > total_funds:
            failures.append(CharacterCheckException(
                'Character does not have enough money. $$ {} needed but only has $$ {}.'.format(
                    self.monetary_funds_spent, total_funds)))

        return failures


class CharacterSkill(object):
    def __init__(self, definition):
        self.definition = definition
        self.modifier = 0
        self.difficulty = 0

    @property
    def name(self):
        return self.definition.name
