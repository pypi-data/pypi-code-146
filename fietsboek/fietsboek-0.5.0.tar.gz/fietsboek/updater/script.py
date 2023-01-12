"""Base class definition for update scripts."""
# Placed in a separate file to avoid cyclic dependencies


class UpdateScript:
    """Base class for update scripts.

    This class provides stub methods for the update script hooks as well as
    methods for user interaction.
    """

    def tell(self, text):
        """Output a message to the user.

        This function should be used in update scripts instead of :func:`print`
        to ensure the right stream is selected.

        :param text: The text to show to the user.
        :type text: str
        """
        print(text)

    def pre_alembic(self, config):
        """Script that is run before the alembic migration is run.

        This method is to be overridden by subclasses.

        :param config: The app configuration.
        :type config: dict
        """

    def post_alembic(self, config):
        """Script that is run after the alembic migrations have been run.

        This method is to be overridden by subclasses.

        :param config: The app configuration.
        :type config: dict
        """
