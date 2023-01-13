import itertools
import os

import click
from click import ClickException
from tabulate import tabulate

from pyqalx.core.encryption import QalxEncrypt
from pyqalx.core.entities import QalxListEntity
from pyqalx.core.entities.bot import Bot
from pyqalx.core.entities.factory import Factory
from pyqalx.core.signals import QalxSignal


def generate_key_file():
    """
    Generate an encryption key file and return the path to the new file if this
    has been successful
    """
    while True:
        key_path = click.prompt(
            "Where do you want to save the key file?",
            default=QalxEncrypt.DEFAULT_KEY_PATH,
        )
        if os.path.exists(key_path):
            click.echo(
                f"\nThe provided path: {key_path} exists. "
                + "Please provide a non-existing path\n"
            )
        else:
            break
    try:
        QalxEncrypt.save_key(key_path)
    except (OSError, PermissionError) as exc:
        message = (
            "There was an error saving the encryption key file:\n\n" + f"{exc}"
        )
        raise ClickException(message)
    else:
        return key_path


class QalxCLITabulation:
    """
    A helper class for building a table of entities to display to the user
    """

    prompt_text = None

    def __init__(self, qalx_session, name, entity_class, tabulate_single=False):
        """
        :param qalx_session: An instance of QalxSession
        :param name: The name of the entity that we are looking for
        :param entity_class: The entity class that is being tabulated
        :param tabulate_single: Whether we should tabulate if a single
        result is found or just return the entity
        """

        self.qalx_session = qalx_session
        self.name = name
        self.tabulate_single = tabulate_single
        self.entity_class = entity_class
        self.entity_type = entity_class.entity_type
        self.next_table_index = 1

        # Get the entities for the prompt
        self.entities_for_prompt = self.get_entities_for_prompt()

    def query_kwargs(self):
        """
        By default there are no additional kwargs passed through to the query
        """
        return {}

    def get_entities_for_prompt(self):
        """
        Queries the API and returns the entities for the prompt based on
        `self.build_query()` and `self.query_kwargs`
        """
        query = self.build_query()
        entities = getattr(self.qalx_session, self.entity_type).find(
            query=query, **self.query_kwargs()
        )
        return entities

    def _update_entities_for_prompt(self, updated_entities):
        """
        Update the entities for prompt. This is needed in the case of paginated
        results from a query.
        """
        self.entities_for_prompt = updated_entities

    def build_query(self):
        """
        Builds the query that will be used to query the api
        :return: A dict of the query, by default just the name will be queried
        """
        return {"name": self.name}

    def build_no_entities_message(self):
        """
        The message to be displayed if no entities are found matching the query
        """
        return f"No {self.entity_class.pluralise()} found called `{self.name}`"

    @staticmethod
    def build_row(index, entity):  # pragma: no cover
        """
        A specific row on a table
        :param index: The index of this row
        :param entity: The entity instance
        :return: A list of data for the entity for a single row
        """
        raise Exception("Must be implemented by subclass")

    @staticmethod
    def build_headers():  # pragma: no cover
        """
        The headers for this table
        :return: A list of strings for the table
        """
        raise Exception("Must be implemented by subclass")

    def tabulate(self):
        """
        For the given `self.entities_for_prompt` will build a table using
        tabulate and display this to the user via `click.echo`
        """
        table = []

        # Massage the remaining entities into a nice format for presentation
        entities_for_prompt = self.entities_for_prompt.data
        for index, entity in enumerate(
            entities_for_prompt, start=self.next_table_index
        ):
            table.append(self.build_row(index, entity))
            self.next_table_index += 1

        # We then display the entities to the user in a list,
        # and potentially prompt them for an index for the specific one they
        # wish to interact with
        headers = self.build_headers()
        # Display a table of entities
        click.echo(tabulate(table, headers, maxcolwidths=20))
        return table

    def get_entity_or_display(self):
        """
        Will either return the entity or display a table of entities
        depending on the number of entities found and the value
        of `self.tabulate_single`.
        If no entities are found always return None
        """
        entities_for_prompt = self.entities_for_prompt.data
        if len(entities_for_prompt) == 1:
            # Only a single entity found matching the name and with active
            # workers.
            # Just return it without showing the user the table of entities
            if self.tabulate_single:
                self.tabulate()
            else:
                return entities_for_prompt[0]
        elif not len(entities_for_prompt):
            # No entities found.  Nothing to do!
            click.echo(self.build_no_entities_message())
            return
        else:
            # Many entities found matching the query.
            # Create a table to allow the user to pick which they want
            table = self.tabulate()

            if (
                self.prompt_text
                or self.entities_for_prompt.query.next is not None
            ):
                while True:
                    # Message the user they can show next page in case of paginated
                    # results
                    has_next_page = (
                        self.entities_for_prompt.query.next is not None
                    )
                    prompt_message = (
                        "(Press ENTER to show the next page)\n\n"
                        if has_next_page
                        else ""
                    )
                    if self.prompt_text:
                        prompt_message += (
                            f"Please choose a {self.entity_type} index "
                            + f"to {self.prompt_text}"
                        )
                    if not prompt_message:
                        return
                    inp = click.prompt(prompt_message, default="")

                    if has_next_page and inp == "":
                        # If the user presses ENTER then we show the next page
                        # and append the results to the existing variables
                        response = getattr(
                            self.qalx_session, self.entity_type
                        )._process_api_request(
                            "get", self.entities_for_prompt.query.next
                        )
                        entities = QalxListEntity(
                            response, child=self.entity_class
                        )

                        self._update_entities_for_prompt(entities)

                        entities_for_prompt += self.entities_for_prompt.data
                        table += self.tabulate()
                    else:
                        # Case where they have provided an index. This needs to
                        # be in the range of the table that was built
                        if self.prompt_text:
                            try:
                                index = int(inp)
                            except ValueError:
                                pass
                            else:
                                if 0 < index <= len(table):
                                    # Get the entity from the index (- 1 because
                                    # the index the user chooses starts at 1)
                                    return entities_for_prompt[index - 1]
                        else:
                            return


