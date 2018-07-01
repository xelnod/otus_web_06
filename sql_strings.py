CREATE_TABLE_STATEMENT = "CREATE TABLE {table_name} ({fields_and_foreign_keys});"
CHECK_TABLE_EXISTS_STATEMENT = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='%s';"
DELETE_TABLE_STATEMENT = "DROP TABLE IF EXISTS %s;"
INSERT_STATEMENT = "INSERT INTO {table_name} ({fields}) VALUES ({values});"
UPDATE_STATEMENT = "UPDATE {table_name} SET {key_value_string} WHERE {pk_field_name} = {pk_lookup_value};"
SELECT_STATEMENT = "SELECT {fields} FROM {table_name} {fk_str} {where_str} {limit_str};"
