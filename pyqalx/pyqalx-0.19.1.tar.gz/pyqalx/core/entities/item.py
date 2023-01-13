from pyqalx.core.entities import QalxListEntity
from pyqalx.core.entities.entity import QalxFileEntity, QalxQueueableEntity


class Item(QalxFileEntity, QalxQueueableEntity):
    """An item is the core of qalx.

    They are structured data or a file or some combination of the two. For example:

    >>> from pyqalx import QalxSession
    >>> qalx = QalxSession()
    >>> dims = qalx.item.add(data={"height":5, "width":5}, meta={"shape":"square"})
    >>> steel = qalx.item.add(source="path/to/316_datasheet.pdf",
    ...                       data={"rho":8000, "E":193e9},
    ...                       meta={"library":"materials",
    ...                             "family":"steel",
    ...                             "grade":"316"})

    We can then use the ``find_one`` and ``find`` methods to search for items

    >>> from pyqalx import QalxSession
    >>> qalx = QalxSession()
    >>> steel_316_item = qalx.item.find_one(query={"metadata.data.library": "materials",
    ...                                            "metadata.data.family": "steel",
    ...                                            "metadata.data.grade": "316"})
    >>> steels = qalx.item.find(query={"metadata.data.family": "steel"})
    >>> squares = qalx.item.find(query={"metadata.data.shape": "square"})
    >>> quads = qalx.item.find(query={"$or": [{"metadata.data.shape": "square"},
    ...                                       {"metadata.data.shape": "rectangle"}]})

    We can edit an item once we have retrieved it and save it back to qalx.
    You can either use attribute style getters/setters (my_shape.data.height = 10)
    or key style getters/setters (my_shape['data']['height'] = 10)

    >>> from pyqalx import QalxSession
    >>> qalx = QalxSession()
    >>> my_shape = qalx.item.find_one(query={"data.height": 5, "data.width": 5})
    >>> my_shape.data.height = 10
    >>> my_shape.meta.shape = 'rectangle'
    >>> qalx.item.save(my_shape)
    >>> # If we think that someone else might have edited my_shape we can reload it:
    >>> my_shape = qalx.item.reload(my_shape)
    """

    entity_type = "item"


class ItemAddManyEntity(QalxListEntity):
    """
    The entity that gets returned when the
    :meth:`~pyqalx.core.adapters.item.QalxItem.add_many` method is called
    """

    _data_key = "items"

    @property
    def items_(self):
        """
        Helper to allow easier lookup for items.  A user can continue to do
        `resp['items']` should they choose - but using this property leads to
        neater code.

        Usage: `resp.items_`

        :return: dict
        :raises: KeyError if `items` key doesn't exist on ItemAddManyEntity
        """
        # We have to use a property rather than an instance attribute even though
        # it's slower because using an instance attribute would cause problems
        # if `add_many` has some items that can't be added (as these get removed
        # from the `items` dict after instantition)
        return self[self._data_key]
