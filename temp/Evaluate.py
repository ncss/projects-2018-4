#web.ncss.life

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
    

x = PyNode(" name ")

g = GroupNode([
    TextNode("<p>"),
    PyNode(" name "),
    TextNode("</p>")
])

g.returnText({'name': 'Joel'}) # Hope to get <p>Joel</p>
