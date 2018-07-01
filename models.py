import inflection
import sqlite3

from config import DB_NAME
from custom_exceptions import ImproperlyConfigured
from fields import PrimaryKeyField, ForeignKey
from object_managers import DefaultObjectManager
from sql_strings import CREATE_TABLE_STATEMENT, DELETE_TABLE_STATEMENT, CHECK_TABLE_EXISTS_STATEMENT, SELECT_STATEMENT, \
    INSERT_STATEMENT, UPDATE_STATEMENT


def make_request(request: str):
    con = sqlite3.connect(DB_NAME)
    with con:
        try:
            c = con.cursor()
            c.execute(request)
            con.commit()
        except sqlite3.OperationalError as e:
            print('select failed: ', e)
        else:
            return c


class Model:

    def __init__(self, object_manager=None):
        if not object_manager:
            self.objects = DefaultObjectManager(self.__class__)
        fields = self._get_fields()
        primary_keys_qty = len([f for f in fields if getattr(f, 'primary_key', False)])
        if primary_keys_qty != 1:
            raise ImproperlyConfigured("Model can't have more or less than one primary key.")
        elif not primary_keys_qty:
            self.id = PrimaryKeyField()

    @classmethod
    def get_table_name(cls):
        return getattr(cls, '__tablename__', inflection.underscore(cls.__name__))

    @classmethod
    def _table_exists(cls):
        request = CHECK_TABLE_EXISTS_STATEMENT % cls.get_table_name()
        return make_request(request).fetchone()[0] == 1

    @classmethod
    def _create_table(cls):
        request = CREATE_TABLE_STATEMENT.format(
                    table_name=cls.get_table_name(),
                    fields_and_foreign_keys=cls._get_fields_and_types_str()
                )
        make_request(request)

    @classmethod
    def _get_fields_and_types_str(cls):
        field_strings = []
        fieldnames = cls._get_field_names()
        for fieldname in fieldnames:
            field = cls._get_field(fieldname)
            field_strings.append("%s %s" % (fieldname, field.get_type_repr()))
            if type(field) is ForeignKey:
                field_strings.append(f'FOREIGN KEY({fieldname}) REFERENCES {field.to.get_table_name()}(id)')
        return ','.join(field_strings)

    @classmethod
    def _get_foreign_keys_str(cls):
        fks = []
        for fieldname in cls._get_field_names():
            field = getattr(cls, fieldname)
            if type(field) is ForeignKey:
                fks.append((fieldname, field.to.get_table_name()))
        fk_strings = [f'FOREIGN KEY({fk[0]}) REFERENCES {fk[1]}(id)' for fk in fks]
        if fk_strings:
            return ','.join(fk_strings)

    @classmethod
    def _get_pk_field_name(cls):
        for fieldname in cls._get_field_names():
            if getattr(cls._get_field(fieldname), 'primary_key', False):
                return fieldname

    @classmethod
    def _delete_table(cls):
        request = DELETE_TABLE_STATEMENT % cls.get_table_name()
        make_request(request)

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

    @classmethod
    def _get_required_field_names(cls):
        return [f for f in cls._get_field_names() if getattr(cls._get_field(f), 'required', False)]

    @classmethod
    def make_fk_join_string(cls):
        return f'INNER JOIN {cls.get_table_name()} ON {cls.get_table_name()}.{cls._get_pk_field_name()}=%s'

    @classmethod
    def select(cls, fields="*", limit=None, **kwargs):
        if fields != "*" and type(fields) is str:
            fields = (fields,)
        limit_clause_str = f'LIMIT {limit}' if limit else ''
        where_clause_str = "WHERE %s " % ", ".join([f"{k}='{v}'" for k, v in kwargs.items()]) if kwargs else ''

        fk_fields_str_bits = []
        fk_fields = ([f for f in cls._get_field_names() if type(cls._get_field(f)) is ForeignKey])

        for fk_field_name in fk_fields:
            bit = cls._get_field(fk_field_name).to.make_fk_join_string() % f'{cls.get_table_name()}.{fk_field_name}'
            fk_fields_str_bits.append(bit)

        fk_clause_str = ' '.join(fk_fields_str_bits)

        request = SELECT_STATEMENT.format(
                    table_name=cls.get_table_name(),
                    fields=', '.join(fields),
                    limit_str=limit_clause_str,
                    where_str=where_clause_str,
                    fk_str=fk_clause_str
                )
        return make_request(request).fetchall()

    @classmethod
    def insert(cls, **kwargs):
        fields, values = zip(*kwargs.items())
        required_field_names = set(cls._get_required_field_names())
        if required_field_names - set(fields):
            raise ValueError(f"missing required fields: {required_field_names - set(fields)}")
        request = INSERT_STATEMENT.format(
                    table_name=cls.get_table_name(),
                    fields=', '.join(fields),
                    values=', '.join([f"'{str(_)}'" for _ in values])
                )
        make_request(request)

    @classmethod
    def update(cls, pk_lookup_value, **kwargs):
        pk_field_name = cls._get_pk_field_name()
        request = UPDATE_STATEMENT.format(
                    pk_field_name=pk_field_name,
                    pk_lookup_value=pk_lookup_value,
                    table_name=cls.get_table_name(),
                    key_value_string=', '.join([f"{k}='{v}'" for k, v in kwargs.items()])
                )
        make_request(request)
