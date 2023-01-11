from typing import List, Union

from .perception import Perception


class Message(Perception):
    '''
    This class specifies a wrapper for a message that is sent to a multiple recipients, and its metadata.

    * The content is specified by the `content` field. This field's type is `Union[int, float, str, bytes, list, tuple, dict]`.
    * The recipients are specified by the `recipient_ids` field. This field's type is `List[str]`.
    * The sender is specified by the `sender_id` field. This field's type is `str`.
    '''
    def __init__(self, content: Union[int, float, str, bytes, list, tuple, dict], sender_id: str, recipient_ids: List[str]=[]) -> None:
        if content is None:
            raise ValueError("The top content of a message cannot be `None`.")
        elif not isinstance(content, (int, float, str, bytes, list, tuple, dict)):
            raise TypeError("The top content of a message must be a `Union[int, float, str, bytes, list, tuple, dict]`.")
        elif sender_id is None:
            raise ValueError("The sender ID of a message cannot be `None`.")
        elif not isinstance(sender_id, str):
            raise TypeError("The sender ID of a message must be a `str`.")
        elif recipient_ids is None:
            raise ValueError("The list of recipient IDs of a message cannot be `None`.")

        self.__content: Union[int, float, str, bytes, list, tuple, dict] = content
        self.__sender_id: str = sender_id
        self.__recipient_ids: List[str] = recipient_ids

    def get_content(self) -> Union[int, float, str, bytes, list, tuple, dict]:
        '''
        Returns the content of the message as a `Union[int, float, str, bytes, list, tuple, dict]`.
        '''
        return self.__content

    def get_sender_id(self) -> str:
        '''
        Returns the sender's ID as a `str`.
        '''
        return self.__sender_id

    def get_recipients_ids(self) -> List[str]:
        '''
        Returns the recipients' IDs as a `List[str]`.

        In case this `Message` is a `BccMessage`, this method returns a `List[str]`containing only one ID.
        '''
        return self.__recipient_ids

    def override_recipients(self, recipient_ids: List[str]) -> None:
        '''
        WARNING: this method needs to be public, but it is not part of the public API.
        '''
        self.__recipient_ids = recipient_ids


class BccMessage(Message):
    '''
    This class specifies a wrapper for a message that is sent to a single recipient, and its metadata.

    * The content is specified by the `content` field. This field's type is `Union[int, float, str, bytes, list, tuple, dict]`.
    * The recipient is specified by the `recipient_id` field. This field's type is `str`.
    * The sender is specified by the `sender_id` field. This field's type is `str`.
    '''
    def __init__(self, content: Union[int, float, str, bytes, list, tuple, dict], sender_id: str, recipient_id: str) -> None:
        if content is None:
            raise ValueError("The top content of a message cannot be `None`.")

        super(BccMessage, self).__init__(content=self.__deep_copy_content(content), sender_id=sender_id, recipient_ids=[recipient_id])

    def __deep_copy_content(self, content: Union[int, float, str, bytes, list, tuple, dict]) -> Union[int, float, str, bytes, list, tuple, dict, None]:
        # The content is deep-copied to avoid that the same object is shared by multiple `BccMessage` instances.
        # The `None` value is not valid for the top content, but it is valid for the content of a list, tuple, or dict.
        # Since this method is called recursively, the check that the top content is not `None` must be performed by the caller.

        if content is None or isinstance(content, (int, float, str, bytes)):
            return content
        elif isinstance(content, list):
            return [self.__deep_copy_content(element) for element in content]
        elif isinstance(content, tuple):
            return tuple([self.__deep_copy_content(element) for element in content])
        elif isinstance(content, dict):
            return {self.__deep_copy_content(key): self.__deep_copy_content(value) for key, value in content.items()}
        else:
            raise ValueError("Invalid content type: {}. The content of a message must be of type `Union[int, float, str, bytes, list, tuple, dict]`, including recursive content.".format(type(content)))

    def __str__(self) -> str:
        return "message:(from: {}, content: {})".format(self.get_sender_id(), self.get_content())
