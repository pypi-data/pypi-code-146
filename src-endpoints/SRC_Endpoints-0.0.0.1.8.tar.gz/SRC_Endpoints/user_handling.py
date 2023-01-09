import requests
import json


def create_user(email: str, password: str, verbose: bool = True):
    """
    This function enables the creation of a new user, required for access and authentication into the
    API, and therefore the DataBase. The function firstly checks that the input arguments are of the expected
    type, followed by checking that the password is an alphanumeric password. The email and password are placed into
    a json object and subsequently posted to the DataBase. If a response code of 200, or 201 is returned, the object has
    been created as a user. Otherwise, the error logs are returned.

    :param email: the email from which the user would like to register, must be @samsonrock.com. (str)
    :param password: the password with which the user would like to register, must be alphanumeric. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: N/A
    """
    if not all(isinstance(v, str) for v in [email, password]):
        raise TypeError("The 'email' and 'password' arguments must be string types.")
    if not password.isalnum():
        raise ValueError("The 'password' argument must be Alphanumeric")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = 'https://www.samsonrockapis.com/users&create'
    my_obj = {
        "email": email,
        "password": password
    }
    my_obj = json.dumps(my_obj, indent=2)
    user = requests.post(url, data=my_obj)
    if user.status_code in [200, 201]:
        user_characteristics = user.json()
        if verbose:
            print("*" * 80)
            print("User ID is: {}".format(user_characteristics['id']))
            print("User Email is: {}".format(user_characteristics['email']))
            print("*" * 80)
    else:
        if verbose:
            print("Status Code was {}, please contact support.".format(user.status_code))


def login_user(username: str, password: str, verbose: bool = True):
    """
    This function enables users to login to the API, allowing an authenticated session to interact directly with the
    database. The function firstly checks that the input arguments are of the expected type, followed by creating a
    json object containing the password and username. Following this, the credentials packet is posted to the API, and
    a response is returned. If the status code is within the range 200-204, the user authorization token is returned,
    otherwise the status code is printed, allowing the user to diagnose the error.

    :param username: the email address of the user, through which the user registered. (str)
    :param password: the password with which the user registered, must be alphanumeric. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: access_token: the access token required for authentication of additional endpoints. (str)
    """
    if not all(isinstance(v, str) for v in [username, password]):
        raise TypeError("The 'username' and 'password' arguments must be string types.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = "https://www.samsonrockapis.com/login"
    myobj = {'username': username,
             'password': password}
    user = requests.post(url, data=myobj)
    if user.status_code in [200, 201, 202, 204]:
        user_characteristics = user.json()
        if verbose:
            print("*" * 80)
            print("Status Code is: {}".format(user.status_code))
            print("User Token: {}".format(user_characteristics['access_token']))
            print("User Auth: {}".format(user_characteristics['token_type']))
            print("*" * 80)
        return user_characteristics['access_token']
    else:
        if verbose:
            print("Status Code: {}, an error occurred during user log-in.".format(user.status_code))


def get_user_identification(identity: int, access_token: str, verbose: bool = True):
    """
    This function allows the user, or any authenticated user, to retrieve the user information of a specific user by
    retrieving through the identity parameter. This endpoint requires authentication through an access token, which
    is passed in through a string. Once the arguments have been validated, the metadata for the user is attempted to
    be retrieved. If the information exists, the information shall be printed, otherwise, an error is displayed if the
    identity is not available, with other errors displayed through status codes.

    :param identity: the numerical identity of the user which we want to retrieve. (int)
    :param access_token: the access token of the user, must be an active access token. (str)
    :param verbose: determines if status is printed. Default=True. (bool)
    :return: N/A
    """
    if not isinstance(identity, int):
        raise TypeError("The 'identity' argument must be an integer type.")
    if not isinstance(access_token, str):
        raise TypeError("The 'access_token' argument must be a string type.")
    if not isinstance(verbose, bool):
        raise TypeError("The 'verbose' argument must be a boolean type.")
    url = "https://www.samsonrockapis.com/users&{}".format(identity)
    header = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(url, headers=header)
    if response.status_code in [200, 201, 202]:
        user_characteristics = response.json()
        if verbose:
            print("*" * 80)
            print("User ID is: {}".format(user_characteristics['id']))
            print("User Email is: {}".format(user_characteristics['email']))
            print("Published Time is: {}".format(user_characteristics['PublishedTime']))
            print("*" * 80)
    elif response.status_code == 404:
        if verbose:
            print("Status Code: {}, no user found".format(response.status_code))
    else:
        if verbose:
            print("Status Code: {}, user not validated".format(response.status_code))
