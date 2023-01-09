from typing import Literal, Union
import pandas as pd
import xml.etree.ElementTree as ET
import requests
from pathlib import Path
from copy import deepcopy
from pydantic import BaseModel

from mappings_utility.sdmx_structures import NS, INVALID, ComponentMap, DataStructure, Dataflow, FixedValueMap, MapType, RepresentationMap, StructureMap 


class KeyRange(BaseModel):
    __root__: dict[str, list[str]]


# Partial key mapping utility working with SDMX 3.0 structure-set and representation mapping objects
class SDMXMappingUtility():

   def __init__(self, mapping_tree: ET.ElementTree , source_file: Union[Path, None]  = None, json: Union[KeyRange, None] = None, sid_based: bool = False):
         self.source_file = source_file
         self.mapping_tree = mapping_tree
         self.json = json
         self._read_mapping()
         if source_file:
            self._read_source('csv', sid_based)
         elif json:
            self._read_source('json', sid_based)
      
   @classmethod
   def initialise_with_registry(cls, registry_url: str, source_file: Path, sid_based: bool = False):
      try:
         headers = {
            'accept': 'application/vnd.sdmx.structure+xml;version=3.0'
         }
         # TODO check if SSL verification can be switched on - needs https for the registry
         response = requests.get(registry_url, verify=False, headers=headers)

      except Exception as err:
         return 'ERROR: ' + str(err)
      else:
         if response.status_code != 200:
            return 'UNEXPECTED: ' + response.text 
         else:
            return cls(ET.ElementTree(ET.fromstring(response.content)), source_file, sid_based=sid_based)

   @classmethod
   def initialise_with_jsonandregistry(cls, registry_url: str, json: KeyRange,  sid_based: bool = False):
      try:
         headers = {
            'accept': 'application/vnd.sdmx.structure+xml;version=3.0'
         }
         # TODO check if SSL verification can be switched on - needs https for the registry
         response = requests.get(registry_url, verify=False, headers=headers)

      except Exception as err:
         return 'ERROR: ' + str(err)
      else:
         if response.status_code != 200:
            return 'UNEXPECTED: ' + response.text 
         else:
            return cls(ET.ElementTree(ET.fromstring(response.content)), json=json, sid_based=sid_based)

   @classmethod
   def initialise_with_file(cls, mapping_file: Path, source_file: Path, sid_based: bool = False):
      return cls(ET.parse(mapping_file), source_file, sid_based=sid_based)         
               

   def _read_mapping(self):
      print('reading mapping objects...')
      try:
         root = self.mapping_tree.getroot()

         dataflow_elements = root.findall('*/str:Dataflows/str:Dataflow', namespaces=NS)
         dataflows = [Dataflow(e) for e in dataflow_elements]
         self.dataflows = dataflows

         datastructure_elements = root.findall('*/str:DataStructures/str:DataStructure', namespaces=NS)
         datastructures = [DataStructure(e) for e in datastructure_elements]
         self.datastructures = datastructures

         struct_map = root.find('*/str:StructureMaps/str:StructureMap', namespaces=NS)
         self.structure_map = StructureMap(struct_map)

         component_maps = list(struct_map.findall('str:ComponentMap', namespaces=NS))
         cms = [ComponentMap(e) for e in component_maps]
         self.component_maps = cms

         fixedvalue_maps = list(struct_map.findall('str:FixedValueMap', namespaces=NS))
         fvms = [FixedValueMap(e) for e in fixedvalue_maps]
         self.fixedvalue_maps = fvms

         representations = root.findall('*/str:RepresentationMaps/str:RepresentationMap', namespaces=NS)
         reps = [RepresentationMap(e) for e in representations]
         self.representation_maps = reps
      except Exception as err:
         print(str(err))
         raise err

   def _read_source(self, stype: Literal['csv', 'json'], sid_based: bool = False):
      print('reading source file...')
      try:
         if stype == 'csv':
            df = pd.read_csv(self.source_file, dtype=str, na_filter=False)
         elif stype == 'json':
            df = pd.DataFrame.from_dict(self.json.dict()['__root__'], dtype=str)
         else:
            raise ValueError
      except Exception as err:
         print(str(err))
         raise err

      if sid_based:
            dsd = self.get_dsd_by_urn(self.structure_map.source)
            source_cols = dsd.dim_list()
            df[source_cols] = df.SID.str.split('.', expand=True)

      self.df_source_partial_keys = self._source_data_cosmetics(df)

   def _source_data_cosmetics(self, df):
         df.rename(columns = {cn: '_S_'+cn for cn in df.columns}, inplace = True)
         # Add missing columns
         for cm in self.component_maps:
            for source in cm.sources:
               if source not in df.columns:
                  df[source] = pd.Series(dtype='str')
         return df 

   def get_representation_by_urn(self, urn: str) -> Union[RepresentationMap, None]:
      for x in self.representation_maps:
         if x.urn == urn:
            return x
      return None

   # the urn to lookup could be that of a Dataflow or the DSD itself 
   def get_dsd_by_urn(self, urn: str) -> DataStructure:
      for df in self.dataflows:
         if df.urn == urn:
            for ds in self.datastructures:
               if ds.urn == df.datastructure:
                  return ds

      for dsd in self.datastructures:
         if dsd.urn == urn:
            return dsd

      return None                   

   # Generate mappings partial keys
   # includeSourceColumns: if true: both keys (from source and from target) will be in the dataframe
   #          false: only keys from target dataflow will be in the dataframe
   # includeAttributesMeasures: if true: all dimensions, attributes, and measures of the target dataflow will be in the dataframe
   #          false: only dimensions from target dataflow will be in the dataframe
   # nulledFixedTargets: if true: the targets with fixed representation will not be inserted (the expected behaviour when partial keys are mapped 
   #          for attribute and referential metadata attachment), false: for full data mappings
   # writeTargetStructInfo: if true: SDMX csv 3.0 style structural and action information will be writtern into the first columns of the generated file
   # dropInvalid: if true: non-mapped and source records containing invalid members will be dropped (in cases when the mapping acts as a filter)
   # TODO correct the order of columns and produce SID - a partial-key for metadata attachments

   def generate_mappings_partial_keys(self, includeSourceColumns=False, includeAttributesMeasures=False, nulledFixedTargets=False, writeTargetStructInfo=False, dropInvalid=False, sid_based=False):
      
         df = self.df_source_partial_keys
         
         # TODO revise the structure components to write (is source needed?, controlling the Action - with an Enum?, Generate SID?)
         if writeTargetStructInfo:
            al = ['STRUCTURE', 'STRUCTURE_ID', 'ACTION']
            df[al] = df.apply(lambda row: [self.structure_map.target_type.lower(), self.structure_map.target_id, 'A'], axis=1, result_type='expand')

         # ComponentMaps
         for cm in self.component_maps:
            if cm.type in [MapType.OneToOne] and cm.implicit:
               # copy identical with target component-name
               print(f'copying source to target {cm.sources} -> {cm.targets}')
               df[cm.targets[0]] = df[cm.sources[0]]
            else:
               # only those cases can be mapped safely where there are valid inputs in all source columns
               print(f'applying representation map {cm.sources} -> {cm.targets}')
               rm = self.get_representation_by_urn(cm.representation)
               df[cm.targets] = df.apply(lambda x: rm.get_target_values_by_sourcelist([x[c] for c in cm.sources]), axis=1, result_type='expand')

         # Add target missing columns mapped as fixed value
         for fvm in self.fixedvalue_maps:
            if not nulledFixedTargets:
               df[fvm.target] = fvm.value
            else:
               df[fvm.target] = ''

         if sid_based:
            dsd = self.get_dsd_by_urn(self.structure_map.target)
            df['SID'] = df.apply(lambda x: '.'.join([x[c] for c in dsd.dim_list()]), axis=1)

         # Remove source columns, which are in the mappings and sid      
         if not includeSourceColumns:
            # Get mapped source columns 
            source_columns = [] 
            for cm in self.component_maps:
               source_columns += cm.sources
            if sid_based: 
               source_columns += ['_S_SID']
            df.drop(source_columns, axis=1, inplace=True)

         # Remove columns, which are not in the dimension list of the target dataflow
         # such as attributes and measures
         if not includeAttributesMeasures:
            dsd = self.get_dsd_by_urn(self.structure_map.target)
            if sid_based:
               columns_to_drop = [column for column in df.columns if (not column =='SID' and not column.startswith("_S_"))]
            else: 
               columns_to_drop = [column for column in df.columns if (not dsd.isdimension(column) and not column.startswith("_S_"))]
            df.drop(columns_to_drop, axis=1, inplace=True)

         if dropInvalid:
            df = df[df.ne(INVALID).all(axis=1)]   

         return deepcopy(df)