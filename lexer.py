# This file exports the lex function, which takes a string and returns a list of tokens.

import re


TEXT = "text"
OPEN_BRACE = "{{"
CLOSE_BRACE = "}}"
OPEN_PERCENT = "{%"
CLOSE_PERCENT = "%}"
IF = "if"
END_IF = "end if"

special_characters_dict = {
    "{{": OPEN_BRACE,
    "}}": CLOSE_BRACE,
    "{%": OPEN_PERCENT,
    "%}": CLOSE_PERCENT,
    "if": IF,
    "end if": END_IF
    }

RE_FIND_BRACES = re.compile(r'({{)|(}})|({%)|(%})', re.MULTILINE)
RE_FIND_IF = re.compile(r'\s+if\s+(.+?)\s+%}', re.MULTILINE)
RE_FIND_END_IF = re.compile(r'\s+end if\s+?%}', re.MULTILINE)

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
            conditional_match = RE_FIND_IF.search(text[end:])
            if conditional_match:
                tokens.append((IF, "if"))
                tokens.append((TEXT, conditional_match.group(1)))
                tokens.append((CLOSE_PERCENT, "%}"))
                start = conditional_match.end()
            else:
                end_conditional = RE_FIND_END_IF.search(text[end:])
                if end_conditional:
                    tokens.append((END_IF, "end if"))
                    tokens.append((CLOSE_PERCENT, "%}"))
                    start = end_conditional.end() + end
                else:
                    raise SyntaxError("The if block must contain `if` and then a condition")
        else: start = match.end()
    tokens.append((TEXT, text))

    return tokens

def lex(text):
    return tokenise(text)

if __name__ == "__main__":
    with open("test_data.txt") as f:
        result_file = open("result.txt", "w")
        for line in f:
            print(tokenise(line), file=result_file)
        result_file.close()
