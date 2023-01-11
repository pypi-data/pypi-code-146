from typing import Literal, Union, List, Optional


DATA_TYPE = Literal['Boolean', 'Number', 'String', 'DateTime', 'Integer', 'List']
SECTION_TYPE = Literal['Object', 'Array', 'StaticArray']

class FieldData:
    id: int
    label: str
    value: Union[bool, int, None, str]
    type: DATA_TYPE

    def __init__(self, id: int, label: str, value: Union[bool, int, None, str], type: DATA_TYPE) -> None:
        self.id = id
        self.label = label
        self.value = value
        self.type = type

class RowData:
    fields: List[FieldData]
    id: int

    def __init__(self, variables: List[FieldData], id: int) -> None:
        self.fields = variables
        self.id = id

    def getFieldById(self, id: int) -> FieldData:
        """Returns the field with the given id, or None if not found
        
        Parameters
        ----------
        id: int
            Field id setup in Form Editor

        Returns
        -------
        FieldData when found, None otherwise

        """

        for field in self.fields:
            if field.id == id:
                return field
        
        return None

    def getFieldByLabel(self, label: str) -> FieldData:
        """Returns the field with the given label, or None if not found
        
        Parameters
        ----------
        label: str
            Field label setup in Form Editor

        Returns
        -------
        FieldData when found, None otherwise

        """

        for field in self.fields:
            if field.label == label:
                return field
        
        return None

class SectionData:
    sectionId: int
    sectionName: str
    sectionType: SECTION_TYPE
    fields: Optional[List[FieldData]]
    rows: List[RowData]

    def __init__(self, id: int, name: str, type: SECTION_TYPE, fields: Optional[List[FieldData]], rows: List[RowData]) -> None:
        self.sectionId = id
        self.sectionName = name
        self.sectionType = type
        self.fields = fields
        self.rows = rows

    def getFieldById(self, id: int) -> FieldData:
        """Returns the field with the given id, or None if not found
        
        Parameters
        ----------
        id: int
            Field id setup in Form Editor

        Returns
        -------
        FieldData when found, None otherwise

        """

        for field in self.fields:
            if field.id == id:
                return field
        
        return None

    def getFieldByLabel(self, label: str) -> FieldData:
        """Returns the field with the given label, or None if not found
        
        Parameters
        ----------
        label: str
            Field label setup in Form Editor

        Returns
        -------
        FieldData when found, None otherwise

        """

        for field in self.fields:
            if field.label == label:
                return field
        return None

    def getRow(self, row_number: int) -> RowData:
        """Returns the row with the given row number, or None if not found
        
        Parameters
        ----------
        id: int
            Row id

        Returns
        -------
        RowData when found, None otherwise

        """

        for row in self.rows:
            if row.id == row_number:
                return row

        return None
    
class FormData:
    sections: dict[int, SectionData]

    def __init__(self, sections: List[SectionData]) -> None:
        self.sections = sections

    def getSectionById(self, section_id: int):
        """Returns the first section with the given id
        At present, section id is unchangeble in Form Editor so this function is safer than getSectionByName

        Parameters
        ----------
        section_id: UUID
            Section Id (order) of the section in Form Editor

        Returns
        -------
        SectionData when found, None otherwise

        """

        if section_id not in self.sections:
            return None

        return self.sections[section_id]

    def getSectionByName(self, section_name: str):
        """Returns the first section with the given name
        Caution, changing section name in Form Editor will break this function

        Parameters
        ----------
        section_name: str
            Name of the section setup in Form Editor

        Returns
        -------
        SectionData when found, None otherwise

        """

        for section in self.sections.values():
            if section.sectionName == section_name:
                return section

        return None