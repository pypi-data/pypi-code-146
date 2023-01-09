from typing import Union, Optional, Dict, List, Set
import re
import uuid
import fnmatch

import ROOT

from .string_utils import remove_whitespace

def copy_attributes(source:"ROOT.RooAbsArg", target:"ROOT.RooAbsArg"):
    if source is target:
        return
    for attrib in source.attributes():
        target.setAttribute(attrib)
    for attrib in source.stringAttributes():
        target.setStringAttribute(attrib.first, attrib.second)
        
def get_variable_attributes(variable:ROOT.RooAbsReal, asym_error:bool=False):
    if isinstance(variable, ROOT.RooRealVar):
        if asym_error:
            attributes = {
                'name' : variable.GetName(),
                'value': variable.getVal(),
                'errorlo': variable.getErrorLo(),
                'errorhi': variable.getErrorHi(),
                'min'  : variable.getMin(),
                'max'  : variable.getMax(),
                'is_constant': variable.isConstant()
            }
        else:
            attributes = {
                'name' : variable.GetName(),
                'value': variable.getVal(),
                'error': variable.getError(),
                'min'  : variable.getMin(),
                'max'  : variable.getMax(),
                'is_constant': variable.isConstant()
            }
    elif isinstance(variable, ROOT.RooAbsReal):
        attributes = {
            'name' : variable.GetName(),
            'value': variable.getVal()
        }
    else:
        raise ValueError("variable must be an instance of RooAbsReal")
    return attributes

def variable_collection_to_dataframe(var_collection:Union[list, ROOT.RooArgSet],
                                     asym_error:bool=False):
    import pandas as pd
    data = []
    for variable in var_collection:
        attributes = get_variable_attributes(variable, asym_error=asym_error)
        data.append(attributes)
    df = pd.DataFrame(data)
    return df
        
def construct_categorized_pdf_dataset(pdf:"ROOT.RooAbsPdf", dataset:"ROOT.RooDataSet", 
                                      workspace:"ROOT.RooWorkspace", label:str,
                                      category_name:str="adhocCat"):
    # make sure pdf is not already a simultaneous pdf
    assert pdf.ClassName() != "RooSimultaneous"
    cat = ROOT.RooCategory(category_name, category_name)
    cat.defineType(label)
    pdf_dict = {label: pdf}
    pdf_map = ExtendedModel.get_object_map(pdf_dict, "RooAbsPdf")
    dataset_dict = {label: dataset}
    dataset_map = ExtendedModel.get_object_map(data_dict, "RooDataSet")
    sim_pdf = ROOT.RooSimultaneous(pdf.GetName(), pdf.GetName(), pdf_map, cat)
    obs_and_weight = dataset.get()
    weight_var = workspace.var("weightVar")
    if not weitht_var:
        raise RuntimeError("workspace does not contain the variable `weightVar`")
    obs_and_weight.add(weight_var)
    indexed_dataset = ROOT.RooDataSet(dataset.GetName(), dataset.GetName(), obs_and_weight, 
                                      ROOT.RooFit.Index(cat),
                                      ROOT.RooFit.Import(dataset_map),
                                      ROOT.RooFit.WeightVar(weight_var))
    return sim_pdf, indexed_dataset


