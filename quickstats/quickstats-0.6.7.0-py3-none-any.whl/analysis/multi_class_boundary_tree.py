from typing import Union, Optional, List, Tuple, Dict
import copy
import json

from quickstats import semistaticmethod

def int_keys(ordered_pairs):
    result = {}
    for key, value in ordered_pairs.items():
        try:
            key = int(key)
        except ValueError:
            pass
        result[key] = value
    return result

class MultiClassBoundaryTree:
    def __init__(self, score_base_name:str="score"):
        self.tree = {}
        self.current_node = None
        self.score_base_name = score_base_name
    
    @semistaticmethod
    def iter_branch(self, branch):
        if not branch:
            return {}
        sub_branch_keys = branch['branch']
        for key in sub_branch_keys:
            sub_branch = branch['branch'][key]
            if not isinstance(key, int):
                branch['branch'].pop(key)
            branch['branch'][int(key)] = self.iter_branch(sub_branch)
        return branch
    
    def load_tree(self, filename:str):
        with open(filename, "r") as file:
            self.tree = json.load(file, object_hook=int_keys)
        
    def get_branch(self, branch_index:Optional[Union[Tuple[int], int]]=None):
        branch = self.tree
        if branch_index is not None:
            if isinstance(branch_index, int):
                branch_index = [branch_index]
            for index in branch_index:
                if 'branch' not in branch:
                    raise ValueError("tree level out of bounds")
                if index not in branch['branch']:
                    raise ValueError("tree index out of bounds")
                branch = branch['branch'][index]
        return branch   
    
    def get_boundaries(self, branch_index:Optional[Union[Tuple[int], int]]=None):
        branch = self.get_branch(branch_index)
        if 'boundaries' not in branch:
            raise RuntimeError("boundaries not defined")
        boundaries = branch['boundaries']
        return boundaries
    
    def set_boundaries(self, class_label:str, boundaries:List[float],
                       branch_index:Optional[Union[Tuple[int], int]]=None, **kwargs):
        leaf = {
            'class': class_label,
            'boundaries': boundaries,
            'branch': {i:{} for i in range(len(boundaries)+1)},
            **kwargs
        }
        target_branch = self.get_branch(branch_index)
        target_branch.update(leaf)      
        
    @staticmethod
    def _get_score_windows(boundaries:List[float]):
        score_windows = []
        closed_boundaries = [0.] + boundaries + [1.]
        for i in range(len(closed_boundaries)-1):
            score_windows.append([closed_boundaries[i], closed_boundaries[i+1]])
        return score_windows

    def get_branch_indices(self, current_branch:Optional[Dict]=None,
                           current_index:Optional[List[int]]=None):
        output = []
        if current_branch is None:
            current_branch = self.tree
        if "branch" in current_branch:
            for branch_index in current_branch["branch"]:
                next_branch = current_branch["branch"][branch_index]
                if current_index is None:
                    next_index = [branch_index]
                    
                else:
                    next_index = list(current_index) + [branch_index]
                output.append(next_index)
                output += self.get_branch_indices(next_branch, next_index)
        return output    
    
    def get_combined_boundaries(self, branch_index:Union[int, List[int]]):
        branch = self.tree
        combined_boundaries = {}
        if isinstance(branch_index, int):
            branch_index = [branch_index]
        for index in branch_index:
            class_name = branch['class']
            boundaries = branch['boundaries']
            score_windows = self._get_score_windows(boundaries)
            # binary-class case
            if (not class_name) and len(branch_index) == 1:
                return score_windows[index]
            if class_name in combined_boundaries:
                raise RuntimeError("found multiple classes with the same name")
            combined_boundaries[class_name] = score_windows[index]
            if 'branch' not in branch:
                raise ValueError("tree level out of bounds")
            if index not in branch['branch']:
                raise ValueError("tree index out of bounds")
            branch = branch['branch'][index]
        return combined_boundaries

    def get_cut_maps(self, source:Dict=None, result:Optional[dict]=None,
                     index:Optional[List[int]]=None, 
                     cuts:Optional[List[str]]=None):
        if source is None:
            source = self.tree
            if not source:
                return {None: None}
        if result is None:
            result = {}
        if index is None:
            index = []
        if cuts is None:
            cuts = []
        class_name = source['class']
        boundaries = source['boundaries']
        score_windows = self._get_score_windows(boundaries)
        if not class_name:
            score_label = self.score_base_name
        else:
            score_label = f"{class_name}_{self.score_base_name}"
        for i, score_window in enumerate(score_windows):
            if score_window[1] != 1.:
                cut = f"({score_label} >= {score_window[0]}) & ({score_label} < {score_window[1]})"
            else:
                cut = f"({score_label} >= {score_window[0]}) & ({score_label} <= {score_window[1]})"
            index_i = list(index) + [i]
            cuts_i = list(cuts) + [cut]
            branch = source['branch'][i]
            if not branch:
                result[tuple(index_i)] = " & ".join(cuts_i)
            else:
                self.get_cut_maps(branch, result, index_i, cuts_i)
        return result
    
    @staticmethod
    def iter_branch_sig(branch:Dict, sublabel:str=None, temp_result:Optional[Dict]=None):
        if temp_result is None:
            temp_result = {}
        class_name = branch['class']
        significance = branch['significance']
        if class_name not in temp_result:
            temp_result[class_name] = {}
        if sublabel is not None:
            temp_result[class_name][sublabel] = significance
        else:
            temp_result[class_name] = significance
        for branch_index in branch['branch']:
            sub_branch = branch['branch'][branch_index]
            if sub_branch:
                if sublabel is None:
                    _sublabel = f"{class_name}_{branch_index}"
                else:
                    _sublabel = f"{sublabel}_{class_name}_{branch_index}"            
                MultiClassBoundaryTree.iter_branch_sig(sub_branch, _sublabel, temp_result)
        return temp_result
    
    def get_significance_summary(self):
        summary = self.iter_branch_sig(self.tree)
        # just report the significance value in case of binary class
        if (len(summary) == 1) and (("" in summary) or None in summary):
            key = list(summary)[0]
            return summary[key]
        return summary
    
    @semistaticmethod
    def _get_str_repr(self, source:Dict, level:int=0):
        str_repr = ""
        class_name = source['class']
        if class_name is None:
            class_name = ""
        boundaries = source['boundaries']
        score_windows = self._get_score_windows(boundaries)
        if 'significance' in source:
            extra_txt = f" (Z = {source['significance']:.3f})"
        else:
            extra_txt = ""
        str_repr += ("  "*2*level + class_name + extra_txt + "\n")
        for i, score_window in enumerate(score_windows):
            str_repr += ("  "*(2*level+1) + f"{i}: [{score_window[0]}, {score_window[1]}]" + "\n")
            branch = source['branch'][i]
            if not branch:
                continue
            str_repr += self._get_str_repr(branch, level+1)
        return str_repr
    
    def __repr__(self):
        return self._get_str_repr(self.tree)