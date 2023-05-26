from Utils.Identifiers import Node, Token

# ├─
# │
# └
# ─


def PrettyPrint(node: Node, indent="", isLast=True):
    marker = "└─" if isLast == True else "├─"
    print(indent, end="")
    print(marker, end="")
    print(node.kind, end="")

    if (isinstance(node, Token) and node.value != None):
        print(" ", end="")
        print(node.value, end="")
    print("")
    indent += "  " if isLast == True else "│  "
    lastChild = node.children[len(
        node.children) - 1] if len(node.children) != 0 else node.children
    for child in node.children:
        PrettyPrint(child, indent, child == lastChild)