def factorize_pdf(observables:"ROOT.RooArgSet", pdf:"ROOT.RooAbsPdf", constraints:"ROOT.RooArgSet"):
    pdf_class = pdf.ClassName()   
    if pdf_class == "RooProdPdf":
        new_factors = ROOT.RooArgList()
        new_owned = ROOT.RooArgSet()
        pdf_list = pdf.pdfList()
        need_new = False
        for i in range(len(pdf_list)):
            pdf_i = pdf_list[i]
            new_pdf = factorize_pdf(observables, pdf_i, constraints)
            if new_pdf == 0:
                need_new = True
                continue
            if new_pdf is not pdf_i:
                need_new = True
                new_owned.add(new_pdf)
            new_factors.add(new_pdf)
        if not need_new:
            return pdf
        elif len(new_factors) == 0:
            return 0
        elif len(new_factors) == 1:
            clone_pdf = new_factors.first().Clone("{}_obsOnly".format(pdf.GetName()))
            copy_attributes(pdf, clone_pdf)
            return clone_pdf
        factorized_pdf = ROOT.RooProdPdf("{}_obsOnly".format(pdf.GetName()), "", new_factors)
        factorized_pdf.addOwnedComponents(new_owned)
        copy_attributes(pdf, factorized_pdf)
        return factorized_pdf
    elif pdf_class == "RooSimultaneous":
        cat = pdf.indexCat().Clone()
        n_bins = cat.numBins("")
        factorized_pdfs = []
        new_owned = ROOT.RooArgSet()
        need_new = False
        for i in range(n_bins):
            cat.setBin(i)
            pdf_i = pdf.getPdf(cat.getLabel())
            new_pdf = factorize_pdf(observables, pdf_i, constraints)
            factorized_pdfs.append(new_pdf)     
            if new_pdf == 0:
                raise RuntimeError("channel `{}` factorized to 0".format(cat.getLabel()))
            if new_pdf is not pdf_i:
                need_new = True
                new_owned.add(new_pdf)
                # this can be removed after version 6.28
                ROOT.SetOwnership(new_pdf, False)
        factorized_pdf = pdf
        if need_new:
            factorized_pdf = ROOT.RooSimultaneous("{}_obsOnly".format(pdf.GetName()), "", pdf.indexCat())
            for i in range(n_bins):
                cat.setBin(i)
                new_pdf = factorized_pdfs[i]
                if new_pdf:
                    factorized_pdf.addPdf(new_pdf, cat.getLabel())
            factorized_pdf.addOwnedComponents(new_owned)
        # has to delete persistent object
        cat.Delete()
        copy_attributes(pdf, factorized_pdf)
        return factorized_pdf         
    elif pdf.dependsOn(observables):
        return pdf
    else:
        if not constraints.contains(pdf):
            constraints.add(pdf)
        return 0
    
    
def rebuild_simultaneous_pdf(observables:"ROOT.RooArgSet", sim_pdf:"ROOT.RooSimultaneous"):
    assert sim_pdf.ClassName() == "RooSimultaneous"
    constraints = ROOT.RooArgList()
    cat = sim_pdf.indexCat().Clone()
    n_bins = cat.numBins("")
    factorized_pdfs = []
    new_owned = ROOT.RooArgSet()
    for i in range(n_bins):
        cat.setBin(i)
        pdf_i = sim_pdf.getPdf(cat.getLabel())
        if pdf_i == 0:
            factorized_pdfs.append(0)
            continue
        new_pdf = factorize_pdf(observables, pdf_i, constraints)     
        factorized_pdfs.append(new_pdf)
        if new_pdf == 0:
            continue
        if new_pdf is not pdf_i:
            new_owned.add(new_pdf)
            # this can be removed after version 6.28
            ROOT.SetOwnership(new_pdf, False)
    rebuilt_pdf = ROOT.RooSimultaneous("{}_reloaded".format(sim_pdf.GetName()), "", sim_pdf.indexCat())
    for i in range(n_bins):
        cat.setBin(i)
        new_pdf = factorized_pdfs[i]
        if new_pdf:
            if constraints.getSize() > 0:
                all_factors = ROOT.RooArgList(constraints)
                all_factors.add(new_pdf)
                newer_pdf = ROOT.RooProdPdf("{}_plus_constr".format(new_pdf.GetName()), "",
                                           all_factors)
                rebuilt_pdf.addPdf(newer_pdf, cat.getLabel())
                copy_attributes(new_pdf, newer_pdf)
                new_owned.add(newer_pdf)
                # this can be removed after version 6.28
                ROOT.SetOwnership(newer_pdf, False)
            else:
                rebuilt_pdf.addPdf(new_pdf, cat.getLabel())
    rebuilt_pdf.addOwnedComponents(new_owned)
    copy_attributes(sim_pdf, rebuilt_pdf)
    return rebuilt_pdf

def print_object(obj, indent=0, spacer="  ", prefix="-", show_address=False):
    if show_address:
        print(f"{spacer*indent}{prefix}{obj.GetName()}({obj.ClassName()} @ {hex(id(obj))})")
    else:
        print(f"{spacer*indent}{prefix}{obj.GetName()}({obj.ClassName()})")
        
