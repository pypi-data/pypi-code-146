import argparse
import numpy as np
import onnx
import onnx.checker
from onnx import ModelProto, NodeProto, GraphProto
from grakel import Graph
from grakel.kernels import ShortestPath, WeisfeilerLehman, VertexHistogram
from google.protobuf.pyext._message import RepeatedCompositeContainer
from copy import deepcopy
from tabulate import tabulate
from colorama import init as colorama_init
from colorama import Fore
from typing import NamedTuple

from dataclasses import dataclass


@dataclass
class SummaryResults:
    exact_match: bool
    score: float
    a_valid: bool
    b_valid: bool
    matches: dict


# https://github.com/ysig/GraKeL
# https://ysig.github.io/GraKeL/0.1a8/index.html


class OnnxDiff:
    def __init__(self, model_a: ModelProto, model_b: ModelProto, verbose: bool = False):
        self._model_a = model_a
        self._model_b = model_b
        self._verbose = verbose
        colorama_init()

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

    def _get_inputs(self, model):
        pass

    # def _get_nodes(self, model) -> list[NodeProto]:
    #     return model.graph.node

    def _get_outputs(self, model):
        pass

    def _node_equals(self, a: NodeProto, b: NodeProto):
        pass

    def _compare_nodes(self) -> tuple[int, int, int]:
        a_nodes = deepcopy(self._model_a.graph.node)
        b_nodes = deepcopy(self._model_b.graph.node)
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

    def _is_valid(self, model: ModelProto) -> bool:
        try:
            onnx.checker.check_model(model)  # TODO: Full check?
            return True
        except:
            return False

    def _color(self, text: str, success: bool) -> str:
        return f"{Fore.GREEN if success else Fore.RED}{text}{Fore.RESET}"

    def _passfail_string(self, success: bool):
        text = "Pass" if success else "Fail"
        return self._color(text=text, success=success)

    def _matches_string(self, count: int, total: int):
        text = f"{count}/{total}"
        return self._color(text=text, success=(count == total))

    def _print_summary(self, results: SummaryResults) -> None:
        print("---- ONNX Diff Summary ----")

        text = (
            "Exact Match"
            if results.exact_match and results.score == 1.0
            else "Difference Found"
        )
        print(f"{text} ({round(results.score * 100, 6)}%)")

        print("")
        # validation results to table.
        data = [
            [
                "Validate",
                self._passfail_string(results.a_valid),
                self._passfail_string(results.b_valid),
            ],
        ]
        # matches to table.
        for key, matches in results.matches.items():
            data.append(
                [
                    key.capitalize(),
                    self._matches_string(matches[0], matches[1]),
                    self._matches_string(matches[0], matches[1]),
                ]
            )

        print(tabulate(data, headers=["", "A", "B"]))

    def _calculate_matches(self) -> dict:
        return {
            "initializers": (0, 0, 0),
            "inputs": (0, 0, 0),
            "outputs": (0, 0, 0),
            "nodes": self._compare_nodes(),
        }

    def summary(self, output=False) -> SummaryResults:
        results = SummaryResults(
            exact_match=(self._model_a == self._model_b),
            score=self._calculate_score(),
            a_valid=self._is_valid(self._model_a),
            b_valid=self._is_valid(self._model_b),
            matches=self._calculate_matches(),
        )

        if output:
            self._print_summary(results)

        return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("model_a", metavar="A", help="ONNX model A to compare")
    parser.add_argument("model_b", metavar="B", help="ONNX model B to compare")
    parser.add_argument("-v", "--verbose", required=False, help="Print verbose output")
    args = parser.parse_args()

    model_a = onnx.load(args.model_a)
    model_b = onnx.load(args.model_b)

    diff = OnnxDiff(model_a=model_a, model_b=model_b, verbose=args.verbose)

    results = diff.summary(output=True)
