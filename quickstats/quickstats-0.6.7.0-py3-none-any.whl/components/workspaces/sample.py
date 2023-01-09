from typing import Optional, Union, List, Dict

import ROOT

from quickstats.utils.common_utils import remove_list_duplicates

from .settings import SELF_SYST_DOMAIN_KEYWORD, PDF_PREFIX

class Sample:
    
    # deprecated name
    @property
    def syst_groups(self):
        return self.syst_domains
    
    @syst_groups.setter
    def syst_groups(self, value):
        self.syst_domains = value
    
    def __init__(self):
        self.process = ""
        self.input_file = ""
        self.norm_factors = []
        self.shape_factors = []
        self.syst_domains = []
        self.expected = ROOT.RooArgSet()
        self.model_name = ""
        self.norm_name = ""
        self.share_pdf_group = ""
        
    def __eq__(self, other:Union[str, "Sample"]):
        if isinstance(other, str):
            return self.process == other
        elif isinstance(other, type(self)):
            return self.process == other.process
        else:
            raise TypeError(f"cannot compare object of type {type(other)} with "
                            "object of type Sample")
        
    def is_equal(self, other:Union[str, "Sample"]):
        return self.__eq__(other)
            
    def get_tag_name(self) -> str:
        is_shared_pdf = self.share_pdf_group != ""
        if is_shared_pdf:
            tag_name = self.share_pdf_group
        else:
            tag_name = self.process
        return tag_name
    
    def update_model_name(self):
        self.model_name = f"{PDF_PREFIX}{self.get_tag_name()}"
        
    def set_syst_domains(self, syst_domains:List[str]):
        # if the domain contains ":self:", then do not take any systematics from outside
        if SELF_SYST_DOMAIN_KEYWORD in syst_domains:
            syst_domains = []
        # all the systematics under the process should be included in any case  
        if self.process not in syst_domains:
            syst_domains.append(self.process)
        self.syst_domains = remove_list_duplicates(syst_domains)