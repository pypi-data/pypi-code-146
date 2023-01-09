from collections import OrderedDict

from django import forms
from django.utils.text import slugify
from wagtail import blocks

from coop.blocks import UnwrappedStreamBlock

from .forms import CustomForm


class BaseFieldBlock(blocks.StructBlock):
    def to_field(self, value):
        defaults = {'label': value['label'], 'required': value['required'],
                    'help_text': value['help_text']}
        field_class = self.get_field_class(value, defaults)
        return slugify(value['label']), field_class(**defaults)

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        field_details = self.to_field(value)
        context.update({
            'field_name': field_details[0],
            'field': field_details[1],
            'bound_field': parent_context['form'][slugify(value['label'])]
        })
        return context

    class Meta:
        abstract = True


class FieldBlock(BaseFieldBlock):
    label = blocks.CharBlock()
    field_type = blocks.ChoiceBlock(choices=[
        ('text', 'Single line text'),
        ('textarea', 'Multi line text'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('time', 'Time'),
        ('checkbox', 'Checkbox'),
    ])
    help_text = blocks.CharBlock(required=False)
    required = blocks.BooleanBlock(default=True, required=False)
    placeholder = blocks.CharBlock(required=False)
    default_value = blocks.CharBlock(required=False)

    def get_field_class(self, value, defaults):
        defaults.update({'initial': value['default_value']})
        field_type = value['field_type']
        widget_props = {'attrs': {'placeholder': value['placeholder']}}
        if field_type == 'textarea':
            defaults.update({'widget': forms.Textarea(**widget_props)})
            return forms.CharField
        elif field_type == 'email':
            defaults.update({'widget': forms.EmailInput(**widget_props)})
            return forms.EmailField
        elif field_type == 'number':
            defaults.update({'widget': forms.NumberInput(**widget_props)})
            return forms.IntegerField
        elif field_type == 'date':
            widget_props['attrs']['type'] = 'date'
            defaults.update({'widget': forms.DateInput(**widget_props)})
            return forms.DateField
        elif field_type == 'time':
            widget_props['attrs']['type'] = 'time'
            defaults.update({'widget': forms.TimeInput(**widget_props)})
            return forms.TimeField
        elif field_type == 'checkbox':
            return forms.BooleanField
        # Default - assume text field
        defaults.update({
            'widget': forms.TextInput(**widget_props)
        })
        return forms.CharField

    class Meta:
        icon = 'fa-edit'
        template = 'blocks/form/form_field.html'


class ChoiceFieldBlock(BaseFieldBlock):
    label = blocks.CharBlock()
    field_type = blocks.ChoiceBlock(choices=[
        ('select', 'Dropdown'),
        ('checkbox', 'Checkboxes'),
        ('radio', 'Radio buttons'),
    ])
    choices = blocks.ListBlock(blocks.CharBlock(icon='fa-square-o'))
    help_text = blocks.CharBlock(required=False)
    required = blocks.BooleanBlock(default=True, required=False)

    def get_field_class(self, value, defaults):
        widget = {
            'select': forms.widgets.Select(),
            'checkbox': forms.widgets.CheckboxSelectMultiple(),
            'radio': forms.widgets.RadioSelect(),
        }[value['field_type']]
        defaults.update({
            'choices': [(c, c) for c in value['choices']],
            'widget': widget
        })
        if value['field_type'] == 'checkbox':
            return forms.MultipleChoiceField
        return forms.ChoiceField

    class Meta:
        icon = 'fa-check-square-o'
        template = 'blocks/form/form_field.html'


class FileFieldBlock(BaseFieldBlock):
    label = blocks.CharBlock()
    help_text = blocks.CharBlock(required=False)
    required = blocks.BooleanBlock(default=True, required=False)

    def get_field_class(self, value, defaults):
        return forms.FileField

    class Meta:
        icon = 'fa-file'
        template = 'blocks/form/file_upload.html'


class HeadingBlock(blocks.CharBlock):
    class Meta:
        template = 'blocks/form/form_heading.html'
        icon = 'fa-header'


class FormBlocks(UnwrappedStreamBlock):
    basic_field = FieldBlock()
    choice_field = ChoiceFieldBlock()
    file_field = FileFieldBlock()
    heading = HeadingBlock()

    def get_fields_from_blocks(self, blocks):
        for child in blocks:
            block = child.block
            if hasattr(block, 'to_field'):
                yield block.to_field(child.value)

    def get_form(self, blocks, **kwargs):
        extra_fields = OrderedDict(self.get_fields_from_blocks(blocks))
        return CustomForm(extra_fields, **kwargs)

    class Meta:
        icon = 'fa-pencil'


class FormStreamBlock(UnwrappedStreamBlock):
    form = FormBlocks()

    class Meta:
        block_counts = {
            'form': {
                'max_num': 1,
            }
        }
