"""src/users/forms.py."""

from django import forms
from django.db import models

from src.users.models import Role
from src.users.models import User


class RoleForm(forms.ModelForm):
    """A form for editing permission fields for a single Role."""

    class Meta:
        """Provide metadata for the RoleForm."""

        model = Role
        # Accessing _meta is a common pattern in Django forms for dynamic fields.
        fields = [
            f.name
            for f in Role._meta.get_fields()  # noqa: SLF001
            if isinstance(f, models.BooleanField)
        ]
        widgets = {
            field: forms.CheckboxInput(attrs={"class": "form-check-input"})
            for field in fields
        }


RoleFormSet = forms.modelformset_factory(Role, form=RoleForm, extra=0)


class CustomUserForm(forms.ModelForm):
    """A custom form for creating and editing users."""

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        """Provide metadata for the CustomUserForm."""

        model = User
        fields = ("email", "first_name", "last_name", "phone", "role", "status")

    def __init__(self, *args, **kwargs):
        """Apply CSS classes to form fields."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            elif field.widget.input_type != "checkbox":
                field.widget.attrs["class"] = "form-control"

    def clean_email(self):
        """Validate that the email is unique."""
        email = self.cleaned_data.get("email")
        error_message = "A user with this email already exists."
        if self.instance.pk:
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(error_message)

        if not self.instance.pk and User.objects.filter(email=email).exists():
            raise forms.ValidationError(error_message)
        return email

    def clean_password2(self):
        """Verify that the entered passwords match."""
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password != password2:
            error_message = "Passwords do not match."
            raise forms.ValidationError(error_message)
        return password2

    def save(self, *, commit: bool = True):
        """Hash the password and set the username before saving."""
        user = super().save(commit=False)

        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)

        if "email" in self.changed_data or not self.instance.pk:
            user.username = self.cleaned_data["email"]

        if commit:
            user.save()
        return user