def print_pdf_structure(pdf:"ROOT.RooAbsPdf", level:int=0, show_address=False, max_level:int=-1):
    if (max_level >= 0) and (level > max_level):
        return None
    print_object(pdf, level, show_address=show_address)
    class_name = pdf.ClassName()
    if class_name == "RooSimultaneous":
        cat = pdf.indexCat().Clone()
        n_bins = cat.numBins("")
        for i in range(n_bins):
            cat.setBin(i)
            pdf_i = pdf.getPdf(cat.getLabel())
            print_pdf_structure(pdf_i, level+1, show_address=show_address, max_level=max_level)
    elif class_name == "RooProdPdf":
        pdf_list = pdf.pdfList()
        for pdf_i in pdf_list:
            print_pdf_structure(pdf_i, level+1, show_address=show_address, max_level=max_level)
    elif class_name == "RooRealSumPdf":
        pdf_list = pdf.getComponents()
        for pdf_i in pdf_list:
            if pdf_i == pdf:
                continue
            print_pdf_structure(pdf_i, level+1, show_address=show_address, max_level=max_level)
                     
def get_correlation_matrix(roofit_result, lib:str="pandas"):
    correlation_hist = roofit_result.correlationHist()
    if lib.lower() == "pandas":
        from quickstats.interface.root import TH2
        df = TH2.correlationHist_to_dataframe(correlation_hist)
        correlation_hist.Delete()
        return df
    elif lib.lower() == "root":
        return correlation_hist
    else:
        raise ValueError(f"unsupported library: {lib} (available options: \"root\", \"pandas\")")
        
def get_relevant_components(target, reference:Set[ROOT.RooArgSet]):
    result = ROOT.RooArgSet()
    if target in reference:
        result.add(target)
    components = None
    if isinstance(target, ROOT.RooAbsPdf):
        components = target.getComponents()
        components.remove(target)
    elif isinstance(target, ROOT.RooProduct):
        components = target.components()
    if (components is not None) and components.getSize():
        for component in components:
            relevant_components = get_relevant_components(component, reference)
            result.add(relevant_components)
    return result

def export_hist_data(data:ROOT.RooDataSet,
                     pdf:Optional[ROOT.RooAbsPdf]=None,
                     observable:Optional[ROOT.RooRealVar]=None,
                     bin_range:Optional[List]=None,
                     bin_error:bool=True,
                     n_bins_data:Optional[int]=None,
                     n_bins_pdf:Optional[int]=1000):

    if observable is None:
        if data.get().size() > 1:
            raise RuntimeError("only single-observable is allowed")
        observable = data.get().first()

    if bin_range is None:
        bin_range = observable.getRange()
        bin_range = [bin_range.first, bin_range.second]

    if n_bins_data is None:
        n_bins_data = observable.getBins()
        
    if n_bins_pdf is None:
        n_bins_pdf = n_bins_data        
        
    binning_data = ROOT.RooFit.Binning(n_bins_data, bin_range[0], bin_range[1])
    binning_pdf  = ROOT.RooFit.Binning(n_bins_pdf, bin_range[0], bin_range[1])

    from quickstats.interface.root import RooAbsData
    h_data = RooAbsData.create_histogram(data, uuid.uuid4().hex, observable, binning_data)
    
    if bin_error:
        # use SumW2 error if weighted, else use Poisson error
        if data.isWeighted():
            bin_errors = {"lo": h_data.bin_error, "hi": h_data.bin_error}
        else:
            from quickstats.interface.root import TH1
            bin_errors = TH1.GetPoissonError(h_data.bin_content)
    else:
        size = len(h_data.bin_content)
        bin_errors = {"lo": np.zeros(size), "hi": np.zeros(size)}

    hist_data = {
        'data': {
            'x': h_data.bin_center,
            'y': h_data.bin_content,
            'yerrlo': bin_errors['lo'],
            'yerrhi': bin_errors['hi']
        }
    }
    
    if pdf is not None:
        
        h_pdf = RooAbsData.create_histogram(pdf, uuid.uuid4().hex, observable, binning_pdf)
        h_pdf_data_binning = RooAbsData.create_histogram(pdf, uuid.uuid4().hex, observable,
                                                         binning_data)
        
        # calculate normalization factors
        norm_data  = h_data.bin_content.sum()
        norm_pdf1  = h_pdf.bin_content.sum()
        norm_pdf2  = h_pdf_data_binning.bin_content.sum()            
            
        hist_data['pdf'] = {
            'x': h_pdf.bin_center,
            'y': h_pdf.bin_content * norm_data / norm_pdf1 * (n_bins_pdf / n_bins_data)
        }
        hist_data['pdf_data_binning'] = {
            'x': h_pdf_data_binning.bin_center,
            'y': h_pdf_data_binning.bin_content * norm_data / norm_pdf2
        }
        
    return hist_data

