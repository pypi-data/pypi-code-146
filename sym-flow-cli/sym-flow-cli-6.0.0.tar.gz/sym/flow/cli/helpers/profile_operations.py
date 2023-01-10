from sym.flow.cli.helpers.api_operations import (
    Operation,
    OperationHelper,
    OperationSets,
    OperationType,
)
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.models import User
from sym.flow.cli.models.service import SYM_CLOUD_KEY


def update_full_name(
    options: GlobalOptions,
    user_to_update: User,
    first_and_middle_name: str,
    last_name: str,
):
    """Given a user, executes the operation helper for creating/updating the first (including middle) and last name of user in Sym identity"""

    sym_identity = user_to_update.get_identity_from_key(SYM_CLOUD_KEY)
    sym_identity.profile["first_name"] = first_and_middle_name
    sym_identity.profile["last_name"] = last_name

    operations = OperationSets(
        # Don't need to send in all the existing identities,
        # just the identity to update and the Sym identity to identify the user
        update_user_ops=[
            Operation(
                operation_type=OperationType.update_user,
                original_value=None,
                new_value=User(id=user_to_update.id, identities=[sym_identity]),
            )
        ],
        delete_identities_ops=[],
        delete_user_ops=[],
    )

    operation_helper = OperationHelper(options, operations)
    operation_helper.handle_update_users()
