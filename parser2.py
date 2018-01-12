# This file exports the parse_tokens function, and the ParseException.
# The nodes are imported from evaluate.py

from lexer import lex
from evaluate import *

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
INCLUDE = "include"
FILE = "file"

class ParseException(Exception):
    pass
'''
parse = [
    (TEXT, "<p>"), (OPEN_BRACE, "{{"), (TEXT, "name"), (CLOSE_BRACE, "}}"), (TEXT, "</p>"), (OPEN_PERCENT, "{%"), (IF, "if"),
    (TEXT, "1==user.friends"), (CLOSE_PERCENT, "%}"), (TEXT, "<br/>"), (OPEN_PERCENT, "{%"), (END_IF, "end if"), (CLOSE_PERCENT, "%}"),
    (TEXT, "<p>"),(OPEN_BRACE, "{{"), (TEXT, "name"), (CLOSE_BRACE, "}}"), (TEXT, "</p>"), (OPEN_PERCENT, "{%"), (FOR, "for"), (TEXT, "i"), (IN, "in"),
    (ITERABLE, "iterable"), (CLOSE_PERCENT, "%}"), (TEXT, "<p>"), (OPEN_BRACE, "{{"), (TEXT, "name"), (CLOSE_BRACE, "}}"), (TEXT, "</p>"), (OPEN_PERCENT, "{%"),
    (END_FOR, "end for"), (CLOSE_PERCENT, "%}")]
    '''

parse = [(OPEN_PERCENT, "{%"), (INCLUDE, "include"), (FILE, "pages/header.html"), (CLOSE_PERCENT, "%}")]

def if_handler(tokens, pos):
    predicate = tokens[pos + 2][1]
    if tokens[pos + 3][0] != CLOSE_PERCENT:
        raise ParseException("Mwahaha you failure, closed squigglies were not detected. Fool.")
    groupnode, new_pos = block(tokens, pos + 4)
    return IfNode(predicate, groupnode),  new_pos

def for_handler(tokens, pos):
    if tokens[pos + 3][0] != IN:
        raise ParseException("What were you thinking‽ Can you write python? No "in" found in for loop.")
    if tokens[pos + 5][0] != CLOSE_PERCENT:
        raise ParseException("Mwahaha you failure, closed squigglies were not detected. Fool.")
    variable = tokens[pos + 2][1]
    iterable = tokens[pos + 4][1]
    groupnode, new_pos = block(tokens, pos + 6)
    return ForNode(variable, iterable, groupnode),  new_pos

def inc_handler(tokens, pos):
    with open(tokens[pos+2][1], 'r') as f:
        tokens = lex(f.read())
        new_node, _ = block(tokens, 0)
        return new_node, pos+4

def python(tokens, pos):
    node = PyNode(tokens[pos + 1][1])
    if tokens[pos + 2][0] != CLOSE_BRACE:
        raise ParseException("Mwahaha you failure, closed squigglies were not detected. Fool.")
    return node, pos + 3

def block(tokens, pos):
    nodes = []
    while pos < len(tokens):
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
            elif tokens[pos+1][0] == FOR:
                new_node, new_pos = for_handler(tokens, pos)
                pos = new_pos
                nodes.append(new_node)
            elif tokens[pos+1][0] == INCLUDE:
                node, new_pos = inc_handler(tokens, pos)
                nodes.append(node)
                pos = new_pos
            elif tokens[pos+1][0] == END_IF or tokens[pos+1][0] == END_FOR:
                pos += 3
                return GroupNode(nodes), pos
        else:
            raise ParseException("Ah Rip. You suck at writting this language :( This is not valid :O")
    return GroupNode(nodes), pos

def parse_tokens(tokens):
    return block(tokens, 0)[0]

if __name__ == '__main__':
    print(parse_tokens(parse).returnText({'title': 'blahblah'}))
