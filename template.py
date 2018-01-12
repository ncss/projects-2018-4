from lexer import lex
from parser import parse_tokens

def render(string, context):
    tokens = lex(string)
    tree = parse_tokens(tokens)
    return tree.returnText(context)

if __name__ == '__main__':
    output = render('<p>{{ name }}</p>', {'name': 'Pikachu'})
    if output == '<p>Pikachu</p>':
        print("Render works!")
    else:
        print("Render broke! It output", output)
