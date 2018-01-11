# This file provides nodes for the parser to use.

class Node:
    pass

class GroupNode(Node):
    def __init__(self, children):
        self.children = children

    def returnText(self, context):
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
        return eval(self.text, {}, context)

class IfNode(Node):
    def __init__(self, predicate, group):
        self.predicate = predicate
        self.group = group

    def returnText(self, context):
        return 'Teach me now to IfNode!'


if __name__ == '__main__':
    x = PyNode(" name ")

    g = GroupNode([
        TextNode("<p>"),
        PyNode(" name "),
        TextNode("</p>")
    ])

    g.returnText({'name': 'Joel'}) # Hope to get <p>Joel</p>
