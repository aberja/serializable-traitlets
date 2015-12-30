"""
Enhanced versions of IPython's traitlets.

Adds the following additional behavior:

- Strict construction/validation of config attributes.
- Serialization to/from dictionaries containing only primitives.
- More strict handling of default values than IPython's built-in behavior.
"""
import traitlets as tr

from .to_primitive import can_convert_to_primitive


class SerializableTrait(tr.TraitType):

    # Override IPython's default values with Undefined so that default values
    # must be passed explicitly to trait instances.
    default_value = tr.Undefined


class Integer(SerializableTrait, tr.Integer):
    pass


class Float(SerializableTrait, tr.Float):
    pass


class Unicode(SerializableTrait, tr.Unicode):
    pass


class Bool(SerializableTrait, tr.Bool):
    pass


class Set(SerializableTrait, tr.Set):
    pass


class List(SerializableTrait, tr.List):
    pass


class Dict(SerializableTrait, tr.Dict):
    pass


class Tuple(SerializableTrait, tr.Tuple):
    pass


class Enum(SerializableTrait, tr.Enum):

    def __init__(self, *args, **kwargs):
        super(Enum, self).__init__(*args, **kwargs)
        for value in self.values:
            if not can_convert_to_primitive(type(value)):
                raise TypeError(
                    "Can't convert Enum value %s to a primitive." % value
                )


class Instance(SerializableTrait, tr.Instance):

    def init(self):
        self._resolve_classes()
        if not can_convert_to_primitive(self.klass):
            raise TypeError(
                "Can't convert instances of %s to primitives." % (
                    self.klass.__name__,
                )
            )

    def validate(self, obj, value):
        from .serializable import Serializable
        if issubclass(self.klass, Serializable) and isinstance(value, dict):
            value = self.klass.from_dict(value)
        return super(Instance, self).validate(obj, value)
