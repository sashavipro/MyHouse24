"""src/finance/forms.py."""

import logging

from django import forms
from django.db import transaction
from django.utils import timezone

from src.building.models import Apartment
from src.building.models import PersonalAccount
from src.users.models import User

from .models import Article
from .models import CashBox
from .models import CounterReading
from .models import Currency
from .models import PaymentDetails
from .models import PrintTemplate
from .models import Receipt
from .models import ReceiptItem
from .models import Service
from .models import Tariff
from .models import TariffService
from .models import Unit

logger = logging.getLogger(__name__)


class ServiceForm(forms.ModelForm):
    """A form for creating and updating Service objects."""

    class Meta:
        """Provide metadata for the ServiceForm."""

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
        """Provide metadata for the UnitForm."""

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
        """Provide metadata for the TariffForm."""

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

    def save(self, *, commit=True):
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


class ArticleForm(forms.ModelForm):
    """A form for creating and editing payment Article objects."""

    class Meta:
        """Provide metadata for the ArticleForm."""

        model = Article
        fields = ["name", "type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "name": "Название",
            "type": "Приход/расход",
        }


class PaymentDetailsForm(forms.ModelForm):
    """A form for updating the singleton PaymentDetails object."""

    class Meta:
        """Provide metadata for the PaymentDetailsForm."""

        model = PaymentDetails
        fields = ["company_name", "info"]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "info": forms.Textarea(attrs={"class": "form-control", "rows": 5}),
        }
        labels = {
            "company_name": "Название компании",
            "info": "Информация",
        }


class CounterReadingForm(forms.ModelForm):
    """Form for creating and editing meter readings."""

    apartment = forms.ModelChoiceField(
        queryset=Apartment.objects.all(), widget=forms.HiddenInput(), required=False
    )

    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(show_in_counters=True).order_by("name"),
        label="Счетчик (Услуга)",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=True,
    )

    class Meta:
        """Provide metadata for the CounterReadingForm."""

        model = CounterReading
        fields = [
            "number",
            "date",
            "apartment",
            "service",
            "counter",
            "value",
            "status",
        ]
        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "date": forms.TextInput(
                attrs={"class": "form-control date-picker", "placeholder": "ДД.ММ.ГГГГ"}  # noqa: RUF001
            ),
            "counter": forms.HiddenInput(),
            "value": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.001", "min": "0"}
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "number": "№",
            "date": "от",
            "value": "Показания счетчика",
            "status": "Статус",
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with optional counter field and default date."""
        super().__init__(*args, **kwargs)
        self.fields["counter"].required = False

        if self.instance and self.instance.pk:
            if self.instance.counter:
                self.initial["service"] = self.instance.counter.service_id
        else:
            self.initial["date"] = timezone.localdate()


class ReceiptForm(forms.ModelForm):
    """Form for creating and editing the main part of the receipt."""

    apartment = forms.ModelChoiceField(
        queryset=Apartment.objects.all(), widget=forms.HiddenInput(), required=False
    )
    personal_account_number = forms.CharField(
        label="Лицевой счет",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите номер для создания/привязки",
            }
        ),
    )

    class Meta:
        """Provide metadata for the ReceiptForm."""

        model = Receipt
        fields = [
            "number",
            "date",
            "apartment",
            "tariff",
            "is_posted",
            "status",
            "period_start",
            "period_end",
        ]
        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "date": forms.TextInput(
                attrs={"class": "form-control date-picker", "placeholder": "ДД.ММ.ГГГГ"}  # noqa: RUF001
            ),
            "tariff": forms.Select(attrs={"class": "form-select"}),
            "is_posted": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "period_start": forms.TextInput(
                attrs={"class": "form-control date-picker", "placeholder": "ДД.ММ.ГГГГ"}  # noqa: RUF001
            ),
            "period_end": forms.TextInput(
                attrs={"class": "form-control date-picker", "placeholder": "ДД.ММ.ГГГГ"}  # noqa: RUF001
            ),
        }
        labels = {
            "number": "№",
            "date": "от",
            "is_posted": "Проведена",
            "status": "Статус",
            "tariff": "Тариф",
            "period_start": "Период c",
            "period_end": "Период по",
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with default values and optional fields."""
        super().__init__(*args, **kwargs)

        self.fields["tariff"].required = False

        if (
            self.instance.pk
            and self.instance.apartment
            and self.instance.apartment.personal_account
        ):
            self.fields[
                "personal_account_number"
            ].initial = self.instance.apartment.personal_account.number

        if not self.instance.pk:
            today = timezone.localdate()
            self.initial["date"] = today

    def clean_apartment(self):
        """Confirm that the apartment has been selected."""
        apartment = self.cleaned_data.get("apartment")
        if not apartment:
            error_msg = "Необходимо выбрать квартиру."
            raise forms.ValidationError(error_msg)
        return apartment

    def clean_personal_account_number(self):
        """Check that the entered personal account is valid and safe to change."""
        number = self.cleaned_data.get("personal_account_number")
        apartment = self.cleaned_data.get("apartment")

        if number:
            query = PersonalAccount.objects.filter(
                number=number, apartment__isnull=False
            ).exclude(apartment=apartment)

            if query.exists():
                error_msg = (
                    f'Лицевой счет "{number}" уже используется другой квартирой.'
                )
                raise forms.ValidationError(error_msg)

        if apartment and apartment.personal_account:
            old_account = apartment.personal_account

            if old_account.number != number:
                has_receipts = Receipt.objects.filter(
                    apartment__personal_account=old_account
                ).exists()

                if has_receipts:
                    error_msg = (
                        f'Нельзя изменить лицевой счет "{old_account.number}", '
                        f"так как по нему уже есть сформированные квитанции."
                    )
                    raise forms.ValidationError(error_msg)

        return number

    def save(self, *, commit=True):
        """Save the receipt and handle personal account assignment."""
        receipt = super().save(commit=False)
        apartment = self.cleaned_data.get("apartment")
        account_number = self.cleaned_data.get("personal_account_number")

        with transaction.atomic():
            if apartment:
                old_personal_account = apartment.personal_account
                new_personal_account = None

                if account_number:
                    new_personal_account, _created = (
                        PersonalAccount.objects.get_or_create(
                            number=account_number, defaults={"status": "active"}
                        )
                    )

                apartment.personal_account = new_personal_account
                apartment.save()

                if (
                    old_personal_account
                    and old_personal_account != new_personal_account
                ):
                    old_personal_account.status = "inactive"
                    old_personal_account.save()

            if commit:
                receipt.save()

        return receipt