def translate_formula(name:str, formula:str):
    variable_regex = re.compile(r"\b[a-zA-Z]\w+\b")
    variables = variable_regex.findall(formula)
    variables = sorted(set(variables))
    expr = formula
    for i, variable in enumerate(variables):
        expr = re.sub(r"\b" + variable + r"\b", f"@{i}", expr)
    translated_formula = f"expr::{name}('{expr}', {', '.join(variables)})"
    return translated_formula, variables

def recover_formula(formula:str):
    expr_regex = re.compile(r"'(.*?)'")
    expressions = expr_regex.findall(formula)
    if len(expressions) != 1:
        raise RuntimeError("invalid RooFit factory expression")
    expression = expressions[0]
    variables_regex = re.compile(r"\('.*?',(.*)\)")
    variables = variables_regex.findall(formula)
    if len(variables) != 1:
        raise RuntimeError("invalid RooFit factory expression")
    variables = [i.strip() for i in variables[0].split(",") if i.strip()]
    recovered_formula = expression
    for i, variable in enumerate(variables):
        recovered_formula = re.sub(f"@{i}(?![0-9])", variable, recovered_formula)
    return recovered_formula

def get_nuis_beta_terms(nuis_name:str, components):
    nuis_term = None
    beta_term = None
    if components.size() != 2:
        return nuis_term, beta_term
    for component in components:
        if component.GetName() == nuis_name:
            nuis_term = component
        else:
            beta_term = component
    return nuis_term, beta_term

def get_gaus_response_variations(nuis:ROOT.RooRealVar, client:ROOT.RooAddition):
    result = {"nominal": None, "low": None, "high": None, "type": None}
    if not isinstance(client, ROOT.RooAddition):
        raise ValueError("gaussian response function must be an instance of RooAddition")
    nuis_name = nuis.GetName()
    nominal_term, beta_term, nuis_term, resp_term = None, None, None
    terms = client.list()
    for term in terms:
        if isinstance(term, ROOT.RooProduct):
            for subterm in term.components():
                if isinstance(subterm, ROOT.RooProduct):
                    nuis_term, beta_term = get_nuis_beta_terms(nuis_name, subterm.components())
                elif isinstance(subterm , ROOT.RooRealVar):
                    resp_term = subterm
        elif isinstance(term, ROOT.RooRealVar):
            nominal_term = term
    if any(term is None for term in [beta_term, nuis_term, nominal_term, resp_term]):
        return result
    nominal = nominal_term.getVal()
    magnitude = resp_term.getVal()
    beta = beta_term.getVal()
    value = round(magnitude * beta, 8)
    return {"nominal": nominal, "low": value, "high": value, "type": "gaus"}

