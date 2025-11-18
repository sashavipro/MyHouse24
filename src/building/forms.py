"""src/building/forms.py."""

from django import forms
from django.db.models import Q

from src.users.models import User

from .models import Apartment
from .models import Floor
from .models import House
from .models import HouseStaff
from .models import PersonalAccount
from .models import Section


class HouseForm(forms.ModelForm):
    """A form for the main fields of a House object."""

    class Meta:
        """Provide metadata for the HouseForm."""

        model = House
        fields = ["title", "address", "image1", "image2", "image3", "image4", "image5"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "image1": forms.FileInput(attrs={"class": "form-control"}),
            "image2": forms.FileInput(attrs={"class": "form-control"}),
            "image3": forms.FileInput(attrs={"class": "form-control"}),
            "image4": forms.FileInput(attrs={"class": "form-control"}),
            "image5": forms.FileInput(attrs={"class": "form-control"}),
        }


class SectionForm(forms.ModelForm):
    """A form for a single Section within a house."""

    class Meta:
        """Provide metadata for the SectionForm."""

        model = Section
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Название"}
            ),
        }


class FloorForm(forms.ModelForm):
    """A form for a single Floor within a house."""

    class Meta:
        """Provide metadata for the FloorForm."""

        model = Floor
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Название"}
            ),
        }


class HouseStaffForm(forms.ModelForm):
    """A form for assigning a staff member to a house."""

    class Meta:
        """Provide metadata for the HouseStaffForm."""

        model = HouseStaff
        fields = ["user", "role_in_house"]
        widgets = {
            "user": forms.Select(attrs={"class": "form-select user-select"}),
            "role_in_house": forms.TextInput(
                attrs={
                    "class": "form-control role-input",
                    "readonly": True,
                    "placeholder": "The role will be substituted automatically.",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form and filters the user queryset."""
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.filter(user_type="employee")


SectionFormSet = forms.inlineformset_factory(
    House, Section, form=SectionForm, extra=1, can_delete=True
)

FloorFormSet = forms.inlineformset_factory(
    House, Floor, form=FloorForm, extra=1, can_delete=True
)

HouseStaffFormSet = forms.inlineformset_factory(
    House, HouseStaff, form=HouseStaffForm, extra=1, can_delete=True
)


class ApartmentForm(forms.ModelForm):
    """A form for creating and editing an Apartment, with personal account handling."""

    personal_account_number = forms.CharField(
        label="Лицевой счет",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите номер для создания"}
        ),
    )

    class Meta:
        """Provide metadata for the ApartmentForm."""

        model = Apartment
        fields = ["number", "area", "house", "section", "floor", "owner", "tariff"]
        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "area": forms.TextInput(attrs={"class": "form-control"}),
            "house": forms.Select(attrs={"class": "form-select"}),
            "section": forms.Select(attrs={"class": "form-select"}),
            "floor": forms.Select(attrs={"class": "form-select"}),
            "owner": forms.Select(attrs={"class": "form-select"}),
            "tariff": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "number": "Номер квартиры",
            "area": "Площадь (кв.м.)",
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form and dynamically sets querysets for section and floor."""
        super().__init__(*args, **kwargs)

        self.fields["owner"].queryset = User.objects.filter(user_type="owner").order_by(
            "last_name", "first_name"
        )
        self.fields["area"].required = False
        self.fields["section"].required = False
        self.fields["floor"].required = False
        self.fields["owner"].required = False
        self.fields["tariff"].required = False

        self.fields["section"].queryset = Section.objects.none()
        self.fields["floor"].queryset = Floor.objects.none()

        if self.instance.pk:
            if self.instance.personal_account:
                self.fields[
                    "personal_account_number"
                ].initial = self.instance.personal_account.number

            if self.instance.house:
                self.fields["section"].queryset = self.instance.house.sections.order_by(
                    "name"
                )
                self.fields["floor"].queryset = self.instance.house.floors.order_by(
                    "name"
                )

        elif "house" in self.data:
            try:
                house_id = int(self.data.get("house"))
                self.fields["section"].queryset = Section.objects.filter(
                    house_id=house_id
                ).order_by("name")
                self.fields["floor"].queryset = Floor.objects.filter(
                    house_id=house_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass

    def clean_personal_account_number(self):
        """Validate that the entered personal account number is not used."""
        number = self.cleaned_data.get("personal_account_number")
        if not number:
            return None

        query = PersonalAccount.objects.filter(number=number, apartment__isnull=False)

        if self.instance and self.instance.pk:
            query = query.exclude(apartment=self.instance)

        if query.exists():
            error_message = (
                f'Лицевой счет "{number}" уже используется другой квартирой.'
            )
            raise forms.ValidationError(error_message)

        return number

    def save(self, commit=True):  # noqa: FBT002
        """Override the save method to handle personal account logic."""
        old_personal_account = self.instance.personal_account

        apartment = super().save(commit=False)

        account_number = self.cleaned_data.get("personal_account_number")
        new_personal_account = None

        if account_number:
            new_personal_account, created = PersonalAccount.objects.get_or_create(
                number=account_number, defaults={"status": "active"}
            )

        apartment.personal_account = new_personal_account

        if commit:
            apartment.save()

        if old_personal_account and old_personal_account != new_personal_account:
            old_personal_account.status = "inactive"
            old_personal_account.save()

        return apartment


class PersonalAccountForm(forms.ModelForm):
    """A form for creating and editing a Personal Account."""

    apartment = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        """Provide metadata for the PersonalAccountForm."""

        model = PersonalAccount
        fields = ["number", "status", "apartment"]
        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(
                choices=[("active", "Активен"), ("inactive", "Неактивен")],
                attrs={"class": "form-select"},
            ),
        }
        labels = {
            "number": "№",
            "status": "Статус",
        }

    def __init__(self, *args, **kwargs):
        """Initialize the form and sets the queryset for the apartment field."""
        super().__init__(*args, **kwargs)
        apartments_without_account = Q(personal_account__isnull=True)
        current_apartment = (
            Q(pk=self.instance.apartment.pk)
            if hasattr(self.instance, "apartment")
            else Q()
        )

        self.fields["apartment"].queryset = Apartment.objects.filter(
            apartments_without_account | current_apartment
        ).select_related("house")

        if hasattr(self.instance, "apartment"):
            self.fields["apartment"].initial = self.instance.apartment
