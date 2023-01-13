import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from flask import jsonify
from flask import make_response
from flask import Response

import jumonc.models.cache.dbmodel as cache_model
from jumonc import settings
from jumonc.models.cache.database import db_session


logger = logging.getLogger(__name__)

def commit() -> None:
    db_session.commit()


def add_cache_entry(API_path:str) -> Optional[int]:
    entry = cache_model.CacheEntry(API_path)
    db_session.add(entry)
    commit()
    
    return entry.cache_id

def delete(cache_id: Optional[int]) -> None:
    cache_model.CacheEntry.query.filter_by(cache_id=cache_id).delete()
    commit()


def addParameter(cache_id:Optional[int], parameter_name:str, parameter_value:str) -> None:
    if not cache_id:
        logger.error("Missing cache_id")
        return
    
    parameter = cache_model.Parameter(cache_id, parameter_name, parameter_value)
    db_session.add(parameter)

    
def addResult(cache_id:Optional[int], result_name:str, result:Any) -> None:
    if not cache_id:
        logger.error("Missing cache_id")
        return
    
    result_entry:Union[cache_model.ResultInt, cache_model.ResultFloat, cache_model.ResultStr]
    if isinstance(result, int):
        result_entry = cache_model.ResultInt(cache_id, result_name, result)
        logger.debug("Adding int result to cache database")
    elif isinstance(result, float):
        result_entry = cache_model.ResultFloat(cache_id, result_name, result)
        logger.debug("Adding float result to cache database")
    elif isinstance(result, str):
        result_entry = cache_model.ResultStr(cache_id, result_name, result)
        logger.debug("Adding str result to cache database")
    else:
        logger.warning("Non valid result will be auto converted to a string for cache database: %s", str(type(result)))
        result_entry = cache_model.ResultStr(cache_id, result_name, str(result))
    
        
    db_session.add(result_entry)


def get_response_for_cache_id(ID: int) -> Response:
        
    entry = cache_model.CacheEntry.query.filter_by(cache_id=ID).first()
    if not entry:
        raise ValueError("Cache entry with ID " + str(ID) + " could not be found.")

            
    data:Dict[str, Union[bool, str, Dict[str, str]]] = {}
    data["Used API path"] = entry.API_path
    data["time"] = str(entry.time.strftime(settings.DATETIME_FORMAT))
            
    parameters:Dict[str, str] = {}
    for parameter in entry.parameters:
        parameters[parameter.parameter_name] = str(parameter.parameter_value)
    data["parameter"] = parameters
            
    results:Dict[str, str] = {}
    for result in entry.results_int:
        results[result.result_name] = str(result.result)
    for result in entry.results_float:
        results[result.result_name] = str(result.result)
    for result in entry.results_str:
        results[result.result_name] = result.result
    data["results"] = results  
            
    return make_response(jsonify(data), 200)


def convert_mpi_multiple_result_to_str(data: Union[List[int], List[float]]) -> str:
    return str(jsonify(data))


def stop() -> None:
    db_session.flush()
    db_session.close_all()
