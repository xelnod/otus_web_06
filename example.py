from fields import IntegerField, TextField, ForeignKey
from models import Model


class SimpleExampleModel(Model):

    integer_field = IntegerField()
    text_field = TextField()


class ExampleModelWithFk(Model):
    __tablename__ = 'example_model_with_fk'

    integer_field = IntegerField()
    text_field = TextField()
    fk_field = ForeignKey(to=SimpleExampleModel)
