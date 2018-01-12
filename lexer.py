import re


TEXT = "text"
OPEN_BRACE = "{{"
CLOSE_BRACE = "}}"
OPEN_PERCENT = "{%"
CLOSE_PERCENT = "%}"
IF = "if"
END_IF = "end if"
FOR = "for"
IN = "in"
END_FOR = "end for"
ITERABLE = "iterable"

special_characters_dict = {
    "{{": OPEN_BRACE,
    "}}": CLOSE_BRACE,
    "{%": OPEN_PERCENT,
    "%}": CLOSE_PERCENT,
    "if": IF,
    "end if": END_IF,
    "for": FOR,
    "in": IN,
    "end for": END_FOR
    }

RE_FIND_BRACES = re.compile(r'({{)|(}})|({%)|(%})', re.MULTILINE)
RE_FIND_IF = re.compile(r'{%\s+if\s+(.+?)\s+%}', re.MULTILINE)
RE_FIND_END_IF = re.compile(r'{%\s+end if\s+?%}', re.MULTILINE)
RE_FIND_FOR = re.compile(r'{%\sfor\s(\w+?)\sin\s(\w+?)\s%}')
RE_FIND_END_FOR = re.compile(r'{%\s+end for\s+?%}')

def tokenise(text: str) -> list:

    tokens = []
    special_characters = RE_FIND_BRACES.finditer(text)

    start = 0
    while True:
        text = text[start:]
        match = RE_FIND_BRACES.search(text)
        if not match:
            break
        end = match.start()

        add_text = text[:end]
        if add_text != "":
            tokens.append((TEXT, add_text))

        special_character = match.group().strip()
        tokens.append((special_characters_dict[special_character], special_character))

        if special_character == "{%":
            start_if = RE_FIND_IF.search(text[end:])
            end_if = RE_FIND_END_IF.search(text[end:])
            start_for = RE_FIND_FOR.search(text[end:])
            end_for = RE_FIND_END_FOR.search(text[end:])

            matches = [start_if, end_if, start_for, end_for]

            code = sorted([i for i in matches if i], key=lambda x: x.start())[0]
            if code == start_if:
                tokens.append((IF, "if"))
                tokens.append((TEXT, start_if.group(1)))
                tokens.append((CLOSE_PERCENT, "%}"))
                start = start_if.end() + end
            elif code == end_if:
                tokens.append((END_IF, "end if"))
                tokens.append((CLOSE_PERCENT, "%}"))
                start = end_if.end() + end
            elif code == start_for:
                tokens.append((FOR, "for"))
                tokens.append((TEXT, start_for.group(1)))
                tokens.append((IN, "in"))
                tokens.append((ITERABLE, start_for.group(2)))
                tokens.append((CLOSE_PERCENT, "%}"))
                start = start_for.end() + end
            elif code == end_for:
                tokens.append((END_FOR, "end for"))
                tokens.append((CLOSE_PERCENT, "%}"))
                start = end_for.end() + end
        else: start = match.end()
    tokens.append((TEXT, text))

    return tokens

def lex(text):
    return tokenise(text)

if __name__ == "__main__":
    fails = []
    def check_equal(input, expected_tokens):
        global fails
        output = lex(input)
        if output != expected_tokens:
            fails += [(output, expected_tokens)]

    check_equal('a', [(TEXT, 'a')])
    check_equal('a{{ name }}b', [(TEXT, 'a'), (OPEN_BRACE, "{{"), (TEXT, " name "), (CLOSE_BRACE, "}}"), (TEXT, "b")])
    check_equal('{% if x %} do stuff with {{ value }} {% end if %}',
    [(OPEN_PERCENT, "{%"), (IF, 'if'), (TEXT, "x"), (CLOSE_PERCENT, "%}"), (TEXT, " do stuff with "), (OPEN_BRACE, "{{"), (TEXT, " value "), (CLOSE_BRACE, "}}"), (TEXT, " "), (OPEN_PERCENT, "{%"), (END_IF, "end if"), (CLOSE_PERCENT, "%}"), (TEXT, "")])
    check_equal('{% if x %}{% for y in z %}', [(OPEN_PERCENT, "{%"), (IF, "if"), (TEXT, "x"), (CLOSE_PERCENT, "%}"), (OPEN_PERCENT, "{%"), (FOR, "for"), (TEXT, "y"), (IN, "in"), (ITERABLE, "z"), (CLOSE_PERCENT, "%}"), (TEXT, "")])
    if fails:
        print(len(fails), 'Tests failed')
        for i, (output, expected) in enumerate(fails):
            print("Fail 1:")
            print("Output was:", output)
            print("Expected:", expected)
            print()
    else:
        print("All tests passed!")
