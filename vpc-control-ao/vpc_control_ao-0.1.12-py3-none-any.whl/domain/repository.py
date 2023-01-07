from typing import Dict
from ddd_objects.domain.repository import Repository
from .entity import CommandRequest, CommandItem
from .value_obj import CommandID

class CommandRepository(Repository):
    def get_queue_info(self)->Dict:
        raise NotImplementedError

    def send_request(self, request:CommandRequest)->CommandID:
        raise NotImplementedError
    
    def find_item(self, request_id: CommandID)->CommandItem:
        raise NotImplementedError
    
    def delete_item(self, request_id: CommandID)->bool:
        raise NotImplementedError