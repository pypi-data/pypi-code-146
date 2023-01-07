from typing import Dict
from ddd_objects.infrastructure.repository_impl import RepositoryImpl
from ..domain.repository import CommandRepository
from .ao import VPCController
from ..settings import vpc_ip, vpc_port, vpc_token
from ..domain.entity import CommandRequest, CommandItem
from ..domain.value_obj import CommandID
from .converter import command_request_converter, command_item_converter

vpc_ao = VPCController(vpc_ip, vpc_port, vpc_token)
class CommandRepositoryImpl(CommandRepository, RepositoryImpl):
    def get_queue_info(self)->Dict:
        return vpc_ao.get_command_queue_info()
    
    def send_request(self, request: CommandRequest) -> CommandID:
        request = command_request_converter.to_do(request)
        request_id = vpc_ao.send_command_request(request)
        return CommandID(request_id)
    
    def find_item(self, request_id: CommandID) -> CommandItem:
        request_id = request_id.get_value()
        item = vpc_ao.find_command_item(request_id)
        return command_item_converter.to_entity(item)
command_repo = CommandRepositoryImpl()
