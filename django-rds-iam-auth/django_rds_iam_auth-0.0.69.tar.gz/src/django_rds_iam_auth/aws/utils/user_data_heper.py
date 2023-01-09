import jwt

def get_user_sub_from_token(auth_string,defaut=None):
    """Returns the sub of a user from auth token."""
    try:
        return jwt.decode(auth_string, verify=False).get('sub', defaut)
    except Exception as ex:
        return 'default'

