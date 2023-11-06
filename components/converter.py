from pydantic import BaseModel, Field
from enum import Enum
from typing import List, get_type_hints, Literal, get_args, get_origin
from datetime import datetime
from components.test_cases import Character, KnowledgeGraph, ThoughtAnswerResponse, Cities, CarAndOwner

def is_generic_typing(type_):
    return hasattr(type_, '__origin__')

def handle_basic_type(field_name, field_type):
    type_mappings = {
        int: "number",
        str: "string",
        bool: "boolean",
        datetime: "datetime",
    }
    bnf_type = type_mappings.get(field_type, None)
    if bnf_type is None:
        raise NotImplementedError(f"Type {field_type} is not supported yet")
    return f'"{field_name}" ws ":" ws {bnf_type}'

def handle_enum(field_name, field_type):
    enum_values = ' | '.join([f'"{name}"' for name in field_type])
    return [f"{field_name.capitalize()} ::= {enum_values}"], f'"{field_name}" ws ":" ws {field_name.capitalize()}'

def handle_literal(field_name, field_type):
    literal_values = ' | '.join([f'"{literal}"' for literal in get_args(field_type)])
    return f"{field_name.capitalize()} ::= {literal_values}", f'"{field_name}" ws ":" ws {field_name.capitalize()}'

def handle_generic_typing(field_name, field_type, pydantic_model_to_bnf):
    inner_type = field_type.__args__[0]
    if isinstance(inner_type, type) and issubclass(inner_type, BaseModel):
        nested_rules = pydantic_model_to_bnf(inner_type, root=False).split('\n')
        model_rules = f'"{field_name}" ws ":" ws {field_name.capitalize()}list'
        return nested_rules, model_rules
    else:
        basic_type_name = getattr(inner_type, '__name__', None) or inner_type.__class__.__name__.lower()
        return [], f'"{field_name}" ws ":" ws {basic_type_name}list'

def handle_nested_model(field_name, field_type, pydantic_model_to_bnf):
    nested_rules = pydantic_model_to_bnf(field_type, root=False).split('\n')
    model_rules = f'"{field_name}" ws ":" ws {field_name.capitalize()}'
    return nested_rules, model_rules

def generate_rule_for_field(field_name, field_type, pydantic_model_to_bnf):
    if is_generic_typing(field_type):
        return handle_generic_typing(field_name, field_type, pydantic_model_to_bnf)
    elif isinstance(field_type, type) and issubclass(field_type, BaseModel):
        return handle_nested_model(field_name, field_type, pydantic_model_to_bnf)
    elif isinstance(field_type, type) and issubclass(field_type, Enum):
        return handle_enum(field_name, field_type)
    elif get_origin(field_type) == Literal:
        return handle_literal(field_name, field_type)
    elif field_type in (int, str, bool, datetime):
        return [], handle_basic_type(field_name, field_type)
    else:
        raise NotImplementedError(f"Type {field_type} is not supported yet")

def add_common_bnf_components():
    return [
        "string ::= '\"' ([^\"]*) '\"'",
        "number ::= [0-9]+ ('.' [0-9]*)?",
        "datetime ::= string",  # Represent datetime as a string in the BNF
        "ws ::= [ \\t\\n]*",
        "boolean ::= 'true' | 'false'",
        "stringlist ::= '[' ws ']' | '[' ws string (ws ',' ws string)* ws ']'",
        "numberlist ::= '[' ws ']' | '[' ws number (ws ',' ws number)* ws ']'",
    ]

def pydantic_model_to_bnf(model_cls, root=True):
    fields = get_type_hints(model_cls)
    bnf_grammar = []

    if root:
        bnf_grammar.append(f"root ::= {model_cls.__name__}")

    model_rules = []
    for field_name, field_type in fields.items():
        additional_rules, rule = generate_rule_for_field(field_name, field_type, pydantic_model_to_bnf)
        bnf_grammar += additional_rules  # Extend with additional rules without newline split
        model_rules.append(rule)

    fields_bnf = " ws ',' ws ".join(model_rules)
    bnf_grammar.insert(1, f"{model_cls.__name__} ::= '{{' ws {fields_bnf} ws '}}'")

    if root:
        bnf_grammar += add_common_bnf_components()  # Extend with common components without newline split

    return '\n'.join(bnf_grammar)


if __name__ == '__main__':
    for test_case in [Character, KnowledgeGraph, ThoughtAnswerResponse, Cities, CarAndOwner]:     
        bnf_grammar = pydantic_model_to_bnf(test_case)
        print(test_case)
        print(bnf_grammar, '\n\n\n')
    