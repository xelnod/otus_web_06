CREATE_TABLE_STATEMENT = "CREATE TABLE {table_name} ({fields_and_foreign_keys});"
CHECK_TABLE_EXISTS_STATEMENT = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='%s';"
DELETE_TABLE_STATEMENT = "DROP TABLE IF EXISTS %s;"
INSERT_STATEMENT = ''
UPDATE_STATEMENT = ''
