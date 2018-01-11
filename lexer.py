# REPLACE ME WITH OWEN'S FILE

TEXT = "text"
OPEN_BRACE = "{{"
CLOSE_BRACE = "}}"
OPEN_PERCENT = "{%"
CLOSE_PERCENT = "%}"
IF = "if"
END_IF = "end if"

def lex(string):
    return [(TEXT, "<p>"), (OPEN_BRACE, "{{"), (TEXT, "name"), (CLOSE_BRACE, "}}"), (TEXT, "</p>"), (OPEN_PERCENT, "{%"), (IF, "if"), (TEXT, "1==name"), (CLOSE_PERCENT, "%}"), (TEXT, "<br/>"), (OPEN_PERCENT, "{%"), (END_IF, "end if"), (CLOSE_PERCENT, "%}"), (TEXT, "<p>"),(OPEN_BRACE, "{{"), (TEXT, "name"), (CLOSE_BRACE, "}}"), (TEXT, "</p>") ]
