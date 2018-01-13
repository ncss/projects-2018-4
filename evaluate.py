# This file provides nodes for the parser to use.
import html


class TemplateError(Exception):
    pass

class Node:
    pass

class GroupNode(Node):
    def __init__(self, children):
        self.children = children

    def returnText(self, context):
        try:
            avar = []
            strr = ""
            for node in self.children:
                avar.append(node.returnText(context))
            return strr.join(avar)
        except NameError as e:
            raise TemplateError("The template attmepted to render an undefined variable: {}".format(e.args), " the available variables were: {}".format(context))

class TextNode(Node):
    def __init__(self, text):
        self.text = text

    def returnText(self, context):
        return self.text

class PyNode(Node):
    def __init__(self, text):
        self.text = text

    def returnText(self, context):
        return html.escape(str(eval(self.text, {}, context)))

class IfNode(Node):
    def __init__(self, predicate, group):
        self.predicate = predicate
        self.group = group

    def returnText(self, context):
        if eval(self.predicate, {}, context) == True:
            return self.group.returnText(context)
        else:
            return ""

class ForNode(Node):
    def __init__(self, variable, iterable, groupnode):
        self.iterable = iterable
        self.variable = variable
        self.groupnode = groupnode
    def returnText(self, context):
        result = ""
        for i in eval(self.iterable, {}, context):
            context["__itervar"] = i
            exec(self.variable + " = __itervar", {}, context)
            result += self.groupnode.returnText(context)
        return result



if __name__ == '__main__':
    x = PyNode(" name ")

    print(x.returnText({'title': 'Foobar'}))

    # {% for x in blah %}{{ x*x }}{% end for %}
    g = IfNode()
    print(g.returnText({'blah': [1, 2, 5]}))
