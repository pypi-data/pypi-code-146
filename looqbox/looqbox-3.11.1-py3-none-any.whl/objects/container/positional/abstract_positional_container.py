import re

from looqbox.objects.component_utility.css_option import CssOption as css
from looqbox.objects.container.abstract_container import AbstractContainer
from looqbox.render.abstract_render import BaseRender
from abc import abstractmethod


class AbstractPositionalContainer(AbstractContainer):
    def __init__(self, *children, **properties):
        """
        :param children: Children to be contained.
        """
        super().__init__(*children, **properties)

    @abstractmethod
    def to_json_structure(self, visitor: BaseRender):
        """
        Convert python objects into json to Front-End render
        """

    @property
    def set_main_alignment_start(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.flex_start)
        return self

    @property
    def set_cross_alignment_start(self):
        self.css_options = css.add(self.css_options, css.AlignContent.flex_start)
        self.css_options = css.add(self.css_options, css.AlignItems.flex_start)
        return self

    @property
    def set_main_alignment_space_around(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.space_around)
        return self

    @property
    def set_cross_alignment_space_around(self):
        self.css_options = css.add(self.css_options, css.AlignContent.space_around)
        self.css_options = css.add(self.css_options, css.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_space_between(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.space_between)
        return self

    @property
    def set_cross_alignment_space_between(self):
        self.css_options = css.add(self.css_options, css.AlignContent.space_between)
        self.css_options = css.add(self.css_options, css.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_space_evenly(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.space_evenly)
        return self

    @property
    def set_cross_alignment_space_evenly(self):
        self.css_options = css.add(self.css_options, css.AlignContent.space_evenly)
        self.css_options = css.add(self.css_options, css.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_center(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.center)
        return self

    @property
    def set_cross_alignment_center(self):
        self.css_options = css.add(self.css_options, css.AlignContent.center)
        self.css_options = css.add(self.css_options, css.AlignItems.stretch)
        return self

    @property
    def set_main_alignment_end(self):
        self.css_options = css.add(self.css_options, css.JustifyContent.flex_end)
        return self

    @property
    def set_cross_alignment_end(self):
        self.css_options = css.add(self.css_options, css.AlignContent.flex_end)
        self.css_options = css.add(self.css_options, css.AlignItems.stretch)
        return self

    @property
    def add_border(self):
        self.css_options = css.add(self.css_options, css.Border("1px solid #DBDBDB"))
        self.css_options = css.add(self.css_options, css.BoxShadow("0px 4px 6px rgb(31 70 88 / 4%)"))
        self.css_options = css.add(self.css_options, css.BorderRadius("10px"))
        return self

    @staticmethod
    def _divide_value(value):
        numbers = re.findall(r"\d+", value)
        if len(numbers) == 0:
            raise ValueError("Value should contain a number")
        temp_value = round(int(numbers[0]) / 2, 2)
        value = re.sub(r"\d+", str(temp_value), value)
        return value

    def _add_inbetween_pars(self, first_par, second_par):
        num_children = len(self.children)
        for idx in range(num_children):
            not_first = idx > 0
            not_last = idx < num_children - 1
            current_child = self.children[idx]

            if not_first:
                current_child.css_options = css.add(current_child.css_options, first_par)

            if not_last:
                current_child.css_options = css.add(current_child.css_options, second_par)

    def set_horizontal_child_spacing(self, value):

        value = self._divide_value(value)
        margin_left = css.Margin.left("{value}".format(value=value))
        margin_right = css.Margin.right("{value}".format(value=value))

        self._add_inbetween_pars(margin_left, margin_right)
        return self

    def set_vertical_child_spacing(self, value):

        value = self._divide_value(value)
        margin_top = css.Margin.top("{value}".format(value=value))
        margin_bottom = css.Margin.bottom("{value}".format(value=value))

        self._add_inbetween_pars(margin_top, margin_bottom)

        return self

    def set_to_all_child(self, css_option):
        for child in self.children:
            child.css_options = css.add(child.css_options, css_option)
        return self

    def _remove_constraint(self, constraint):
        self.obj_class = [e for e in self.obj_class or [] if constraint not in e]

    def _set_single_constraint(self, value, constraint):
        if value not in list(range(1, 13)):
            raise ValueError("Invalid constraint, must be between 1 and 12 - Received: {value}".format(value=value))
        self.obj_class = (self.obj_class or []) + [constraint + "-" + str(value)]
        self.css_options = css.add(self.css_options, css.Padding("0px"))

    def _set_constraints(self, value, constraint):
        self._remove_constraint(constraint)
        self._set_single_constraint(value, constraint)
        return self

    def set_size(self, value, constraints=("col-md", "col-sm", "col-xs")):
        for constraint in constraints:
            self._set_constraints(value, constraint)
        return self

    def set_desktop_size(self, value):
        return self.set_size(value, constraints=["col-md"])

    def set_tablet_size(self, value):
        return self.set_size(value, constraints=["col-sm"])

    def set_mobile_size(self, value):
        return self.set_size(value, constraints=["col-xs"])
