"""src/finance/forms.py."""

from django import forms

from .models import Currency
from .models import Service
from .models import Tariff
from .models import TariffService
from .models import Unit


class ServiceForm(forms.ModelForm):
    """A form for creating and updating Service objects."""

    class Meta:
        """Provides metadata for the ServiceForm."""

        model = Service
        fields = ["name", "unit", "show_in_counters"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-select"}),
            "show_in_counters": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
        labels = {
            "name": "Услуга",
            "unit": "Ед. изм.",
            "show_in_counters": "Показывать в счетчиках",
        }


class UnitForm(forms.ModelForm):
    """A form for creating and updating Unit objects."""

    class Meta:
        """Provides metadata for the UnitForm."""

        model = Unit
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Ед. изм.",
        }


ServiceFormSet = forms.modelformset_factory(
    Service, form=ServiceForm, can_delete=True, extra=1
)

UnitFormSet = forms.modelformset_factory(Unit, form=UnitForm, can_delete=True, extra=1)


class TariffForm(forms.ModelForm):
    """A form for the main fields of a Tariff object."""

    class Meta:
        """Provides metadata for the TariffForm."""

        model = Tariff
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
        labels = {
            "name": "Название тарифа",
            "description": "Описание тарифа",
        }


class TariffServiceForm(forms.ModelForm):
    """A form for a single service within a tariff."""

    class Meta:
        """Provide metadata for the TariffServiceForm."""

        model = TariffService
        fields = ["service", "price"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-select"}),
            "price": forms.TextInput(attrs={"class": "form-control"}),
        }

    def save(self, *, commit: bool = True):
        """Override the save method to automatically set the currency."""
        instance = super().save(commit=False)
        if not instance.currency_id:
            try:
                uah_currency = Currency.objects.get(name__iexact="грн")
                instance.currency = uah_currency
            except Currency.DoesNotExist as e:
                first_currency = Currency.objects.first()
                if not first_currency:
                    error_message = "No currencies found in the system!"
                    raise ValueError(error_message) from e
                instance.currency = first_currency
        if commit:
            instance.save()
        return instance


TariffServiceFormSet = forms.inlineformset_factory(
    Tariff, TariffService, form=TariffServiceForm, extra=1, can_delete=True
)
