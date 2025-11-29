"""src/cabinet/forms.py."""

from django import forms

from src.building.models import Apartment
from src.users.models import Ticket

CARD_NUMBER_LENGTH = 16
MIN_EXPIRY_LENGTH = 5


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


class PaymentCardForm(forms.Form):
    """PaymentCardForm."""

    card_number = forms.CharField(
        label="Номер карты",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control card-number-input",
                "placeholder": "0000 0000 0000 0000",
            }
        ),
    )
    expiry_date = forms.CharField(
        label="Срок действия",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "MM / YY",
                "style": "width: 80px; display: inline-block;",
            }
        ),
    )
    cvv = forms.CharField(
        label="CVV",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "...",
                "style": "width: 60px; display: inline-block;",
            }
        ),
    )

    def clean_card_number(self):
        """Clean_card_number."""
        data = self.cleaned_data["card_number"]
        clean_data = data.replace(" ", "")

        if not clean_data.isdigit():
            msg = "Номер карты должен содержать только цифры."
            raise forms.ValidationError(msg)

        if len(clean_data) != CARD_NUMBER_LENGTH:
            msg = (
                f"Номер карты должен содержать {CARD_NUMBER_LENGTH} цифр "
                f"(сейчас {len(clean_data)})."
            )
            raise forms.ValidationError(msg)

        return clean_data

    def clean_expiry_date(self):
        """clean_expiry_date."""
        data = self.cleaned_data["expiry_date"]

        if len(data) < MIN_EXPIRY_LENGTH:
            msg = "Неверный формат даты."
            raise forms.ValidationError(msg)

        return data
