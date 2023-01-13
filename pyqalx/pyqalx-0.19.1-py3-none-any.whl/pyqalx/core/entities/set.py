from pyqalx.core.entities.item import Item
from pyqalx.core.entities.entity import QalxQueueableEntity


class Set(QalxQueueableEntity):
    """A set is simply a collection of items.

    They are mapped with keys so that you can retrieve specific items from the
    set later:

    >>> from pyqalx import QalxSession
    >>> qalx = QalxSession()
    >>> dims = qalx.item.add(data={"height":5, "width":5}, meta={"shape":"square"})
    >>> steel = qalx.item.add(source="path/to/316_datasheet.pdf",
    ...                       data={"rho":8000, "E":193e9},
    ...                       meta={"library":"materials",
    ...                             "family":"steel", "grade":"316"})
    >>> steel_square_set = qalx.set.add(items={"shape":dims, "material":steel},
    ...                                 meta={"profile":"square_steel"})

    As with items we can then use the ``find_one`` and ``find`` methods to search
    for sets and easily get the item data:.
    You can use attribute style getters/setters or key style getters/setters

    >>> from pyqalx import QalxSession
    >>> qalx = QalxSession()
    >>> my_set = qalx.set.find_one(query={"metadata.data.profile": "square_steel"})
    >>> # Key style
    >>> youngs_mod = my_set.get_item_data("material")['E']
    >>> # Attribute style
    >>> younds_mod = my_set.get_item_data("material").E

    .. note::
        Sets store a **reference to an item** rather than a copy of the item.
        Changes to the item will be reflected in all sets containing that item.

    """

    entity_type = "set"
    child_entity_class = Item

    def get_item_data(self, item_key):
        """
        helper method to get data from an item in the set

        :param item_key: key on the set to add the item as
        :type item_key: str
        :return: dict or None if key is missing
        """
        if self.items_.get(item_key):
            return self.items_.get(item_key)["data"]
        else:
            return None

    @property
    def items_(self):
        """
        Helper to allow easier lookup for items.  A user can continue to do
        `myset['items']` should they choose - but using this property leads to
        neater code.

        Usage: `myset.items_`

        :return: dict
        :raises: KeyError if `items` key doesn't exist on Set
        """
        # We have to use a property rather than an instance attribute even though
        # it's slower because using an instance attribute would prevent the
        # user from doing `Set({})`.
        return self["items"]
