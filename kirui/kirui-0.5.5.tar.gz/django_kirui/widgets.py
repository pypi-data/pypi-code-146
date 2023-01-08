from django.forms import widgets


class CheckboxSwitch(widgets.CheckboxInput):
    input_type = 'kr-checkbox-switch'


class SimpleFileInput(widgets.FileInput):
    input_type = 'kr-file'
