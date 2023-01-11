import copy
from collections import defaultdict
from typing import Optional

from json_merge_patch import create_patch as json_diff_function

from libcove2.common import fields_present_generator


class JSONToGeoJSONConverter:
    """Converts JSON data to GeoJSON."""

    def __init__(self):
        self._nodes_geojson_features: list = []
        self._spans_geojson_features: list = []

    def process_package(self, package_data: dict) -> None:
        """Process network package. Pass in data. Results are stored on object to get with other methods."""
        for network in package_data.get("networks", []):
            self._process_network(network)

    def _process_network(self, network_data: dict) -> None:
        nodes = network_data.pop("nodes", [])
        spans = network_data.pop("spans", [])
        phases = network_data.pop("phases", [])
        organisations = network_data.pop("organisations", [])

        # Dereference `phases.funders`
        for phase in phases:
            if "funders" in phase and isinstance(phase["funders"], list):
                phase["funders"] = [
                    self._dereference_object(organisation, organisations)
                    for organisation in phase["funders"]
                ]

        # Dereference `contracts.relatedPhases`
        if "contracts" in network_data and isinstance(network_data["contracts"], list):
            for contract in network_data["contracts"]:
                if "relatedPhases" in contract and isinstance(
                    contract["relatedPhases"], list
                ):
                    contract["relatedPhases"] = [
                        self._dereference_object(phase, phases)
                        for phase in contract["relatedPhases"]
                    ]

        # Convert nodes to features
        for node in nodes:
            self._nodes_geojson_features.append(
                self._convert_node_to_feature(node, network_data, organisations, phases)
            )

        # Convert spans to features
        for span in spans:
            self._spans_geojson_features.append(
                self._convert_span_to_feature(
                    span, network_data, organisations, phases, nodes
                )
            )

    def get_nodes_geojson(self) -> dict:
        """After processing, call to get nodes GeoJSON output."""
        return {"type": "FeatureCollection", "features": self._nodes_geojson_features}

    def get_spans_geojson(self) -> dict:
        """After processing, call to get spans GeoJSON output."""
        return {"type": "FeatureCollection", "features": self._spans_geojson_features}

    def get_meta_json(self) -> dict:
        """After processing, call to get meta information on the conversion."""
        out: dict = {
            "nodes_output_field_coverage": {},
            "spans_output_field_coverage": {},
        }
        # nodes field coverage
        for key, value in fields_present_generator(self.get_nodes_geojson()):
            if key not in out["nodes_output_field_coverage"]:
                out["nodes_output_field_coverage"][key] = {"count": 1}
            else:
                out["nodes_output_field_coverage"][key]["count"] += 1
        # spans field coverage
        for key, value in fields_present_generator(self.get_spans_geojson()):
            if key not in out["spans_output_field_coverage"]:
                out["spans_output_field_coverage"][key] = {"count": 1}
            else:
                out["spans_output_field_coverage"][key]["count"] += 1
        # Any geometries?
        out["any_spans_with_geometry"] = bool(
            [True for s in self._spans_geojson_features if s.get("geometry")]
        )
        out["any_nodes_with_geometry"] = bool(
            [True for n in self._nodes_geojson_features if n.get("geometry")]
        )
        # return
        return out

    def _dereference_object(self, ref, list):
        """
        Return from list the object referenced by ref. Otherwise, return ref.
        """

        if "id" in ref:
            for item in list:
                if isinstance(item, dict) and item.get("id") == ref["id"]:
                    return item

        return ref

    def _convert_node_to_feature(
        self,
        node_data: dict,
        reduced_network_data: dict,
        organisations: list,
        phases: list,
    ) -> dict:

        reduced_node_data = copy.deepcopy(node_data)

        feature = {
            "type": "Feature",
            "geometry": reduced_node_data.pop("location")
            if isinstance(reduced_node_data.get("location"), dict)
            else None,
        }

        # Dereference organisation references
        if isinstance(reduced_node_data.get("physicalInfrastructureProvider"), dict):
            reduced_node_data[
                "physicalInfrastructureProvider"
            ] = self._dereference_object(
                reduced_node_data["physicalInfrastructureProvider"], organisations
            )
        if isinstance(reduced_node_data.get("networkProviders"), list):
            reduced_node_data["networkProviders"] = [
                self._dereference_object(i, organisations)
                for i in reduced_node_data["networkProviders"]
                if isinstance(i, dict)
            ]

        # Dereference phase references
        if "phase" in reduced_node_data:
            reduced_node_data["phase"] = self._dereference_object(
                reduced_node_data["phase"], phases
            )

        feature["properties"] = reduced_node_data
        feature["properties"]["network"] = reduced_network_data

        return feature

    def _convert_span_to_feature(
        self,
        span_data: dict,
        reduced_network_data: dict,
        organisations: list,
        phases: list,
        nodes: list,
    ) -> dict:

        reduced_span_data = copy.deepcopy(span_data)

        feature = {
            "type": "Feature",
            "geometry": reduced_span_data.pop("route")
            if isinstance(reduced_span_data.get("route"), dict)
            else None,
        }

        # Dereference organisation references
        if isinstance(reduced_span_data.get("physicalInfrastructureProvider"), dict):
            reduced_span_data[
                "physicalInfrastructureProvider"
            ] = self._dereference_object(
                reduced_span_data["physicalInfrastructureProvider"], organisations
            )
        if isinstance(reduced_span_data.get("networkProviders"), list):
            reduced_span_data["networkProviders"] = [
                self._dereference_object(i, organisations)
                for i in reduced_span_data["networkProviders"]
                if isinstance(i, dict)
            ]

        # Dereference phase references
        if "phase" in reduced_span_data:
            reduced_span_data["phase"] = self._dereference_object(
                reduced_span_data["phase"], phases
            )

        # Dereference endpoints
        for endpoint in ["start", "end"]:
            if endpoint in reduced_span_data:
                for node in nodes:
                    if "id" in node and node["id"] == reduced_span_data[endpoint]:
                        reduced_span_data[endpoint] = node

        feature["properties"] = reduced_span_data
        feature["properties"]["network"] = reduced_network_data

        return feature


