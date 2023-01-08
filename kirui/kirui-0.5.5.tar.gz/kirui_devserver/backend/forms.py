import datetime

from django import forms
from django.forms import widgets
from django_kirui.widgets import CheckboxSwitch, SimpleFileInput
from kirui_devserver.backend.models import Topic, Activity


class SampleForm(forms.ModelForm):
    elso = forms.CharField(label='Első mező', required=True, disabled=False, initial='charfield')
    masodik = forms.ChoiceField(label='Második mező', choices=[(None, '-----------------'), (1, 'One'), (2, 'Two'), (3, 'Three')], initial=2)
    harmadik = forms.MultipleChoiceField(label='Harmadik', choices=[(1, "One\\aaaasdfsdfsdf'"), (2, 'Two'), (3, 'Three')], initial=[2, 3],
                                         widget=widgets.CheckboxSelectMultiple, disabled=False, required=True)
    negyedik = forms.BooleanField(label='Negyedik mező', widget=CheckboxSwitch, disabled=False, initial=True)
    otodik = forms.CharField(label='Ötödik', widget=widgets.Textarea, initial='<b>asdf</b>', disabled=False)
    hatodik = forms.IntegerField(label='Hatodik', disabled=False)
    hetedik = forms.DateField(label='Hetedik', disabled=False, initial=datetime.date.today())
    nyolcadik = forms.FileField(label='Nyolcadik', widget=SimpleFileInput)
    hetedik_b = forms.DateField(label='Hetedik (b)', disabled=False, initial=datetime.date.today())

    class Meta:
        model = Activity
        fields = [] #'topics', 'reason'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #for i in range(0, 80):
        #    self.fields[f'field_{i}'] = forms.BooleanField(label='Negyedik mező', disabled=False)  # widget=CheckboxSwitch,
        # self.fields['elso'].initial = str(datetime.datetime.now())


class FilterForm(forms.Form):
    field = forms.CharField(label='Filter field', required=False)
