import collections

_ITERABLE_TYPES = (collections.Iterable,)
_STRING_TYPES = (str, bytes, bytearray)


def _wrap_value(value):
    wrapped = value
    if isinstance(value, dict):
        wrapped = DictBacked(value)
    elif isinstance(value, _ITERABLE_TYPES) and not isinstance(value, _STRING_TYPES):
        wrapped = ListBacked(value)

    return wrapped


class ListBacked(object):
    def __init__(self, contents):
        self._values = [v for v in contents]

    def __iter__(self):
        return (_wrap_value(v) for v in self._values)

    def __delitem__(self, key):
        del self._values[key]

    def __setitem__(self, key, value):
        self._values[key] = value

    def __getitem__(self, key):
        return _wrap_value(self._values[key])

    def __len__(self):
        return len(self._values)

    def __str__(self):
        return self._values.__str__()


class DictBacked(object):
    _RESERVED_KEYS = ('_contents', '_strict')

    def __init__(self, contents, strict=True):
        self._contents = contents
        self._strict = strict

    def __delattr__(self, key):
        if key in DictBacked._RESERVED_KEYS:
            super(DictBacked, self).__delattr__(key)
        else:
            del self._contents[key]

    def __setattr__(self, key, value):
        if key in DictBacked._RESERVED_KEYS:
            super(DictBacked, self).__setattr__(key, value)
        else:
            self._contents[key] = value

    def __getattr__(self, key):
        value = self._contents.get(key)
        if self._strict is True and value is None:
            raise AttributeError('Attribute {} does not exist.'.format(key))

        return _wrap_value(value)

    def __len__(self):
        return len(self._values)

    def __str__(self):
        return self._contents.__str__()