def get_logn_response_variations(nuis:ROOT.RooRealVar, client:ROOT.RooFormulaVar):
    result = {"nominal": None, "low": None, "high": None, "type": None}
    if not isinstance(client, ROOT.RooFormulaVar):
        raise ValueError("lognormal response function must be an instance of RooFormulaVar")    
    nuis_name = nuis.GetName()
    formula = client.formula()
    formula_str = formula.formulaString()
    formula_str = remove_whitespace(formula_str)
    if not formula_str.startswith("exp("):
        return result
    dependents = formula.actualDependents()
    if dependents.size() != 2:
        return result
    beta_term, nuis_term, resp_term = None, None, None
    for dependent in dependents:
        if isinstance(dependent, ROOT.RooProduct):
            nuis_term, beta_term = get_nuis_beta_terms(nuis_name, dependent.components())
        elif isinstance(dependent, ROOT.RooFormulaVar):
            resp_term = dependent
    if any(term is None for term in [beta_term, nuis_term, resp_term]):
        return result
    beta = beta_term.getVal()
    resp_formula_str = resp_term.formula().formulaString()
    resp_formula_str = remove_whitespace(resp_formula_str)
    if resp_formula_str == "log(1+x[0]/x[1])":
        resp_dependents = resp_term.formula().actualDependents()
        magnitude = resp_dependents[0].getVal()
        value = round(magnitude * beta, 8)
        nominal = resp_dependents[1].getVal()
        return {"nominal": nominal, "low": value, "high": value, "type": "logn"}
    return result

def get_asym_response_variations(nuis:ROOT.RooRealVar, client):
    if not isinstance(client, ROOT.RooStats.HistFactory.FlexibleInterpVar):
        raise ValueError("asymmetric response function must be an instance of RooFormulaVar") 
    low = client.low()
    high = client.high()
    nominal = client.nominal()
    if (low.size() != 1) or (high.size() != 1):
        raise RuntimeError(f'invalid low/high value format for the FlexibleInterpVar '
                           f'intance "{client.GetName()}"')
    return {"nominal": nominal, "low": round(low[0], 8), "high": round(high[0], 8), "type": "asym"}

def get_ProcessNormalization_response_variations(nuis:ROOT.RooRealVar, client):
    if client.ClassName() != "ProcessNormalization":
        raise ValueError("response function must be an instance of ProcessNormalization")
    nuis_name = nuis.GetName()
    kappas = client.getKappa(nuis_name)
    if not kappas:
        raise RuntimeError(f'failed to extract magnitude for the systematic "{nuis_name}" from '
                           f'the ProcessNormalization client "{client.GetName()}"')
    if len(kappas) == 1:
        return {"nominal": 1, "low":  round(kappas[0] - 1, 8), "high": round(kappas[0] - 1, 8), "type": "logn"}
    elif len(kappas) == 2:
        return {"nominal": 1, "low":  round(kappas[0] - 1, 8), "high": round(kappas[1] - 1, 8), "type": "asym"}
    else:
        raise RuntimeError(f'invalid kappa values for the systematic "{nuis_name}" from '
                           f'the ProcessNormalization client "{client.GetName()}"')
            
def get_systematic_variations_from_client(nuis:ROOT.RooRealVar, client):
    result = {"client": None, "nominal": None, "low": None, "high": None, "type": None}
    class_name = client.ClassName()
    nuis_name = nuis.GetName()
    # CMS dedicated normalization response function
    if class_name == "ProcessNormalization":
        result["client"] = client.GetName()
        result.update(get_ProcessNormalization_response_variations(nuis, client))
    elif class_name == "RooProduct":
        parent_clients = client.clients()
        if parent_clients.size() != 1:
            return result
        parent_client = parent_clients[0]
        result["client"] = parent_client.GetName()
        parent_class_name = parent_client.ClassName()
        if isinstance(parent_client, ROOT.RooFormulaVar):
            result.update(get_logn_response_variations(nuis, parent_client))
        elif isinstance(parent_client, ROOT.RooAddition):
            result.update(get_gaus_response_variations(nuis, parent_client))
        elif isinstance(parent_client, ROOT.RooStats.HistFactory.FlexibleInterpVar):
            result.update(get_asym_response_variations(nuis, parent_client))
    return result

def get_systematic_variations_from_clients(nuis:ROOT.RooRealVar, constr_pdf:ROOT.RooAbsPdf):
    constr_pdf_name = constr_pdf.GetName()
    clients = [c for c in nuis.clients() if c.GetName() != constr_pdf_name]
    result = {}
    for client in clients:
        client_result = get_systematic_variations_from_client(nuis, client)
        client_name = client_result.pop("client")
        if client_name is not None:
            result[client_name] = client_result
    return result

