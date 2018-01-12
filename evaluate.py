# This file provides nodes for the parser to use.

class Node:
    pass

class GroupNode(Node):
    def __init__(self, children):
        self.children = children

    def returnText(self, context):
        print(self, self.children, context)
        avar = []
        strr = ""
        for node in self.children:
            avar.append(node.returnText(context))
        return strr.join(avar)

class TextNode(Node):
    def __init__(self, text):
        self.text = text

    def returnText(self, context):
        return self.text

class PyNode(Node):
    def __init__(self, text):
        self.text = text

    def returnText(self, context):
        return str(eval(self.text, {}, context))

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
            context[self.variable.strip()] = i
            print(context)
            result += self.groupnode.returnText(context)
        return result

if __name__ == '__main__':
    x = PyNode(" name ")

    # {% for x in blah %}{{ x*x }}{% end for %}
    g = IfNode()
    print(g.returnText({'blah': [1, 2, 5]}))
