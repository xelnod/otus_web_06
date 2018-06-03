import sqlite3
import inflection

from config import DB_NAME
from custom_exceptions import ImproperlyConfigured
from fields import PrimaryKeyField, ForeignKey
from object_managers import DefaultObjectManager
from sql_strings import CREATE_TABLE_STATEMENT, DELETE_TABLE_STATEMENT, CHECK_TABLE_EXISTS_STATEMENT


class Model:
    # TODO: make class abstract

    def __init__(self, object_manager=None):
        if not object_manager:
            self.objects = DefaultObjectManager(self.__class__)
        fields = self._get_fields()
        primary_keys_qty = len([f for f in fields if getattr(f, 'primary_key', False)])
        if primary_keys_qty > 1:
            raise ImproperlyConfigured("Model can't have more than one primary key.")
        elif not primary_keys_qty:
            self.id = PrimaryKeyField()

    @classmethod
    def get_table_name(cls):
        return getattr(cls, '__tablename__', inflection.underscore(cls.__name__))

    @classmethod
    def _table_exists(cls):
        con = sqlite3.connect(DB_NAME)
        with con:
            c = con.cursor()
            c.execute(CHECK_TABLE_EXISTS_STATEMENT % cls.get_table_name())
            result = c.fetchone()[0] == 1
        return result

    @classmethod
    def _create_table(cls):
        con = sqlite3.connect(DB_NAME)
        with con:
            try:
                print(CREATE_TABLE_STATEMENT.format(
                    table_name=cls.get_table_name(),
                    fields_and_foreign_keys=cls._get_fields_and_types_str()))
                con.execute(CREATE_TABLE_STATEMENT.format(
                    table_name=cls.get_table_name(),
                    fields_and_foreign_keys=cls._get_fields_and_types_str()
                ))
            except sqlite3.OperationalError as e:
                print('Cannot create table %s: %s' % (cls.get_table_name(), e))

    @classmethod
    def _get_fields_and_types_str(cls):
        field_strings = []
        fieldnames = cls._get_field_names()
        for fieldname in fieldnames:
            field = cls._get_field(fieldname)
            field_strings.append("%s %s" % (fieldname, field.get_type_repr()))
            if type(field) is ForeignKey:
                field_strings.append('FOREIGN KEY(%s) REFERENCES %s(id)' % (fieldname, field.to.get_table_name()))
        return ','.join(field_strings)

    @classmethod
    def _get_foreign_keys_str(cls):
        fks = []
        for fieldname in cls._get_field_names():
            field = getattr(cls, fieldname)
            if type(field) is ForeignKey:
                fks.append((fieldname, field.to.get_table_name()))
        fk_strings = ['FOREIGN KEY({field_name}) REFERENCES {table_name}(id)'.format(field_name=fk[0], table_name=fk[1]) for fk in fks]
        if fk_strings:
            return ','.join(fk_strings)

    @classmethod
    def _delete_table(cls):
        con = sqlite3.connect(DB_NAME)
        with con:
            con.execute(DELETE_TABLE_STATEMENT % cls.get_table_name())

    @classmethod
    def sync_table(cls):
        if cls._table_exists():
            cls._delete_table()
        cls._create_table()

    @classmethod
    def _get_field(cls, field_name):
        return getattr(cls, field_name)

    @classmethod
    def _get_field_names(cls):
        return [i for i in cls.__dict__ if not i.startswith('__')]

    @classmethod
    def _get_fields(cls):
        return [cls._get_field(i) for i in cls._get_field_names()]
