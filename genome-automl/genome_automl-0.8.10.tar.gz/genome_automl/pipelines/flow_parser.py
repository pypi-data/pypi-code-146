import inspect
import ast
import re

import logging

class GraphNode(object):
    def __init__(self, func_ast, decos, doc):
        self.name = func_ast.name
        self.func_lineno = func_ast.lineno
        self.decorators = decos
        self.doc = doc

        # populated by _get_decorator_keyword
        self.step_target_step_type = self._get_decorator_keyword(decos, "step_type")
        self.step_input_type = self._get_decorator_keyword(decos, "input_type")
        self.step_output_type = self._get_decorator_keyword(decos, "output_type")
        self.step_image = self._get_decorator_keyword(decos, "image")
        self.step_retry = self._get_decorator_keyword(decos, "retry")

        self.step_expression_input = self._get_decorator_keyword(decos, "expression_input")


        self.step_has_resources = self._get_decorator_keyword(decos, "resources")

        # this is populated by compile_run in step_annotations,
        # it typically can contain either dict or a proper TransformExecution object
        self.step_resources = None


        self.step_annotation_type = self._get_step_decorator_type(decos)



        # these attributes are populated by _parse
        self.tail_next_lineno = 0
        self.type = None
        self.out_funcs = []
        self.out_args = []

        self.has_tail_next = False
        self.invalid_tail_next = False
        self.num_args = 0
        self.condition = None
        self.foreach_param = None
        self._parse(func_ast)

        # these attributes are populated by _traverse_graph
        self.in_funcs = set()
        self.split_parents = []
        self.matching_join = None

        # these attributes are populated by _postprocess
        self.is_inside_foreach = False

    def _expr_str(self, expr):
        return '%s.%s' % (expr.value.id, expr.attr)


    def _get_decorator_keyword(self, decorators, key):
        for deco in decorators:
            if getattr(deco, "func", None):
                for keyword in deco.keywords:
                    if keyword.arg == key:

                        if isinstance(keyword.value, ast.Name):
                            return keyword.value.id

                        # decorator involving a call or an object instantiation
                        # i.e. like in expression_input, resources etc.
                        elif isinstance(keyword.value, ast.Call):
                            if len(keyword.value.args):
                                return (keyword.value.func.id, keyword.value.args[0])

                            return (keyword.value.func.id, keyword.value.args)

                        # when a simple dict is provided
                        elif isinstance(keyword.value, ast.Dict):
                            return (keyword.value.keys, keyword.value.values)

                        # handle lists
                        elif isinstance(keyword.value, ast.Subscript):
                            if isinstance(keyword.value.slice, ast.Name):
                                return (keyword.value.value.id, keyword.value.slice.id)
                            return (keyword.value.value.id, keyword.value.slice.value.id)

                        # handle strings
                        elif isinstance(keyword.value, ast.Str):
                            return keyword.value.s


                        elif isinstance(keyword.value, ast.Constant):
                            return keyword.value.value


        return None


    def _get_step_decorator_type(self, decorators):
        for deco in decorators:
            if getattr(deco, "func", None) and (isinstance(deco.func, ast.Name)
               and deco.func.id in ['transform_step', 'step']):
                # function decorated with step
                return deco.func.id
            elif not getattr(deco, "func", None) and (isinstance(deco, ast.Name)
               and deco.id in ['transform_step', 'step']):

                # function decorated with step
                return deco.id

        return None



    def _get_input_annotation_type(self, arg):
        if isinstance(arg.annotation, ast.Name):
            return arg.annotation.id
        elif isinstance(arg.annotation, ast.Subscript):
            return (arg.annotation.value.id, arg.annotation.slice.value.id)


    def _is_func_attr(self, arg):
        return isinstance(arg, ast.Attribute)


    def _parse(self, func_ast):

        self.num_args = len(func_ast.args.args)
        tail = func_ast.body[-1]

        # end doesn't need a transition
        if self.name == 'end':
            # TYPE: end
            self.type = 'end'

        # ensure that the tail is an expression
        if not isinstance(tail, ast.Expr):

            return

        # determine the type of self.next transition
        try:
            if not self._expr_str(tail.value.func) == 'self.next':
                return


            self.has_tail_next = True
            self.invalid_tail_next = True
            self.tail_next_lineno = tail.lineno

            self.out_funcs = [e.attr for e in tail.value.args if self._is_func_attr(e)]
            self.out_args = [ast.literal_eval(e) for e in tail.value.args if isinstance(e, ast.Dict)]

            keywords = dict((k.arg, k.value) for k in tail.value.keywords)


            if len(keywords) == 1:

                if 'foreach' in keywords:
                    # TYPE: foreach
                    self.type = 'foreach'
                    if len(self.out_funcs) == 1:
                        self.foreach_param = keywords['foreach'].value
                        self.invalid_tail_next = False

                elif 'condition' in keywords:
                    # TYPE: split-or
                    self.type = 'split-or'
                    if len(self.out_funcs) == 2:
                        self.condition = (ast.literal_eval(keywords['condition']) if isinstance(keywords['condition'], ast.Dict)
                                         else keywords['condition'].value)
                        self.invalid_tail_next = False

                elif 'join_input' in keywords:
                    # TYPE: sequence for step prior to join
                    # this check applies to self.next(..) keyword, not on signature of the step
                    self.type = 'sequence'
                    self.invalid_tail_next = False


            elif len(keywords) == 0:

                if len(self.out_funcs) >1:

                    if self.step_annotation_type == "transform_step":
                        raise Exception("an @transform_step should not use branches in self.next.\nUse a subsequent @step annotated function for branching")

                    # TYPE: split-and
                    self.type = 'split-and'
                    self.invalid_tail_next = False


                elif len(self.out_funcs) == 1:

                    # sequence
                    self.type = 'sequence'
                    self.invalid_tail_next = False






        except AttributeError:
            return



        # handle join steps via checking function **signature**,
        # i.e. this check is NOT on self.next(..)
        # join_input should be a keyword in the function definition)
        if self.num_args == 2 and func_ast.args.args[-1].arg == "join_input":
            self.type = 'join'
            self.invalid_tail_next = False





    def __str__(self):
        return\
