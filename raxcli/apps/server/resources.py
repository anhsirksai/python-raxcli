from raxcli.resources import Object, Attribute, Collection

class Node(Object):
    """
    Node resource.
    """
    name = Attribute()
    uuid = Attribute()
    state = Attribute()
