from looqbox.render.abstract_render import BaseRender
from looqbox.objects.looq_object import LooqObject
from looqbox.global_calling import GlobalCalling
from looqbox.json_encoder import JsonEncoder
from looqbox import ObjMessage
from pandas import DataFrame
import json
import os


class ObjSimpleTable(LooqObject):

    def __init__(self,
                 data: DataFrame = None,
                 metadata: dict = None,
                 rows: int = None,
                 null_as: int or str = None,
                 name: str = "objSimpleTable"):
        """
        Creates a table with minimal information

        :param data: Table content
        :param metadata: Metadata retrieved from query
        :param rows: Number of rows
        :param null_as: Value to replace None or NaN cells
        :param name: Object name
        """

        super().__init__()

        metadata = metadata or dict()
        null_as = null_as or "-"

        self.data = data
        self.name = name
        self.metadata = metadata
        self.rows = rows
        if self.rows is None and self.data is not None:
            self.rows = self.data.shape[0]
        self.null_as = null_as

        self.total = None

    def to_json_structure(self, visitor: BaseRender):
        return visitor.simple_table_render(self)


    @staticmethod
    def head_element_to_json(column, metadata):
        element = {
            "title": column,
            "dataIndex": column,
            "metadata":  metadata.get(column)
        }

        return element

    def build_head_content(self, table_data, metadata):
        return [self.head_element_to_json(column, metadata) for column in table_data]

    @staticmethod
    def build_body_content(table_data):
        return table_data.to_dict('records')

    def save_as(self, file_name: str, file_extension: str = "csv", file_path: str = None, dropna=True, **kwargs) -> ObjMessage:
        """
        Save SimpleTable data as a file

        @param file_path: file path to save the file
        @param file_name: Name to be saved as
        @param file_extension: Can be
            .csv: Comma-separated values
            .xlsx: Excel sheet
            .json: JSON string
            .txt: Tabular text
            .xml: XML document
        @return: String with filename and extention
        """

        if file_path is None:
            file_path = GlobalCalling.looq.entity_sync_path or ""

        if file_extension[0] != ".":
            file_extension = "." + file_extension

        file_path_with_name = os.path.join(
            file_path,
            file_name + file_extension
        )

        save_function_map = {
            ".csv": "to_csv({}, **kwargs)",
            ".xlsx": "to_excel({}, **kwargs)",
            ".json": "to_json({}, **kwargs)",
            ".txt": "to_string({}, **kwargs)",
            ".xml": "to_xml({}, **kwargs)"
        }

        function_args = '"{}"'.format(file_path_with_name)
        save_function = save_function_map.get(file_extension).format(function_args)

        save_function = "self.data." + save_function
        if dropna:
            self.data.dropna(inplace=True)
        self.data = escape_characters_in_pandas_dataframe(self.data)
        exec(save_function)
        replace_double_double_quotes_on_csv(file_path_with_name)

        return ObjMessage(file_name + file_extension, type="success")


def escape_characters_in_pandas_dataframe(dataframe: DataFrame, characters_to_escape: dict = None):
    """
    Escape characters in a pandas dataframe

    @param dataframe: Pandas dataframe
    @param characters_to_escape: Dict of characters to escape
    @return: Pandas dataframe
    """

    if not characters_to_escape:
        characters_to_escape = {
            '"': r'\"',
            ';': r'\;'
        }

    for column in dataframe.columns:
        escaped_values = []
        for value in dataframe[column].values:
            if isinstance(value, str):
                value = value.translate(str.maketrans(characters_to_escape))
            escaped_values.append(value)
        dataframe[column] = escaped_values

    return dataframe


def replace_double_double_quotes_on_csv(filename: str):
    """
    Replace double double quotes on CSV file
        "" -> "
    @param filename: CSV file name
    """

    with open(filename, 'r') as file:
        lines = file.readlines()
        file.close()

    with open(filename, 'w') as file:
        file.writelines([line.replace('""', '"') for line in lines])
        file.close()