class BotTabulation(QalxCLITabulation):
    def __init__(self, *args, **kwargs):
        super(BotTabulation, self).__init__(entity_class=Bot, *args, **kwargs)

    @staticmethod
    def build_headers():
        return [
            "Index",
            "Name",
            "State",
            "Platform",
            "Node",
            "No. Workers \n(Active/Total)",
            "Created On \n(UTC)",
            "Created By",
        ]

    @staticmethod
    def build_row(index, entity):
        created_on = entity.info.created.on.strftime("%d/%m/%Y %H:%M:%S")
        num_active_workers = len(
            [worker for worker in entity.workers if worker.state == "active"]
        )
        row = [
            index,
            entity.name,
            entity.state,
            entity.host.get("platform"),
            entity.host.get("node"),
            f"{num_active_workers}/{len(entity.workers)}",
            created_on,
            entity.info.created.by.email,
        ]
        return row


class TerminateBotTabulation(BotTabulation):
    prompt_text = "terminate"

    def build_query(self):
        query = super(TerminateBotTabulation, self).build_query()
        query["workers"] = {"$exists": True, "$not": {"$size": 0}}
        return query

    def build_no_entities_message(self):
        message = super(
            TerminateBotTabulation, self
        ).build_no_entities_message()
        return f"{message} that have workers that are not already terminated"

    @staticmethod
    def _filterfalse_signal(_worker):
        """
        itertools.filterfalse is used to exclude workers if a specific signal
        IS FALSE.
        Returns the status of this workers terminate signal.  If this signal
        is True (i.e. the worker is terminated) then it WON'T get returned
        to the user
        """
        return QalxSignal(_worker).terminate

    def _filter_entities(self, bots_for_prompt):
        """
        Filter the bots to only show those that have workers that aren't
        terminated
        """

        def _has_workers_with_specific_signal(_bot):
            # For each bot, we only return it if any of the
            # workers ARE NOT on a status of `self._filterfalse_signal`.
            # As a separate function to avoid nested lambdas
            return list(
                itertools.filterfalse(self._filterfalse_signal, _bot.workers)
            )

        # We then filter the bots to only be those that have any workers that
        # don't have a self._filterfalse signal.
        bots = list(
            filter(_has_workers_with_specific_signal, bots_for_prompt.data)
        )
        bots_for_prompt.data = bots
        return bots_for_prompt

    def get_entities_for_prompt(self):
        """
        For the termination prompt, only show bots that exist with workers
        that aren't terminated.
        """
        entities_for_prompt = super(
            TerminateBotTabulation, self
        ).get_entities_for_prompt()
        return self._filter_entities(entities_for_prompt)

    def _update_entities_for_prompt(self, updated_entities):
        self.entities_for_prompt = self._filter_entities(updated_entities)


class StopBotTabulation(TerminateBotTabulation):
    prompt_text = "stop"

    def build_no_entities_message(self):
        message = super(
            TerminateBotTabulation, self
        ).build_no_entities_message()
        return (
            f"{message} that have workers that are not already stopped "
            f"or terminated"
        )

    @staticmethod
    def _filterfalse_signal(_worker):
        """
        itertools.filterfalse is used to exclude workers if a specific signal
        IS FALSE.
        :return: If the workers stop signal is True (i.e. the worker is stopped)
        then the worker WON'T get returned to the user OR if the workers
        terminate signal is True (i.e. the worker is terminated)
         then the worker WON'T get returned to the user.
         Therefore, this will only return bots with non terminated workers that
         are also not stopped
        """
        signal = QalxSignal(_worker)
        return signal.terminate is True or signal.stop is True


class ResumeBotTabulation(TerminateBotTabulation):
    prompt_text = "resume"

    def build_no_entities_message(self):
        message = super(
            TerminateBotTabulation, self
        ).build_no_entities_message()
        return f"{message} that have workers that can be resumed"

    @staticmethod
    def _filterfalse_signal(_worker):
        """
        itertools.filterfalse is used to exclude workers if a specific signal
        IS FALSE.
        :return: if the workers stop signal is False (i.e. the worker is not stopped)
        then the worker WON'T get returned to the user OR if the workers terminate
        signal is True (i.e. the worker is terminated) then the worker WON'T get
        returned to the user.
        Therefore, this will only return bots with non terminated workers that
        are also stopped
        """
        signal = QalxSignal(_worker)
        return signal.terminate is True or signal.stop is False


class FactoryTabulation(QalxCLITabulation):
    def __init__(self, *args, **kwargs):
        super(FactoryTabulation, self).__init__(
            entity_class=Factory, *args, **kwargs
        )

    @staticmethod
    def build_headers():
        return [
            "Index",
            "Name",
            "Stage",
            "Status",
            "Created On (UTC)",
            "Created By",
        ]

    @staticmethod
    def build_row(index, entity):
        created_on = entity.info.created.on.strftime("%d/%m/%Y %H:%M:%S")
        row = [
            index,
            entity.name,
            entity.stage,
            entity.status,
            created_on,
            entity.info.created.by.email,
        ]
        return row


class DemolishFactoryTabulation(FactoryTabulation):
    prompt_text = "demolish"
