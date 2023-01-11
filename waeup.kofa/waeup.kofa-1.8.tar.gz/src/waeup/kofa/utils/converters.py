## $Id: converters.py 16818 2022-02-21 06:21:10Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""Converters for zope.schema-based datatypes.
"""
import grok
from zope.component import createObject
from zope.formlib import form
from zope.formlib.boolwidgets import CheckBoxWidget
from zope.formlib.form import (
    _widgetKey, WidgetInputError, ValidationError, InputErrors, expandPrefix)
from zope.formlib.interfaces import IInputWidget, ConversionError
from zope.interface import Interface
from zope.publisher.browser import TestRequest
from zope.schema.interfaces import IList
from waeup.kofa.interfaces import (
    IObjectConverter, IResultEntryField, IFieldConverter, SubjectSource,
    GradeSource, DELETION_MARKER, IGNORE_MARKER)
from waeup.kofa.schema.interfaces import IPhoneNumber
from waeup.kofa.schoolgrades import ResultEntry

class ExtendedCheckBoxWidget(CheckBoxWidget):
    """A checkbox widget that supports more input values as True/False
    markers.

    The default bool widget expects the string 'on' as only valid
    ``True`` value in HTML forms for bool fields.

    This widget also accepts '1', 'true' and 'yes' for that. Also all
    uppercase/lowecase combinations of these strings are accepted.

    The widget still renders ``True`` to ``'on'`` when a form is
    generated.
    """
    true_markers = ['1', 'true', 'on', 'yes']

    def _toFieldValue(self, input):
        """Convert from HTML presentation to Python bool."""
        if not isinstance(input, basestring):
            return False
        return input.lower() in self.true_markers

    def _getFormInput(self):
        """Returns the form input used by `_toFieldValue`.

        Return values:

          ``'on'``  checkbox is checked
          ``''``    checkbox is not checked
          ``None``  form input was not provided

        """
        value = self.request.get(self.name)
        if isinstance(value, basestring):
            value = value.lower()
        if value in self.true_markers:
            return 'on'
        elif self.name + '.used' in self.request:
            return ''
        else:
            return None

def getWidgetsData(widgets, form_prefix, data):
    """Get data and validation errors from `widgets` for `data`.

    Updates the dict in `data` with values from the widgets in
    `widgets`.

    Returns a list of tuples ``(<WIDGET_NAME>, <ERROR>)`` where
    ``<WIDGET_NAME>`` is a widget name (normally the same as the
    associated field name) and ``<ERROR>`` is the exception that
    happened for that widget/field.

    This is merely a copy from the same-named function in
    :mod:`zope.formlib.form`. The only difference is that we also
    store the fieldname for which a validation error happened in the
    returned error list (what the original does not do).
    """
    errors = []
    form_prefix = expandPrefix(form_prefix)

    for input, widget in widgets.__iter_input_and_widget__():
        if input and IInputWidget.providedBy(widget):
            name = _widgetKey(widget, form_prefix)

            if not widget.hasInput():
                continue
            try:
                data[name] = widget.getInputValue()
            except ValidationError, error:
                error = ConversionError(u'Validation failed')
                errors.append((name, error))
            except WidgetInputError, error:
                error = ConversionError(u'Invalid input')
                errors.append((name, error))
            except ConversionError, error:
                errors.append((name, error))
    return errors

class DefaultFieldConverter(grok.Adapter):
    grok.context(Interface)
    grok.implements(IFieldConverter)

    def request_data(self, name, value, schema_field, prefix='',
                     mode='create'):
        if prefix == 'form.sex' and isinstance(value, basestring):
            value = value.lower()
        return {prefix: value}

class ListFieldConverter(grok.Adapter):
    grok.context(IList)
    grok.implements(IFieldConverter)

    def request_data(self, name, value, schema_field, prefix='',
                     mode='create'):
        value_type = schema_field.value_type
        try:
            items = eval(value)
        except:
            return {prefix: value}
        result = {'%s.count' % prefix: len(items)}
        for num, item in enumerate(items):
            sub_converter = IFieldConverter(value_type)
            result.update(sub_converter.request_data(
                unicode(num), unicode(item),
                value_type, "%s.%s." % (prefix, num)))
        return result

class PhoneNumberFieldConverter(grok.Adapter):
    """Convert strings into dict as expected from forms feeding PhoneWidget.

    If you want strings without extra-checks imported, you can use
    schema.TextLine in your interface instead of PhoneNumber.
    """
    grok.context(IPhoneNumber)
    grok.implements(IFieldConverter)

    def request_data(self, name, value, schema_field, prefix='',
                     mode='create'):
        parts = value.split('-', 2)
        country = ''
        area = ''
        ext = ''
        if len(parts) == 3:
            country = parts[0]
            area = parts[1]
            ext = parts[2]
        elif len(parts) == 2:
            country = parts[0]
            ext = parts[1]
        else:
            ext = value
        result = {
            u'%s.country' % prefix: country,
            u'%s.area' % prefix: area,
            u'%s.ext' % prefix: ext}
        return result

class ResultEntryConverter(grok.Adapter):
    grok.context(IResultEntryField)
    grok.implements(IFieldConverter)

    def request_data(self, name, value, schema_field, prefix='',
                     mode='create'):
        """Turn CSV values into ResultEntry-compatible form data.

        Expects as `value` a _string_ like ``(u'mysubject',
        u'mygrade')`` and turns it into some dict like::

          {
            'form.grade.subject': u'9234896395...',
            'form.grade.grade': u'7e67e9e777..'
            }

        where the values are tokens from appropriate sources.

        Such dicts can be transformed into real ResultEntry objects by
        input widgets used in converters.
        """
        try:
            entry = ResultEntry.from_string(value)
            subj, grade = entry.subject, entry.grade
        except:
            return {prefix: value}
        # web forms send tokens instead of real values
        s_token = SubjectSource().factory.getToken(subj)
        g_token = GradeSource().factory.getToken(grade)
        result = {
            "%ssubject" % (prefix): s_token,
            "%sgrade" % (prefix): g_token,
            }
        return result

class DefaultObjectConverter(grok.Adapter):
    """Turn string values into real values.

    A converter can convert string values for objects that implement a
    certain interface into real values based on the given interface.
    """

    grok.context(Interface)
    grok.implements(IObjectConverter)

    def __init__(self, iface):
        self.iface = iface
        # Omit known dictionaries since there is no widget available
        # for dictionary schema fields
        self.default_form_fields = form.Fields(iface).omit('description_dict')
        return

    def fromStringDict(self, data_dict, context, form_fields=None,
                       mode='create'):
        """Convert values in `data_dict`.

        Converts data in `data_dict` into real values based on
        `context` and `form_fields`.

        `data_dict` is a mapping (dict) from field names to values
        represented as strings.

        The fields (keys) to convert can be given in optional
        `form_fields`. If given, form_fields should be an instance of
        :class:`zope.formlib.form.Fields`. Suitable instances are for
        example created by :class:`grok.AutoFields`.

        If no `form_fields` are given, a default is computed from the
        associated interface.

        The `context` can be an existing object (implementing the
        associated interface) or a factory name. If it is a string, we
        try to create an object using
        :func:`zope.component.createObject`.

        Returns a tuple ``(<FIELD_ERRORS>, <INVARIANT_ERRORS>,
        <DATA_DICT>)`` where

        ``<FIELD_ERRORS>``
           is a list of tuples ``(<FIELD_NAME>, <ERROR>)`` for each
           error that happened when validating the input data in
           `data_dict`

        ``<INVARIANT_ERRORS>``
           is a list of invariant errors concerning several fields

        ``<DATA_DICT>``
           is a dict with the values from input dict converted.

        If mode is ``'create'`` or ``'update'`` then some additional
        filtering applies:

        - values set to DELETION_MARKER are set to missing_value (or
          default value if field is required) and

        - values set to IGNORE_MARKER are ignored and thus not part of
          the returned ``<DATA_DICT>``.

        If errors happen, i.e. the error lists are not empty, always
        an empty ``<DATA_DICT>`` is returned.

        If ``<DATA_DICT>`` is non-empty, there were no errors.
        """
        if form_fields is None:
            form_fields = self.default_form_fields

        request = TestRequest(form={})
        new_data = dict()
        for key, val in data_dict.items():
            val = val.strip()
            field = form_fields.get(key, None)
            if field is not None:
                # let adapters to the respective schema fields do the
                # further fake-request processing
                schema_field = field.interface[field.__name__]
                field_converter = IFieldConverter(schema_field)
                if mode in ('update', 'create'):
                    if val == IGNORE_MARKER:
                        continue
                    elif val == DELETION_MARKER:
                        val = schema_field.missing_value
                        if schema_field.required:
                            val = schema_field.default
                        new_data[key] = val
                        continue
                request.form.update(
                    field_converter.request_data(
                        key, val, schema_field, 'form.%s' % key)
                    )
            else:
                request.form['form.%s' % key] = val

        obj = context
        if isinstance(context, basestring):
            # If we log initialization transitions in the __init__
            # method of objects, a second (misleading) log entry
            # will be created here.
            obj = createObject(context)

        widgets = form.setUpInputWidgets(
            form_fields, 'form', obj, request)

        errors = getWidgetsData(widgets, 'form', new_data)

        invariant_errors = form.checkInvariants(form_fields, new_data)

        if errors or invariant_errors:
            err_messages = [(key, err.args[0]) for key, err in errors]
            invariant_errors = [err.message for err in invariant_errors]
            return err_messages, invariant_errors, {}

        return errors, invariant_errors, new_data
