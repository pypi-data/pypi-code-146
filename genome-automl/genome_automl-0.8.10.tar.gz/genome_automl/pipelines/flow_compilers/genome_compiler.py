import json
import logging


from typing import Mapping, List, Tuple, Dict, Any
from ..flows import BaseGraph




class GenomeFlowCompiler():

    def __init__(self, flow: BaseGraph):

        self.flow = flow



    def _get_step_cls(self, node:Dict[str, Any]):

        node_flow_class = node["step_flow_class"]
        if not node_flow_class:
            if node["name"] == "start":
                node_flow_class = "PassStep"
            elif node["name"] == "end":
                node_flow_class = "EndStep"
            elif node["condition"]:
                node_flow_class = "Conditional"
            elif node["foreach"]:
                node_flow_class = "Branching"
            elif node["step_image"]:
                node_flow_class = "TransformStep"
            else:
                node_flow_class = "PassStep"


        return node_flow_class




    def _compile_target_genome_step(self, node:Dict[str, Any]) -> Dict[str, Any]:

        step_class_mapping = {
          "TransformStep": "model",
          "PushStep": "pushStep",
          "QueryStep": "queryStep",
          "Conditional": "conditional",
          "Branching": "branching",
          "JoinStep": "joinStep",
          "PassStep": "passStep",
          "StartStep": "startStep",
          "EndStep": "endStep"
        }

        genome_node = {
          "stepName":node["name"],
          "stepType":self._get_step_cls(node),
        }


        # if there is an expression fetch it via running the method in empty mode
        if ("step_has_expression_input" in node and node["step_has_expression_input"]) or (
          "step_has_resources" in node and node["step_has_resources"]):

            # execute node in compile mode to fetch its expression input or resources
            getattr(self.flow, node["name"])(compile_run=True)

            if "step_has_expression_input" in node and node["step_has_expression_input"]:
                genome_node["expression_input"] = node["step_expression_input"]


            if "step_has_resources" in node and node["step_has_resources"]:
                genome_node["resources"] = {}

                # probably a better way to do this mapping
                if "provisionType" in node["step_resources"]:
                    genome_node["resources"]["provisionType"] = node["step_resources"]["provisionType"]
                if "provision_type" in node["step_resources"]:
                    genome_node["resources"]["provisionType"] = node["step_resources"]["provision_type"]

                if "machineType" in node["step_resources"]:
                    genome_node["resources"]["machineType"] = node["step_resources"]["machineType"]
                if "instance_type" in node["step_resources"]:
                    genome_node["resources"]["machineType"] = node["step_resources"]["instance_type"]




        if "step_image" in node and node["step_image"]:
            genome_node["image"] = node["step_image"]

        if "step_retry" in node and node["step_retry"]:
            genome_node["retry"] = node["step_retry"]


        # handle conditional steps
        if node["type"] == "split-or" and node["condition"] and node["next"] and len(node["next"]) == 2:
            genome_node["condition"] = node["condition"]
            left = self._compile_target_genome_branch(node["name"], node["next"][0])
            right = self._compile_target_genome_branch(node["name"], node["next"][1])

            genome_node["onTrue"] = left if len(left["steps"]) else node["next"][0]
            genome_node["onFalse"] = right if len(right["steps"]) else node["next"][1]

        # handle parallel branching via nested steps
        if node["type"] == "split-and" and len(node["next"]) > 1:
            genome_branches = []

            for b in node["next"]:
                branch = self._compile_target_genome_branch(node["name"], b)
                genome_branches.append(branch)

            return genome_branches


        if node["type"] == "foreach" and node["next"]:
            genome_node["foreach"] = node["foreach"]
            branch_steps = self._compile_target_genome_branch(node["name"], node["next"][0])
            genome_node["steps"] = branch_steps["steps"]



        return genome_node




    def _compile_target_genome_branch(self, parent, branch_start):

        genome_branch = {"steps": []}
        full_branch = []

        parent_node = self.flow._graph_steps_map[parent]
        node = self.flow._graph_steps_map[branch_start]


        while node and (parent in node["split_parents"]):

            # handle joins
            # don't add the join step in every one of the subbranches its joining
            # branches and joins should work like below:
            # [{start}, [{branch-1}, {branch-2}], {join}, {end}]
            if node["type"] == "join" and parent == node["split_parents"][-1]:
                node = None

            # handle end
            elif node["type"] == "end" and len(node["next"]) == 0:
                full_branch.append(self._compile_target_genome_step(node))

                # assign node to next node
                node = None


            # handle sequences, or foreach
            elif node["next"] and len(node["next"]) == 1:
                full_branch.append(self._compile_target_genome_step(node))

                if node["matching_join"]:
                    # assign node to next node
                    node = self.flow._graph_steps_map[node["matching_join"]]
                else:
                    # assign node to next node
                    node = self.flow._graph_steps_map[node["next"][0]]


            # handle conditions, parallel branches
            elif node["next"] and len(node["next"]) > 1:

                sub_branch = self._compile_target_genome_step(node)
                full_branch.append(sub_branch)

                if node["matching_join"]:
                    # assign node to next node
                    node = self.flow._graph_steps_map[node["matching_join"]]
                else:
                    node = None




        genome_branch["steps"] = full_branch

        return genome_branch




    def compile(self) -> str:

        genome_flow_steps = []

        node = self.flow._graph_steps_map["start"]

        while node:

            genome_node = self._compile_target_genome_step(node)
            genome_flow_steps.append(genome_node)

            if node["next"] and len(node["next"]) == 1:
                node = self.flow._graph_steps_map[node["next"][0]]
            elif node["next"] and len(node["next"]) > 1:
                node = self.flow._graph_steps_map[node["matching_join"]]
            else:
                node = None


        return json.dumps(genome_flow_steps)