class ReceiptItemForm(forms.ModelForm):
    """Form for one service on the receipt."""

    class Meta:
        """Provide metadata for the ReceiptItemForm."""

        model = ReceiptItem
        fields = ["service", "consumption", "price_per_unit", "amount"]
        widgets = {
            "service": forms.Select(attrs={"class": "form-select service-select"}),
            "consumption": forms.NumberInput(
                attrs={"class": "form-control consumption-input"}
            ),
            "price_per_unit": forms.NumberInput(
                attrs={"class": "form-control price-input"}
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control amount-input", "readonly": True}
            ),
        }


ReceiptItemFormSet = forms.inlineformset_factory(
    Receipt,
    ReceiptItem,
    form=ReceiptItemForm,
    extra=1,
    can_delete=True,
    can_delete_extra=True,
)


class PrintTemplateForm(forms.ModelForm):
    """Form for uploading a new template."""

    class Meta:
        """Provide metadata for the PrintTemplateForm."""

        model = PrintTemplate
        fields = ["name", "template_file"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": 'Например, "Счет на оплату"',
                }
            ),
            "template_file": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Название",
            "template_file": "Файл шаблона (.xlsx)",
        }


class ManagerChoiceField(forms.ModelChoiceField):
    """Manager Choice Field."""

    def label_from_instance(self, obj):
        """Label from instance."""
        role_name = obj.role.name if obj.role else "Без роли"
        full_name = obj.get_full_name()
        return f"{role_name} - {full_name}"


class CashBoxForm(forms.ModelForm):
    """Base form for CashBox."""

    manager = ManagerChoiceField(
        queryset=User.objects.none(),
        label="Менеджер",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )

    class Meta:
        """Meta class."""

        model = CashBox
        fields = [
            "number",
            "date",
            "is_posted",
            "amount",
            "article",
            "comment",
            "manager",
        ]
        widgets = {
            "number": forms.TextInput(attrs={"class": "form-control"}),
            "date": forms.TextInput(
                attrs={"class": "form-control date-picker", "placeholder": "ДД.ММ.ГГГГ"}  # noqa: RUF001
            ),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "article": forms.Select(attrs={"class": "form-select"}),
            "manager": forms.Select(attrs={"class": "form-select"}),
            "is_posted": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.fields["manager"].queryset = (
            User.objects.filter(
                user_type=User.UserType.EMPLOYEE,
                role__name__in=["Директор", "Управляющий", "Бухгалтер"],
            )
            .select_related("role")
            .order_by("role__name", "last_name")
        )

        self.fields["manager"].empty_label = "Выберите..."

        if (
            not self.instance.pk
            and "initial" in kwargs
            and "manager" in kwargs["initial"]
        ):
            self.fields["manager"].initial = kwargs["initial"]["manager"]


class CashBoxIncomeForm(CashBoxForm):
    """Form for INCOME."""

    owner = forms.ModelChoiceField(
        queryset=User.objects.filter(user_type=User.UserType.OWNER),
        label="Владелец квартиры",
        required=False,
        widget=forms.Select(attrs={"class": "form-select select2-simple"}),
    )

    personal_account = forms.ModelChoiceField(
        queryset=PersonalAccount.objects.all(),
        label="Лицевой счет",
        required=False,
        widget=forms.Select(attrs={"class": "form-select select2-simple"}),
    )

    class Meta(CashBoxForm.Meta):
        """Meta class."""

        fields = [*CashBoxForm.Meta.fields, "personal_account"]

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.fields["article"].queryset = Article.objects.filter(
            type=Article.ArticleType.INCOME
        )

        if self.instance.pk and self.instance.personal_account:
            try:
                apt = self.instance.personal_account.apartment
                if apt and apt.owner:
                    self.fields["owner"].initial = apt.owner
            except Apartment.DoesNotExist:
                logger.warning(
                    "Personal account %s has no apartment",
                    self.instance.personal_account.number,
                )
            except AttributeError as e:
                logger.warning(
                    "Error accessing apartment owner for personal account %s: %s",
                    self.instance.personal_account.number,
                    e,
                )


class CashBoxExpenseForm(CashBoxForm):
    """Form for EXPENSE."""

    def __init__(self, *args, **kwargs):
        """Init."""
        super().__init__(*args, **kwargs)
        self.fields["article"].queryset = Article.objects.filter(
            type=Article.ArticleType.EXPENSE
        )
