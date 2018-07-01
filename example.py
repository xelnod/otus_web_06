from fields import IntegerField, TextField, ForeignKey, PrimaryKeyField
from models import Model


class SimpleExampleModel(Model):

    id = PrimaryKeyField()
    integer_field = IntegerField()
    text_field = TextField(required=False)
    required_text_field = TextField(required=True)


class ExampleModelWithFk(Model):
    __tablename__ = 'example_model_with_fk'

    id = PrimaryKeyField()
    integer_field = IntegerField()
    text_field = TextField()
    fk_field = ForeignKey(to=SimpleExampleModel)
