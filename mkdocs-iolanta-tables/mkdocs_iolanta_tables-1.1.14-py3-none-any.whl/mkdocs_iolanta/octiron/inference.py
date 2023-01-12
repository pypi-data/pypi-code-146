import logging

import owlrl
from owlrl import OWLRL_Extension
from rdflib import ConjunctiveGraph

logger = logging.getLogger(__name__)


def apply_inference_owlrl(graph: ConjunctiveGraph) -> None:
    """Apply OWL RL inference rules."""
    logger.info('Inference: OWL RL started...')
    owlrl.DeductiveClosure(OWLRL_Extension).expand(graph)
    logger.info('Inference: OWL RL complete.')

