import copy

from operator import itemgetter
from inspect import getmembers


class Placeholder(object):
    """
    Some libcloud calls require an object with the id field instead of
    just taking an id.
    """
    def __init__(self, id):
        self.id = id


class Attribute(object):
    """
    Generic attribute that represents a field on a resource.
    """
    _creation_count = 0

    def __init__(self, view_single=True, view_list=True):
        self.view_single = view_single
        self.view_list = view_list

        # Keep a count that is incremented on instantiation so we can iterate
        # in the same order that attributes are delcared on an Object.
        self._creation_count = Attribute._creation_count + 1
        Attribute._creation_count = self._creation_count


class Object(object):
    """
    Generic object that allows you to declaratively define how resources
    should be presented.
    """
    def get_attrs(self, view_type=None):
        attrs = []
        for attr, _ in getmembers(self):
            field = getattr(self, attr)
            if not isinstance(field, Attribute):
                continue
            if not view_type or getattr(field, view_type):
                attrs.append((field._creation_count, attr))
        return [attr for field, attr in sorted(attrs, key=itemgetter(0))]

    def __init__(self, obj):
        for attr in self.get_attrs():
            field = getattr(self, attr)
            field.value = getattr(obj, attr)
            setattr(self, attr, copy.copy(field))

    def generate_output(self):
        columns = self.get_attrs(view_type='view_single')
        data = [getattr(self, attr).value for attr in columns]
        return (columns, data)


class Collection(object):
    """
    A collection of resources for outputting to a list.
    """
    def __init__(self, objs):
        self.objs = objs

    def generate_output(self):
        columns = []
        data = []
        for obj in self.objs:
            if not columns:
                columns = obj.get_attrs(view_type='view_list')
            data.append([getattr(obj, attr).value for attr in columns])
        return (columns, data)


