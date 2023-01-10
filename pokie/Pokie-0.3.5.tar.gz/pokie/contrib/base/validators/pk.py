from rick.base import Di
from rick.mixin import Translator
from rick.validator import registry
from rick.validator import Rule

from pokie.constants import DI_SERVICES
from pokie.contrib.base.constants import SVC_VALIDATOR

# dependency injector
_di = None


def init_validators(di: Di):
    global _di
    _di = di


@registry.register_cls(name="pk")
class DbPrimaryKey(Rule):
    MSG_ERROR = "Invalid primary key value"

    def validate(
        self, value, options: list = None, error_msg=None, translator: Translator = None
    ):
        if len(options) == 0:
            raise RuntimeError("DbPrimaryKey(): missing table name")

        if _di is None:
            raise RuntimeError("DbPrimaryKey(): di not initialized")

        table_name = str(options[0])
        tokens = table_name.split(".")
        if len(tokens) > 2 or len(tokens) == 0:
            raise ValueError(
                "DbPrimaryKey(): invalid table name '{}'".format(table_name)
            )
        schema = None
        table_name = tokens[0]
        if len(tokens) == 2:
            schema = tokens[1]

        pk_name = ""
        if len(options) > 1:
            pk_name = str(options[1])

        svc = _di.get(DI_SERVICES).get(SVC_VALIDATOR)
        try:
            if svc.id_exists(pk_name, value, table_name, schema):
                return True, ""
            return False, self.error_message(error_msg, translator)

        except Exception:
            return False, self.error_message(error_msg, translator)
