from lexer import lex
from parser import parse_tokens

def render(string, context):
    tokens = lex(string)
    tree = parse_tokens(tokens)
    return tree.returnText(context)
