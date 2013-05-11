from raxcli.models import Model, Attribute, Collection

class Node(Model):
    """
    Node resource.
    """
    id = Attribute()
    name = Attribute()
    state = Attribute()
    uuid = Attribute()
    public_ips = Attribute()
    private_ips = Attribute()
    size = Attribute()
    image = Attribute()
    extra = Attribute()
