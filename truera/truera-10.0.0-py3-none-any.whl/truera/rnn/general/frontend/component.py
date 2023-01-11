from abc import ABC
from abc import abstractmethod
from collections import deque
from collections import namedtuple
from itertools import chain

from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State


class ComponentData(object):
    pass


def data(component=None, *argv, **kwargs):
    # component is the component which handles the data stored in this class.

    class DataClass(ComponentData, namedtuple(*argv, **kwargs)):
        pass

    DataClass.component = component

    return DataClass


class Component(ABC):
    """Purely python-based custom components. The purpose of this class is 1) combine dash/html bits
    into coherent components defined in one spot (a subclass definition) and 2) to provide a
    convenient way to refer to the data used by the component in callback definitions. The first
    purpose is accomplished by subclassing from this class and putting all of the relevant
    dash/html generation in its render method. The second point is accomplished by this class
    keeping track of data element names used by its content. It uses these (see element_names) to
    construct dash callback inputs/outputs for all of the contained elements without having to list
    them all. It boxes them up automatically in the Component.Data class which is a namedtuple for
    convnient access. It further unboxes it up when returning from a callback when used in the
    output position. To use, include a Component in a callback's input/output/state list. Make sure
    you use App class as it overrides callback method to add the special handling.

    The Component now supports nested components, in that elements of this component can also be of
    type Component. However, there are restrictions. The subcomponents must be known and specified
    as part of the elements field before any callbacks can be processed. Subcomponents must also be
    immediate children of the parent. That is, you cannot have a component where an element is a
    tuple, whose element is a component.
    """

    def __init__(self, id=None, element_names=[], ui_element_names=[]):
        if id is None:
            id = "NOID"

        self.id = id  # Id must be unique for each Component of the same class.

        self.element_names = element_names
        # Data element names.

        self.ui_element_names = ui_element_names
        # Non-data element names. Ui elements are not passed to and from callbacks.

        self.Data = data(
            component=self,
            typename=self.__class__.__name__,
            field_names=self.element_names
        )
        self.Data.__new__.__defaults__ = (None,) * len(self.element_names)

        # Class, subclass of namedtuple, for accessing this Component's data in callbacks. If you
        # specify this Component as a callback input/state, you will be provided an instance of
        # self.Data which bundles all of the components data. If you specify callback output as
        # Component, you need to return an instance of self.Data which will be unwrapped for you to
        # Dash's expected form. The last element of the data namedtuple is this Component itself if
        # you need it. Values in Data are not known statically but are only filled in when
        # processing callbacks. Note however that we are also using this Data class for handling
        # subcomponents as noted below.

        self.elements = self.Data()
        # Store any elements that are subcomponents here. Everything that is not Component can be
        # left as None. Note that this namedtuple does not need to be filled EXCEPT if some
        # elements of this component are components themselves.

    def __str__(self):
        return f"{self.__class__.__name__}-{self.id}"

    def _element_id(self, element_name):
        return f"{self.__class__.__name__}-{self.id}-{element_name}"

    def _box(self, element_name, box, field="value"):
        return box(self._element_id(element_name), field)

    def _boxs(self, box, element_names=None, field="value"):
        if element_names is None:
            element_names = self.element_names
        return list(
            chain.from_iterable(
                self._expand_one(getattr(self.elements, element_name), box)
                if isinstance(getattr(self.elements, element_name), Component)
                else [box(self._element_id(element_name), field)]
                for element_name in element_names
            )
        )

    def input(self, element_name, field="value"):
        return self._box(element_name, Input, field=field)

    def inputs(self, element_names=None, field="value"):
        return self._boxs(Input, element_names=element_names, field=field)

    def output(self, element_name, field="value"):
        return self._box(element_name, Output, field=field)

    def outputs(self, element_names=None, field="value"):
        return self._boxs(Output, element_names=element_names, field=field)

    def state(self, element_name, field="value"):
        return self._box(element_name, State, field=field)

    def states(self, element_names=None, field="value"):
        return self._boxs(State, element_names=element_names, field=field)

    @classmethod
    def _expand(cls, ls, box):
        return list(chain.from_iterable(cls._expand_one(l, box) for l in ls))

    @classmethod
    def _expand_one(cls, l, box):
        return l._boxs(box) if isinstance(l, Component) else [l]

    @classmethod
    def collapse_args(cls, inputs, args):
        """Transforms an unstructured callback method argument list into a structured version containing
        Component.Data where indicated by inputs list. Given a list of callback inputs (inputs)
        that may contain Components, and values for those inputs (args), produces a collapsed
        version of the args by nesting the raw arguments inside the Data class of the corresponding
        components. The dual of expand_outputs which then reverses the process on a callback
        method's outputs.
        """

        args_expanded = []

        if not isinstance(args, deque):
            args = deque(args)

        def recur(ele):
            if isinstance(ele, Component):
                return [
                    ele.Data(*(cls.collapse_args(list(ele.elements), args)))
                ]
            else:
                return [args.popleft()]

        for input in inputs:
            args_expanded += recur(input)

        return args_expanded

    @classmethod
    def expand_outputs(cls, outs, multiple=True):
        """Given a list of callback method outputs that may contain compound ComponentData, produces a
        flattened version that contains the same as list of non-compound (not ComponentData)
        elements by repeatedly expanding the elements inside ComponentData's. The dual of
        collapse_args.

        """

        ret = list(
            chain.from_iterable(
                (
                    map(Component.expand_outputs, t[:])
                    if isinstance(t, ComponentData) else [t]
                    for t in (outs if multiple else [outs])
                )
            )
        )
        return ret

    @classmethod
    def expand_callback(cls, inputs, output, state):
        return dict(
            inputs=Component._expand(inputs, Input),
            output=Component._expand(output, Output),
            state=Component._expand(state, State)
        )

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def register(self):
        pass

    @abstractmethod
    def deregister(self):
        pass
