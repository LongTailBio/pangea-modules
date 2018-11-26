"""Proxy class copied from http://code.activestate.com/recipes/496741-object-proxying/."""

SPECIAL_METHOD_NAMES = [
    '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__',
    '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__',
    '__eq__', '__float__', '__floordiv__', '__ge__', '__getitem__',
    '__getslice__', '__gt__', '__hash__', '__hex__', '__iadd__', '__iand__',
    '__idiv__', '__idivmod__', '__ifloordiv__', '__ilshift__', '__imod__',
    '__imul__', '__int__', '__invert__', '__ior__', '__ipow__', '__irshift__',
    '__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__',
    '__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__',
    '__neg__', '__oct__', '__or__', '__pos__', '__pow__', '__radd__',
    '__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__',
    '__repr__', '__reversed__', '__rfloorfiv__', '__rlshift__', '__rmod__',
    '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__',
    '__rtruediv__', '__rxor__', '__setitem__', '__setslice__', '__sub__',
    '__truediv__', '__xor__', 'next',
]


def make_method_maker(check_type, return_type, change_types=None):
    """Return a function that itself makes wrapped functions."""
    if not change_types:
        change_types = {}
    change_types[check_type] = return_type
    change_types_rev = {val: key for key, val in change_types.items()}
    all_types, all_types_rev = tuple(change_types.keys()),  tuple(change_types_rev.keys())

    def revise_if(val, type_tuple, type_map, reviser=None):
        """Return a value with types switched out, recursively."""
        if not reviser:
            reviser = lambda my_val: type_map[type(my_val)](my_val)
        if isinstance(val, (tuple, list)):
            revised = [revise_if(sub_val, type_tuple, type_map) for sub_val in val]
            return type(val)(revised)
        elif isinstance(val, type_tuple):
            return reviser(val)
        return val

    def make_method(func):
        """Return a function that converts <check_type> in <return_type>."""

        def wrap_func(*args, **kwargs):
            """Intercept calls to pandas functions and conver to vectors."""
            args = revise_if(args, all_types_rev, change_types_rev, reviser=lambda val: val._obj)
            pd_val = func(*new_args, **kwargs)
            return revise_if(pd_val, all_types, change_types)

        return wrap_func
    return make_method


class Proxy:
    """Flow through methods to another object."""

    def __init__(self, obj, change_types={}):
        self._obj = obj
        self.make_method = make_method_maker(
            type(self._obj), type(self), change_types=change_types
        )

    def __getattr__(self, key):
        pd_attr = getattr(self._obj, key)
        return self.make_method(pd_attr)

    def __delattr__(self, name):
        delattr(object.__getattribute__(self, "_obj"), name)

    def __nonzero__(self):
        return bool(self._obj)

    def __str__(self):
        return str(self._obj)

    def __repr__(self):
        return repr(self._obj)

    @classmethod
    def _create_class_proxy(cls, proxied_class):
        """creates a proxy for the given class"""
        make_method = make_method_maker(proxied_class, cls)
        namespace = {}
        for name in SPECIAL_METHOD_NAMES:
            if not hasattr(cls, name) and hasattr(proxied_class, name):
                namespace[name] = make_method(getattr(proxied_class, name))
        return type(
            f'{cls.__name__}({proxied_class.__name__})',
            (cls,),
            namespace
        )

    def __new__(cls, obj, *args, **kwargs):
        """
        creates an proxy instance referencing `obj`. (obj, *args, **kwargs) are
        passed to this class' __init__, so deriving classes can define an
        __init__ method of their own.
        note: _class_proxy_cache is unique per deriving class (each deriving
        class must hold its own cache)
        """
        try:
            cache = cls.__dict__["_class_proxy_cache"]
        except KeyError:
            cls._class_proxy_cache = cache = {}
        try:
            theclass = cache[obj.__class__]
        except KeyError:
            cache[obj.__class__] = theclass = cls._create_class_proxy(obj.__class__)
        ins = object.__new__(theclass)
        theclass.__init__(ins, obj, *args, **kwargs)
        return ins


'''
class Proxy:
    """Flow through methods to another object."""

    __slots__ = ["_obj", "__weakref__"]

    def __init__(self, obj):
        object.__setattr__(self, "_obj", obj)

    def _set_obj(self, obj):
        object.__setattr__(self, "_obj", obj)

    def __getattribute__(self, name):
        return getattr(object.__getattribute__(self, "_obj"), name)

    def __delattr__(self, name):
        delattr(object.__getattribute__(self, "_obj"), name)

    def __setattr__(self, name, value):
        setattr(object.__getattribute__(self, "_obj"), name, value)

    def __nonzero__(self):
        return bool(object.__getattribute__(self, "_obj"))

    def __str__(self):
        return str(object.__getattribute__(self, "_obj"))

    def __repr__(self):
        return repr(object.__getattribute__(self, "_obj"))



    _special_names = [
        '__abs__', '__add__', '__and__', '__call__', '__cmp__', '__coerce__',
        '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__',
        '__eq__', '__float__', '__floordiv__', '__ge__', '__getitem__',
        '__getslice__', '__gt__', '__hash__', '__hex__', '__iadd__', '__iand__',
        '__idiv__', '__idivmod__', '__ifloordiv__', '__ilshift__', '__imod__',
        '__imul__', '__int__', '__invert__', '__ior__', '__ipow__', '__irshift__',
        '__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__',
        '__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__',
        '__neg__', '__oct__', '__or__', '__pos__', '__pow__', '__radd__',
        '__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__',
        '__repr__', '__reversed__', '__rfloorfiv__', '__rlshift__', '__rmod__',
        '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__',
        '__rtruediv__', '__rxor__', '__setitem__', '__setslice__', '__sub__',
        '__truediv__', '__xor__', 'next',
    ]

    @classmethod
    def _create_class_proxy(cls, theclass):
        """creates a proxy for the given class"""

        def make_method(name):
            def method(self, *args, **kw):
                return getattr(object.__getattribute__(self, "_obj"), name)(*args, **kw)
            return method

        namespace = {}
        for name in cls._special_names:
            if hasattr(theclass, name):
                namespace[name] = make_method(name)
        return type("%s(%s)" % (cls.__name__, theclass.__name__), (cls,), namespace)

    def __new__(cls, obj, *args, **kwargs):
        """
        creates an proxy instance referencing `obj`. (obj, *args, **kwargs) are
        passed to this class' __init__, so deriving classes can define an
        __init__ method of their own.
        note: _class_proxy_cache is unique per deriving class (each deriving
        class must hold its own cache)
        """
        try:
            cache = cls.__dict__["_class_proxy_cache"]
        except KeyError:
            cls._class_proxy_cache = cache = {}
        try:
            theclass = cache[obj.__class__]
        except KeyError:
            cache[obj.__class__] = theclass = cls._create_class_proxy(obj.__class__)
        ins = object.__new__(theclass)
        theclass.__init__(ins, obj, *args, **kwargs)
        return ins
'''
