from commons.python.decorators import redirect_authenticated_user
from commons.python.helper import is_post_method
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from account.python.form import CustomAuthenticationForm, CustomPasswordChangeForm, CustomPasswordResetForm
from account.python.form import CustomSetPasswordForm, UserRegistrationForm
from account.python import static_messages as stm, smtp
from core.settings import HOME_REDIRECT


class CustomLoginView(LoginView, FormView):
    form_class = CustomAuthenticationForm


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = HOME_REDIRECT


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = '/account/login/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, stm.user_restore_password_send_email)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def create_email(self, request, form: UserRegistrationForm):
        html_content = render_to_string(self.html_email_template_name, context=request)
        text_content = strip_tags(html_content)
        subject = form.cleaned_data.get('username')
        to = form.cleaned_data.get('email')
        smtp.send_html_email(subject, text_content, to, html_content)
        # smtp.send_email(subject, None, to, self.html_email_template_name)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = '/account/login/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.success(request, stm.user_restore_password_success)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def dashboard(request):
    return redirect(HOME_REDIRECT)


@redirect_authenticated_user(redirect_to=HOME_REDIRECT)
def signup_view(request):
    if is_post_method(request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data.get('password'))
            new_user.save()
            messages.success(request, stm.user_registration_success)
            return redirect('account:login')
        else:
            messages.error(request, stm.user_registration_invalid_form)
            return redirect(request, template_name='account/register.html', context={'user_form': user_form})

    user_form = UserRegistrationForm()
    context = {'user_form': user_form}
    return render(request, template_name='account/register.html', context=context)


@login_required
def dummy_view(request):
    return render(request, template_name='account/dummy.html', context={'section': 'dummy'})
