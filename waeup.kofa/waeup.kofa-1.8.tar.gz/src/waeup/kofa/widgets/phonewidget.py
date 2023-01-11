"""A phone number widget.

This widget is an input widget (not made for display forms but for
edit and add forms).

It can be used for :class:`zope.schema.TextLine` fields but has to be
requested by the form manually (otherwise the regular TextLine widget
will be used for rendering).

If you use the PhoneWidget for rendering regular TextLine attributes
(preferably in edit forms or add forms), the phone number is displayed
by three input fields representing the international code, the area
code and the extension line.

When the entered input is stored with a context object, it is stored
as a single unicode string with the numbers divided by single hyphen.

So, input <+12>, <111>, <444> becomes the string ``'+12-111-444'`` for
the context object.
"""
import grok
import re
from zope.component import queryUtility
from zope.formlib.interfaces import MissingInputError, InputErrors
from zope.interface import Interface
from zope.formlib.textwidgets import (
    TextWidget, renderElement, ConversionError)
from waeup.kofa.interfaces import IKofaUtils
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.utils import KofaUtils

RE_INT_PREFIX = re.compile('^\+\d+')
RE_NUMBERS = re.compile('^\d+$')
RE_NUMBERS_AND_HYPHENS = re.compile('^[\d\-]+$')

class PhoneWidget(TextWidget):

    subwidget_names = ('country', 'area', 'ext')
    cssClass = 'phone-input'

    def _renderPrefixWidget(self, value):
        prefix_func = getattr(
            queryUtility(IKofaUtils), 'sorted_phone_prefixes',
            KofaUtils.sorted_phone_prefixes)
        options = []
        for ptitle, pval in prefix_func(request=self.request):
            selected = ''
            if value == pval:
                selected = ' selected="selected" '
            options.append(
                '<option value="%s"%s>%s</option>' % (pval, selected, ptitle))
        options = '\n'.join(options)
        return '<select id="%s" name="%s" size="1" class="%s">\n%s\n</select>' % (
            '%s.%s' % (self.name, 'country'),
            '%s.%s' % (self.name, 'country'),
            self.cssClass,
            options)

    def __call__(self):
        value = self._getFormValue()
        if value is None or value == self.context.missing_value:
            value = ''
        if len(value.split('-')) < 2:
            value = '--' + value
        subvalues = value.split('-', 2)

        kwargs = {'type': self.type,
                  'name': self.name,
                  'id': self.name,
                  'value': value,
                  'cssClass': self.cssClass,
                  'style': self.style,
                  'size': self.displayWidth,
                  'extra': self.extra}
        if self.displayMaxWidth:
            kwargs['maxlength'] = self.displayMaxWidth # TODO This is untested.
        fields = []
        for num, subname in enumerate(self.subwidget_names):
            if num == 0:
                select = self._renderPrefixWidget(subvalues[num])
                fields.append(select)
                continue
                print select
            kwargs.update(name = '%s.%s' % (self.name, subname))
            kwargs.update(id=kwargs['name'])
            kwargs.update(cssClass = '%s %s' % ('', self.cssClass))
            kwargs.update(value = subvalues[num])
            fields.append(renderElement(self.tag, **kwargs))
        return '-'.join(fields)

    def _getFormInput(self):
        """Returns current form input.

        The value returned must be in a format that can be used as the 'input'
        argument to `_toFieldValue`.

        The default implementation returns the form value that corresponds to
        the widget's name. Subclasses may override this method if their form
        input consists of more than one form element or use an alternative
        naming convention.
        """
        result = '-'.join(
            [self.request.get('%s.%s' % (self.name, name), '')
             for name in self.subwidget_names])
        return result

    def _toFieldValue(self, input):
        """Check value entered in form further.

        Raises ConversionError if values entered contain non-numbers.

        For the extension line we silently allow slashes as well.
        """
        # In import files we can use the hash symbol at the end of a
        # date string to avoid annoying automatic number transformation
        # by Excel or Calc
        input = input.strip('#')
        result = super(PhoneWidget, self)._toFieldValue(input)
        parts = input.split('-', 2)
        if '' in parts and self.context.required:
            raise ConversionError(
                _("Empty phone field(s)."), MissingInputError(
                    self.name, self.label, None))
        if parts[0] != '' and not RE_INT_PREFIX.match(parts[0]):
            raise ConversionError(
                _("Int. prefix requires format '+NNN'"),
                ValueError('invalid international prefix'))
        # Make sure there are only numbers in parts 1..N. We do not allow
        # dashes in last field any more.
        errors = [(x != '' and not RE_NUMBERS.match(x)) for x in parts[1:]]
        error = True in errors
        if error:
            raise ConversionError(
                _("Phone numbers may contain numbers only."),
                ValueError('non numbers in phone number'))
        # We consider also values ending with empty ending as missing
        # values.  An 'empty ending' is a form where the fields
        # following the prefix are all empty.  This means that any
        # prefix setting in the form will switch back to default upon
        # submit if no further phone fields are filled.  As advantage
        # we get only valid phone numbers or missing value.
        empty_ending = '-'*(len(parts) - 1)
        if result in ('', None) or result.endswith(empty_ending):
            result = self.context.missing_value
        return result

    def _getFormValue(self):
        """Returns a value suitable for use in an HTML form.

        Detects the status of the widget and selects either the input value
        that came from the request, the value from the _data attribute or the
        default value.
        """
        try:
            input_value = self._getCurrentValueHelper()
        except InputErrors:
            form_value = '-'.join(
                [self.request.form.get('%s.%s' % (self.name, name), '')
                 for name in self.subwidget_names]
                )
        else:
            form_value = self._toFormValue(input_value)
        return form_value

    def hasInput(self):
        """A phone widget has input if all three subfields have input.
        """
        for name in self.subwidget_names:
            if '%s.%s' % (self.name, name) not in self.request.form:
                return False
        return True
