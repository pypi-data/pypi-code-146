"""
This Script can be used to create custom claims on some registered user in Identity Platform.

For the script to run, remember to add the environment variable
for the Default App engine service account JSON.

Instructions:
    1. Call the script with the following parameters in this order:
        - MAIN email of the user to set the claims
        - claim to set on the user

The email must be the main email from the user in Identity Platform:
    https://firebase.google.com/docs/auth/admin/manage-users#retrieve_user_data

Example with one claim:
    python script_create_custom_claims.py Admin

"""
import sys
import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin.exceptions import FirebaseError


if __name__ == '__main__':
    default_app = firebase_admin.initialize_app()
    user_email = sys.argv[1]
    print(f"Trying to create claims for the user with email: {user_email}")

    try:
        user = firebase_auth.get_user_by_email(user_email)
    except ValueError as e:
        print(f'There was an error, the email is invalid or malformed: {e}')
        exit(1)
    except firebase_auth.UserNotFoundError:
        print(f'The user was not found.')
        exit(1)
    except FirebaseError as e:
        print(f'There was an unknown error: {e}')
        exit(1)

    print(f"User found: {user.display_name}")

    claims = {'role': sys.argv[2]}

    print(f"The following claims will be configured: {claims}")

    try:
        firebase_auth.set_custom_user_claims(user.uid, claims)

    except ValueError:
        print("The claims are invalid.")
        exit(1)
    except FirebaseError as e:
        print(f'There was an unknown error: {e}')
        exit(1)

    print(f"SUCCESS: The claims were updated for the user.")

    # user_email = sys.argv[1]
    # user = firebase_auth.create_user(
    #     email=user_email,
    #     email_verified=True
    # )
