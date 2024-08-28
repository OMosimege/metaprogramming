from django.db import models

class Field:
    def __init__(self, label=None, precondition=None):
        self.label = label
        self.precondition = precondition
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        if hasattr(instance, self.name):
            raise AttributeError(f"Cannot modify '{self.name}' once it's set")
        if self.precondition is not None and not self.precondition(value):
            raise TypeError(f"Value '{value}' for '{self.name}' does not satisfy the precondition")
        instance.__dict__[self.name] = value


class RecordMeta(type):
    def __new__(cls, name, bases, attr):
        fields = {}
        mro = cls.mro()

        for base_cls in reversed(mro):
            for key, value in base_cls.__dict__.items():
                if isinstance(value, Field):
                    if key not in fields:
                        fields[key] = value

        for key, value in attr.items():
            if isinstance(value, Field):
                fields[key] = value
                value.label = value.label or key

        attr['_fields'] = fields
        
        def init(self, **kwargs):
            for key, value in kwargs.items():
                if key not in self._fields:
                    raise TypeError(f"Unexpected keyword argument '{key}'")
                setattr(self, key, value)
        
        attr['__init__'] = init
        
        for field_name, field_obj in fields.items():
            attr[field_name] = property(
                lambda self, fname=field_name: getattr(self, fname),
                lambda self, value, fname=field_name: setattr(self, fname, value)
            )

        def __setattr__(self, name, value):
            if name in self._fields:
                raise AttributeError(f"Cannot modify '{name}' once it's set")
            super().__setattr__(name, value)
        
        attr['__setattr__'] = __setattr__
        
        def __str__(self):
            field_str = ', '.join(f"{field_obj.label}={getattr(self, field_name)}" for field_name, field_obj in self._fields.items())
            return f"{name}({field_str})"
        
        attr['__str__'] = __str__

        return super().__new__(cls, name, bases, attr)


class Record(metaclass=RecordMeta):
    pass

