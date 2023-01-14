from enum import Enum

class CredentialElement(Enum):
    firstName = 'First Name'
    lastName = 'Last Name'
    sex = 'Sex'
    dob = 'Date of Birth'
    countryOfResidence = 'Country of Residence'
    nationality = 'Nationatility'
    idDocType = 'Identity Document Type'
    idDocNo = 'Identity Document Number'
    idDocIssuer = 'Identity Document Issuer'
    idDocIssuedAt = 'ID Valid from'
    idDocExpiresAt = 'ID Valid to'
    nationalIdNo = 'National ID number'
    taxIdNo = 'Tax ID number'

class CredentialDocType(Enum):
    na = '0'
    Passport = '1'
    National_ID_Card = '2'
    Driving_License = '3'
    Immigration_Card = '4'    
    
class Credentials:
    '''
    This class processes credential information as retrieved from the node.
    '''
    def __init__(self):
        pass

    def determine_id_providers(self, ac):
        '''
        Input to this method is the output from the node.
        '''
        credentials = []
        for key, v in ac.items():
            c = {
                'ipIdentity': v['value']['contents']['ipIdentity'],
                'Created at': v['value']['contents']['policy']['createdAt'],
                'Valid to':   v['value']['contents']['policy']['validTo'],
            }
            if len(v['value']['contents']['policy']['revealedAttributes'].keys()) > 0:
                for key, revealedAttribute in v['value']['contents']['policy']['revealedAttributes'].items():
                    if key == 'idDocType':
                        value = CredentialDocType(revealedAttribute).name.replace("_", " ")
                    else:
                        value = revealedAttribute
                    c.update({
                        CredentialElement[key].value: value
                    })
            credentials.append(c)
        return credentials

class Identity:
    def __init__(self, node_account_info):
        if node_account_info:
            self.credentials = Credentials().determine_id_providers(node_account_info.get('accountCredentials', {}))
            self.threshold = node_account_info.get('accountThreshold', 0)
        else:
            self.credentials = []
            self.threshold = 0