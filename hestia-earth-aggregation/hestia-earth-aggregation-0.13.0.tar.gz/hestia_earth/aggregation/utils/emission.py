import os
import requests
from hestia_earth.schema import NodeType, TermTermType
from hestia_earth.utils.api import find_node
from hestia_earth.utils.tools import flatten


def _get_config(): return requests.get(f"{os.getenv('ORCHESTRATOR_CONFIG_URL')}/Cycle.json").json()


def get_emissions_system_boundary():
    results = find_node(NodeType.TERM, {
        'termType': TermTermType.EMISSION.value
    }, limit=1000)
    models = flatten(_get_config().get('models'))
    return [
        r.get('@id') for r in results if any([
            m for m in models if m.get('value') == r.get('@id')
        ])
    ]
