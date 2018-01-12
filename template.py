from lexer import lex
from parser2 import parse_tokens

def render(string, context):
    tokens = lex(string)
    tree = parse_tokens(tokens)
    return tree.returnText(context)

def render_file(path, context):
    with open(path) as f:
        return render(f.read(), context)

if __name__ == '__main__':
    print(lex('''{% for i in range(3) %}{{ i }}{% end for %}'''))
    print(render('''{% for i in range(3) %}{{ i }} {% end for %}''', {}))
    output = render('<p>{{ name }}</p>', {'name': 'Pikachu'})
    if output == '<p>Pikachu</p>':
        print("Render works!")
    else:
        print("Render broke! It output", output)
