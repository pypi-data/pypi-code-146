from baseblock import Enforcer, FileIO

from owl_finder.multiquery.bp import FindOntologyData
from owl_parser.bp import MutatoAPI

from .bp import *
from .dmo import *
from .dto import *
from .svc import *


def owl_parse(tokens: list,
              ontology_name: str,
              absolute_path: str):

    Enforcer.is_list_of_dicts(tokens)
    Enforcer.is_str(ontology_name)
    FileIO.exists_or_error(absolute_path)

    finder = FindOntologyData(ontologies=[ontology_name],
                              absolute_path=absolute_path)

    api = MutatoAPI(finder)
    svcresult = api.swap(tokens=tokens)

    Enforcer.is_list_of_dicts(svcresult)

    return svcresult
