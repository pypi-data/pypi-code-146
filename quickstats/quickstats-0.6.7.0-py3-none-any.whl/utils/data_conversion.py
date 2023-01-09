from typing import Union, Optional, Dict, List
import uuid

import numpy as np

root_datatypes = ["bool", "Bool_t", "Byte_t", "char", "char*", "Char_t", 
                  "double", "Double32_t", "Double_t", "float",
                  "Float16_t", "Float_t", "int", "Int_t", 
                  "long", "long long", "Long_t", "Long64_t",
                  "short", "Short_t", "Size_t", "UChar_t",
                  "UInt_t", "ULong64_t", "ULong_t",
                  "unsigned", "unsigned char", "unsigned int",
                  "unsigned long", "unsigned long long",
                  "unsigned short", "UShort_t"]

uproot_datatypes = ["double", "float", "int", "int64_t", "char*", "int32_t", "uint64_t"]

def get_default_library(custom_columns:bool=False):
    if custom_columns:
        return "root"
    try:
        import uproot
        has_uproot = True
        from packaging import version
        uproot_version = uproot.__version__
        if version.parse(uproot_version) < version.parse("4.2.0"):
            print("WARNING: uproot version too old (<4.2.0), will switch to using ROOT instead")
            has_uproot = False
    except ImportError:
        has_uproot = False
    if has_uproot:
        return "uproot"
    return "root"

def downcast_dataframe(df):
    import pandas as pd
    fcols = df.select_dtypes('float').columns
    icols = df.select_dtypes('integer').columns

    df[fcols] = df[fcols].apply(pd.to_numeric, downcast='float')
    df[icols] = df[icols].apply(pd.to_numeric, downcast='integer')

def array2root(array_data:Dict[str, np.ndarray], fname:str, treename:str,
               library:str="auto", multithread:bool=True):
    if library.lower() == "auto":
        library = get_default_library()
    if library == "root":
        from quickstats.interface.root.helper import RMultithreadEnv
        from quickstats.interface.cppyy.vectorize import np_type_str_maps
        with RMultithreadEnv(multithread):
            columns = list(array_data.keys())
            snapshot_templates = []
            for column in columns:
                template_type = np_type_str_maps.get(array_data[column].dtype, None)
                if template_type is None:
                    raise ValueError(f"unsupported array type \"{array_data[column].dtype}\""
                                     f" from the column \"{column}\"")
                if template_type == "bool":
                    template_type = "int"
                    array_data[column] = array_data[column].astype("int32")
                snapshot_templates.append(template_type)
            snapshot_templates = tuple(snapshot_templates)
            import ROOT
            df = ROOT.RDF.MakeNumpyDataFrame(array_data)
            df.Snapshot.__getitem__(snapshot_templates)(treename, fname, columns)
    elif library == "uproot":
        import uproot
        from packaging import version
        uproot_version = uproot.__version__
        if version.parse(uproot_version) < version.parse("4.2.0"):
            raise RuntimeError("uproot version too old (requires 4.2.0+)")
        file = uproot.recreate(fname)
        file[treename] = array_data
        file.close()
    else:
        raise RuntimeError(f'unknown library "{library}" for root data conversion')            
        
numpy2root = array2root

def dataframe2numpy(df:"pandas.DataFrame", columns:Optional[List[str]]=None):
    if columns is not None:
        arrays = dict(zip(columns, df[columns].to_numpy().T))
    else:
        arrays = dict(zip(df.columns.values, df.to_numpy().T))
    for column in arrays:
        arrays[column] = arrays[column].astype(df[column].dtype)
    return arrays 

def numpy2dataframe(array_data:Dict[str, np.ndarray]):
    array_shallow_copy = {**array_data}
    for key, array in array_data.items():
        if (array.ndim > 1) and (array.dtype != object):
            array_shallow_copy[key] = list(array)
    import pandas as pd
    df = pd.DataFrame(array_shallow_copy)
    return df

array2dataframe = numpy2dataframe

