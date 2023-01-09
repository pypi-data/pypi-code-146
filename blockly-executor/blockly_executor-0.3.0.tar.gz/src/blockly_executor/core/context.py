from blockly_executor import Helper, ArrayHelper
from blockly_executor.core.exceptions import LimitCommand
from .context_props import ContextProps


class Context(ContextProps):
    def __init__(self):
        super().__init__()
        self.data = {}
        # self.params = {}  # параметры операции передающиеся между вызовами
        # self.variables = {}  # значения переменных
        # self.block_context = {'__thread_vars': {}}  # контекст текущего блока, показывется при отладке
        # self.operation = {}  # контекст операции
        # self.deferred = []
        self.protocol = None

        self.algorithm = None
        self.debug_mode = None
        self.current_block = None
        self.current_algorithm = None
        self.current_thread = None

        self.is_deferred = False
        self.is_next_step = False
        self.deferred_result = None
        self.limit_commands = 25

    def _init_from_dict(self, data):
        # self.variables = data.get('variables', {})
        # self.block_context = data.get('block_context', {'__thread_vars': {}})
        # self.operation = data.get('operation', {
        #     'status': 'run',
        #     'result': None,
        #     'commands': []
        # })
        # self.deferred = data.get('deferred', [])
        pass

    @classmethod
    def init(cls, *, debug_mode=None, protocol=None, current_block=None, current_algorithm=None,
             algorithm=None, data=None, **kwargs):
        # if not operation_id:
        #     operation_id = str(uuid4())
        self = cls()
        if protocol:
            self.data = protocol.blockly_context
        else:
            self.data = data if data else {}
        self.protocol = protocol
        self.debug_mode = debug_mode
        self.current_block = current_block
        self.current_algorithm = current_algorithm if current_algorithm else algorithm
        self.algorithm = algorithm
        self.is_next_step = True if not current_block and self.debug_mode else None

        # if not data:
        #     data = {}
        # self._init_from_dict(data)
        #
        # self.params = params if params else {}

        # self.operation['begin'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return self

    def init_deferred(self, block_context):
        _self = self.__class__()
        # _self.params = self.params
        _self.block_context = block_context['block_context']
        _self.is_deferred = True
        _self.variables = self.variables
        # _self.operation = self.operation
        _self.deferred = self.deferred
        return _self

    def init_nested(self, block_context):
        _self = self.__class__()
        # _self.params = self.params
        _self.block_context = block_context.get('_child_block_context', {})
        _self.is_deferred = True
        _self.variables = block_context.get('_child_variables', {})
        # _self.operation = self.operation
        _self.deferred = self.deferred
        _self.protocol = self.protocol
        _self.debug_mode = self.debug_mode
        _self.current_block = self.current_block
        _self.current_algorithm = self.current_algorithm
        # _self.algorithm = algorithm
        return _self

    @property
    def operation_id(self):
        return self.operation.get('operation_id')

    def to_parallel_dict(self):
        return dict(
            variables=self.variables,
            block_context=self.block_context,
            operation=self.operation,
        )

    def to_dict(self):
        return self.data

    def to_result(self, debug_mode):
        res = dict(
            result=self.result,
            status=self.status,
            commands=self.commands,
        )
        if self.protocol:
            res['protocol'] = self.protocol.uuid
        if debug_mode:
            res['variables'] = self.current_variables
            res['current_block'] = self.current_block
            res['current_algorithm'] = self.current_algorithm

        return res

    def set_next_step(self, block_id):
        if self.debug_mode == 'step':
            if block_id == self.current_block and self.current_algorithm == self.algorithm:
                self.is_next_step = True

    def set_step(self, block_id):
        if self.debug_mode:
            # if self.executor.current_block != self.block_id:
            self.is_next_step = False
            self.current_block = block_id

    @staticmethod
    def get_child_context(block_context):
        try:
            child_context = block_context['__child']
        except KeyError:
            child_context = {}
            block_context['__child'] = child_context
        return child_context

    @staticmethod
    def clear_child_context(block_context, result=None, delete_children=True):
        if delete_children:
            block_context.pop('__child', None)

    def copy(self):
        _self = Context()
        # _self.params = self.params
        _self.operation = self.operation
        _self.deferred = self.deferred
        _self.block_context = Helper.copy_via_json(self.block_context)
        # _self._init_from_dict(copy_via_json(self.to_dict()))
        return _self

    def add_deferred(self, deferred_exception):

        _local_context = deferred_exception.args[2]
        _operation_context = deferred_exception.args[1]
        try:
            i = ArrayHelper.find_by_key(self.deferred, _local_context['__deferred'], key_field='__deferred')
        except KeyError:
            self.deferred.append({})
            i = len(self.deferred) - 1

        self.deferred[i] = {
            '__deferred': _local_context['__deferred'],
            'block_context': Helper.copy_via_json(_operation_context.block_context)
        }

        try:
            i = ArrayHelper.find_by_key(self.commands, _local_context['__path'], key_field=2)
        except KeyError:
            self.commands.append([])
            i = len(self.commands) - 1
        self.commands[i] = deferred_exception.to_command()

    def check_command_limit(self):
        if len(self.commands) >= self.limit_commands:
            raise LimitCommand()

    def set_command_limit(self, debug_mode=None):
        self.limit_commands = 1 if debug_mode else 25
