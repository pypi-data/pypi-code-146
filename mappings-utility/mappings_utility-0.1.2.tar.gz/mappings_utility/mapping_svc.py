from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
from typing import Union
from sdmx_mapping_utility import KeyRange, SDMXMappingUtility


app = FastAPI()

@app.get("/")
def info():
    return f"the partial key mapping service says hello"

@app.get("/map_withURN")
async def map_withURN(
                    source_file: str,
                    mapping: str,
                    registry: str,
                    return_source_dimensions: Union[bool, None] = False,
                    return_target_attributes: Union[bool, None] = False,
                    generate_nulls_for_fixed_targets: Union[bool, None] = False,
                    write_target_struct_info: Union[bool, None] = False,
                    drop_invalid_mappings: Union[bool, None] = False
                    ):
    """ Mapping with mapping provided as a structure-set in a registry \n
        e.g. mapping:  OECD.SDD.NAD/QNA_NAMAIN1_MAPPING/latest \n
        registry: http://sdmxri-dev-2.main.oecd.org:8080/FusionRegistry/ws/public/sdmxapi/rest 
    """
    print(f'map_withURN called with source_file: {source_file}, registry: {registry}, mapping: {mapping}')
    url = f'{registry}/structuremap/{mapping}/?detail=full&references=descendants'
    mu = SDMXMappingUtility.initialise_with_registry(registry_url=url, source_file=source_file)
    df = mu.generate_mappings_partial_keys(
            includeSourceColumns=return_source_dimensions,
            includeAttributesMeasures=return_target_attributes,
            nulledFixedTargets=generate_nulls_for_fixed_targets,
            writeTargetStructInfo=write_target_struct_info,
            dropInvalid=drop_invalid_mappings)
    
    
    return StreamingResponse(iter([df.to_csv(index=False)]), media_type="text/csv")
    
@app.get("/map_withFile")
async def map_withFile(
                    source_file: str,
                    mapping_file: str,
                    return_source_dimensions: Union[bool, None] = False,
                    return_target_attributes: Union[bool, None] = False,
                    generate_nulls_for_fixed_targets: Union[bool, None] = False,
                    write_target_struct_info: Union[bool, None] = False,
                    drop_invalid_mappings: Union[bool, None] = False
                    ):
    """ Mapping with mapping provided as a file with interrelated structures 
    """
    print( f'map_withFile called with source_file: {source_file}, mapping_file: {mapping_file}') 
    mu = SDMXMappingUtility.initialise_with_file(mapping_file=mapping_file, source_file=source_file)
    df = mu.generate_mappings_partial_keys(
            includeSourceColumns=return_source_dimensions,
            includeAttributesMeasures=return_target_attributes,
            nulledFixedTargets=generate_nulls_for_fixed_targets,
            writeTargetStructInfo=write_target_struct_info,
            dropInvalid=drop_invalid_mappings)
    

    return StreamingResponse(iter([df.to_csv(index=False)]), media_type="text/csv")

@app.post("/map_json_withURN")
async def map_json_withURN(
                    mapping: str,
                    registry: str,
                    json: KeyRange = Body(),
                    return_source_dimensions: Union[bool, None] = False,
                    return_target_attributes: Union[bool, None] = False,
                    generate_nulls_for_fixed_targets: Union[bool, None] = False,
                    write_target_struct_info: Union[bool, None] = False,
                    drop_invalid_mappings: Union[bool, None] = False, 
                    sid_based: Union[bool, None] = False
                    ):
    """ Mapping with mapping provided as a structure-set in a registry \n
        e.g. mapping:  OECD.SDD.NAD/QNA_NAMAIN1_MAPPING/latest \n
        registry: http://sdmxri-dev-2.main.oecd.org:8080/FusionRegistry/ws/public/sdmxapi/rest 
    """
    print(f'map_withURN called with source_file: {json}, registry: {registry}, mapping: {mapping}')
    url = f'{registry}/structuremap/{mapping}/?detail=full&references=descendants'
    mu = SDMXMappingUtility.initialise_with_jsonandregistry(registry_url=url, json=json, sid_based=sid_based)
    df = mu.generate_mappings_partial_keys(
            includeSourceColumns=return_source_dimensions,
            includeAttributesMeasures=return_target_attributes,
            nulledFixedTargets=generate_nulls_for_fixed_targets,
            writeTargetStructInfo=write_target_struct_info,
            dropInvalid=drop_invalid_mappings)
    
    
    return StreamingResponse(iter([df.to_csv(index=False)]), media_type="text/csv")