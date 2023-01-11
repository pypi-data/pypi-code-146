""" Classe principal que realiza o processo de mapeamento de dados e métodos para o ETL.
"""

from pandas import DataFrame

from .entity_base.entity_utils import EntityUtils

from .models.csv_file import CSVFile
from .models.xls_file import XLSFile
from .models.shape_file import ShapeFile
from .models.database_file import DatabaseFile
from .models.sql_file import SQLFile


class Entity(EntityUtils):
    """ Classe representativa da entidade.
    """
    csv_file = CSVFile()
    xls_file = XLSFile()
    shape_file = ShapeFile()
    database_file = DatabaseFile()
    sql_file = SQLFile()

    def extract(self, where:str="1=1"):
        """ Método que extrai os valores da entidade.
        """        
        if self.input["TYPE"] == "XLS":
            features, geometries, indexes = self.xls_file.extract(
                self.name, self.input, self.in_fields, self.spacial)
        elif self.input["TYPE"] == "CSV":
            raise NotImplementedError("Método ainda não implementado")
        elif self.input["TYPE"] == "SHAPE":
            raise NotImplementedError("Método ainda não implementado")
        elif self.input["TYPE"] == "DATABASE":
            features, geometries, indexes = self.database_file.extract(
                self.name, self.input, self.out_fields, self.spacial)
        elif self.input["TYPE"] == "SQL":
            features, geometries, indexes = self.sql_file.extract(
                self.name, self.input, self.in_fields, self.spacial, self.connection)
        else:
            raise NotImplementedError("Método ainda não implementado")

        dataframe = DataFrame(features, columns=self.out_fields, index=indexes)
        if self.spacial:
            dataframe.insert(loc=0, column="Shape@", value=geometries)
        self.values = dataframe

    def transform(self):
        """ Método que converte os valores da entidade de acordo com as regras de negócio.
        """
        for field in self.fields:
            self.values[field.get("CAMPO_SAIDA")] =\
                self.values[field.get("CAMPO_SAIDA")].apply(
                    lambda val: self.utils_service.convert_type(
                        val, field.get("TIPO"), field.get("CAMPO_SAIDA").startswith("ID")))

    def load(self, filter_index:tuple=None):
        """ Método que carrega os valores na saída de dados.
        """
        if filter_index is None or filter_index == self.indexes:
            values = self.values
        elif isinstance(filter_index, list) and len(filter_index):
            values = self.values.query("index in @filter_index")
        else:
            return

        if self.output["TYPE"] == "XLS":
            self.xls_file.charge(values, self.name, self.output_path, self.out_fields, self.spacial)
        elif self.output["TYPE"] == "CSV":
            raise NotImplementedError("Método ainda não implementado")
        elif self.output["TYPE"] == "SHAPE":
            raise NotImplementedError("Método ainda não implementado")
        elif self.output["TYPE"] == "DATABASE":
            self.database_file.charge(values, self.name, self.output_path, self.out_fields)
        else:
            raise NotImplementedError("Método ainda não implementado")

    def clear_output(self, where="1=1"):
        """ Método que limpa os registros da base de saida.
        """
        if self.output["TYPE"] == "XLS":
            raise NotImplementedError("Método ainda não implementado")
        elif self.output["TYPE"] == "CSV":
            raise NotImplementedError("Método ainda não implementado")
        elif self.output["TYPE"] == "SHAPE":
            raise NotImplementedError("Método ainda não implementado")
        elif self.output["TYPE"] == "DATABASE":
            self.database_file.clear(self.output_path, where)
        else:
            raise NotImplementedError("Método ainda não implementado")

    def apply_output(self, rules:list):
        """ Método que aplica modificações na base de saida.
        """
        if self.output["TYPE"] == "XLS":
            raise NotImplementedError("Método ainda não implementado")
        elif self.output["TYPE"] == "CSV":
            raise NotImplementedError("Método ainda não implementado")
        elif self.output["TYPE"] == "SHAPE":
            raise NotImplementedError("Método ainda não implementado")
        elif self.output["TYPE"] == "DATABASE":
            self.database_file.apply_edits(self.output_path, rules=rules)
        else:
            raise NotImplementedError("Método ainda não implementado")
