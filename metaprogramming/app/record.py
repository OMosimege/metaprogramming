class Field:
    def __init__(self, label=None, precondition=None):
        self.label = label
        self.precondition = precondition
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)
    
    def __set__(self, instance, value):
        if self.name in instance.__dict__:
            raise AttributeError(f"Cannot modify '{self.name}' once it's set")
        if self.precondition is not None and not self.precondition(value):
            raise TypeError(f"Value '{value}' for '{self.name}' does not satisfy the precondition")
        instance.__dict__[self.name] = value

class RecordMeta(type):
    def __new__(cls, name, bases, attr):
        fields = {}
        for base in bases:
            if hasattr(base, '_fields'):
                fields.update(base._fields)

        for key, value in attr.items():
            if isinstance(value, Field):
                fields[key] = value

        attr['_fields'] = fields

        def init(self, **kwargs):
            for key, field in fields.items():
                if key not in kwargs:
                    raise TypeError(f"Missing required argument: {key}")
                field.__set__(self, kwargs[key])
            for key in kwargs:
                if key not in fields:
                    raise TypeError(f"Unexpected keyword argument '{key}'")

        attr['__init__'] = init

        def __str__(self):
            lines = [f"{self.__class__.__name__}("]
            last_index = len(self._fields) - 1
            for index, (field_name, field) in enumerate(self._fields.items()):
                value = getattr(self, field_name)
                lines.append(f"  # {field.label}")
                lines.append(f"  {field_name}={repr(value)}")

                if index != last_index:
                    lines.append("")
            lines.append(")")
            return "\n".join(lines)

        attr['__str__'] = __str__

        return super().__new__(cls, name, bases, attr)

class Record(metaclass=RecordMeta):
    """Base class for records using RecordMeta"""
    pass


