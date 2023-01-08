from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UsernameField, PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from account.python import static_messages


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": 'form-control', 'placeholder': 'Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": 'form-control', 'placeholder': 'Password confirmation'}),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Passwords don't match.")
        return cd.get('password2')


class CustomUsernameField(UsernameField):
    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            "autocapitalize": "none",
            "autocomplete": "off",
            "required": "true",
            "class": "form-control",
            "placeholder": "username"
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = CustomUsernameField()
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "off",
                                          "class": "form-control",
                                          "placeholder": "********"}),
    )

    error_messages = {
        "invalid_login": _(static_messages.invalid_login),
        "inactive": _(static_messages.inactive),
    }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autofocus": True, "class": "form-control", "placeholder": "Old password"}),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": 'form-control', 'placeholder': 'New Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": 'form-control', 'placeholder': 'New Password2'}),
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", 'class': 'form-control', 'placeholder': 'New Password2'}),
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": 'form-control', 'placeholder': 'New Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": 'form-control', 'placeholder': 'New Password2'}),
    )
