import datetime

from django.core.files.uploadedfile import UploadedFile
from django.forms import widgets, fields
from django.templatetags.l10n import unlocalize

from samon.elements import BaseElement, AnonymusElement
from samon.constants import XML_NAMESPACE_DATA_BINDING
from samon.expressions import Bind
from samon.render import RenderedElement
from django_kirui.widgets import CheckboxSwitch


widgets.TextInput.input_type = 'kr-input'
widgets.NumberInput.input_type = 'kr-number-input'
widgets.Select.input_type = 'kr-select'
widgets.SelectMultiple.input_type = 'kr-multi-select-checkbox'
widgets.CheckboxSelectMultiple.input_type = 'kr-multi-select-checkbox'
widgets.CheckboxInput.input_type = 'kr-checkbox-switch'
widgets.DateInput.input_type = 'kr-date-picker'
widgets.Textarea.input_type = 'kr-textbox'


class RenderedField(RenderedElement):
    def _eval_node_attributes(self, context) -> dict:
        retval = super(RenderedField, self)._eval_node_attributes(context)
        self.bf: fields.BoundField = retval.pop('boundField')

        retval['value'] = self.bf.value()
        if retval['value'] is None:
            retval['value'] = ''

        # TODO: serializálásnál a datetime nem alakítható JSON-ná, ezt az átalakítást máshova kellene tenni
        if 'value' in retval.keys():
            if isinstance(retval['value'], (datetime.datetime, datetime.date)):
                retval['value'] = retval['value'].strftime('%Y-%m-%d')
            elif isinstance(retval['value'], UploadedFile):
                retval['value'] = ''

        if self.bf.name in self.bf.form.errors.keys():
            retval['error'] = list(self.bf.form.errors[self.bf.name])[0]

        retval['widget'] = self.bf.field.widget.input_type

        if self.bf.field.label:
            retval['label'] = self.bf.field.label

        retval['required'] = self.bf.field.required
        retval['field_id'] = f'id_{self.bf.name}'
        retval['name'] = self.bf.name
        retval['disabled'] = int(self.bf.field.disabled)
        # retval['onChange'] = f"{retval.pop('formReactContextRef')}.handleInputChange"

        return retval

    @property
    def children(self):
        if choices := getattr(self.bf.field, 'choices', None):
            value = self.node_attributes.get('value', None)
            if isinstance(value, (list, tuple)):
                value = [unlocalize(_) for _ in value]
            else:
                value = unlocalize(value)

            for choice in choices:
                if self.node_attributes['widget'] == 'kr-multi-select-checkbox':
                    el = BaseElement(xml_tag='kr-option-checkbox', xml_attrs={})
                else:
                    el = BaseElement(xml_tag='option', xml_attrs={})

                if hasattr(choice[0], 'value'):
                    el.xml_attrs['value'] = choice[0].value or ''
                else:
                    el.xml_attrs['value'] = choice[0] or ''

                if isinstance(value, list) and unlocalize(el.xml_attrs['value']) in value or value == unlocalize(el.xml_attrs['value']):
                    el.xml_attrs['selected'] = True

                el.children = [AnonymusElement(choice[1])]
                yield RenderedElement(el, context=self._context)

        for child in super().children:
            yield child


class KrField(BaseElement):
    RENDERED_ELEMENT_CLASS = RenderedField
    TAG_NAME = 'kr-form-field'


class RenderedForm(RenderedElement):
    @property
    def children(self):
        if self._element.context_var_name:
            form_obj = self._context[self._element.context_var_name]

            for name, field in form_obj.fields.items():
                bf = form_obj[name]
                xml_attrs = {
                    (None, 'name'): name,
                    (None, 'boundField'): bf,
                    # (None, 'formReactContextRef'): self._element.xml_attrs['reactContextRef'],
                    (None, 'field-width'): self._element.xml_attrs['field-width']
                }
                if bf.field.label:
                    xml_attrs[(None, 'label-width')] = self._element.xml_attrs['label-width']

                kr_field = KrField(xml_tag=KrField.TAG_NAME, xml_attrs=xml_attrs)
                yield RenderedField(kr_field, self._context)

        for child in super().children:
            yield child


class KrForm(BaseElement):
    RENDERED_ELEMENT_CLASS = RenderedForm

    def _parse_xml_attrs(self, xml_attrs):
        attrs = super()._parse_xml_attrs(xml_attrs)

        form_obj = attrs.pop(f'{{{XML_NAMESPACE_DATA_BINDING}}}object', None)
        if form_obj is None:
            var_name = None
        else:
            var_name = form_obj.expr

        if 'method' not in attrs.keys():
            attrs['method'] = 'POST'

        if f'{{{XML_NAMESPACE_DATA_BINDING}}}csrfmiddlewaretoken' not in attrs.keys():
            attrs[f'{{{XML_NAMESPACE_DATA_BINDING}}}csrfmiddlewaretoken'] = Bind(expr='djsamon.csrf_token')

        #if 'reactContextRef' not in attrs.keys():
        #    attrs['reactContextRef'] = var_name

        #if 'whenSubmit' not in attrs.keys():
        #    attrs['whenSubmit'] = f"{attrs['reactContextRef']}.handleSubmit"

        self.context_var_name = var_name
        return attrs
