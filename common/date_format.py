from dateutil import parser

from exceptions.http_exceptions import HttpServerException

def transfer_object_datetime_properties(input_obj, output_dict, field_names):
    for f in field_names:
        value = getattr(input_obj, f)
        output_dict[f] = get_iso_format_date_string(value) if value is not None else None


def get_iso_format_date_string(datetime_obj):
    return datetime_obj.isoformat()

def parse_datetime_string(raw_string_value):
    if raw_string_value is not None:
        try:
            return parser.parse(raw_string_value)
        except ValueError as err:
            raise HttpServerException("Field '{}', Value '{}': ".format(f, raw_string_value) + str(err))

def parse_object_datetime_string_properties(obj, field_names):
    for f in field_names:
        raw_string_value = obj.get(f)
        if raw_string_value is not None:
            try:
                parsed_value = parser.parse(raw_string_value)
            except ValueError as err:
                raise HttpServerException("Field '{}', Value '{}': ".format(f, raw_string_value) + str(err))
            obj[f] = parsed_value
