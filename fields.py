# Fields


class Field:
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class PrimaryKeyField(Field):

    def __init__(self):
        super().__init__()
        self.primary_key = True

    def get_type_repr(self):
        return 'INTEGER PRIMARY KEY'


class IntegerField(Field):
    def get_type_repr(self):
        return 'INTEGER PRIMARY KEY' if getattr(self, 'primary_key', False) else 'INTEGER'


class TextField(Field):
    def get_type_repr(self):
        return 'TEXT'


class ForeignKey(Field):
    def __init__(self, to):
        super().__init__()
        self.to = to

    def get_type_repr(self):
        return ''
