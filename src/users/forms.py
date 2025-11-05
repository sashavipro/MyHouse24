"""src/users/forms.py - Fixed version."""

from django import forms
from django.db import models

from src.users.models import Role
from src.users.models import User


class RoleForm(forms.ModelForm):
    """A form for editing permission fields for a single Role."""

    class Meta:
        """Provide metadata for the RoleForm."""

        model = Role
        fields = [
            f.name
            for f in model._meta.fields  # noqa: SLF001
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


class OwnerForm(forms.ModelForm):
    """A form for creating and editing owner users."""

    owner_id = forms.CharField(
        label="ID",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password"}
        ),
        required=False,
    )
    password2 = forms.CharField(
        label="Повторить пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        """Provides metadata for the OwnerForm."""

        model = User
        fields = (
            "avatar",
            "last_name",
            "first_name",
            "middle_name",
            "birthday",
            "description",
            "phone",
            "viber",
            "telegram",
            "email",
            "status",
        )
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Фамилия"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Имя"}
            ),
            "middle_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Отчество"}
            ),
            "birthday": forms.DateInput(
                format="%Y-%m-%d",  # Добавляем формат
                attrs={"class": "form-control", "type": "date"},
            ),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Телефон"}
            ),
            "viber": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Viber"}
            ),
            "telegram": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Telegram"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email (логин)"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "avatar": "Сменить изображение",
            "last_name": "Фамилия",
            "first_name": "Имя",
            "middle_name": "Отчество",
            "birthday": "Дата рождения",
            "description": "O владельце (заметки)",
            "phone": "Телефон",
            "email": "Email (логин)",
            "status": "Статус",
        }

    def __init__(self, *args, **kwargs):
        """Initialize the owner_id field with the model's value when editing."""
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["owner_id"].initial = self.instance.user_id

    def clean_owner_id(self):
        """Validate the uniqueness of the entered ID."""
        owner_id = self.cleaned_data.get("owner_id")
        queryset = User.objects.filter(user_id=owner_id)
        if self.instance and self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        # FIX: TRY003, EM101 - Assign error message to variable
        if queryset.exists():
            error_msg = "An owner with this ID already exists."
            raise forms.ValidationError(error_msg)
        return owner_id

    def clean_password2(self):
        """Verify that the entered passwords match."""  # FIX: D401
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        # FIX: TRY003, EM101 - Assign error message to variable
        if password and password != password2:
            error_msg = "Passwords do not match."
            raise forms.ValidationError(error_msg)
        return password2

    def save(self, *, commit=True):  # FIX: FBT002 - Use keyword-only argument
        """Save the form data to the User model."""
        user = super().save(commit=False)

        owner_id = self.cleaned_data.get("owner_id")
        if owner_id:
            user.user_id = owner_id

        user.birthday = self.cleaned_data.get("birthday")

        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)

        if "email" in self.changed_data or not self.instance.pk:
            user.username = self.cleaned_data["email"]

        if commit:
            user.save()
        return user