def get_systematics_variations(nuis_set:Union[List, ROOT.RooArgSet], constr_set:Union[List, ROOT.RooArgSet],
                               filter_name:Optional[str]=None,
                               filter_client:Optional[str]=None,
                               fmt:str="pandas"):
    assert len(nuis_set) == len(constr_set)
    result = {}
    for nuis, constr in zip(nuis_set, constr_set):
        nuis_name = nuis.GetName()
        result[nuis_name] = get_systematic_variations_from_clients(nuis, constr)
    import pandas as pd
    data = []
    for nuis_name, client_results in result.items():
        for client_name, client_result in client_results.items():
            data.append({"name": nuis_name, "client": client_name, **client_result})
    df = pd.DataFrame(data)
    if filter_name is not None:
        df = df[df.apply(lambda x: fnmatch.fnmatch(x["name"], filter_name), axis=1)]
    if filter_client is not None:
        df = df[df.apply(lambda x: fnmatch.fnmatch(x["client"], filter_client), axis=1)]
    if fmt.lower() == "dict":
        df = df.set_index(["name", "client"])
        return {level: df.xs(level).to_dict('index') for level in df.index.levels[0]}
    if fmt.lower() == "pandas":
        return df
    raise ValueError(f'invalid output format "{fmt}" (choose between "dict" or "pandas")')
    
def decompose_nll(nll:"ROOT.RooRealSum", global_observables:"ROOT.RooArgSet", fmt:str="pandas"):
    nll_main_components = [component for component in nll.list()]
    data_terms = [component for component in nll_main_components if component.ClassName() == "RooNLLVar"]
    assert len(data_terms) > 0
    constr_terms = [component for component in nll_main_components if component.ClassName() == "RooConstraintSum"]
    result = {
        "name": [],
        "class": [],
        "type": [],
        "nll":[]
    }
    for data_term in data_terms:
        result["name"].append(data_term.GetName())
        result["class"].append(data_term.ClassName())
        result["type"].append("data")
        result["nll"].append(data_term.getVal())
    for constr_term in constr_terms:
        for constr_pdf in constr_term.list():
            result["name"].append(constr_pdf.GetName())
            result["class"].append(constr_pdf.ClassName())
            result["type"].append("constraint")
            result["nll"].append(-constr_pdf.getLogVal(global_observables))
    if fmt.lower() == "dict":
        return result
    if fmt.lower() == "pandas":
        import pandas as pd
        return pd.DataFrame(result)
    raise ValueError(f'invalid output format "{fmt}" (choose between "dict" or "pandas")')
    
def get_pdf_attributes(pdfs:"ROOT.RooArgSet", attributes, pdf_class=None, fmt:str="pandas"):
    import quickstats
    if not (quickstats.root_version >= (6, 26, 0)):
        raise RuntimeError("this method requires ROOT version > 6.26.0")
    results = []
    for pdf in pdfs:
        if (pdf_class is not None) and (not isinstance(pdf, pdf_class)):
            continue
        result = {}
        result["name"] = pdf.GetName()
        result["value"] = pdf.getVal()
        for attribute in attributes:
            getter_method_str = f"get{attribute}"
            if not hasattr(pdf, getter_method_str):
                raise ValueError(f"pdf {pdf.GetName()}(class = {pdf.Class()}) does not contain the method {getter_method_str}")
            variable = getattr(pdf, getter_method_str)()
            result[f"{attribute.lower()} (name)"] = variable.GetName()
            result[f"{attribute.lower()} (value)"] = variable.getVal()
        results.append(result)
    if fmt.lower == "dict":
        return results
    if fmt.lower() == "pandas":
        import pandas as pd
        return pd.DataFrame(results)
    raise ValueError(f'invalid output format "{fmt}" (choose between "dict" or "pandas")')
    
def get_gaussian_pdf_attributes(pdfs:"ROOT.RooArgSet", fmt:str="pandas"):
    return get_pdf_attributes(pdfs, ["X", "Mean", "Sigma"], ROOT.RooGaussian, fmt=fmt)

def get_poisson_pdf_attributes(pdfs:"ROOT.RooArgSet", fmt:str="pandas"):
    return get_pdf_attributes(pdfs, ["X", "Mean"], pdf_class=ROOT.RooPoisson, fmt=fmt)
    