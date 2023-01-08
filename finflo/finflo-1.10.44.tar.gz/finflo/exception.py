
## BASIC EXCEPTION CLASSES 


from rest_framework.exceptions import APIException

class ModelNotFound(APIException):
    status_code = 204
    default_detail = 'Matching action and type not found , try with some other type '
    default_code = 'model_object_not_found'

class VersionError(Exception):
    pass

class PartyLengthError(Exception):
    pass

class DefaultsNotFoundError(Exception):
    pass

class ModelError(APIException):
    pass

class TransitionNotAllowed(APIException):
    status_code = 204
    default_detail = 'Transition Not Allowed .'
    default_code = 'transition_unavailable'


class ReturnModelNotFound(APIException):
    status_code = 204
    default_detail = 'Unable to find the default model object  , try again .'
    default_code = 'model_object_not_found'



class SignaturesNotMatching(APIException):
    status_code = 204
    default_detail = 'Signatures not matching , only positive index accepted'
    default_code = 'signatures_index_not_matching'