"""*[{0.name} {0.type} (line {0.func_lineno})]*
    in_funcs={in_funcs}
    out_funcs={out_funcs}
    split_parents={parents}
    matching_join={matching_join}
    is_inside_foreach={is_inside_foreach}
    decorators={decos}
    num_args={0.num_args}
    has_tail_next={0.has_tail_next} (line {0.tail_next_lineno})
    invalid_tail_next={0.invalid_tail_next}
    condition={0.condition}
    foreach_param={0.foreach_param}
    -> {out}"""\
    .format(self,
            matching_join=self.matching_join and '[%s]' % self.matching_join,
            is_inside_foreach=self.is_inside_foreach,
            out_funcs=', '.join('[%s]' % x for x in self.out_funcs),
            in_funcs=', '.join('[%s]' % x for x in self.in_funcs),
            parents=', '.join('[%s]' % x for x in self.split_parents),
            decos=' | '.join(map(str, self.decorators)),
            out=', '.join('[%s]' % x for x in self.out_funcs))




class GraphVisitor(ast.NodeVisitor):

    def __init__(self, nodes, flow):
        self.nodes = nodes
        self.flow = flow
        super(GraphVisitor, self).__init__()


    def _is_step(self, decos):
        for dec in decos:
            if getattr(dec, "func", None) and (isinstance(dec.func, ast.Name)
               and dec.func.id in ['transform_step', 'step']):
                # function decorated with step
                return True
            elif not getattr(dec, "func", None) and (isinstance(dec, ast.Name)
               and dec.id in ['transform_step', 'step']):

                # function decorated with step
                return True


        return False


    def visit_FunctionDef(self, node):
        func = getattr(self.flow, node.name)
        if self._is_step(node.decorator_list):
            self.nodes[node.name] = GraphNode(node, node.decorator_list, func.__doc__)


"""
The FlowGraph class represents a compiler that accepts graph execution plans as defined by a Python class definition
that follows the **Genome Python flow DSL** structure with the appropriate annotations.
The python class definition is converted by this compiler into a structured
Internal Representation, that can be serialized as JSON object.
This comilers' **Internal representation** can be used by local/remote **execution engines**,
as well as other compilers, to translate into other representations that are understood
by local or remote (cloud: AWS, Google currently supported) workflow engines.
"""
class FlowGraph(object):

    def __init__(self, flow):
        self.name = flow.__name__
        self.nodes = self._create_nodes(flow)
        self._traverse_graph()
        self._postprocess()

    def _create_nodes(self, flow):
        tree = ast.parse(inspect.getsource(flow)).body
        root = [n for n in tree\
                if isinstance(n, ast.ClassDef) and n.name == self.name][0]
        nodes = {}
        GraphVisitor(nodes, flow).visit(root)
        return nodes

    def _postprocess(self):
        # any node who has a foreach as any of its split parents
        # has is_inside_foreach=True *unless* all of those foreaches
        # are joined by the node
        for node in self.nodes.values():
            foreaches = [p for p in node.split_parents
                         if self.nodes[p].type == 'foreach']
            if [f for f in foreaches
                if self.nodes[f].matching_join != node.name]:
                node.is_inside_foreach = True

    def _traverse_graph(self):

        def traverse(node, seen, split_parents):

            if node.type in ('split-or', 'split-and', 'foreach'):
                node.split_parents = split_parents
                split_parents = split_parents + [node.name]
            elif node.type == 'join':
                # ignore joins without splits
                if split_parents:
                    self[split_parents[-1]].matching_join = node.name
                    node.split_parents = split_parents
                    split_parents = split_parents[:-1]
            else:
                node.split_parents = split_parents

            for n in node.out_funcs:
                # graph may contain loops - ignore them
                if n not in seen:
                    # graph may contain unknown transitions - ignore them
                    if n in self:
                        child = self[n]
                        child.in_funcs.add(node.name)
                        traverse(child, seen + [n], split_parents)

        if 'start' in self:
            traverse(self['start'], [], [])

        # fix the order of in_funcs
        for node in self.nodes.values():
            node.in_funcs = sorted(node.in_funcs)



    def __getitem__(self, x):
        return self.nodes[x]

    def __contains__(self, x):
        return x in self.nodes

    def __iter__(self):
        return iter(self.nodes.values())

    def __str__(self):
        return '\n'.join(str(n) for _, n in sorted((n.func_lineno, n)\
                                for n in self.nodes.values()))
