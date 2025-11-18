"""src/core/forms.py."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from hcaptcha.fields import hCaptchaField


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form for administrators with hCaptcha."""

    captcha = hCaptchaField()

    def __init__(self, *args, **kwargs):
        """Add Bootstrap classes to form fields."""
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Email"}
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Пароль"}
        )


class ResidentHCaptchaForm(forms.Form):
    """A simple form to validate hCaptcha for the resident login tab."""

    captcha = hCaptchaField()
