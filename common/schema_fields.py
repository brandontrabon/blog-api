class SchemaFields:
    INT64 = {'type': 'integer', 'format': 'int64'}
    INT32 = {'type': 'integer', 'format': 'int32'}
    FLOAT = {'type': 'number', 'format': 'float'}
    OBJECT = {'type': 'object'}
    BOOLEAN = {'type': 'boolean'}
    STRING = {'type': 'string'}
    NULLABLE_STRING = {'type': ['string', 'null']}
    NULLABLE_INT32 = {'type': ['integer', 'null'], 'format': 'int32'}
    NULLABLE_FLOAT = {'type': ['float', 'null'], 'format': 'float'}
    BASE64 = {
        'type': 'string',
        'media': {
            'binaryEncoding': 'base64',
            'type': 'application/octet-stream'
        }
    }
    DATETIME = {'type': 'datetime', 'format': 'date-time'}
    INT32_ARRAY = {'type': 'array', 'items': {'type': 'int32'}}
    STRING_ARRAY = {'type': 'array', 'items': {'type': 'string'}}
    ALL_TYPES = [
        INT64,
        INT32,
        FLOAT,
        OBJECT,
        BOOLEAN,
        STRING,
        NULLABLE_STRING,
        NULLABLE_INT32,
        NULLABLE_FLOAT,
        BASE64,
        DATETIME,
        INT32_ARRAY,
        STRING_ARRAY
    ]

    @classmethod
    def is_schema_fields_type(cls, data_type):
        return isinstance(data_type, dict) and data_type in cls.ALL_TYPES
