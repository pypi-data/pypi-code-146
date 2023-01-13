
import traits.api as tr

state_change_counter = 0

class ModelNotifyMixin(tr.HasTraits):
    """Mixin for notifications
    """

    name = tr.Str("<unnamed>")

    depends_on = tr.List(tr.Str, [])

    def traits_init(self):
        for name in self.depends_on:
            trait = self.trait(name)
            if trait is None:
                return
                #raise ValueError('no trait named %s' % name)
            trait_type = trait.trait_type
            if trait_type is None:
                raise TypeError('trait type not specified for %s, %s' % self, name)
            # value = self.trait_get(name)
            value = getattr(self, name, None)
            # print('name', name, self.__class__, trait_type, value)
            post_setattr = getattr(trait_type, 'post_setattr', None)
            if post_setattr:
                post_setattr(self, name, value)
#                trait_type.post_setattr(self, name, value)
        return
            # name_ = trait_type.get_name_(name)
            # trait_ = getattr(self, name_, None)
            # if trait_ is None:
            #     value = getattr(self, name, None)
            #     if value:
            #         trait_type.post_setattr(self, name, value)
            # trait_ = getattr(self, name_, None)
            # if trait_:
            #     trait_.parents.add(self)

    parents = tr.Set(tr.WeakRef, {})

    _state_change_debug = tr.Bool(False)

    state_change_debug = tr.Property(tr.Bool)

    def _get_state_change_debug(self):
        if self._state_change_debug == True:
            return True
        for parent in self.parents:
            if parent.state_change_debug == True:
                return True

    def _set_state_change_debug(self, value=True):
        self._state_change_debug = value

    @tr.observe('+TIME,+MESH,+MAT,+CS,+BC,+ALG,+FE,+DSC,+GEO,+ITR')
    def notify_value_change(self, event):
        if self.state_change_debug:
            print('value_changed', self, event)
        self.value_changed = True
        self.state_changed = True
        self.notify_parents_value_changed()

    def notify_graph_change(self, event):
        if self.state_change_debug:
            print('graph_changed', self, event)
        self.graph_changed = True
        self.state_changed = True
        self.notify_parents_graph_changed()

    value_changed = tr.Event
    graph_changed = tr.Event
    state_changed = tr.Event

    @tr.observe('state_changed')
    def record_state_change(self, event):
        global state_change_counter
        state_change_counter += 1

    def reset_state_change(self):
        global state_change_counter
        state_change_counter = 0

    state_change_counter = tr.Property
    def _get_state_change_counter(self):
        global state_change_counter
        return state_change_counter

    def notify_parents_graph_changed(self):
        for parent in self.parents:
            if parent: # ignore if parent is garbage collected
                parent.notify_graph_change('Notification from child %s' % self)

    def notify_parents_value_changed(self):
        for parent in self.parents:
            if parent: # ignore if parent is garbage collected
                parent.notify_value_change('Notification from child %s' % self)

    def __del__(self):
        if self.state_change_debug:
            print('deleting %s', self)