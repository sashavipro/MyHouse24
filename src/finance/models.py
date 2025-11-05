"""src/finance/models.py."""

from django.db import models
from django.utils import timezone


class Unit(models.Model):
    """Unit."""

    name = models.CharField(max_length=50, unique=True, verbose_name="name")

    class Meta:
        """Meta class."""

        verbose_name = "Unit"
        verbose_name_plural = "Units"

    def __str__(self):
        """__str__."""
        return self.name


class Currency(models.Model):
    """Currency."""

    name = models.CharField(max_length=50, unique=True, verbose_name="Currency")

    class Meta:
        """Meta class."""

        verbose_name = "Currency"
        verbose_name_plural = "Currency"

    def __str__(self):
        """__str__."""
        return self.name


class Service(models.Model):
    """Service."""

    name = models.CharField(max_length=255, unique=True, verbose_name="Service")
    show_in_counters = models.BooleanField(
        default=True, verbose_name="Show in counters"
    )
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name="Unit")

    class Meta:
        """Meta class."""

        verbose_name = "Service"
        verbose_name_plural = "Service"

    def __str__(self):
        """__str__."""
        return self.name


class Tariff(models.Model):
    """Tariff."""

    name = models.CharField(max_length=255, verbose_name="Tariff")
    description = models.TextField(blank=True, verbose_name="description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")
    services = models.ManyToManyField(
        Service, through="TariffService", verbose_name="Service"
    )

    class Meta:
        """Meta class."""

        verbose_name = "Tariff"
        verbose_name_plural = "Tariffs"

    def __str__(self):
        """__str__."""
        return self.name


class TariffService(models.Model):
    """TariffService."""

    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name="Tariff")
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, verbose_name="Service"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="price")
    currency = models.ForeignKey(
        Currency, on_delete=models.PROTECT, verbose_name="currency"
    )

    class Meta:
        """Meta class."""

        verbose_name = "Service included in the tariff"
        verbose_name_plural = "Service included in the tariffs"
        unique_together = (
            "tariff",
            "service",
        )

    def __str__(self):
        """__str__."""
        return f"{self.service.name} в {self.tariff.name}"


class Counter(models.Model):
    """Counter."""

    serial_number = models.CharField(
        max_length=100, unique=True, verbose_name="Serial Number"
    )
    apartment = models.ForeignKey(
        "building.Apartment",
        on_delete=models.CASCADE,
        related_name="counters",
        verbose_name="Apartment",
    )
    service = models.ForeignKey(
        Service, on_delete=models.PROTECT, verbose_name="Service"
    )
    is_active = models.BooleanField(default=True, verbose_name="is active")

    class Meta:
        """Meta class."""

        verbose_name = "Counter"
        verbose_name_plural = "Counters"

    def __str__(self):
        """__str__."""
        return f"{self.service.name} ({self.serial_number}) в {self.apartment}"


class CounterReading(models.Model):
    """CounterReading."""

    class CounterStatus(models.TextChoices):
        """Counter status."""

        NEW = "new", "Новое"
        CONSIDERED = "considered", "Учтено"
        ZERO = "zero", "Нулевое"

    counter = models.ForeignKey(
        Counter,
        on_delete=models.CASCADE,
        related_name="readings",
        verbose_name="Counter",
    )
    date = models.DateField(verbose_name="Date of removal")
    value = models.DecimalField(
        max_digits=12, decimal_places=3, verbose_name="Indication"
    )
    status = models.CharField(
        max_length=20,
        choices=CounterStatus.choices,
        default=CounterStatus.NEW,
        verbose_name="status",
    )

    class Meta:
        """Meta class."""

        verbose_name = "Meter reading"
        verbose_name_plural = "Meter reading"
        ordering = ["-date"]

    def __str__(self):
        """__str__."""
        return f"Indication {self.value} от {self.date}"


class Receipt(models.Model):
    """Receipt."""

    class ReceiptStatus(models.TextChoices):
        """Receipt status."""

        UNPAID = "unpaid", "He оплачено"
        PARTIALLY_PAID = "partially_paid", "Частично оплачено"
        PAID = "paid", "Оплачено"

    apartment = models.ForeignKey(
        "building.Apartment",
        on_delete=models.PROTECT,
        related_name="receipts",
        verbose_name="apartment",
    )
    month = models.PositiveIntegerField(verbose_name="month")
    year = models.PositiveIntegerField(verbose_name="year")
    status = models.CharField(
        max_length=20,
        choices=ReceiptStatus.choices,
        default=ReceiptStatus.UNPAID,
        verbose_name="status",
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="total amount"
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="created_at")

    services = models.ManyToManyField(
        Service, through="ReceiptItem", verbose_name="services"
    )

    class Meta:
        """Meta class."""

        verbose_name = "Receipt"
        verbose_name_plural = "Receipts"
        unique_together = ("apartment", "month", "year")

    def __str__(self):
        """__str__."""
        return f"Квитанция для {self.apartment} за {self.month}.{self.year}"


class ReceiptItem(models.Model):
    """A line item within a receipt, detailing a specific service."""

    receipt = models.ForeignKey(
        Receipt, on_delete=models.CASCADE, verbose_name="Receipt"
    )
    service = models.ForeignKey(
        Service, on_delete=models.PROTECT, verbose_name="Service"
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Amount charged"
    )
    consumption = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="consumption",
    )
    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="price per unit.",
    )

    class Meta:
        """Meta class."""

        verbose_name = "Receipt line"
        verbose_name_plural = "Receipts line"
        unique_together = ("receipt", "service")

    def __str__(self):
        """Return a string representation of the receipt item."""
        # E501: Line too long - перенесено на новую строку
        return (
            f"{self.service.name}: {self.amount} in receipt " f"№{self.receipt.number}"
        )


class Article(models.Model):
    """An article for income or expense tracking."""

    class ArticleType(models.TextChoices):
        """Article type."""

        INCOME = "income", "Приход"
        EXPENSE = "expense", "Расход"

    name = models.CharField(max_length=255, verbose_name="name")
    type = models.CharField(
        max_length=10, choices=ArticleType.choices, verbose_name="type"
    )

    class Meta:
        """Meta class."""

        verbose_name = "Revenue/expense item"
        verbose_name_plural = "Revenue/expense item"

    def __str__(self):
        """Return the name of the article."""
        return self.name


class CashBox(models.Model):
    """CashBox."""

    personal_account = models.ForeignKey(
        "building.PersonalAccount",
        on_delete=models.PROTECT,
        verbose_name="personal account",
    )
    article = models.ForeignKey(
        Article, on_delete=models.PROTECT, verbose_name="Article"
    )
    receipt = models.ForeignKey(
        Receipt,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="receipt",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="amount")
    date = models.DateTimeField(default=timezone.now, verbose_name="Transaction date")
    comment = models.TextField(blank=True, verbose_name="comment")

    class Meta:
        """Meta class."""

        verbose_name = "Cash transaction"
        verbose_name_plural = "Cash transaction"

    def __str__(self):
        """Return a string representation of the receipt item."""
        return f"{self.service.name}: {self.amount} " f"in receipt №{self.receipt.id}"


class PaymentDetails(models.Model):
    """A singleton model to store company payment details."""

    company_name = models.CharField(max_length=255, verbose_name="Название компании")
    info = models.TextField(verbose_name="Информация")

    class Meta:
        """Meta class."""

        verbose_name = "Платежные реквизиты"
        verbose_name_plural = "Платежные реквизиты"

    def __str__(self):
        """Str."""
        return self.company_name
