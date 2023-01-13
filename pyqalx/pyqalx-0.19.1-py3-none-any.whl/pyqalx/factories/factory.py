"""
Factory module. Contains the main factory class
"""
import logging

from botocore.exceptions import ClientError

from .mixins import BaseFactory
from ..core.errors import (
    QalxFactoryPackError,
    QalxAPIResponseError,
    QalxFactoryDemolishError,
    QalxFactoryBuildError,
)


class Factory(BaseFactory):
    """
    Main factory class. Inherits from BaseFactory and contains methods for
    specific functionality related to the distinct stages of a factory
    """

    DEPLOYING_STATUS = "deploying"
    DEPLOYED_STATUS = "deployed"
    DELETING_STATUS = "deleting"

    def validate(self, plan):
        """
        Calls the validate method on the adapter

        :param plan: Path to a .yaml file containing the definition of the factory plan
        :type plan: str
        :raises QalxFactoryValidationError: If there is a problem validating the plan
        """
        self._msg_user(msg="Starting Factory Validation")
        self.session.factory.validate(plan)
        self.plan = self.read_plan(plan)
        self._msg_user(msg="Factory Validation Successful")

    def pack(self, plan, stage=None, delete=True):
        """
        Packs a factory. Calls validate method on the plan provided

        :param plan:    Path to a .yaml file containing the definition of the
                        factory plan
        :type plan: str
        :param stage:   Stage to be packed. This argument is optional. If None
                        is provided, then all stages will be packed
        :type stage: str
        :param delete:  Should the packed code be deleted when this command
                        completes?
        :type delete: bool

        :raises QalxFactoryPackError:   If a stage is provided and it cannot be
                                        found on the plan, or if there are any
                                        issues creating the build directory
        """
        self._msg_user(msg="Starting Factory Pack")

        self.validate(plan)

        if stage and stage not in self._plan_stages:
            raise QalxFactoryPackError(
                f"Stage {stage} was not found in the factory plan"
            )
        self._create_build_path()

        bots = self._bots_for_pack(stage=stage)
        self._download_bots(bots)
        if delete:
            self._delete_build_path()
        self._msg_user(msg="Factory Pack Successful")

    def build(self, plan, stage):
        """
        Builds a factory. Calls pack method with the provided plan and stage.

        :param plan:    Path to a .yaml file containing the definition of the
                        factory plan
        :type  plan:    str
        :param stage:   Stage to be built
        :type  stage:   str
        :raises QalxFactoryBuildError: - if there is a problem with the build
        """
        self._msg_user(msg="Starting Factory Build")
        self.stage = stage
        self.pack(plan=plan, stage=self.stage, delete=False)

        # Add the key value tag pairs from the factory plan to the session
        for key, val in self._plan_tags.items():
            self.session.tags.add(name=key, value=val)

        def _delete_resources(_delete_stacks=True):
            """
            The build could fail in numerous places.  This private method handles
            consistent messaging and the actual deletion depending on the debug
            value
            """
            if self._plan_debug._demolish_on_failure:
                self._delete_resources(delete_stacks=_delete_stacks)
                # Message the user and raise an exception
                _error = (
                    "Factory Build Failed. No bots on this factory "
                    "have been started. Created resources have been "
                    "deleted. See the logs for more details"
                )
            else:
                # We aren't deleting resources despite the build failure.
                # Explicitly inform the user
                _error = (
                    f"Factory Build Failed. "
                    f"{self._plan_debug._demolish_on_failure_msg}"
                )
            self._msg_user(msg=_error, title="pyqalx", level=logging.ERROR)
            raise QalxFactoryBuildError(_error)

        try:
            self._add_entity(plan=plan)
            self._create_bot_items()
        except QalxAPIResponseError:
            # QalxAPIResponseError: An error occurred when trying to create the
            #                       items.  Unlikely if the user got to this
            #                       point but tidy up should still be attempted
            _delete_resources()
            return
        success = self._create_stacks()

        if success:
            try:
                self._add_factory_bots()
                self._resume_bots()
                self.entity.status = self.DEPLOYED_STATUS
                self.session.factory.save(self.entity)
                self._msg_user(msg="Factory Build Successful")
            except QalxAPIResponseError:
                # QalxAPIResponeError - There was an issue with saving back to
                #                       the API. Unlikely to happen if the user
                #                       has got this far but we
                #                       should still attempt tidy up.
                _delete_resources()
        else:
            # all stacks will have been deleted.  But the other
            # resources need to be tidied up
            _delete_resources(_delete_stacks=False)

    def demolish(self, factory_guid):
        """
        Demolishes a factory

        :param: factory_guid:   The guid of the factory entity to demolish
        """
        self._msg_user(msg="Starting Factory Demolish")
        try:
            self.entity = self.session.factory.get(factory_guid)
            self.entity.status = self.DELETING_STATUS
            self.session.factory.save(self.entity)
            self.breadth_first_terminate()
            self._delete_resources()
        except (ClientError, QalxAPIResponseError) as exc:
            # Catches possible errors and reraises as QalxFactoryDemolishError
            # to give users a consistent API when using programmatically
            # ClientError: An error occurred when trying to delete stacks
            # QalxAPIResponseError: An error occurred when trying to delete
            #                       qalx resources.
            raise QalxFactoryDemolishError(exc)
        self._msg_user(msg="Factory Demolish Successful")
