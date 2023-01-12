from typing import List, Optional
from pydantic import BaseModel


class UIPortGroupParams(BaseModel):
    """UI port logic for port group
    :param id_: port_group_id
    :param show_ports: show port panels
    :param can_add: can add new port to group
    :param can_delete: can delete port from group
    :param can_move: can move port inside group
    :param can_hide: can hide port
    :param can_set_type: can set porttype to port
    :param has_code: has editable code field
    :param has_special: has special binary switch
    :param has_required: has required binary switch
    :param copy_name_from_code: copy port name from code field when code edting
    :param group_title: visual title for port group
    :param special_title: title|tooltip for special
    :param code_title: title|tooltip for code
    :param copy_from_group: port group name
    :param ports_generator_callback_name: name of callback for port generator
    :param ports_validator_callback_name: name of callback for port code validation
    :param valid_types: valid types for ports in this group
    """
    id_: str = ''  # port_group_id
    show_ports: bool = True  # show port panels
    can_add: bool = False  # can add new port to group
    can_delete: bool = False  # can add delete port from group
    can_move: bool = False  # can move port inside group
    can_hide: bool = False  # can hide port
    can_set_type: bool = True  # can set porttype to port
    has_code: bool = False  # has editable code field
    has_special: bool = False  # has special binary switch
    has_required: bool = False  # has required binary switch
    copy_name_from_code: bool = True  # copy port name from code field when code edting
    group_title: Optional[str]  # visual title for port group
    special_title: Optional[str]  # title|tooltip for special
    code_title: Optional[str]  # title|tooltip for code
    copy_from_group: Optional[str]  # port group name
    ports_generator_callback_name: Optional[str]
    ports_validator_callback_name: Optional[str]
    valid_types: List[str] = []


class UIParams(BaseModel):
    """UI parameters for node UI port logic
    """
    inputs: UIPortGroupParams = UIPortGroupParams(id_='inputs')
    outputs: UIPortGroupParams = UIPortGroupParams(id_='outputs')
    input_groups: List[UIPortGroupParams] = []
    output_groups: List[UIPortGroupParams] = []


class DestructurerUIParams(UIParams):
    """Destructurer UI port logic
    """
    inputs = UIPortGroupParams(id_='inputs', show_ports=False)
    outputs = UIPortGroupParams(
        id_='outputs',
        has_code=True,
        has_required=True,
        can_hide=True,
        has_special=True,
        code_title='field name',  # noqa: F722
        special_title='use jspath'  # noqa: F722
    )


class StructurerUIParams(UIParams):
    """Structurer UI port logic
    """
    inputs = UIPortGroupParams(
        id_='inputs',
        has_code=True,
        has_required=True,
        can_hide=True,
        has_special=True,
        code_title='field name',  # noqa: F722
        special_title='use jspath'  # noqa: F722
    )
    outputs = UIPortGroupParams(id_='outputs', show_ports=False)
