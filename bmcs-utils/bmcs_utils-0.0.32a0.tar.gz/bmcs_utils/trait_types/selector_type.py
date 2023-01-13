# -------------------------------------------------------------------------
#
# Copyright (c) 2009, IMB, RWTH Aachen.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in simvisage/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.simvisage.com/licenses/BSD.txt
#
# Thanks for using Simvisage open source!
#
# Created on Aug 7, 2009 by: rchx

from .trait_types import TraitBase
from traits.api import TraitType, TraitError
from bmcs_utils.editors import EitherTypeEditor


class Selector(TraitBase, TraitType):
    """Property trait."""

    editor_factory = EitherTypeEditor

    info_text = 'Property trait test'

    def __init__(self, options=[], on_option_change=None, **metadata):
        # validate that these are trait types
        self.options_dict = {key: value for key, value in options}
        self.on_option_change = on_option_change
        metadata.update({'options': options})
        super().__init__(**metadata)
        self.map = {}

    def validate(self, object, name, value):
        if value in self.options_dict:
            return value
        self.error(object, name, value)

    def set(self, obj, name, value):
        self.pre_setattr(obj, name)
        # setattr(self, name, value)
        self.set_value(obj, name, value)
        self.post_setattr(obj, name, value)

    def pre_setattr(self, object, name):
        if name in object.children:
            selector_trait = object.trait(name)
            if selector_trait:
                old_value = selector_trait.val
                if old_value:
                    old_value.parents.remove(object)

    def post_setattr(self, object, name, value):
        self.pre_setattr(obj, name)
        # check if the last instance of the klass has been
        # registered earlier in the trait history
        klass = self.options_dict.get(value, None)
        sub_obj = klass()
        # set the shadow attribute
        # editor uses it to associate the value with the option.
        selector_trait = object.trait(name)
        selector_trait.obj = sub_obj
#        setattr(object, name + "_", new_value)
        if name in object.children:
            sub_obj.parents.add(object)
            object.notify_graph_change('Notification from child %s' % sub_obj)
        if self.on_option_change:
            getattr(object, self.on_option_change)()

    def get_name_(self, name):
        return name

    def get(self, obj, name):
        val = self.get_value(obj, name)
        if val is None:
            val = self.default_value
        return val

    def get_default_value(self):
        '''Take the first class to construct the value'''
        key, _ = self.options[0]
        return (0, key)

    def full_info(self, object, name, value):
        """ Returns a description of the trait.
        """
        values = self.options_dict
        return " or ".join([repr(x) for x in values])
