class SchemaFields:
    INT64 = {'type': 'integer', 'format': 'int64'}
    INT32 = {'type': 'integer', 'format': 'int32'}
    BOOLEAN = {'type': 'boolean'}
    STRING = {'type': 'string'}
    NULLABLE_STRING = {'type': ['string', 'null']}
    NULLABLE_INT32 = {'type': ['integer', 'null'], 'format': 'int32'}
    DATETIME = {'type': 'datetime', 'format': 'date-time'}
    ALL_TYPES = [INT64, INT32, BOOLEAN, STRING, NULLABLE_STRING, NULLABLE_INT32, DATETIME]

    @classmethod
    def is_schema_fields_type(cls, data_type):
        return isinstance(data_type, dict) and data_type in cls.ALL_TYPES