def dataframe2root(df:"pandas.DataFrame", fname:str, treename:str,
                   columns:Optional[List[str]]=None,
                   library:str="auto", multithread:bool=True):
    array_data = dataframe2numpy(df, columns)
    array2root(array_data, fname, treename, library=library,
               multithread=multithread)
    
def uproot_get_standard_columns(uproot_tree):
    typenames = uproot_tree.typenames()
    columns = list(typenames.keys())
    column_types = list(typenames.values())
    return np.array(columns)[np.where(np.isin(column_types, uproot_datatypes))]

def rdf2numpy(rdf, columns:Union[Dict[str, str], List[str]]=None,
              cut:Optional[str]=None, convert_vectors:bool=True,
              remove_non_standard_types:bool=True):
    if cut is not None:
        rdf = rdf.Filter(cut)     
    rename_columns = {}
    if columns is None:
        save_columns = [str(name) for name in rdf.GetColumnNames()]
    elif isinstance(columns, dict):
        save_columns = []
        for column_name, definition in columns.items():
            if column_name == definition:
                save_columns.append(column_name)
                continue
            if rdf.HasColumn(column_name):
                new_column_name = f"var_{uuid.uuid4().hex}"
                rename_columns[new_column_name] = column_name
                column_name = new_column_name
            rdf = rdf.Define(column_name, definition)
            save_columns.append(column_name)
    else:
        save_columns = list(columns)
    if remove_non_standard_types:
        column_types = np.array([rdf.GetColumnType(column_name) for column_name in save_columns])
        save_columns = list(np.array(save_columns)[np.where(np.isin(column_types, root_datatypes))])
        rename_columns = {k:v for k,v in rename_columns.items() if k in save_columns}
    vector_columns = []
    if convert_vectors:
        vector_columns_tmp = []
        for column_name in save_columns:
            column_type = rdf.GetColumnType(column_name)
            if column_type.count("ROOT::VecOps::RVec") == 1:
                vector_columns_tmp.append(column_name)
        if len(vector_columns_tmp) > 0:
            import quickstats
            quickstats.load_processor_methods()
            for column_name in vector_columns_tmp:
                new_column_name = f"var_{uuid.uuid4().hex}"
                if column_name in save_columns:
                    save_columns = [new_column_name if name == column_name else name for name in save_columns]
                # mapped twice
                if column_name in rename_columns:
                    rename_columns[new_column_name] = rename_columns.pop(column_name)
                else:
                    rename_columns[new_column_name] = column_name
                rdf = rdf.Define(new_column_name, f"RVec2Vec({column_name})")
                vector_columns.append(new_column_name)

    available_columns = [str(name) for name in rdf.GetColumnNames()]
    missing_columns = np.setdiff1d(save_columns, available_columns)
    if len(missing_columns) > 0:
        raise RuntimeError(f'missing column(s): {", ".join(missing_columns)}')
    result = rdf.AsNumpy(save_columns)
    for vector_column in vector_columns:
        # not the most efficient way, but easiest
        numpy_array = np.array([np.array(v.data()) for v in result[vector_column]], dtype=object)
        # in case it't array of regular size
        if len(numpy_array) and (numpy_array[0].dtype == object):
            result[vector_column] = np.array([np.array(v.data()) for v in result[vector_column]])
        else:
            result[vector_column] = numpy_array
    for old_column, new_column in rename_columns.items():
        result[new_column] = result.pop(old_column)
    # reorder the columns to match the order given by the user
    if columns is not None:
        result = {column: result[column] for column in columns if column in result}
    return result
    