class GeoJSONToJSONConverter:
    """Converts GeoJSON data to JSON."""

    def __init__(self):
        self._networks: dict = {}
        self._inconsistent_phase_ids_by_network_id: defaultdict = defaultdict(set)
        self._inconsistent_organisation_ids_by_network_id: defaultdict = defaultdict(
            set
        )
        self._inconsistent_network_ids_seen: set = set()

    def process_data(self, nodes_data: dict, spans_data: dict) -> None:
        """Process data. Results are stored on object to get with other methods."""
        # Network
        for geojson_feature in nodes_data.get("features", []):
            self._process_network(geojson_feature)
        for geojson_feature in spans_data.get("features", []):
            self._process_network(geojson_feature)

        # Nodes
        for geojson_feature in nodes_data.get("features", []):
            self._process_node(geojson_feature)

        # Spans
        for geojson_feature in spans_data.get("features", []):
            self._process_span(geojson_feature)

    def _process_network(self, geojson_feature_node_or_span: dict) -> None:
        if (
            "properties" in geojson_feature_node_or_span
            and "network" in geojson_feature_node_or_span["properties"]
        ):
            network = geojson_feature_node_or_span["properties"]["network"]
            if isinstance(network, dict):
                network_id = network.get("id")
                if isinstance(network_id, str) and network_id:

                    # TODO nodes/spans/phases/organisations should not be set in network - check this and warn if so

                    # Is data already seen?
                    if network_id in self._networks:
                        # Is it inconsistent with what we have seen before?
                        if json_diff_function(
                            self._networks[network_id]["network_data_original"], network
                        ):
                            # record error for later
                            self._inconsistent_network_ids_seen.add(network_id)

                            # Check references to phases in contracts are consistent with what we have seen before.
                            # This will give a more specific error on the phase_id.
                            # (However, 2 errors will be recorded - one for network_id and one for phase_id!
                            #  Can we make that tidier?
                            #  Suspect as we work to make errors more informative that will happen anyway #TODO)
                            if "contracts" in self._networks[network_id][
                                "network_data_output"
                            ] and isinstance(
                                self._networks[network_id]["network_data_output"][
                                    "contracts"
                                ],
                                list,
                            ):
                                for contract in self._networks[network_id][
                                    "network_data_output"
                                ]["contracts"]:
                                    if "relatedPhases" in contract and isinstance(
                                        contract["relatedPhases"], list
                                    ):
                                        for phase_reference in contract[
                                            "relatedPhases"
                                        ]:
                                            self._process_phase(
                                                network_id, phase_reference
                                            )
                    else:

                        # Not seen this before!

                        # Store it
                        self._networks[network_id] = {
                            "network_data_original": copy.deepcopy(network),
                            "network_data_output": copy.deepcopy(network),
                            "nodes": [],
                            "spans": [],
                            "phases": {},
                            "organisations": {},
                        }

                        # Sort references to phases in contracts
                        # (Must do after storing, as this writes data to the stored network)
                        if "contracts" in self._networks[network_id][
                            "network_data_output"
                        ] and isinstance(
                            self._networks[network_id]["network_data_output"][
                                "contracts"
                            ],
                            list,
                        ):
                            for contract in self._networks[network_id][
                                "network_data_output"
                            ]["contracts"]:
                                if "relatedPhases" in contract and isinstance(
                                    contract["relatedPhases"], list
                                ):
                                    out: list = []
                                    for phase_reference in contract["relatedPhases"]:
                                        phase_data = self._process_phase(
                                            network_id, phase_reference
                                        )
                                        if phase_data:
                                            out.append(phase_data)
                                        else:
                                            out.append(phase_reference)
                                    contract["relatedPhases"] = out

    def _process_node(self, geojson_feature_node: dict) -> None:
        node = copy.deepcopy(geojson_feature_node.get("properties", {}))
        for key_to_remove in ["network"]:
            if key_to_remove in node:
                del node[key_to_remove]
        network_id = (
            geojson_feature_node.get("properties", {}).get("network", {}).get("id")
        )
        if network_id not in self._networks.keys():
            # TODO log error
            return

        # sort organisations
        if isinstance(node.get("physicalInfrastructureProvider"), dict):
            node["physicalInfrastructureProvider"] = self._process_organisation(
                network_id, node["physicalInfrastructureProvider"]
            )
        if isinstance(node.get("networkProviders"), list):
            node["networkProviders"] = [
                self._process_organisation(network_id, i)
                for i in node["networkProviders"]
                if isinstance(i, dict)
            ]

        # sort phase
        if isinstance(node.get("phase"), dict) and node.get("phase"):
            phase_data = self._process_phase(network_id, node["phase"])
            if phase_data:
                node["phase"] = phase_data

        if geojson_feature_node.get("geometry"):
            node["location"] = geojson_feature_node["geometry"]

        self._networks[network_id]["nodes"].append(node)

    def _process_span(self, geojson_feature_span: dict) -> None:
        span = copy.deepcopy(geojson_feature_span.get("properties", {}))
        for key_to_remove in ["network"]:
            if key_to_remove in span:
                del span[key_to_remove]
        network_id = (
            geojson_feature_span.get("properties", {}).get("network", {}).get("id")
        )
        if network_id not in self._networks.keys():
            # TODO log error
            return

        # sort organisations
        if isinstance(span.get("physicalInfrastructureProvider"), dict):
            span["physicalInfrastructureProvider"] = self._process_organisation(
                network_id, span["physicalInfrastructureProvider"]
            )
        if isinstance(span.get("networkProviders"), list):
            span["networkProviders"] = [
                self._process_organisation(network_id, i)
                for i in span["networkProviders"]
                if isinstance(i, dict)
            ]

        # sort phase
        if isinstance(span.get("phase"), dict) and span.get("phase"):
            phase_data = self._process_phase(network_id, span["phase"])
            if phase_data:
                span["phase"] = phase_data

        if geojson_feature_span.get("geometry"):
            span["route"] = geojson_feature_span["geometry"]

        span["start"] = span.get("start", {}).get("id")
        span["end"] = span.get("end", {}).get("id")

        self._networks[network_id]["spans"].append(span)

    def _process_phase(self, network_id: str, phase: dict) -> Optional[dict]:
        phase_id = phase.get("id")
        # If no id, can't do anything. TODO log somewhere?
        if not phase_id or not isinstance(phase_id, str):
            return None
        # Check funders
        funders = phase.get("funders")
        if isinstance(funders, list) and funders:
            new_funders = []
            for funder in funders:
                funder_data = self._process_organisation(network_id, funder)
                if funder_data:
                    new_funders.append(funder_data)
            phase["funders"] = new_funders
        # Check data
        if phase_id in self._networks[network_id]["phases"]:
            # Is it inconsistent with what we have seen before?
            if json_diff_function(
                self._networks[network_id]["phases"][phase_id], phase
            ):
                self._inconsistent_phase_ids_by_network_id[network_id].add(phase_id)
        else:
            # Not seen this before; store it
            self._networks[network_id]["phases"][phase_id] = phase
        # Make output
        out: dict = {"id": phase_id}
        # Take name from data on network, not data that is passed to this function.
        # This means that if inconsistent names are in input, we'll have consistent names in the output.
        name = self._networks[network_id]["phases"][phase_id].get("name")
        if name:
            out["name"] = name
        return out

    def _process_organisation(self, network_id: str, organisation: dict) -> dict:
        organisation_id = organisation.get("id")
        # If no id, can't do anything. TODO log somewhere?
        if not organisation_id or not isinstance(organisation_id, str):
            return organisation
        # Check data
        if organisation_id in self._networks[network_id]["organisations"]:
            # Is it inconsistent with what we have seen before?
            if json_diff_function(
                self._networks[network_id]["organisations"][organisation_id],
                organisation,
            ):
                self._inconsistent_organisation_ids_by_network_id[network_id].add(
                    organisation_id
                )
        else:
            # Not seen this before; store it
            self._networks[network_id]["organisations"][organisation_id] = organisation
        # Make output
        out: dict = {"id": organisation_id}
        # Take name from data on network, not data that is passed to this function.
        # This means that if inconsistent names are in input, we'll have consistent names in the output.
        name = self._networks[network_id]["organisations"][organisation_id].get("name")
        if name:
            out["name"] = name
        return out

    def get_json(self) -> dict:
        """After processing, call to get JSON output."""
        out: dict = {"networks": []}
        for network in self._networks.values():
            # We are going to change network, so we need to take a copy
            network_data = copy.deepcopy(network["network_data_output"])
            # Copy other data we have built to network_data
            # Arrays have minItems: 1 set - so only add if we actually have content
            for key in ["nodes", "spans"]:
                if network[key]:
                    network_data[key] = network[key]
            for key in ["phases", "organisations"]:
                if network[key]:
                    network_data[key] = list(network[key].values())
            # build return
            out["networks"].append(network_data)
        return out

    def get_meta_json(self) -> dict:
        """After processing, call to get meta information on conversion."""
        out: dict = {"output_field_coverage": {}}
        # field coverage
        for key, value in fields_present_generator(self.get_json()):
            if key not in out["output_field_coverage"]:
                out["output_field_coverage"][key] = {"count": 1}
            else:
                out["output_field_coverage"][key]["count"] += 1
        # inconsistent
        out["inconsistent_phases_by_network_id"] = {
            k: {"phase_ids": sorted(list(v))}
            for k, v in self._inconsistent_phase_ids_by_network_id.items()
        }
        out["inconsistent_organisations_by_network_id"] = {
            k: {"organisation_ids": sorted(list(v))}
            for k, v in self._inconsistent_organisation_ids_by_network_id.items()
        }
        out["inconsistent_network_ids"] = list(self._inconsistent_network_ids_seen)
        # return
        return out
