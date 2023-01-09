from typing import List, Tuple
from django import forms

from django.apps import apps


class DBSchemaSelectionForm(forms.Form):
    # * Get apps with models for selection
    stateful_apps = [app.label for app in apps.get_app_configs() if app.models]
    # * Get model list
    model_list = [app for app in apps.get_models()]
    app_choices: List[Tuple[str, str]] = sorted(
        set(
            (app_name, app_name)
            for app_name in stateful_apps
            if next(apps.get_app_config(app_name).get_models(), None) is not None
        )
    )
    model_choices: List[Tuple[str, str]] = sorted(
        set((model_name._meta.object_name, model_name._meta.object_name) for model_name in model_list)
    )
    selected_apps = forms.MultipleChoiceField(
        choices=app_choices,
        required=False,
        label="Selected apps",
        widget=forms.CheckboxSelectMultiple,
    )
    selected_models = forms.MultipleChoiceField(
        required=False,
        choices=model_choices,
        label="Selected models",
        widget=forms.CheckboxSelectMultiple,
    )
