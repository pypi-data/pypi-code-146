import onnx
import onnx.checker
from onnx import ModelProto, NodeProto, GraphProto
from grakel import Graph
from grakel.kernels import ShortestPath
from copy import deepcopy
import onnx_diff.utils as utils
from onnx_diff.structs import SummaryResults


# https://github.com/ysig/GraKeL
# https://ysig.github.io/GraKeL/0.1a8/index.html


class OnnxDiff:
    def __init__(self, model_a: ModelProto, model_b: ModelProto, verbose: bool = False):
        self._model_a = model_a
        self._model_b = model_b
        self._verbose = verbose

    def _onnx_to_edge_list(self, graph):
        # From: https://github.com/onnx/onnxmltools/blob/main/onnxmltools/utils/visualize.py
        nodes = graph.node
        initializer_names = [init.name for init in graph.initializer]
        output_node_hash = {}
        edge_list = []
        for i, node in enumerate(nodes, 0):
            for output in node.output:
                if output in output_node_hash.keys():
                    output_node_hash[output].append(i)
                else:
                    output_node_hash[output] = [i]
        for i, inp in enumerate(graph.input, len(nodes)):
            output_node_hash[inp.name] = [i]
        for i, node in enumerate(nodes, 0):
            for input in node.input:
                if input in output_node_hash.keys():
                    edge_list.extend(
                        [(node_id, i) for node_id in output_node_hash[input]]
                    )
                else:
                    if not input in initializer_names:
                        print("No corresponding output found for {0}.".format(input))
        for i, output in enumerate(graph.output, len(nodes) + len(graph.input) + 1):
            if output.name in output_node_hash.keys():
                edge_list.extend(
                    [(node_id, i) for node_id in output_node_hash[output.name]]
                )
            else:
                pass
        return edge_list

    def _calculate_score(self) -> float:
        a_edges = self._onnx_to_edge_list(self._model_a.graph)
        b_edges = self._onnx_to_edge_list(self._model_b.graph)
        a_graph = Graph(a_edges)
        b_graph = Graph(b_edges)

        sp_kernel = ShortestPath(normalize=True, with_labels=False)

        sp_kernel.fit_transform([a_graph])
        fit = sp_kernel.transform([b_graph])

        return fit[0][0]

    def _matches(self, a, b) -> tuple[int, int, int]:
        a_nodes = deepcopy(a)
        b_nodes = deepcopy(b)
        a_nodes_total = len(a_nodes)
        b_nodes_total = len(b_nodes)

        # different or missing
        match_count = 0
        while len(a_nodes) > 0:
            a = a_nodes.pop()
            try:
                b_nodes.remove(a)
                match_count += 1
            except ValueError:
                pass

        return match_count, a_nodes_total, b_nodes_total

    def _calculate_matches(self) -> dict:
        a_graph = self._model_a.graph
        b_graph = self._model_b.graph
        return {
            "initializers": self._matches(a_graph.initializer, b_graph.initializer),
            "inputs": self._matches(a_graph.input, b_graph.input),
            "outputs": self._matches(a_graph.output, b_graph.output),
            "nodes": self._matches(a_graph.node, b_graph.node),
        }

    def _validate(self, model: ModelProto) -> bool:
        try:
            onnx.checker.check_model(model)  # TODO: Full check?
            return True
        except:
            return False

    def summary(self, output=False) -> SummaryResults:
        results = SummaryResults(
            exact_match=(self._model_a == self._model_b),
            score=self._calculate_score(),
            a_valid=self._validate(self._model_a),
            b_valid=self._validate(self._model_b),
            matches=self._calculate_matches(),
        )

        if output:
            utils.print_summary(results)

        return results
