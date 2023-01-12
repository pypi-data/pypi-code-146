import sqlalchemy.types
import sqlalchemy.util


_type_map = {
    "ARRAY": sqlalchemy.types.ARRAY,
    "INT16": sqlalchemy.types.SMALLINT,
    "INT32": sqlalchemy.types.Integer,
    "BOOL": sqlalchemy.types.Boolean,
    "BINARY": sqlalchemy.types.BINARY,
    "DATE": sqlalchemy.types.DATE,
    "FLOAT64": sqlalchemy.types.Float,
    "FLOAT32": sqlalchemy.types.Float,
    "INT64": sqlalchemy.types.BIGINT,
    "STRING": sqlalchemy.types.String,
    "VARCHAR": sqlalchemy.types.VARCHAR,
    "CHAR": sqlalchemy.types.CHAR,
    "DECIMAL": sqlalchemy.types.DECIMAL,
    "TIMESTAMP": sqlalchemy.types.TIMESTAMP,
}

ARRAY = _type_map["ARRAY"]
INT16 = _type_map["INT16"]
INT32 = _type_map["INT32"]
BOOL = _type_map["BOOL"]
BINARY = _type_map["BINARY"]
DATE = _type_map["DATE"]
FLOAT64 = _type_map["FLOAT64"]
FLOAT32 = _type_map["FLOAT32"]
INT64 = _type_map["INT64"]
STRING = _type_map["STRING"]
VARCHAR = _type_map["VARCHAR"]
CHAR = _type_map["CHAR"]
DECIMAL = _type_map["DECIMAL"]
TIMESTAMP = _type_map["TIMESTAMP"]


def get_clickzetta_column_type(field):
    try:
        coltype = _type_map[field.field_type]
    except KeyError:
        sqlalchemy.util.warn(
            "Did not recognize type '%s' of column '%s'"
            % (field.field_type, field.name)
        )
        coltype = sqlalchemy.types.NullType
    else:
        if field.field_type == "DECIMAL":
            coltype = coltype(precision=field.precision, scale=field.scale)
        elif field.field_type == "VARCHAR" or field.field_type == "CHAR":
            coltype = coltype(field.length)
        else:
            coltype = coltype()

    return coltype
