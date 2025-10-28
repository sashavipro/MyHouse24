"""src/building/forms.py."""

from django import forms

from src.users.models import User

from .models import Floor
from .models import House
from .models import HouseStaff
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
