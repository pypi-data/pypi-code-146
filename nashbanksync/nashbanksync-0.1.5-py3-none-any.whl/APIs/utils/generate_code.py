import string
import random
import jwt
try:
    from django.conf import settings
except Exception as e:
    pass


def get_code(digits_only=False, length=6):
    # length of the string.
    S = length
    # call random.choices() string module to find the string in Uppercase + numeric data.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))

    if digits_only:
        ran = ''.join(random.choices(string.digits, k=S))

    return ran


def is_authenticated(access_token):
    if access_token is not None:
        try:
            # _, token = access_token.split(' ')
            decoded = jwt.decode(access_token, options={
                                 "verify_signature": False})
            OAUTH2_SCOPE = getattr(settings, 'OAUTH2_SCOPE', None)

            if OAUTH2_SCOPE in decoded.get('scope', []):
                return True
        except Exception as e:
            print(f'is_authenticated: {e}')
            return False

    return False
