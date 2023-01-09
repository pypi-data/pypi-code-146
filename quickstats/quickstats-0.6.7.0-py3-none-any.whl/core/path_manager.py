from typing import Optional, Union, List, Dict, Tuple
import os

class DynamicFilePath:
    def __init__(self, basename:str, dirname:Optional[str]=None):
        self.dirname  = dirname
        self.basename = basename
        
    def resolve_basename(self, **parameters):
        return self.basename.format(**parameters)
        
class PathManager:
    
    @property
    def directories(self):
        return self._directories
    
    @directories.setter
    def directories(self, values:Optional[Dict[str, str]]=None):
        self._directories = self._parse_directories(values)
    
    @property
    def files(self):
        return self._files
    
    @files.setter
    def files(self, values:Optional[Union[Dict[str, Union[str, DynamicFilePath, Tuple[Optional[str], str]]],
                                    List[Union[str, DynamicFilePath, Tuple[Optional[str], str]]]]]=None):
        self._files = self._parse_files(values)
    
    def __init__(self, base_path:Optional[str]=None,
                 directories:Optional[Dict[str, str]]=None,
                 files:Optional[Union[Dict[str, Union[str, DynamicFilePath, Tuple[Optional[str], str]]],
                                List[Union[str, DynamicFilePath, Tuple[Optional[str], str]]]]]=None):
        self.base_path   = base_path
        self.directories = directories
        self.files       = files
    
    @staticmethod
    def _parse_directories(directories:Optional[Dict[str, str]]=None):
        if directories is None:
            new_directories = {}
        else:
            if not isinstance(directories, dict):
                raise TypeError("directories must be specified in dict format")
            for key, value in directories.items():
                if (not isinstance(key, str)) or (not isinstance(value, str)):
                    raise TypeError("directory key and value must be strings")
            # make a copy
            new_directories = {**directories}
        return new_directories
    
    @staticmethod
    def _parse_file_path(file_path:Union[str, DynamicFilePath, Tuple[Optional[str], str]]):
        if not isinstance(file_path, (str, tuple, DynamicFilePath)):
            raise TypeError("file path must be a tuple/string/DynamicFilePath")
        if isinstance(file_path, tuple):
            if len(file_path) != 2:
                raise ValueError("a tuple file path format must have a size of two in the form (dirname, basename)")
            return DynamicFilePath(file_path[1], file_path[0])
        elif isinstance(file_path, str):
            return DynamicFilePath(file_path, None)
        elif isinstance(file_path, DynamicFilePath):
            return file_path
        else:
            raise TypeError("unknown file path format")    
    
    @staticmethod
    def _parse_files(files:Optional[Union[Dict[str, Union[str, DynamicFilePath, Tuple[Optional[str], str]]],
                                    List[Union[str, DynamicFilePath, Tuple[Optional[str], str]]]]]=None):
        if files is None:
            new_files = {}
        else:
            if isinstance(files, str):
                files = [files]
            if isinstance(files, list):
                files = {str(i):value for i, value in enumerate(files)}
            if not isinstance(files, dict):
                raise TypeError("files must be specified in dict format")
            new_files = {}
            for key, value in files.items():
                if not isinstance(key, str):
                    raise TypeError("file name must be a string")
                file = PathManager._parse_file_path(value)
                new_files[key] = file
        return new_files
        
    def update_directories(self, directories:Optional[Dict[str, str]]=None):
        new_directories = self._parse_directories(directories)
        self._directories.update(new_directories)
        
    def update_files(self, files:Optional[Dict[str, Union[str, DynamicFilePath, Tuple[Optional[str], str]]]]=None):
        new_files = self._parse_files(files)
        self._files.update(new_files)
        
    def set_directory(self, directory_name:str, path:str, absolute:bool=False):
        if absolute:
            path = os.path.abspath(path)
        self.update_directories({directory_name: path})
        
    def set_file(self, file_name:str, file:Union[str, DynamicFilePath, Tuple[Optional[str], str]]):
        self.update_files({file_name: file})
        
    def get_directory(self, directory_name:str, check_exist:bool=False):
        if directory_name not in self.directories:
            raise KeyError(f'unrecognized directory name "{directory_name}"')
        if self.base_path is not None:
            return os.path.join(self.base_path, self.directories[directory_name])
        directory = self.directories[directory_name]
        if check_exist:
            if not os.path.exists(directory):
                raise FileNotFoundError(f'directory "{directory}" does not exist')
        return directory
    
    def get_resolved_file(self, file_name:str, check_exist:bool=False,
                          subdirectory:Optional[str]=None, **parameters):
        if file_name not in self.files:
            raise KeyError(f'unrecognized file name "{file_name}"')
        file = self.files[file_name]
        if parameters:
            basename = file.resolve_basename(**parameters)
        else:
            basename = file.basename
        if subdirectory is None:
            subdirectory = ""
        if file.dirname is not None:
            dirname  = self.get_directory(file.dirname)
            fullname = os.path.join(dirname, subdirectory, basename)
        else:
            if self.base_path is not None:
                fullname = os.path.join(self.base_path, subdirectory, basename)
            else:
                fullname = os.path.join(subdirectory, basename)
        if check_exist:
            if not os.path.exists(fullname):
                raise FileNotFoundError(f'file "{fullname}" does not exist')
        return fullname
    
    def get_file(self, file_name:str, check_exist:bool=False):
        return self.get_resolved_file(file_name, check_exist=check_exist)
    
    def get_directories(self, directory_names:Optional[List[str]]=None):
        directory_paths = {}
        if directory_names is None:
            directory_names = list(self.directories.keys())
        for directory_name in directory_names:
            directory_paths[directory_name] = self.get_directory(directory_name)
        return directory_paths
    
    def get_files(self, file_names:Optional[List[str]]=None):
        file_paths = {}
        if file_names is None:
            file_names = list(self.files.keys())
        for file_name in file_names:
            file_paths[file_name] = self.get_file(file_name)
        return file_paths
    
    def get_relpath(self, path:str):
        if self.base_path is None:
            return path
        return os.path.join(self.base_path, path)
    
    def directory_exists(self, directory_name:str):
        directory = self.get_directory(directory_name)
        return os.path.exists(directory)
    
    def file_exists(self, file_name:str, **parameters):
        file = self.get_resolved_file(file_name, **parameters)
        return os.path.exists(file)
    
    def check_directory(self, directory_name:str):
        self.get_directory(directory_name, check_exist=True)
            
    def check_file(self, file_name:str, **parameters):
        self.get_resolved_file(file_name, check_exist=True, **parameters)
    
    def makedirs(self, include_names:Optional[List[str]]=None,
                 exclude_names:Optional[List[str]]=None):
        if include_names is None:
            include_names = list(self.directories.keys())
        if exclude_names is None:
            exclude_names = []
        directory_names = list(set(include_names) - set(exclude_names))
        for directory_name in directory_names:
            if directory_name not in self.directories:
                raise KeyError(f'unrecognized directory name "{directory_name}"')
            dirname = self.get_directory(directory_name)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
    
    def makedir_for_files(self, file_names:Union[str, List[str]]):
        if isinstance(file_names, str):
            file_names = [file_names]
        files = self.get_files(file_names)
        for file in files.values():
            dirname = os.path.dirname(file)
            if (dirname != "") and not os.path.exists(dirname):
                os.makedirs(dirname)