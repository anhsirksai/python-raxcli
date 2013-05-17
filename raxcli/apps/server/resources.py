from raxcli.models import Model, Attribute


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
    flavor = Attribute(src='size')
    image = Attribute()
    extra = Attribute()


class Image(Model):
    """
    Image resource.
    """
    id = Attribute()
    name = Attribute()
    extra = Attribute()


class Size(Model):
    """
    Size resource.
    """
    id = Attribute()
    name = Attribute()
    ram = Attribute()
    disk = Attribute()
    bandwidth = Attribute()
    price = Attribute()
