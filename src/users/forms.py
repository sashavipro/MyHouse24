"""src/users/forms.py."""

from django import forms
from django.db import models
from django.db.models import Q

from src.building.models import Apartment
from src.building.models import Floor
from src.building.models import House
from src.building.models import Section
from src.users.models import Message
from src.users.models import Role
from src.users.models import Ticket
from src.users.models import User


class RoleForm(forms.ModelForm):
    """A form for editing permission fields for a single Role."""

    class Meta:
        """Provide metadata for the RoleForm."""

        model = Role
        fields = [
            f.name
            for f in model._meta.get_fields()  # noqa: SLF001
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
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password"}
        ),
        required=False,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "new-password"}
        ),
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
        if "email" in self.fields:
            self.fields["email"].widget.attrs["autocomplete"] = "off"

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

    def save(self, *, commit=True):
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

        if queryset.exists():
            error_msg = "An owner with this ID already exists."
            raise forms.ValidationError(error_msg)
        return owner_id

    def clean_password2(self):
        """Verify that the entered passwords match."""
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password != password2:
            error_msg = "Passwords do not match."
            raise forms.ValidationError(error_msg)
        return password2

    def save(self, *, commit=True):
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


class OwnerProfileForm(forms.ModelForm):
    """A form for owners to edit their own profile information."""

    owner_id = forms.CharField(
        label="ID",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Новый пароль",
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
        """Provides metadata for the OwnerProfileForm."""

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
        )
        widgets = {
            "avatar": forms.FileInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "birthday": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "viber": forms.TextInput(attrs={"class": "form-control"}),
            "telegram": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
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
        if queryset.exists():
            error_msg = "A user with this ID already exists."
            raise forms.ValidationError(error_msg)
        return owner_id

    def clean_password2(self):
        """Verify that the entered passwords match."""
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password != password2:
            error_msg = "Пароли не совпадают."
            raise forms.ValidationError(error_msg)
        return password2

    def save(self, *, commit=True):
        """Save the form data to the User model."""
        user = super().save(commit=False)
        owner_id = self.cleaned_data.get("owner_id")
        if owner_id:
            user.user_id = owner_id
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if "email" in self.changed_data:
            user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class MessageForm(forms.ModelForm):
    """Form for creating a new message with advanced recipient filtering."""

    to_debtors = forms.BooleanField(
        label="Владельцам c задолженностью",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    house = forms.ModelChoiceField(
        label="ЖК",
        queryset=House.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    section = forms.ModelChoiceField(
        label="Секция",
        queryset=Section.objects.none(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    floor = forms.ModelChoiceField(
        label="Этаж",
        queryset=Floor.objects.none(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    apartment = forms.ModelChoiceField(
        label="Квартира",
        queryset=Apartment.objects.none(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        """Provides metadata for the MessageForm."""

        model = Message
        fields = ["title", "text"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Тема сообщения"}
            ),
            "text": forms.Textarea(attrs={"class": "tinymce-editor"}),
        }
        labels = {"title": "Тема сообщения", "text": "Текст сообщения"}

    def __init__(self, *args, **kwargs):
        """Initialize form with dynamic querysets based on parent selections."""
        super().__init__(*args, **kwargs)

        self.fields["house"].empty_label = "Всем..."
        self.fields["section"].empty_label = "Всем..."
        self.fields["floor"].empty_label = "Всем..."
        self.fields["apartment"].empty_label = "Всем..."

        if "house" in self.data:
            try:
                house_id = int(self.data.get("house"))
                self.fields["section"].queryset = Section.objects.filter(
                    house_id=house_id
                )
                self.fields["floor"].queryset = Floor.objects.filter(house_id=house_id)
            except (ValueError, TypeError):
                pass

        if "section" in self.data and self.data.get("section"):
            try:
                section_id = int(self.data.get("section"))
                self.fields["apartment"].queryset = Apartment.objects.filter(
                    section_id=section_id
                )
            except (ValueError, TypeError):
                pass

        elif "house" in self.data and self.data.get("house"):
            try:
                house_id = int(self.data.get("house"))
                self.fields["apartment"].queryset = Apartment.objects.filter(
                    house_id=house_id
                )
            except (ValueError, TypeError):
                pass

    def clean(self):
        """Gather all recipients and verify that at least one is selected."""
        cleaned_data = super().clean()

        recipients_qs = User.objects.none()
        filters_applied = False

        location_filters = Q()
        if apartment := cleaned_data.get("apartment"):
            location_filters &= Q(pk=apartment.pk)
            filters_applied = True
        elif floor := cleaned_data.get("floor"):
            location_filters &= Q(floor=floor)
            filters_applied = True
        elif section := cleaned_data.get("section"):
            location_filters &= Q(section=section)
            filters_applied = True
        elif house := cleaned_data.get("house"):
            location_filters &= Q(house=house)
            filters_applied = True

        if filters_applied:
            recipients_qs = User.objects.filter(
                apartments__in=Apartment.objects.filter(location_filters)
            )

        if not filters_applied and not cleaned_data.get("to_debtors"):
            recipients_qs = User.objects.filter(user_type=User.UserType.OWNER)

        if cleaned_data.get("to_debtors"):
            debtor_qs = User.objects.filter(apartments__personal_account__balance__lt=0)
            recipients_qs = (
                (recipients_qs | debtor_qs) if recipients_qs.exists() else debtor_qs
            )

        final_recipients = recipients_qs.distinct()

        if not final_recipients.exists():
            error_msg = "Необходимо выбрать хотя бы одного получателя."
            raise forms.ValidationError(error_msg)

        cleaned_data["final_recipients"] = final_recipients
        return cleaned_data


class TicketForm(forms.ModelForm):
    """Form for creating and editing tickets."""

    class Meta:
        """Meta class."""

        model = Ticket
        fields = [
            "date",
            "time",
            "user",
            "description",
            "apartment",
            "role",
            "status",
            "master",
            "comment",
        ]
        widgets = {
            "date": forms.TextInput(
                attrs={"class": "form-control date-picker", "placeholder": "ДД.ММ.ГГГГ"}  # noqa: RUF001
            ),
            "time": forms.TextInput(
                attrs={
                    "class": "form-control time-picker",
                    "placeholder": "Выберите время",
                }
            ),
            "user": forms.Select(
                attrs={
                    "class": "form-select select2-owner",
                    "data-placeholder": "Выберите владельца...",
                }
            ),
            "apartment": forms.Select(
                attrs={
                    "class": "form-select select2-apartment",
                    "data-placeholder": "Сначала выберите владельца...",
                }
            ),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
            "role": forms.Select(
                attrs={"class": "form-select", "data-placeholder": "Любой специалист"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
            "master": forms.Select(
                attrs={"class": "form-select", "data-placeholder": "Выберите..."}
            ),
            "comment": forms.Textarea(attrs={"class": "tinymce-editor"}),
        }
        labels = {
            "date": "",
            "time": "",
            "user": "Владелец квартиры",
            "description": "Описание",
            "apartment": "Квартира",
            "role": "Тип мастера",
            "status": "Статус",
            "master": "Мастер",
            "comment": "Комментарий",
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form with dynamic querysets for fields."""
        super().__init__(*args, **kwargs)

        self.fields["user"].queryset = User.objects.filter(
            user_type=User.UserType.OWNER
        ).order_by("last_name", "first_name")

        self.fields["master"].queryset = User.objects.filter(
            user_type=User.UserType.EMPLOYEE
        ).order_by("last_name", "first_name")
        self.fields["master"].required = False

        if self.data:
            self.fields["apartment"].queryset = Apartment.objects.all()
        elif self.instance.pk and self.instance.user:
            self.fields["apartment"].queryset = Apartment.objects.filter(
                owner=self.instance.user
            )
        else:
            self.fields["apartment"].queryset = Apartment.objects.none()

    def clean(self):
        """Validate form data ensuring consistency between user and apartment."""
        cleaned_data = super().clean()
        apartment = cleaned_data.get("apartment")
        user = cleaned_data.get("user")

        if not apartment:
            self.add_error("apartment", "Необходимо выбрать квартиру")

        if not user:
            self.add_error("user", "Необходимо выбрать владельца квартиры")

        if apartment and user:
            if apartment.owner != user:
                error_msg = (
                    f"Квартира №{apartment.number} не принадлежит владельцу "
                    f"{user.get_full_name()}."
                )
                raise forms.ValidationError(error_msg)

        return cleaned_data


class MessageToOwnerForm(forms.ModelForm):
    """Form for sending a message to a specific owner (with a dropdown)."""

    owner = forms.ModelChoiceField(
        label="Владелец квартир",
        queryset=User.objects.filter(user_type=User.UserType.OWNER),
        widget=forms.Select(
            attrs={"class": "form-select select2-simple", "style": "width: 100%;"}
        ),
        required=True,
    )

    class Meta:
        """Meta clas."""

        model = Message
        fields = ["title", "text"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Тема сообщения"}
            ),
            "text": forms.Textarea(attrs={"class": "tinymce-editor"}),
        }
        labels = {"title": "Тема сообщения", "text": "Текст сообщения"}


class InviteOwnerForm(forms.Form):
    """Form to send an invitation to a new owner."""

    phone = forms.CharField(
        label="Телефон",
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "+380991234567"}
        ),
    )
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "info@example.com"}
        ),
    )
