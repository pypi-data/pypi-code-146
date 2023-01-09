import importlib
import logging
import os
import pkgutil
import xml.etree.ElementTree as XmlTree
from typing import Optional

from blockly_executor import Action
from blockly_executor import ExtException
from blockly_executor import Helper
from blockly_executor.core.exceptions import DeferredOperation, StepForward, LimitCommand
from blockly_executor.plugins.standard_blocks.blocks.procedures_defnoreturn import ProceduresDefnoreturn
from blockly_executor.plugins.standard_blocks.blocks.procedures_defreturn import ProceduresDefreturn
from blockly_executor.plugins.standard_blocks.blocks.root import Root


class BlocklyExecutor:
    ns = {'b': 'https://developers.google.com/blockly/xml'}
    _blocks_index = None
    _blocks_class = {}

    def __init__(self, *, current_block: str = None, current_algorithm: str = None, logger=None,
                 plugins: Optional[list] = None, breakpoints: Optional[dict] = None,
                 debug_mode: str = None, **kwargs):
        """
        :param current_block: идентификатор блока который сейчас исполняется
        :param current_algorithm: имя схемы которая в настоящий момент исполняется
        :param logger: класс обеспечивающий вывод лога
        :param plugins: список модулей содержащих реализацию блоков
        :param breakpoints: список идентификаторов блоков на которых требуется остановиться в режиме отладки -
                словарь в ключе имя workspace для которого точки, в значении массив с идентификаторами блоков
        :param debug: режим отладки, исполнение идет до следующей точки останова
        :param step_by_step: режим пошагового исполнения
        :param kwargs:
        """
        # self.current_block = current_block
        # self.current_algorithm = current_algorithm
        # self.current_thread = None
        self.breakpoints = breakpoints
        self.debug_mode = debug_mode
        self.logger = logger if logger else logging.getLogger(self.__class__.__name__)

        self.extend_plugins = plugins

        self.functions = None
        self.variables = None
        self.root = None

        self.multi_thread_mode = False

        self.gather = []

        self.commands_result = {}
        self.algorithm = None

        self.action: Optional[Action] = None

    @property
    def blocks_index(self) -> dict:
        if self._blocks_index is not None:
            return self._blocks_index

        import blockly_executor.plugins
        plugins = {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in pkgutil.iter_modules(blockly_executor.plugins.__path__, blockly_executor.plugins.__name__ + ".")
        }
        if self.extend_plugins:
            for elem in self.extend_plugins:
                plugins[elem] = importlib.import_module(elem)

        self._blocks_index = {}
        for plugin_name in plugins:
            plugin = plugins[plugin_name]
            blocks_dir = os.path.join(plugin.__path__[0], 'blocks')
            if not os.path.isdir(blocks_dir):
                continue
            blocks_files = os.listdir(blocks_dir)
            for file_name in blocks_files:
                if file_name[-3:] != '.py' or file_name == '__init__.py':
                    continue
                self._blocks_index[file_name[:-3]] = plugin_name
                pass
        return self._blocks_index

    def get_block_class(self, block_name):
        block_name = block_name.lower()
        try:
            return self._blocks_class[block_name]
        except KeyError:
            pass
        try:
            index = self.blocks_index[block_name]
        except (KeyError, TypeError):
            raise ExtException(message='Block handler not found', detail=block_name)

        try:
            full_name = f'{index}.blocks.{block_name}.{Helper.to_camel_case(block_name)}'
            self._blocks_class[block_name] = Helper.get_class(full_name)
            return self._blocks_class[block_name]
        except Exception as err:
            raise ExtException(message='Block handler not found', detail=block_name, parent=err)

    @staticmethod
    def workspace_to_tree(workspace_xml):
        XmlTree.register_namespace('', 'https://developers.google.com/blockly/xml')
        return XmlTree.fromstring(workspace_xml)

    def _init_start_block(self, workspace_xml, endpoint, context):
        # стартуем с функции
        self.root = self.workspace_to_tree(workspace_xml)
        self.read_procedures_and_functions()
        self.variables = self.read_variables()
        if endpoint:
            try:
                block = self.functions[endpoint]
            except KeyError:
                context.status = 'error'
                context.result = f'not found endpoint {endpoint}'
                return context
        else:
            try:
                block = self.functions['main']
            except KeyError:
                block = Root.init(self, '', self.root, logger=self.logger)
        return block

    async def execute_nested(self, workspace_xml, context, *, endpoint=None, commands_result=None, algorithm=None):
        self._check_workspace(workspace_xml, algorithm)
        self.algorithm = algorithm
        # self.commands_result = commands_result
        start_block = self._init_start_block(workspace_xml, endpoint, context)

        return await start_block.execute(start_block.node, '', context, context.block_context)

    async def execute(self, workspace_xml, context, *, endpoint=None, commands_result=None, algorithm=None):
        self._check_workspace(workspace_xml, algorithm)
        self.algorithm = algorithm
        context.status = 'run'
        context.set_command_limit(self.debug_mode)
        self.action = Action('BlocklyExecutor.execute')

        start_block = self._init_start_block(workspace_xml, endpoint, context)

        try:
            self._index_commands_result(context, commands_result)
            context.commands = []

            if context.deferred:
                await self._execute_deferred(start_block, context)
            context.check_command_limit()

            self.logger.debug('')
            self.logger.debug('--------execute----------------------------')
            self.logger.debug(
                f'deferred:{len(context.deferred)}, '
                f'commands:{len(context.commands)}, '
                f'result:{len(self.commands_result.keys())}')

            result = await start_block.execute(start_block.node, '', context, context.block_context)
            context.result = result
            self.logger.debug('Complete')
            context.status = 'complete'
        except DeferredOperation:
            self.logger.debug('raise DeferredOperation')
            pass
        except LimitCommand:
            self.logger.debug('raise LimitCommand')
            pass
        except StepForward as step:
            context.result = step.args[2]
            context.current_variables = step.args[1].variables
            context.current_block = step.args[0]
            context.current_algorithm = step.args[3]
            self.logger.debug('raise StepForward')
        except ExtException as err:
            context.status = 'error'
            context.result = err.to_dict()
        except Exception as err:
            context.status = 'error'
            error = ExtException(parent=err, skip_traceback=-2)
            context.result = error.to_dict()
        # context.commands = self.commands
        # context.deferred = self.gather

        self.logger.debug(
            f'commands {len(context.commands)} command'
            f'gather:{len(self.gather)}, '
            f'result:{len(self.commands_result)}')
        # self.logger.block_context(f'------------------')
        self.action.set_end()
        return context

    async def _execute_deferred(self, robot, context):
        self.logger.block_context('')
        self.logger.block_context('--------execute deferred--------------')
        self.logger.block_context(
            f'deferred:{len(context.deferred)}, '
            f'commands:{len(context.commands)}, '
            f'result:{len(self.commands_result)}')
        # if len(self.commands_result) < len(context.deferred):
        #     raise Exception('не все ответы получены')
        _deferred = context.deferred
        _commands = context.commands
        context.commands = []
        # context.deferred = []
        _delete = []
        for i in range(len(_deferred)):
            _context = context.init_deferred(context, _deferred[i])
            try:
                await robot.execute(robot.node, '', _context, _context.block_context)
                _delete.append(i)
            except DeferredOperation as operation:
                context.add_deferred(operation)
                _delete.append(i)
                continue
        _delete.reverse()
        for elem in _delete:
            context.deferred.pop(elem)

    def read_procedures_and_functions(self):
        self.functions = {}
        for node in self.root.findall("./b:block[@type='procedures_defreturn']", self.ns):
            name = node.find("./b:field[@name='NAME']", self.ns).text
            self.functions[name] = ProceduresDefreturn.init(self, name, node, logger=self.logger)

        for node in self.root.findall("./b:block[@type='procedures_defnoreturn']", self.ns):
            name = node.find("./b:field[@name='NAME']", self.ns).text
            self.functions[name] = ProceduresDefnoreturn.init(self, name, node, logger=self.logger)

    def read_variables(self):
        result = {}
        for node in self.root.findall("./b:variables/b:variable", self.ns):
            name = node.text
            result[name] = None
        return result

    @property
    def current_algorithm_breakpoints(self):
        try:
            return self.breakpoints[self.algorithm]
        except (KeyError, TypeError):
            return None

    @staticmethod
    def _check_workspace(workspace_xml, algorithm):
        if not workspace_xml:
            raise ExtException(message='Передан пустой алгоритм', detail=algorithm)

    def _index_commands_result(self, context, commands_result):
        if commands_result:
            for command in commands_result:
                if 'uuid' in command:
                    self.commands_result[command['uuid']] = command
                else:
                    raise ExtException(message='У результата команды не указан идентификатор')
        for command in context.commands:
            command_uuid = command.get('uuid')
            if command_uuid and command_uuid not in self.commands_result:
                raise ExtException(message='Не получен ответ на команду', detail=command_uuid)

