from collections import namedtuple

from pyqalx.core.adapters.adapter import QalxAdapter
from pyqalx.core.errors import QalxInvalidTagError, QalxAPIResponseError


class Tags(list):
    """
    Tags are a list of Tag() instances.

    These tags are then used on every `add` and `save` request for the
    duration of the session.
    Each individual tag is instantiated as a Tag instance to handle validation
    to ensure they are in the correct format.
    To add new tags to a session do `session.tags.add(name='<name>',
                                                      value='<value>')`
    """

    def __init__(self, *args, **kwargs):
        # rest_api is required to validate tags
        self.rest_api = kwargs.pop("rest_api")

        super(Tags, self).__init__(*args, **kwargs)

        self._make_iterable(self)

    def _make_tag(self, name, value, validate=True):
        """
        Helper method for converting a name & value into a namedtupled and
        then to a dictionary to be added to `Tags`
        :param name: The value for the `name` key on a Tag
        :param value: The value for the `value` key on a Tag
        :return: A dict
        """
        tag = dict(
            Tag(
                name=name.lower().strip(), value=value.lower().strip()
            )._asdict()
        )
        if validate:
            # We don't always validate (i.e. if this was called from
            # `_make_iterable`) as we can validate all tags in a single request
            # on the `_make_iterable` method.
            self._validate(tag)
        return tag

    def _make_iterable(self, iterable):
        """
        Mutates the given iterable to ensure that the keys on it our
        valid for a `Tag`
        """
        for index, tag in enumerate(iterable):
            iterable[index] = self._make_tag(validate=False, **tag)

        self._validate(iterable)

    def _validate(self, tags):
        """
        Makes an API request that validates that the user has
        permission to write to the given tags
        """
        if not isinstance(tags, list):
            tags = [tags]
        if len(tags):
            # Non standard endpoint so cannot use a QalxSession instance
            success, data = self.rest_api.post(
                "tags/validate", json={"tags": tags}
            )
            if not success:
                try:
                    QalxAdapter.raise_api_response_error(data)
                except QalxAPIResponseError as exc:
                    raise QalxInvalidTagError(exc)

    def add(self, name, value):
        """
        A helper method to make it easier for users to add tags.
        :param name: The name of the tag
        :param value: The value of the tag
        """
        super(Tags, self).append(self._make_tag(name=name, value=value))

    def append(self, p_object):
        super(Tags, self).append(self._make_tag(**p_object))

    def insert(self, index, p_object):
        super(Tags, self).insert(index, self._make_tag(**p_object))

    def extend(self, iterable):
        self._make_iterable(iterable)
        super(Tags, self).extend(iterable)

    def __add__(self, iterable):
        self._make_iterable(iterable)
        super(Tags, self).__add__(iterable)

    def __iadd__(self, iterable):
        self._make_iterable(iterable)
        super(Tags, self).__iadd__(iterable)

    def _query(self):
        """
        Returns the tags in a format for querying
        """
        return [
            {
                "tags": {
                    "$elemMatch": {
                        "name": p["name"].lower().strip(),
                        "value": p["value"].lower().strip(),
                    }
                }
            }
            for p in self
        ]


# An individual tag is just a namedtuple with a "name" and "value" key.
# These get converted to `OrderedDict` when being added to `Tags`
Tag = namedtuple("Tag", ["name", "value"])
