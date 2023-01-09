from blockly_executor.core.block import Block
from blockly_executor.core.exceptions import LimitCommand, DeferredOperation


class MultiThreadLoop(Block):
    def __init__(self, executor, **kwargs):
        super().__init__(executor, **kwargs)

    async def _get_items(self, context, block_context):
        raise NotImplemented(self.__class__.__name__)

    async def _execute_item(self, node_loop, path, context, block_context):
        self.logger.debug(
            f'{self.__class__.__name__} '
            f'{self.block_id} execute page {block_context["page"]} item {block_context["index"]}'
        )
        await self.execute_all_next(node_loop, path, context, block_context, True)

    def _on_before_loop(self, node, path, context, block_context):
        pass

    def _on_loop(self, node, path, context, block_context):
        self.set_variable(context, node[0].text, block_context['items'][block_context['index']])

    def _on_deferred_item(self, node, path, context, block_context, deferred):
        pass

    def _calc_item(self, node, path, context, block_context):
        pass

    async def _execute_items(self, node, path, context, block_context):
        self._on_before_loop(node, path, context, block_context)
        var_name = node[0].text
        try:
            node_loop = self.get_node_statement(node)  # алгоритм внутри цикла
        except IndexError:  # не заполнено содержимое
            return
        if 'items' not in block_context:
            block_context['items'] = []
        while True:
            if not len(block_context['items']):
                try:  # считаем итерации
                    block_context['page'] += 1
                except KeyError:
                    block_context['page'] = 0

                block_context['items'] = await self._get_items(context, block_context)
                block_context['index'] = 0
                if not len(block_context['items']):
                    if context.operation['commands']:  # если список кончился, а команды не выполнены
                        raise LimitCommand()
                    return
            for i in range(block_context['index'], len(block_context['items'])):
                block_context['index'] = i
                try:
                    context.check_command_limit()
                except LimitCommand as err:
                    context.clear_child_context(block_context)  # когда мы вернемся это будет уже новая запись
                    raise err from err
                self._on_loop(node, path, context, block_context)
                self._check_step(context, block_context)
                try:
                    await self._execute_item(node_loop, f'{path}.{block_context["page"]}_{block_context["index"]}',
                                             context, block_context)
                except DeferredOperation as deferred:
                    if not deferred.args:  # не переданы параметры, значит функционал в цикле не поддерживается
                        raise Exception('В цикле есть блоки параллельная работа которых не поддерживается')
                    context.add_deferred(deferred)
                    self._on_deferred_item(node, path, context, block_context, deferred)
                    context.set_next_step(self.block_id)
                context.set_step(self.block_id)
                context.clear_child_context(block_context)

            block_context['items'] = []

            try:
                context.check_command_limit()
            except LimitCommand as err:
                raise LimitCommand from err

    async def _execute(self, node, path, context, block_context):
        # нужно продолжить выполнение определенной записи, т.к. было прерывание
        self.executor.multi_thread_mode = True
        if context.is_deferred:
            i = block_context['index']
            # block_context = context.get_child_context(block_context)
            node_loop = node[1]
            await self._execute_item(node_loop, f'{path}.{i}', context, block_context)
            context.set_step(self.block_id)
            return

        await self._execute_items(node, path, context, block_context)
        self.executor.multi_thread_mode = False

    @classmethod
    def get_node_statement(cls, node):
        return node.find("./b:statement", cls.ns)
