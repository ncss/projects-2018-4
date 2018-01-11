# This file exports the parse_tokens function, and the ParseException.
# The nodes are imported from evaluate.py

from evaluate import *

TEXT = "text"
OPEN_BRACE = "{{"
CLOSE_BRACE = "}}"
OPEN_PERCENT = "{%"
CLOSE_PERCENT = "%}"
IF = "if"
END_IF = "end if"

class ParseException(Exception):
    pass

parse = [(TEXT, "<p>"), (OPEN_BRACE, "{{"), (TEXT, "name"), (CLOSE_BRACE, "}}"), (TEXT, "</p>"), (OPEN_PERCENT, "{%"), (IF, "if"), (TEXT, "1==user.friends"), (CLOSE_PERCENT, "%}"), (TEXT, "<br/>"), (OPEN_PERCENT, "{%"), (END_IF, "end if"), (CLOSE_PERCENT, "%}"), (TEXT, "<p>"),(OPEN_BRACE, "{{"), (TEXT, "name"), (CLOSE_BRACE, "}}"), (TEXT, "</p>") ]

def if_handler(tokens, pos):
    predicate = tokens[pos + 2][1]
    if tokens[pos + 3][0] != CLOSE_PERCENT:
        raise ParseException("Mwahaha you failure, closed squigglies were not detected. Fool.")
    groupblock = block(tokens, pos + 4)
    print("MEMEMEMEMS")
    return IfNode(predicate, groupblock),  groupblock[1]

def python(tokens, pos):
    node = PyNode(tokens[pos + 1][1])
    if tokens[pos + 2][0] != CLOSE_BRACE:
        raise ParseException("Mwahaha you failure, closed squigglies were not detected. Fool.")
    return node, pos + 3

def block(tokens, pos):
    nodes = []
    while pos < len(tokens):
        print(pos, tokens[pos])
        if tokens[pos][0] == TEXT:
            nodes.append(TextNode(tokens[pos][1]))
            pos += 1
        elif tokens[pos][0] == OPEN_BRACE:
            node, new_pos = python(tokens, pos)
            nodes.append(node)
            pos = new_pos
        elif tokens[pos][0] == OPEN_PERCENT:
            if tokens[pos+1][0] == IF:
                new_node, new_pos = if_handler(tokens, pos)
                pos = new_pos
                nodes.append(new_node)
            elif tokens[pos+1][0] == END_IF:
                pos += 3
                return GroupNode(nodes), pos
        else:
            raise ParseException("Ah Rip. You suck at writting this language :( This is not valid :O")
    return GroupNode(nodes), pos

def parse_tokens(tokens):
    return block(tokens, 0)[0]

if __name__ == '__main__':
    print(parse_tokens(parse).children)