def root2numpy(filename:Union[str, List[str]], treename:str,
               columns:Union[Dict[str, str], List[str]]=None,
               cut:Optional[str]=None, convert_vectors:bool=True,
               remove_non_standard_types:bool=True,
               library:str="auto"):
    if library.lower() == "auto":
        library = get_default_library(custom_columns=isinstance(columns,dict))
    if library.lower() == "root":
        import ROOT
        rdf = ROOT.RDataFrame(treename, filename)
        return rdf2numpy(rdf, columns=columns, cut=cut,
                         convert_vectors=convert_vectors,
                         remove_non_standard_types=remove_non_standard_types)
    elif library.lower() == "uproot":
        if isinstance(columns, dict):
            raise RuntimeError('defining new columns are not supported when using "uproot" as the library')
        import uproot
        if isinstance(filename, str):
            f = uproot.open(filename)
            t = f[treename]
            if remove_non_standard_types:
                standard_columns = uproot_get_standard_columns(t)
                if columns is None:
                    columns = standard_columns
                else:
                    columns = [column for column in columns if column in standard_columns]
            return f[treename].arrays(columns, library="numpy", cut=cut)
        else:
            # iterate over multiple files
            files = {f:treename for f in filename}
            if remove_non_standard_types:
                filter_typename = list(uproot_datatypes)
            else:
                filter_typename = None
            result = {}
            for batch in uproot.iterate(files, expressions=columns,
                                        filter_typename=filter_typename,
                                        cut=cut, library="numpy"):
                for column in batch:
                    if column not in result:
                        result[column] = batch[column]
                    else:
                        result[column] = np.concatenate([result[column], batch[column]])
            return result
    else:
        raise RuntimeError(f'unknown library "{library}" for root data conversion')

root2array = root2numpy
        
def root2dataframe(filename:Union[str, List[str]], treename:str,
                   columns:Union[Dict[str, str], List[str]]=None,
                   cut:Optional[str]=None,
                   remove_non_standard_types:bool=True,
                   downcast:bool=True,
                   library:str="auto"):
    if library.lower() == "auto":
        library = get_default_library(custom_columns=isinstance(columns,dict))
    if library.lower() == "root":
        numpy_data = root2numpy(filename, treename, columns=columns, cut=cut,
                                convert_vectors=True,
                                remove_non_standard_types=remove_non_standard_types,
                                library=library)
        result = numpy2dataframe(numpy_data)
    elif library.lower() == "uproot":
        if isinstance(columns, dict):
            raise RuntimeError('defining new columns are not supported when using "uproot" as the library')
        import uproot
        if isinstance(filename, str):
            f = uproot.open(filename)
            t = f[treename]
            if remove_non_standard_types:
                standard_columns = uproot_get_standard_columns(t)
                if columns is None:
                    columns = standard_columns
                else:
                    columns = [column for column in columns if column in standard_columns]
            result = f[treename].arrays(columns, library="pandas")
        else:
            import pandas as pd
            # iterate over multiple files
            files = {f:treename for f in filename}
            if remove_non_standard_types:
                filter_typename = list(uproot_datatypes)
            else:
                filter_typename = None
            result = None
            for batch in uproot.iterate(files, expressions=columns,
                                        filter_typename=filter_typename,
                                        cut=cut, library="pandas"):
                if result is None:
                    result = batch
                else:
                    result = pd.concat([result, batch])
    if downcast:
        downcast_dataframe(result)
    return result

def root2rdataset(filename:Union[str, List[str], "quickstats.PathManager"], treename:str,
                  observable:Union[str, dict, "ROOT.RooRealVar",
                                   "quickstats.interface.root.RooRealVar"],
                  weight_name:Optional[str]=None,
                  dataset_name:str="obsData"):
    from quickstats.components.modelling import TreeDataSource
    source = TreeDataSource(treename, filename, observable, weight_name)
    dataset = source.construct_dataset(dataset_name)
    return dataset

def rdataset2numpy(dataset:"ROOT.RooDataSet"):
    from quickstats.interface.root import RooDataSet
    return RooDataSet.to_numpy(dataset)

def rdataset2dataframe(dataset:"ROOT.RooDataSet"):
    from quickstats.interface.root import RooDataSet
    return RooDataSet.to_pandas(dataset)

def rdataset2hist(dataset:"ROOT.RooDataSet"):
    pass

def root2hist(filename:Union[str, List[str]], treename:str,
              column:str, bins:int=10, range:List[float]=None, weight_column:Optional[str]=None):
    pass