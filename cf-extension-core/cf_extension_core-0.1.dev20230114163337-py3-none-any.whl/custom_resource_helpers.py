import datetime

from cloudformation_cli_python_lib.identifier_utils import generate_resource_identifier
import cloudformation_cli_python_lib.exceptions as exceptions
from typing import Any, MutableMapping


class CustomResourceHelpers:
    ALL_HANDLER_TIMEOUT_THAT_SUPPORTS_IN_PROGRESS = 60
    READ_LIST_HANDLER_TIMEOUT = 30
    STANDARD_SEPARATOR = "::"

    @staticmethod
    def generate_primary_identifier_for_resource_tracking(
        stack_id: str,
        logical_resource_id: str,
        resource_identifier,
    ) -> str:
        identifier = (
            stack_id
            + CustomResourceHelpers.STANDARD_SEPARATOR
            + logical_resource_id
            + CustomResourceHelpers.STANDARD_SEPARATOR
            + CustomResourceHelpers.STANDARD_SEPARATOR
            + resource_identifier
        )
        """
        # Why are we doing this?
        # The resource code will need to take care of - does the resource I am about ready to create exist (examples)
        # Does the route 53 record with Name X already exist- if so Fail out creating the resource
        # Should I create that Transit gateway route -
        #   interrogate the routes first and see if we should fail to create because of existence.

        # What about resources like an AD Trust While the resource_identifier could be a trust id - The custom
        # resource will have to ask the question - does a trust exist with this directory with the same name - if so
        # fail out.

        # We have 2 fundamental problems with this current implementation above - with or without prepended stack id and
            logical resource id
        # If we dont prepend with stack info -
        # We are hoping all unique identifiers across all applications we ever integrate with are unique across any
        service AWS/Security/Azure/Random Webservice Integration - that seems like hope and dreams and no way to enforce
        # If we DO prepend with stack info
        # Now resources will almost never run into eachother, but we are putting the onus on the developer to not create
            something that may not be unique.
        # For example - If developer has to create an AD group in stack1 and tries to create an ad group in stack 2 with
            same name, at the dynamo DB level nothing will fail with this design.  The developer will have to do the
            work to ensure no onverlap

        # If the developer in previous use case used the primary identifier of ad group name - that would in fact work -
        but with the N number of custom resources planned we would almost certaintly eventually have a collission with
        primary identifiers - especially if they can be human parameters like trusted domain name.  The only way we
        could guarantee no collission is a separate Dynamo Table per custom resource - this would guarantee the "alike"
         primary identifiers are only being compared with eachother.  Then its up to the implementor to pick good
         primary identifiers.

        # A seperate Dynamo table per resource feels like overkill - Technically possible - but it would guarantee no
        overlap.  That would allow us to implement each resource in a way where we wouldnt have to do "as much"
        defensive programming.  But it doesnt solve it completely.

        # Take the trust issue with AD again.  While the trust ID would be unique.  The trust is a singleton from a
        name perspective.  So you can only have N trust names to one directoryid but you cant have the same trust name
         times 2 to one directory.  That will require defensive programming

        # An example where we wouldnt have thte problem is ACM - You can request N number of certs with the same name
        but the DNS records to verify are always unique.  In this case however - one table per resource would HELP on
        the collission issue.

        # So what do we do?
        # The reason we are implementing custom resources is because either AWS failed us or we are integrating with
        other APIs.  Another use case is we need to read auto created resource info.
        # The reason we are doing dynamo DB work is because we need to honor the contract tests specifically for RO
        resources.  That is not in scope for this method

        # Decision:
        # The simplest to implemnent answer feels like the right path - Use a single table - dump all resources in there
         that are almost guaranteed to be unique and use defensive programming in each custom resource.  Each custom
         resource will have to do some kind of defensive programming anyways - so lets just assume it will happen
         anyways.  This will keep the dynamo db layer simpler and easier to think about.

        """

        return identifier

    @staticmethod
    def generate_primary_identifier_for_resource_tracking_read_only_resource(
        stack_id: str,
        logical_resource_id: str,
    ) -> str:
        import uuid

        uuidstr = str(uuid.uuid4())  # Not guaranteed unique technically - but the best we can do
        # We really dont care if a read only resource is executed 100 + times in a region -
        # its just reading data so it doesnt matter the complexity of this implementation.
        # The likelihood of having generated uuids overlapping in the same CF stack is almost impossible.

        identifier = (
            stack_id
            + CustomResourceHelpers.STANDARD_SEPARATOR
            + logical_resource_id
            + CustomResourceHelpers.STANDARD_SEPARATOR
            + CustomResourceHelpers.STANDARD_SEPARATOR
            + uuidstr
        )

        return identifier

    @staticmethod
    def get_naked_resource_identifier_from_string(primary_identifier: str):
        array = primary_identifier.split(
            CustomResourceHelpers.STANDARD_SEPARATOR + CustomResourceHelpers.STANDARD_SEPARATOR
        )
        assert len(array) == 2

        return array[-1]

    # Initial thinking.  Now way overcomplicated.
    #
    # @staticmethod
    # def generate_primary_identifier_for_read_only_resource(create_only_property_values: list, stack_id,
    # logical_resource_id):
    #     #These are immutable values that can not change for the life of the resource.
    #     #For a read only request it MUST be a generated value
    #     # I think we will want this to be a combination of CreateOnlyProperties in general
    #
    #     # The framework (AWS) will not allow an update operation to happen if a create only property
    #     gets changed - instead it will do a create/delete or delete/create based on schema
    #         #Any property not explicitly listed in the createOnlyProperties element can be specified by the
    #         user during a resource update operation.  That means anything outside of createonly properties cannot
    #         be part of the generated identifier.
    #
    #     #What happens if there are are no create only properties? (IE no parameters) - We generate a GUID or a
    #     hash - best we can do
    #     #That is another method
    #
    #     #How do we get the list of create only properties generically and append them together?  We cant, schema isnt
    #     exposed in generated code, stupid AWS framework design.
    #     #Force developer to send in create_only_property_values as a list
    #
    #     #This needs to be regionally unique to allow for the same resource to be "read" in multiple regions - how do
    #     we allow for that?
    #     #We for the unique identifier to be prefixed by stack_id and logical resource id.
    #     #If an update gets called and create_only dont change - then the identifier is constant
    #     #if an update gets called and create_only is changed - its invalid and should cause a contract test failure
    #     #SO - the physical identifier of stack name + logical resource id ANDed with create_only_property values
    #     should be  enough to be unique
    #
    #     #This is all theory - will need to test it.
    #
    #     if len(create_only_property_values) == 0 :
    #         raise Exception("There must be at least 1 create_only_property for this method")
    #
    #     separator="::"
    #     identifier = stack_id+separator+logical_resource_id
    #     for item in create_only_property_values:
    #         identifier=identifier+separator+item
    #
    #     identifier = identifier.strip(separator)
    #
    #     return identifier

    @staticmethod
    def generate_unique_resource_name(
        stack_id: str,
        logical_resource_name: str,
        client_request_token: str,
        max_length: int = 255,
    ) -> str:
        primary_name = generate_resource_identifier(
            stack_id_or_name=stack_id,
            logical_resource_id=logical_resource_name,
            client_request_token=client_request_token,
            max_length=max_length,
        )
        return primary_name

    @staticmethod
    def _callback_add_handler_entry_time(
        callback_context: MutableMapping[str, Any],
    ) -> None:
        # No if statement here
        # If we get re-invoked we need to reset handler entry time to the new invocation
        callback_context["handler_entry_time"] = datetime.datetime.utcnow()

    @staticmethod
    def _callback_add_resource_end_time(
        callback_context: MutableMapping[str, Any],
        total_allowed_time_in_minutes: int,
    ) -> None:
        # If statement makes sure this gets set once and only once for every resource create/update/delete call.
        if "resource_entry_end_time" not in callback_context:
            callback_context["resource_entry_end_time"] = datetime.datetime.utcnow() + datetime.timedelta(
                minutes=total_allowed_time_in_minutes
            )

    @staticmethod
    def should_return_in_progress_due_to_handler_timeout(
        callback_context: MutableMapping[str, Any],
    ) -> bool:
        if "entry_time" not in callback_context:
            raise exceptions.InternalFailure("entry_time not set in callback state")
        else:
            if (
                callback_context["entry_time"]
                + datetime.timedelta(seconds=CustomResourceHelpers.ALL_HANDLER_TIMEOUT_THAT_SUPPORTS_IN_PROGRESS)
                - datetime.timedelta(seconds=10)
                > datetime.datetime.utcnow()
            ):
                # If handler entry time + Max return time (60)
                # - 10 seconds(arbitrary for wiggle room for dynamodb code) > Current time -->
                # Return before CF kills us.
                return True
            else:
                return False

    @staticmethod
    def _return_failure_due_to_timeout(
        callback_context: MutableMapping[str, Any],
    ) -> None:
        if "resource_entry_end_time" not in callback_context:
            raise exceptions.InternalFailure("resource_entry_end_time not set in callback state")
        else:
            if callback_context["resource_entry_end_time"] > datetime.datetime.utcnow():
                # If resource end time is greater than now we need to return failure due to timeout
                raise exceptions.InternalFailure(" Timed out trying to create/update/delete resource.")

    @staticmethod
    def initialize_handler(
        callback_context: MutableMapping[str, Any],
        total_allowed_time_in_minutes: int,
    ) -> None:

        # TODO: Consider overriding the Table name based on Type Name here

        CustomResourceHelpers._callback_add_resource_end_time(
            callback_context=callback_context,
            total_allowed_time_in_minutes=total_allowed_time_in_minutes,
        )
        CustomResourceHelpers._callback_add_handler_entry_time(callback_context=callback_context)
        CustomResourceHelpers._return_failure_due_to_timeout(callback_context)
