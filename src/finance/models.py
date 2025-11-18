"""src/finance/models.py."""

from django.core.validators import FileExtensionValidator
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
        """Return string representation of the unit."""
        return self.name


class Currency(models.Model):
    """Currency."""

    name = models.CharField(max_length=50, unique=True, verbose_name="Currency")

    class Meta:
        """Meta class."""

        verbose_name = "Currency"
        verbose_name_plural = "Currency"

    def __str__(self):
        """Return string representation of the currency."""
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
        """Return string representation of the service."""
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
        """Return string representation of the tariff."""
        return self.name


class TariffService(models.Model):
    """TariffService."""

    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name="Tariff")
    service = models.ForeignKey(
        Service, on_delete=models.PROTECT, verbose_name="Service"
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
        """Return string representation of the tariff service."""
        return f"{self.service.name} в {self.tariff.name}"


class Counter(models.Model):
    """Счетчик, привязанный к квартире и услуге."""

    serial_number = models.CharField(
        max_length=100, unique=True, verbose_name="Серийный номер"
    )
    apartment = models.ForeignKey(
        "building.Apartment",
        on_delete=models.CASCADE,
        related_name="counters",
        verbose_name="Квартира",
    )
    service = models.ForeignKey(
        Service, on_delete=models.PROTECT, verbose_name="Услуга"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        """Meta class."""

        verbose_name = "Счетчик"
        verbose_name_plural = "Счетчики"

    def __str__(self):
        """Return string representation of the counter."""
        return f"{self.service.name} ({self.serial_number}) в {self.apartment}"


class CounterReading(models.Model):
    """Одно показание, снятое для счетчика."""

    class CounterStatus(models.TextChoices):
        """Counter status choices."""

        NEW = "new", "Новое"
        CONSIDERED = "considered", "Учтено"
        ZERO = "zero", "Нулевое"
        PAID = "paid", "Учтено и оплачено"

    number = models.CharField(max_length=20, unique=True, verbose_name="№")

    # Используем Counter как связь
    counter = models.ForeignKey(
        Counter,
        on_delete=models.CASCADE,
        related_name="readings",
        verbose_name="Счетчик",
    )

    date = models.DateField(verbose_name="Дата снятия")
    value = models.DecimalField(
        max_digits=12, decimal_places=3, verbose_name="Показание"
    )
    status = models.CharField(
        max_length=20,
        choices=CounterStatus.choices,
        default=CounterStatus.NEW,
        verbose_name="Статус",
    )

    class Meta:
        """Meta class."""

        verbose_name = "Показание счетчика"
        verbose_name_plural = "Показания счетчиков"
        ordering = ["-date", "-id"]

    def __str__(self):
        """Return string representation of the counter reading."""
        return f"Показание №{self.number} ({self.counter.service.name}) от {self.date}"

    @property
    def apartment(self):
        """Get the apartment from the counter."""
        return self.counter.apartment

    @property
    def service(self):
        """Get the service from the counter."""
        return self.counter.service


class Receipt(models.Model):
    """Receipt."""

    class ReceiptStatus(models.TextChoices):
        """Receipt status."""

        UNPAID = "unpaid", "Неоплачена"
        PARTIALLY_PAID = "partially_paid", "Частично оплачена"
        PAID = "paid", "Оплачена"

    number = models.CharField(
        max_length=50, unique=True, verbose_name="Номер квитанции"
    )
    date = models.DateField(default=timezone.now, verbose_name="Дата")

    is_posted = models.BooleanField(default=False, verbose_name="Проведена")

    period_start = models.DateField(null=True, blank=True, verbose_name="Период c")
    period_end = models.DateField(null=True, blank=True, verbose_name="Период по")

    apartment = models.ForeignKey(
        "building.Apartment",
        on_delete=models.PROTECT,
        related_name="receipts",
        verbose_name="Квартира",
    )
    tariff = models.ForeignKey(
        Tariff,
        on_delete=models.PROTECT,
        verbose_name="Тариф",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=ReceiptStatus.choices,
        default=ReceiptStatus.UNPAID,
        verbose_name="Статус оплаты",
    )
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Итоговая сумма", default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    services = models.ManyToManyField(
        Service, through="ReceiptItem", verbose_name="Услуги"
    )

    class Meta:
        """Meta class."""

        verbose_name = "Квитанция"
        verbose_name_plural = "Квитанции"
        ordering = ["-date", "-pk"]

    def __str__(self):
        """Return string representation of the receipt."""
        return f"Квитанция №{self.number} от {self.date.strftime('%d.%m.%Y')}"


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
        return (
            f"{self.service.name}: {self.amount} " f"in receipt №{self.receipt.number}"
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
        """Return a string representation of the cash transaction."""
        return f"{self.service.name}: {self.amount} in receipt №{self.receipt.id}"


class PaymentDetails(models.Model):
    """A singleton model to store company payment details."""

    company_name = models.CharField(max_length=255, verbose_name="Название компании")
    info = models.TextField(verbose_name="Информация")

    class Meta:
        """Meta class."""

        verbose_name = "Платежные реквизиты"
        verbose_name_plural = "Платежные реквизиты"

    def __str__(self):
        """Return string representation of payment details."""
        return self.company_name


class PrintTemplate(models.Model):
    """Model for storing templates of printed receipt forms."""

    name = models.CharField(max_length=255, verbose_name="Название шаблона")
    template_file = models.FileField(
        upload_to="receipt_templates/",
        verbose_name="Файл шаблона (.xlsx)",
        validators=[FileExtensionValidator(allowed_extensions=["xlsx"])],
    )
    is_default = models.BooleanField(default=False, verbose_name="По умолчанию")

    class Meta:
        """Meta class."""

        verbose_name = "Шаблон для печати"
        verbose_name_plural = "Шаблоны для печати"

    def __str__(self):
        """Return string representation of the print template."""
        return self.name

    def save(self, *args, **kwargs):
        """Save template and ensure only one default template exists."""
        if self.is_default:
            PrintTemplate.objects.filter(is_default=True).exclude(pk=self.pk).update(
                is_default=False
            )
        super().save(*args, **kwargs)
