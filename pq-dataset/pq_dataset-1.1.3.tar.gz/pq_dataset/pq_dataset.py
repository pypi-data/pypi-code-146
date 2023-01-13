from datetime import datetime
import logging
import pandas as pd
from pathlib import Path
from zipfile import ZipFile
import pyarrow.parquet as pq
import shutil
import os
import codecs
import json
import re
from lxml import etree as et
from typing import List

# Module specific functions

from pq_dataset.utils.extract_calculated_from_report_spec import extract_calculated_from_report_spec
from pq_dataset.utils.generate_variable_overview import generate_variable_overview
from pq_dataset import room_specific_config as room_config

class PQDataset:
    """A class making it easier to work with dataset from H&H
    
    Attributes
    ----------
    analysis_id: int
        The analysis id of the data from SX.
    file_type: str
        Source of the data file - at this time 'csv_vukvo' or 'parquet' are allowed formats.
        Files should be named either [analysid_id].[csv|parquet]
    input_path: str
        Path of the input files (datasets, json strings with grapql export etc.)
    output_path: str
        Path of the output_path files generated
    room_id: int
        The source of the datasets - 
        429, 729 or 999999 are valid entries. 999999 indicates non-H&H Results room. 
    predaycare: bool, default: False
        If this is aplied only cases from predaycare (Sundhedsplejen) is included in the data, which speeds up things considerably
    relevant_scopes: List[str]
        List of strings matching scopes or parts of scopes. Every variable matching the string will be included in the dataframe. 
        E.g. 'background__ptype' includes every ptype variable
    relevant_variables: List[str]
        List of variables to be included in the dataframe
        
    Output
    ------
    When initiated this class adds two dataframes to the class.
    .data which holds the data as a pandas dataframe
    .var_overview which holds a variable overview of the full dataset
    
    E.g. 'sprog = PQDataset()' allows for sprog.data and sprog.var_overview to be called
    
    Methods
    -------
    The class have the following methods which can be called
    
    .clients_only(): Returns a dataset which only contains clients data - the selection depends on the room (491 or 729)
    .identify_relevante_data_ftp(): Allows for identifying which variables are relevant for data which are to be made avaiable for our clients
    .create_json_ftp_config(): 
    
    Config
    ------
    The file room_specific_config.py holds basic configuration for each of the allowed Results rooms
   
    
    """
    
    def __init__(self, 
                 analysis_id: int, 
                 file_type: str, 
                 input_path: str, 
                 output_path: str, 
                 room_id: int, 
                 predaycare: bool = False, 
                 relevant_scopes: List[str] = [],
                 relevant_variables: List[str] = []
                 ):
        
        self.accepted_file_types = ['csv_vukvo', 'parquet']
        self.file_extensions = ['csv', 'zip']
        self.accepted_rooms = [491, 729, 999999]
        
        self.relevant_scopes = relevant_scopes
        self.relevant_variables = relevant_variables
        self.file_type = file_type
        self.analysis_id = analysis_id
        self.input_path = input_path
        self.output_path = output_path
        self.room_id = room_id
        self.predaycare = predaycare
        
        self.byte_decoded = True
        
        # Adding filehandler to root logger - move to function
        self.logger = logging.getLogger()

        log_path = f'{self.output_path}{os.path.sep}logging'
        
        if not Path(log_path).exists():
            os.makedirs(log_path)
        
        logfile_name = f'{log_path}{os.path.sep}{datetime.today().strftime("%Y-%m-%d")}_{self.analysis_id}.log'
        file_handler = logging.FileHandler(logfile_name)
        file_handler.setLevel(logging.DEBUG)
        file_handler_format = '%(asctime)s | %(levelname)s | %(lineno)d: %(message)s'
        file_handler.setFormatter(logging.Formatter(file_handler_format))
        self.logger.addHandler(file_handler)
        
        # self.__logging_setup()
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f'Started preparing data from analysisid {self.analysis_id}')
       
        if not self.__validate_inputs():
            
            exit()
        
        self.config = room_config.setup_config(self.room_id)

        self.data, self.var_overview = self.__load_data()
        
        self.data = self.__clean_up_columns()
        
        if self.file_type == 'parquet':
            
            self.data = self.__unencode_byte_strings_parquet('Initial')
        
        self.data = self.__rename_columns()
        
        self.logger.info(f'Done preparing data from analysisid {self.analysis_id}. You can access the dataframe by appending .data to the \
            object that you created - i.e. barnbg.data')
  
    def __load_data(self) -> pd.DataFrame:
        
        def load_data_csv(csv_file: str) -> pd.DataFrame:
            
            df = pd.read_csv(csv_file, encoding='utf-8-sig', sep=';', decimal=',', low_memory=False)
            
            self.logger.debug(f'load_data_csv loaded csv file containing {df.shape[0]} cases and {df.shape[1]} columns')
            
            return df
        
        def load_data_parquet(parquet_file: str, col_list: List[str] = []) -> pd.DataFrame:
            
            os.chdir(Path(self.input_path))
            
            only_file_name = parquet_file.rsplit('\\', 1)[-1]
            
            with ZipFile(only_file_name, 'r') as zipObj:
                zipObj.extractall('temp_parq')

            # Reading parquet data and converting it to a pandas dataframe
            
            file_dir = Path.cwd() / 'temp_parq'

            dataset = pq.ParquetDataset(file_dir)
            
            if col_list:
                table = dataset.read(columns=col_list)
            else:
                table = dataset.read()
                
            df = table.to_pandas()

            # # Removing unzipped files and folder

            if Path(file_dir).exists():
                self.logger.debug(f'Deleting temporary folder incl. files: {file_dir}')
                shutil.rmtree(file_dir)    

            self.logger.debug(f'load_data_parquet loaded parquet file containing {df.shape[0]} cases and {df.shape[1]} columns')

            return df

        def clean_root_data(df: pd.DataFrame, root_variable: List[str]) -> pd.DataFrame:
            
            query_string_temp = [f'`{var}`.notnull()' for var in root_variable]
                
            query_string = ' and '. join(query_string_temp)
                
            try:
                df2 = df.query(query_string)
            except KeyError: 
                self.logger.debug('clean_root_data tried to filter df, but variable does not exist')
                return df
            
            self.logger.debug(f'clean_root_data removed {df.shape[0] - df2.shape[0]} cases from dataframe')
               
            return df2
        
        def return_relevant_cols(var_overview: pd.DataFrame, relevant_scopes: List[str], relevant_variables: List[str]) -> List[str]:
            
            relevant_cols = []
            
            # Append variables under the relevant scope to relevant_cols
            if relevant_scopes:
                relevant_cols = [col for col in var_overview.adj_name.to_list() for scope in relevant_scopes if col.startswith(scope)]

            # Appending individual variables
            if relevant_variables:
                for variable in relevant_variables:
                    if not variable in var_overview.adj_name.to_list():
                        self.logger.warning(f'The variable {variable} was not found in dataset. This indicates an error in the specification of relevant_variables')
                    else:
                        relevant_cols.append(variable)
            
            variable_map = dict(zip(var_overview.adj_name.to_list(), var_overview.reference.to_list()))
            relevant_cols_varreference = [variable_map[col] for col in relevant_cols]
            
            return relevant_cols_varreference
        
        file_name = self.__parse_file_specification()
        root_ptype = self.__return_config_parameter('root_variable')
        
        # This is dumb - should be changed 
        
        if self.file_type == 'csv_vukvo':
            df = load_data_csv(file_name)
            variable_overview = generate_variable_overview(self.input_path, self.analysis_id)            
            if root_ptype:
                df = clean_root_data(df, root_ptype)
            
        elif self.file_type == 'parquet':
            variable_overview = generate_variable_overview(self.input_path, self.analysis_id)
            if self.relevant_scopes or self.relevant_variables:
                variable_overview_reduced = variable_overview.query('referenceType != "TypeChoiceSingle"')
                relevant_cols = return_relevant_cols(variable_overview_reduced, self.relevant_scopes, self.relevant_variables)
            else:
                relevant_cols = []
            
            # Temp
            variable_overview_reduced.to_excel('barnbg_var_overview.xlsx')
            
            df = load_data_parquet(file_name, col_list=relevant_cols)
            # Renaming columnnames based on variable overview
            colnames_dict = dict(zip(variable_overview.reference, variable_overview.fullName))
            df.rename(columns=colnames_dict, inplace=True)
            if root_ptype:
                df = clean_root_data(df, root_ptype)
            
        else:
            
            exit()
            
        if self.predaycare and self.room_id == 491:
            df = df.query('`background/ptype133`.notnull()')                    

        return df, variable_overview

    def __clean_up_columns(self) -> pd.DataFrame:
        
        self.logger.debug(f'__clean_up_columns: Starting')
        # Drops all columns where all values are null/nan
        df = self.data.dropna(how='all', axis=1)
        self.logger.debug(f'__clean_up_columns: step 1')
        # Drops all columns which only contains 0's - multiple choice variables
        df = df.loc[:, (df != 0).any(axis=0)]
        self.logger.debug(f'__clean_up_columns: step 2')
        # Test of unique values in each column
        nb_unique = df.apply(pd.Series.nunique) 
        static_cols = nb_unique[nb_unique==1].index # Cols containing only one value - though NANs as well
        columns_with_nan = df.columns[df.isna().any()].tolist()
        possible_cols = [col for col in static_cols if col not in columns_with_nan]
        self.logger.debug(f'__clean_up_columns: step 3')
        # Close your eyes... this is ugly!
        remove_these_cols = []

        for col in possible_cols:
            if col.startswith('background/ptype') and col.endswith('t'):
                if possible_cols.count(col[:-1]) == 1:
                    remove_these_cols.append(col[:-1])
                    remove_these_cols.append(col)
        self.logger.debug(f'__clean_up_columns: step 4')

        df2 = df.drop(columns=remove_these_cols)

        self.logger.debug(f'__clean_up_columns removed {len(self.data.columns) - len(df2.columns)} columns')

        return df2
    
    def __reduce_columns_based_on_input(self,
                                        dataframe,
                                        relevant_scopes: List[str] = [], 
                                        relevant_variables: List[str] = [],
                                        include_cpr: bool = True
                                        ) -> pd.DataFrame:
    
        def validate_inputs(existing_columns: List[str], 
                            relevant_scopes: List[str], 
                            relevant_variables: List[str] = []) -> None:
            
            for scope in relevant_scopes:
                nb_cols_with_scope = [col for col in existing_columns if col.startswith(scope)]
                
                if len(nb_cols_with_scope) == 0:
                    self.logger.warning(f'No columns were found starting with {scope}. This indicates an error in the specification of relevant_scopes')
            
            if relevant_variables:
                for variable in relevant_variables:
                    if not variable in existing_columns:
                        self.logger.warning(f'The variable {variable} was not found in dataset. This indicates an error in the specification of relevant_variables')
                        
            return None
               
        validate_inputs(dataframe.columns, relevant_scopes, relevant_variables)
        
        relevant_cols = []
        
        # Only select the variable scopes defined in relevant_scopes
        relevant_cols = [col for col in dataframe.columns for scope in relevant_scopes if col.startswith(scope)]
        
        if include_cpr:
            cpr_var = self.__return_config_parameter('cpr_variable')
            if cpr_var:
                relevant_cols.extend(self.__return_config_parameter('cpr_variable')[0])

        # Appending individual variables
        if relevant_variables:
            relevant_cols.extend(relevant_variables)
        
        # Appending variables which should always be included
        for variable in self.__return_config_parameter('must_include_variables'):
            relevant_cols.append(variable)

        if self.config.get('closed_ptype_variable') in relevant_cols:
            relevant_cols.remove(self.__return_config_parameter('closed_ptype_variable')[0])

        # Adding room specific variables to be indcluded in dataset
        relevant_cols.extend(self.__return_config_parameter('room_specific_variables'))

        # Reducing number of columns in dataframe
        dataframe = dataframe[[col for col in dataframe.columns if col in relevant_cols]]
        
        return dataframe
    
    def __unencode_byte_strings_parquet(self, context: str, df: pd.DataFrame = None) -> pd.DataFrame:
        
        def byte_columns_are_decoded(df: pd.DataFrame = None) -> bool:
            
            # Returns a boolean series of the first object column with an indication of whether or not the column contains byte strings
            first_object_column = df.select_dtypes(include='object').iloc[:,0].apply(type) != bytes
            # Returns False if first_object_column contains at least one byte encoded string - else True
            return first_object_column.all()
        
        def size_of_dataframe_suitable_for_decoding(df: pd.DataFrame = None) -> bool:
                
            # Calculating size of dataframe and skipping decode of byte strings if it is larger than 10M cells.
            objects_size = (str_df.shape[0] * str_df.shape[1])/1000000
            
            self.logger.debug(f'The size of objects columns/rows are {str_df.shape[0] * str_df.shape[1]}')
            
            if objects_size > 30:
                self.logger.debug(f'Size of objects columns/rows deemed too large - decoding skipped')
                return False
            
            return True
        
        #Rewrite
        
        if context == 'Initial':
        
            df = self.data
        
        elif context == 'FTP':
            
            df = self.data_ftp
        
        elif context == 'df_included':
            
            df = df.copy()

        else:
            
            self.logger.critical(f'Context for unencode_byte_strings is unknown')
            
            exit()
            
        # Creating df consising of only object columns
        str_df = df.select_dtypes([object])            
            
        if byte_columns_are_decoded(str_df):
            return df
        
        if not size_of_dataframe_suitable_for_decoding(str_df):
            return df

        # Decoding byte encoded columns
        str_df = str_df.stack().str.decode('utf-8').unstack()
            
        for col in str_df:
            df[col] = str_df[col]
                
        self.logger.debug(f'Converted parquet byte encoded strings to regular strings')

        return df

    def __rename_columns(self) -> pd.DataFrame:
        
        df_temp = self.data.rename(columns=lambda x: re.sub('(\/)','__',x))
        
        df_temp.columns = map(str.lower, df_temp.columns)
 
        return df_temp

    def __parse_file_specification(self) -> str:
        
        file_extention = f'{self.file_extensions[self.accepted_file_types.index(self.file_type)]}' 
        file_name = f'{str(self.analysis_id)}.{file_extention}' 
        file_path = f'{self.input_path}\{file_name}'
        
        return file_path
   
    def __validate_inputs(self) -> bool:
        
        valid_input = True
       
        if self.file_type not in self.accepted_file_types:
            
            self.logger.critical(f'{self.file_type} is not an accepted file type. Allowed types are: {", ".join(self.accepted_file_types)}')            
            valid_input = False
            return valid_input
        
        if type(self.analysis_id) != int:
            
            valid_input = False            
            self.logger.critical(f'analysis_id should be int - not {type(self.analysis_id)}')
            
        if not Path(self.input_path).exists():
            
            valid_input = False            
            self.logger.critical(f'The path {self.input_path} does not exist.')

            return valid_input
        
        # Setting filename
        
        file_name = self.__parse_file_specification()
            
        if not Path(file_name).exists():
            
            valid_input = False
            self.logger.critical(f'{file_name} is not a valid file path.')

        # Checking if json config is avaiable

        file_name = f'{file_name.split(".", 1)[0]}.json'

        if not Path(file_name).exists() and self.file_type=='parquet':
            
            valid_input = False
            self.logger.critical(f'When parsing parquet files a .json file with variable information is required.')
            
        if not self.room_id in self.accepted_rooms:
            
            valid_input = False
            self.logger.critical(f'Unknown room id {self.room_id}')
        
        return valid_input
    
    def __return_config_parameter(self, parameter_name: str) -> List[str]:
        return self.config.get(parameter_name)    
    
    def clean_up_data(self,
                      clients_only: bool = True,
                      remove_testareas: bool = True,
                      remove_archive: bool = False,
                      relevant_scopes: List[str] = [],
                      relevant_variables: List[str] = []) -> pd.DataFrame:
        """Missing description
        
        
        
        
        """
        
        def general_setup_check(df: pd.DataFrame, parameter_bool: bool, parameter_variables: List[str]) -> bool:

            parameter_should_be_included_in_query = True
            
            if not parameter_bool:
                self.logger.debug(f'clean_up_data: Skipping parameter as it is false')
                parameter_should_be_included_in_query = False
                return parameter_should_be_included_in_query
            
            if not parameter_variables:
                self.logger.debug(f'clean_up_data: List of variables is empty')
                parameter_should_be_included_in_query = False
                return parameter_should_be_included_in_query
            
            variables_in_df = [var for var in parameter_variables if var in df.columns]
            
            if not variables_in_df:
                self.logger.debug(f'clean_up_data: None of the variables supplied is present in dataframe')                
                parameter_should_be_included_in_query = False
                return parameter_should_be_included_in_query
            
            return parameter_should_be_included_in_query
       
        def parse_testarea_setup(df: pd.DataFrame, remove_testareas: bool, testarea_variables: List[str]) -> str:
            
            if general_setup_check(df, remove_testareas, testarea_variables):
                
                testarea_variables_reduced = [var for var in testarea_variables if var in df.columns]
                
                if not self.byte_decoded:
                    for col in testarea_variables_reduced:
                        df[col] = df[col].str.decode('utf-8')        

                testarea_variables_queries = [f'not({col}.str.startswith("*Test", na=False).values)' for col in testarea_variables_reduced]
                
                testarea_query = ' and '.join(testarea_variables_queries)
                        
                return testarea_query
            
            return None             
        
        def parse_archive_setup(df: pd.DataFrame, remove_archive: bool, archive_variables: List[str]) -> str:
            
            if general_setup_check(df, remove_archive, archive_variables):
                
                archive_variables_reduced = [var for var in archive_variables if var in df.columns]
                archive_queries = [f'{var}.isnull()' for var in archive_variables_reduced if var in df.columns]
                
                archive_query = ' and '.join(archive_queries)
                
                return archive_query
            
            return None

        query_string_total  = []
        archive_variables = self.__return_config_parameter('archive_variables')
        testarea_variables = self.__return_config_parameter('testarea_variables')
        
        df = self.data
        
        if self.file_type == 'parquet':
            df = self.__unencode_byte_strings_parquet('df_included', df)

        if clients_only:
            clients_query = self.__return_config_parameter('clients_query')
            if clients_query:
                query_string_total.append(f'{clients_query[0]}')
            
        if parse_archive_setup(df, remove_archive, archive_variables):
            query_string_total.append(f'({parse_archive_setup(df, remove_archive, archive_variables)})')

        if parse_testarea_setup(df, remove_testareas, testarea_variables):
            query_string_total.append(f'({(parse_testarea_setup(df, remove_testareas, testarea_variables))})')

        if query_string_total:
            query_string_total_str = ' and '.join(query_string_total)
            df_temp = df.query(f'{query_string_total_str}', engine='python')
        else:
            df_temp = df

        if relevant_scopes or relevant_variables:
            df_temp = self.__reduce_columns_based_on_input(df_temp, relevant_scopes, relevant_variables)

        if self.file_type == 'parquet':
            df_temp = self.__unencode_byte_strings_parquet('df_included', df_temp)

        return df_temp
    
    def identify_relevante_data_ftp(self, 
                                    reduced_data: pd.DataFrame = None, 
                                    relevant_scopes: List[str] = ['background__ptype', 'questionnaire__'],
                                    relevant_variables: List[str] = [],
                                    include_cpr: bool = True,
                                    include_calculated_from_report: str = '',
                                    save_variable_overview: bool = True,
                                    save_ai_json_config: List[str] = []
                                    ) -> None:
        """Prepares and returns client relevant dataset (pandas dataframe) and variables. 
        
        Parameters
        ----------
        reduced_data : pd.DataFrame, optional (default=None)
            Useful if 
        relevant_scopes : List[str], optional (default=[background__ptype] and [questionnaire__])
            Specifies which scopes should be included. If not specified then [background__ptype] and [questionnaire__] scope is included.
        relevant_variables : List[str], optional (default=None)
            Specifies which specfic variables should be included. This is used if only certain variables from a specific scope are relevant
        include_cpr : bool, optional (default=True)
            Whether or not to include cpr
        include_calculated_from_report : str, optional (default=None)
            This is useful for a 'automated' mode for indentifying relevant variables. The supplied string should be the name of the file with the xml config of the relevant report. In most cases this would be the report on child level and not aggregated.
        save_variable_overview : bool, optional (default=True)
            Whether or not an excel-file with a description of the included variables should be saved.  
        
        """

        if reduced_data is None:
            df = self.data
        else:
            df = reduced_data

        if include_calculated_from_report:
            used_calc_vars = extract_calculated_from_report_spec(self.input_path, include_calculated_from_report, self.analysis_id, self.var_overview, self.logger)
            relevant_variables.extend(used_calc_vars)

        df = self.__reduce_columns_based_on_input(df, relevant_scopes, relevant_variables)
        
        self.data_ftp = df

        # Decoding byte encoded columns
        if self.file_type == 'parquet':
            self.__unencode_byte_strings_parquet('FTP')
        
        self.var_overview_reduced = self.var_overview[self.var_overview['adj_name'].isin(self.data_ftp.columns)]
        
        if save_variable_overview:
            file_name = f'{self.analysis_id}_variabel_beskrivelse.xlsx'
            file_path = f'{self.output_path}\{file_name}'
            relevant_cols = ['fullName', 'name', 'referenceType', 'text', 'choice_value']
            self.var_overview_reduced[relevant_cols].to_excel(file_path, index=False)
            self.logger.info(f'Saved description of variables to be transferred to ftp as {file_path}')
        
        return None
        
    def create_json_ftp_config(self, name: str, ftp_path: str) -> None:
        
        json_output = {'name': name,
                    'analysisId': self.analysis_id,
                    'output_path': ftp_path,
                    'variables': []
                    }

        for index, row in self.var_overview_reduced.iterrows():
            if row['referenceType'] == 'TypeChoiceSingle':
                continue
            json_output['variables'].append({'reference':row['reference'], 'displayName':row['adj_name']})

        file_name = f'{self.analysis_id}_ftp_config.json'

        json_output_file = self.output_path + os.path.sep + file_name

        with codecs.open(json_output_file,'w','UTF-8-SIG') as outfile:
            json.dump(json_output, outfile, indent=4)
            
        print(f'Json file saved as {file_name} in {self.output_path}')

        return None