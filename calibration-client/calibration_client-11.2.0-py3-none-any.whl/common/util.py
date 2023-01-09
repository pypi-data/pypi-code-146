"""Util Class with helper methods"""
import datetime


class Util(object):
    @staticmethod
    def val_to_api_bool(value_in):
        if not isinstance(value_in, int):  # bool inherits from int
            # FIXME: raise!
            return 'Error: Value {} is of type {}'.format(
                value_in, type(value_in)
            )

        # FIXME: values other than 0 or 1 probably shouldn't mean false
        return 'true' if (value_in == 1) else 'false'

    @staticmethod
    def get_opt_hash_val(h, element_name, def_val=''):
        if element_name in h:
            return h[element_name]
        else:
            return def_val

    @staticmethod
    def datetime_converter(o):
        if isinstance(o, datetime.datetime):
            return str(o)
