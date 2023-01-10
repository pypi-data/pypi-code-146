import abc

from autoai_ts_libs.deps.tspy.data_structures.cross_language.Converters import Converters
from autoai_ts_libs.deps.tspy.data_structures.cross_language.JavaImplementations import JavaImplementations
from autoai_ts_libs.deps.tspy.data_structures.cross_language.Packages import Packages
from autoai_ts_libs.deps.tspy.data_structures.observations.TSBuilder import TSBuilder


class JavaBridge(object, metaclass=abc.ABCMeta):
    """a JavaBridge abstract class for Python code"""

    def __init__(self, tsc):
        self._tsc = tsc
        self._java_apis = None  # to be instantiated in `startJVM` API

    @abc.abstractmethod
    def startJVM(self, **kwargs):
        """start the jvm or set up the jvm"""
        pass

    @abc.abstractmethod
    def stopJVM(self):
        """stop the jvm"""
        pass

    @abc.abstractmethod
    def is_instance_of_java_class(self, obj, fully_qualified_class):
        """check if given object is an instance of the fully qualified class
        Parameters
        ----------
        obj
            python object
        fully_qualified_class : str
            fully qualified class name as a string

        Returns
        -------
        bool
            True if the obj is an instance of the given class, otherwise False
        """
        pass

    @abc.abstractmethod
    def is_java_obj(self, obj):
        """check if the given object is a JObject object"""
        pass

    @abc.abstractmethod
    def convert_to_primitive_java_array(self, values, type_in):
        """convert the python list to a primitive java array

        Parameters
        ----------
        values : list
            list of values
        type_in : type
            type of array to output

        Returns
        -------
        java primitive array
            a java primitive array
        """
        pass

    @abc.abstractmethod
    def convert_to_java_map(self, python_dict):
        """convert the python dict to a java HashMap"""
        pass

    @abc.abstractmethod
    def convert_to_java_list(self, python_list):
        """convert the python list to a java ArrayList"""
        pass

    @abc.abstractmethod
    def convert_to_java_set(self, python_list):
        """convert the python list to a java HashSet"""
        pass

    @abc.abstractmethod
    def cast_to_py_if_necessary(self, obj, obj_type=None):
        """cast the python object to java if necessary"""
        pass

    @abc.abstractmethod
    def cast_to_j_if_necessary(self, obj):
        """cast the java object to python if necessary"""
        pass

    @abc.abstractmethod
    def builder(self) -> TSBuilder:
        pass

    @property
    @abc.abstractmethod
    def converters(self) -> Converters:
        pass

    @property
    def java_implementations(self) -> JavaImplementations:
        """an implementation of a set of interfaces needed by the library

        Returns
        -------
        JavaImplementations
            a set of Java Implementations
        """
        return self._java_apis

    @property
    @abc.abstractmethod
    def package_root(self) -> Packages:
        """the root to all java packages needed for the library"""
        pass
