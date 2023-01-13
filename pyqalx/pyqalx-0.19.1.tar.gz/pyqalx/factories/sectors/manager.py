import logging
import threading
from time import sleep
import concurrent.futures

from pyqalx.factories.sectors.providers import LocalProvider


class SectorManager:
    """
    A manager that ensures that all the stacks are created
    and that if any error during creation that all existing stacks get destroyed
    """

    # An arbitrary sleep length to avoid frequent network calls
    POLL_TIME = 10

    def __init__(self, providers, plan_debug):
        self.providers = providers
        self.plan_debug = plan_debug

    def _all_completed(self):
        """
        Have all the stacks for all providers been created successfully?
        """
        return all([p.created for p in self.providers])

    @staticmethod
    def _delete_stacks(providers):
        """
        For the given list of providers will delete the stack
        :param providers: A list of Providers
        """
        for provider in providers:
            provider.delete_stack(provider.stack_id)

    def _monitor_completion(self, provider, error):
        stack_id = provider.stack_id
        stack_status = provider.describe_stack()

        while stack_status != provider.CREATED_STATUS:
            if stack_status in provider.ERRORED_STATUSES:
                # Set the error flag so we can start deleting any stacks
                # that have already created or are in the process of
                # creating.  This stack will delete itself automatically
                # due to the value of OnFailure
                error_reasons = ", ".join(provider._get_error_reason())
                msg = (
                    f"An error occured during stack creation.  "
                    f"Reason was: `{error_reasons}`"
                )
                provider._msg_user(msg, level=logging.ERROR)
                error.set()
                if isinstance(provider, LocalProvider):
                    # LocalProviders don't auto delete if they fail,
                    # so the deletion needs to be called explicitly
                    self._delete_stacks([provider])
                return False, stack_id
            if error.is_set():
                # Another stack has errored.  Therefore, delete this
                # stack before it finishes creating
                self._delete_stacks([provider])
                return provider.created, stack_id

            provider._msg_user("creating, please wait...", should_log=False)
            sleep(self.POLL_TIME)
            stack_status = provider.describe_stack()

        provider._msg_user("stack creation completed")
        provider.created = True
        return provider.created, stack_id

    def _monitor_stack_deletion(self):
        # A stack errored so any completed stacks are being completed.
        def _do_delete_check(provider):
            stack_status = provider.describe_stack()

            while (
                stack_status not in provider.DELETED_STATUSES
                and stack_status is not None
            ):
                # Wait for the stacks to delete.
                # Treat a stack that cannot be found (None status) as deleted
                stack_status = provider.describe_stack()
                provider._msg_user("deleting, please wait...", should_log=False)
                sleep(self.POLL_TIME)
            extra = "completed"
            if stack_status == provider.DELETE_FAILED:
                # better error message for the user if the stack deletion
                # fails
                extra = "failed"
            provider._msg_user(f"stack deletion {extra}")
            return True

        if self.plan_debug._demolish_on_failure:
            # Only do the delete wait check if we are actually deleting stacks,
            # otherwise we'd wait forever
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=len(self.providers)
            ) as executor:
                for provider in self.providers:
                    executor.submit(_do_delete_check, provider)

    def _monitor_stack_creation(self):
        error = threading.Event()
        results = []

        if all([p.stack_id for p in self.providers]) is False:
            # Handles the request to create a stack failing for some reason.
            # This is unlikely to happen but if a single stack can't even
            # start creation we should ensure that stacks that did start
            # creation are deleted.
            self._delete_stacks(
                filter(lambda x: x.stack_id is not None, self.providers)
            )
            self._monitor_stack_deletion()
            return
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=len(self.providers)
        ) as executor:
            for provider in self.providers:
                results.append(
                    executor.submit(self._monitor_completion, provider, error)
                )

            for future in concurrent.futures.as_completed(results):
                # Waits until all stacks complete.  If any other stacks
                # error after these have completed then we delete the completed
                # stacks.  Once all are completed then we exit

                all_completed = self._all_completed()
                while not all_completed and not error.is_set():
                    # Sit and wait until either all the stacks are completed or
                    # the error event is set (meaning that one stack failed to
                    # create)
                    all_completed = self._all_completed()
                is_created, _ = future.result()
                if is_created is True and error.is_set():
                    # Delete any stacks that have already completed
                    self._delete_stacks(
                        filter(lambda x: x.created, self.providers)
                    )

        if error.is_set():
            # Stacks are being deleted because one errored.  Sit and wait until
            # they are all completed.
            self._monitor_stack_deletion()
