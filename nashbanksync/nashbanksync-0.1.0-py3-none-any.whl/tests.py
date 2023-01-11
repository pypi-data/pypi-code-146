import requests

_client_id = "NashSyncERP"
_client_secret = "secret"

_payload = {
    'grant_type': 'client_credentials',
    'scope': "NashSyncERP TreasuryService",
    'client_id': _client_id,
    'client_secret': _client_secret
}


_auth_token_url = "https://authserver.purplecliff-03d4fbdd.westeurope.azurecontainerapps.io/connect/token"

_identity_token = requests.request("POST", _auth_token_url, data=_payload)

print('=======================================================')
print(f'_identity_token angular purple: {_identity_token.text}')
print('=======================================================')

# print()
# print()
# print()

# _auth_token_url="https://identity.nashglobal.co/connect/token"

# _identity_token = requests.request("POST", _auth_token_url, data=_payload)

# print('=======================================================')
# print(f'_identity_token: {_identity_token.text}')
# print('=======================================================')
