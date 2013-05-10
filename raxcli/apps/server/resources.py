from raxcli.models import Model, Attribute, Collection

class Node(Model):
    """
    Node resource.
    """
    name = Attribute()
    uuid = Attribute()
    state = Attribute()
