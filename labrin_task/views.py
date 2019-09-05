from django.contrib.auth import login, authenticate
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect

from .forms import SignUpForm, SignInForm, ResetPasswordForm, PasswordResetConfirmForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'registration/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


class SignInView(auth_views.LoginView):
    form_class = SignInForm


class ResetPasswordView(auth_views.PasswordResetView):
    form_class = ResetPasswordForm
    template_name = 'registration/password_reset_form.html'
    from_email = 'e.cahangirovtest@gmail.com'
    html_email_template_name = 'registration/password_reset_email.html'


class ConfirmPasswordResetView(auth_views.PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm
    template_name = 'registration/password_reset_confirm.html'

