import datetime
import os

from gwdg_idm_api.benutzerverwaltung import Benutzerverwaltung
from gwdg_idm_api.models import BaseGWDGUser, CreateTemplate
from gwdg_idm_api.util import AlreadyDeletedError, pretty_print


# This are the values for our CreateTemplate for a new IDM user
# Adjust the fields to your template.
class NewGWDGUser(CreateTemplate):
    create_template_name: str = os.environ["IDM_CREATE_TEMPLATE"]
    givenName: str
    sn: str
    workGroup: str
    departmentNumber: str
    roomNumber: str = ""
    telephoneNumber: str = ""
    goesternUserType: str = "0"
    externalTaskCommand: str = "CreateMailbox"


# This are the values for our MPIDoUser, we have some additional fields
# for workGroup, dn, and externalTaskCommand
# Adjust the fields to your template.
class MPIDoUser(BaseGWDGUser):
    workGroup: str
    dn: str
    externalTaskCommand: str


# Load idm credentials
# Do not upload credentials in any way to github/gitlab etc.
idm_username = os.environ["IDM_USERNAME"]
idm_password = os.environ["IDM_PASSWORD"]


# For testing purposes, we are using the idm-stage endpoint.
# This one is a copy of the previous day and can be used
# for sandbox testing.
# Change to "https://idm.gwdg.de/api/v3" for production.
benutzerverwaltung = Benutzerverwaltung(
    api_url=os.environ["IDM_API_URL"],
    username=idm_username,
    password=idm_password,
)
# Set the user class you would like to return
benutzerverwaltung.set_user_class(MPIDoUser)

# Get all users having their surename starting with 'a'
sn_a_users = benutzerverwaltung.get_multiple_users("$sn -eq 'a*'")
print("# First two entries starting with 'a'")
print(pretty_print(sn_a_users[:2]))

# Take the first user and print a more detailed view
print("# Get detailed information")
single_user = benutzerverwaltung.get_single_user(sn_a_users[0].id)
print(pretty_print(single_user))


# Change the lastname of the user to 'Upps bad lastnäme' and workGroup to '-'
# and check if the update happened
print("# Update user")
updated_user = benutzerverwaltung.update_user(
    single_user, {"workGroup": "-", "sn": "Upps bad lastnäme"}
)
print(pretty_print(updated_user))

# Ah that did not work out well!
# Now lets remove the user in 10 days (set goesternExpirationDate)
# If
print("# Delete user in 10 days")
try:
    deleted_user = benutzerverwaltung.delete_user(
        single_user, datetime.datetime.now() + datetime.timedelta(days=10)
    )
except AlreadyDeletedError:
    # If the user is already deleted an AlreadyDeletedError is thrown
    print("Already deleted")
else:
    print(pretty_print(deleted_user))

# Actually, lets delete him yesterday
# The delete_user functions will automatically just check the
# isScheduledForDeletion flag if the expire_datetime is in the past
print("# Delete user now")
try:
    deleted_user = benutzerverwaltung.delete_user(
        updated_user, datetime.datetime.now() - datetime.timedelta(days=1)
    )
except AlreadyDeletedError:
    print("Already deleted")
else:
    print(pretty_print(deleted_user))

# Lets create a new user
print("# Create new user")
new_user_tmp = NewGWDGUser(
    givenName="john", sn="doe", workGroup="-", departmentNumber="ZE"
)
new_user = benutzerverwaltung.create_user(new_user_tmp)
print(pretty_print(new_user))

print("# All done :)")
