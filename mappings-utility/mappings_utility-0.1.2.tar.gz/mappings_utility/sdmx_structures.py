from copy import deepcopy
from typing import Literal, NamedTuple, Union
from dataclasses import dataclass
from enum import Enum
import re
import xml.etree.ElementTree as ET

NS = {"xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "message": "http://www.sdmx.org/resources/sdmxml/schemas/v3_0/message",
        "str": "http://www.sdmx.org/resources/sdmxml/schemas/v3_0/structure",
        "com": "http://www.sdmx.org/resources/sdmxml/schemas/v3_0/common"
        }

INVALID = '!_INVALID_'


class MapType(Enum):
   OneToOne = 0
   OneToMany = 1
   ManyToOne = 2
   ManyToMany = 3

class SourceField(NamedTuple):
  isRegEx: bool
  value: str   


@dataclass
class Dataflow():
   urn: str
   isexternalreference: bool
   agencyID: str
   id: str
   version: str
   datastructure: str

   def __init__(self, elem: ET.Element) -> None:
      self.urn = elem.get('urn')
      if elem.get('isExternalReference') == 'false': 
         self.isexternalreference = False
      else:
         self.isexternalreference = True
      self.agencyID = elem.get('agencyID')
      self.id = elem.get('id')
      self.version = elem.get('version')
      self.datastructure = elem.find('str:Structure', namespaces=NS).text

   @property
   def fullid(self):
      return f'{self.agencyID}:{self.id}({self.version})'   
     


@dataclass
class DataStructure():
   urn: str
   isexternalreference: bool
   agencyID: str
   id: str
   version: str
   dimensions: list

   def __init__(self, elem: ET.Element) -> None:
      self.urn = elem.get('urn')
      if elem.get('isExternalReference') == 'false': 
         self.isexternalreference = False
      else:
         self.isexternalreference = True
      self.agencyID = elem.get('agencyID')
      self.id = elem.get('id')
      self.version = elem.get('version')

      self.dimensions = [] 
      for dimensions_element in elem.findall('*/str:DimensionList/str:Dimension', namespaces=NS):
         dimension = {k: dimensions_element.get(k) for k in ['id', 'position']}
         self.dimensions.append(deepcopy(dimension))
      for dimensions_element in elem.findall('*/str:DimensionList/str:TimeDimension', namespaces=NS):
         dimension = {k: dimensions_element.get(k) for k in ['id', 'position']}
         self.dimensions.append(deepcopy(dimension))


   def isdimension(self, dimension) -> bool:
      for d in self.dimensions:
         if d['id'] == dimension:
            return True

      return False
   
   def dim_list(self) -> list:
      return [d['id'] for d in self.dimensions]       


@dataclass
class StructureMap():
   source: str 
   target: str
   target_type: str = ''
   target_id: str = '' 
   
   def __init__(self, elem: ET.Element) -> None:
      self.source = elem.find('str:Source', namespaces=NS).text
      self.target = elem.find('str:Target', namespaces=NS).text
      p = re.compile(r'.*datastructure\.(.+)=(.+:.+\([0-9]+\.[0-9]+\))')
      m = p.match(self.target)      
      if m:
         self.target_type, self.target_id = m.groups()

      

@dataclass
class ComponentMap():
   sources: list
   targets: list
   type: MapType
   implicit: bool
   representation: str = ''
  
   def __init__(self, elem: ET.Element) -> None:
      sl = list(elem.findall('str:Source', namespaces=NS))
      self.sources = ['_S_'+e.text for e in sl]

      tl = list(elem.findall('str:Target', namespaces=NS))
      self.targets = [e.text for e in tl]

      rm = elem.findall('str:RepresentationMap', namespaces=NS)
      if rm:
            self.representation = rm[0].text
            self.implicit = False
      else:
            self.implicit = True

      if len(sl)==1:
            if len(tl)==1:
               self.type = MapType.OneToOne
            else:
               self.type = MapType.OneToMany
      else:
         if len(tl)==1:
            self.type = MapType.ManyToOne
         else:
            self.type = MapType.ManyToMany


@dataclass
class FixedValueMap():
   value: str
   target: str
  
   def __init__(self, elem: ET.Element) -> None:
      self.target = elem.find('str:Target', namespaces=NS).text
      self.value = elem.find('str:Value', namespaces=NS).text


@dataclass
class RepresentationMap():
   urn: str
   isexternalreference: bool
   mappings: list 

   def __init__(self, elem: ET.Element) -> None:
      self.urn = elem.get('urn')

      if elem.get('isExternalReference') == 'false': 
         self.isexternalreference = False
      else:
         self.isexternalreference = True

      self.mappings = [] 
      for rm in elem.findall('str:RepresentationMapping', namespaces=NS):
         rmd = {'sourcevalues': [], 'targetvalues': []}
         for sv in rm.findall('str:SourceValue', namespaces=NS):
            if 'isRegEx' in sv.attrib.keys():
               rmd['sourcevalues'].append(SourceField(value=sv.text, isRegEx=bool(sv.attrib['isRegEx'])))
            else:   
               rmd['sourcevalues'].append(SourceField(value=sv.text, isRegEx=False))   
               
         for tv in rm.findall('str:TargetValue', namespaces=NS):
            rmd['targetvalues'].append(tv.text)
         self.mappings.append(deepcopy(rmd))
      
   def _replace_matches(self, matching_groups: tuple, target_list: list[str]) -> list[str]:
      sp = re.compile(r'.*(\\[1-9]).*')
      for idx, val in enumerate(target_list):
         sm = sp.match(val)
         if sm: 
            for x in sm.groups():
               # index correction to allow end-user to use 1 based indexing for matching groups
               target_list[idx] = val.replace(x, matching_groups[int(x[1])-1], 1)
   
      return target_list

   def get_target_values_by_sourcelist(self, sourcelst: list) -> Union[list[str], None]:
      
         for m in self.mappings:
            pairs = zip(m['sourcevalues'], sourcelst)
            matched = True
            target = deepcopy(m['targetvalues'])
            # assumption: only one of the fields in source has RegEx
            for pair in pairs:
               if pair[0].isRegEx:
                  p = re.compile(pair[0].value)
                  matches = p.match(pair[1])
                  if matches:
                     target = self._replace_matches(matches.groups(), deepcopy(target))
                  else: 
                     matched = False
               else:
                  if pair[0].value != pair[1]:
                     matched = False
            if matched:
               return target
         if any([s!='' for s in sourcelst]):
            return [INVALID] * len(self.mappings[0]['targetvalues'])
         else:
            return [''] * len(self.mappings[0]['targetvalues'])   