"""src/cabinet/forms.py."""

from django import forms

from src.building.models import Apartment
from src.users.models import Ticket


class CabinetTicketForm(forms.ModelForm):
    """Form for creating a ticket (master call) in the cabinet."""

    class Meta:
        """Meta class."""

        model = Ticket
        fields = ["role", "apartment", "date", "time", "description"]
        widgets = {
            "role": forms.Select(attrs={"class": "form-select"}),
            "apartment": forms.Select(attrs={"class": "form-select"}),
            "date": forms.TextInput(
                attrs={"class": "form-control date-picker", "placeholder": "ДД.ММ.ГГГГ"}  # noqa: RUF001
            ),
            "time": forms.TextInput(
                attrs={
                    "class": "form-control time-picker",
                    "placeholder": "Выберите время",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Опишите проблему",
                }
            ),
        }
        labels = {
            "role": "Тип мастера",
            "apartment": "Квартира",
            "date": "Дата работ",
            "time": "Время работ",
            "description": "Описание",
        }

    def __init__(self, user, *args, **kwargs):
        """Filter apartments by the current owner."""
        super().__init__(*args, **kwargs)
        self.fields["apartment"].queryset = Apartment.objects.filter(owner=user)
        self.fields["apartment"].empty_label = "Выберите квартиру..."
