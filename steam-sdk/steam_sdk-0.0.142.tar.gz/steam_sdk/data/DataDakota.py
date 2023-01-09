from pydantic import BaseModel
from typing import (Dict, List, Union, Literal)


# from steam_sdk.data.DataAnalysis import WorkingFolders
# from steam_sdk.data.DataSettings import DataSettings

### SUB-SUB-LEVEL
# class interface(BaseModel):
#     analysis_drivers: str = ''
#     fork: str = None
#     interface_arguments: Dict = {}
#
#
# class responses(BaseModel):
#     response_functions: int = 0
#     descriptors: List[str] = None
#     objective_functions: int = 0
#     nonlinear_inequality_constraints: int = 0
#     calibration_terms: int = 0
#     type_gradients: str = ''
#     numerical_gradients: Dict = {}
#     analytical_gradients: Dict = {}
#     no_gradients: bool = False
#     no_hessians: bool = False
#
#
# class variables(BaseModel):
#     type_variable: str = ''
#     variable_arguments: Dict = {}
#
#
# class model(BaseModel):
#     type_model: str = ''
#
#
# class method(BaseModel):
#     type_method: str = ''
#     method_argument: Dict = {}
#
#
# class environment(BaseModel):
#     graphics: bool = False
#     type_tabular_data: str = ''
#     tabular_data_argument: Dict = {}
#
#
# # SUB-LEVEL
# class DAKOTA_analysis(BaseModel):
#     interface: interface = interface()
#     responses: responses = responses()
#     variables: variables = variables()
#     method: method = method()
#     model: model = model()
#     environment: environment = environment()

# Helper Classes
class Auxiliary(BaseModel):
    """
        Class for FiQuS multipole
    """
    partitions: list = []
    lower_bounds: list = []
    upper_bounds: list = []


# Fourth Level
class Bound(BaseModel):
    """
        Class for FiQuS multipole
    """
    min: float = None
    max: float = None


# Third Level
class SamplingVar(BaseModel):
    """
        Class for FiQuS multipole
    """
    bounds: Bound = Bound()


class MultiDimParStudyVar(BaseModel):
    """
        Class for FiQuS multipole
    """
    data_points: int = None
    bounds: Bound = Bound()


# Second Level: Responses
# class ObjectiveFunction(BaseModel):
#     """
#         Class for FiQuS multipole
#     """
#     #type: Literal['objective_functions']
#
#
# class ResponseFunction(BaseModel):
#     """
#         Class for FiQuS multipole
#     """
#     #type: Literal['response_functions']


# Second Level: Methods
class Sampling(BaseModel):
    """
        Class for FiQuS multipole
    """
    type: Literal['sampling']
    samples: int = None
    seed: int = None
    response_levels: float = None
    variables: Dict[str, SamplingVar] = {}


class MultiDimParStudy(BaseModel):
    """
        Class for FiQuS multipole
    """
    type: Literal['multidim_parameter_study']
    variables: Dict[str, MultiDimParStudyVar] = {}


class Response(BaseModel):
    """
        Class for FiQuS multipole
    """
    response: str = None  # Union[ResponseFunction, ObjectiveFunction] = {'type': 'response_functions'}
    descriptors: List[str] = None


# First Level
class DataDakota(BaseModel):
    output_file_path: str = None
    study: Union[MultiDimParStudy, Sampling] = {'type': 'multidim_parameter_study'}
    responses: Response = Response()
