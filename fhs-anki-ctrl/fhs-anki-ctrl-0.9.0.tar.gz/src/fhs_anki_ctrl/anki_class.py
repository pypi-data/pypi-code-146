"""Anki class type."""

import requests


class AnkiClass(object):
    """Anki class."""

    def __init__(self, config_dict, debug=False):
        """Init anki class.

        Args:
            config_dict: config dict to use
            debug: debug
        """
        self.__config_dict = config_dict
        self.__debug = debug

    def convert_string(self, my_string):
        """Unicode string.

        Args:
            my_string: string

        Returns:
            my_string
        """
        # return my_string.replace("  ","&nbsp;&nbsp;").replace('"',"&quot;").replace("\n","<br>")
        return my_string.replace(" ", "&nbsp;").replace('"', "&quot;").replace("\n", "<br>")

    def post(self, payload):
        """Post request, using command and payload.

        Args:
            payload: what to send

        Returns:
            result
        """
        try:
            result = requests.post(self.__config_dict["host"], json=payload)
        except Exception as e:  # noqa: B902
            if 'Connection refused' in str(e):
                print("ERROR: connection error is the anki desktop with anki-connect running?")
            else:
                print(f"ERROR: {str(e)}")
            exit(1)
        # self.print(r)
        # """ import pdb; pdb.set_trace() """
        if result:
            return result.json()
        return None

    def push_sync(self):
        """Request a sync.

        Returns:
            result
        """
        payload = {"action": "sync", "version": 6}
        return self.post(payload)

    def payload_add_card(self, deck, question, answer, tags=None):
        """Create payload for card.

        Args:
            deck: str: deck to use
            question: str:question
            answer: str: answer
            tags: extra tags

        Returns:
            payload
        """
        if tags is None:
            tags = []
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck,
                    "modelName": "Basic",
                    "fields": {"Front": self.convert_string(question), "Back": self.convert_string(answer)},
                    "options": {"allowDuplicate": False},
                    "tags": tags,
                }
            },
        }

        return payload

    def add_card(self, deck, question, answer, tags=None):
        """Post question.

        Args:
            deck: str: deck to use
            question: str:question
            answer: str: answer
            tags: extra tags

        Returns:
            result
        """
        payload = self.payload_add_card(deck, question, answer, tags)
        return self.post(payload)

    def add_card_list(self, deck, questions, tags=None):
        """Post multiple questions.

        Args:
            deck: str: deck to use
            questions: array[dict]
            tags: extra tags

        Returns:
            result
        """
        results = []
        for i in questions:
            payload = self.payload_add_card(deck, i["q"], i["a"], tags)
            results.append(self.post(payload))
        return results
