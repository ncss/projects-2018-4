from lexer import lex
from parser2 import parse_tokens

def render(string, context):
    tokens = lex(string)
    tree = parse_tokens(tokens)
    return tree.returnText(context)

#print(render("<p> {% if 1==0 %} {{ x }} {% end if %}", {"x": 3}))

print(render('''{% for i in range(3) %}{{ i }} {% end for %}''', {}))
