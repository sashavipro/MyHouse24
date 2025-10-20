from django.db import models
from django.utils import timezone

from src import building



class Unit(models.Model):
    """Единицы измерения (кВт, м3, и т.д.)"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название (м3)")

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"

    def __str__(self):
        return self.name


class Currency(models.Model):
    """Валюты (грн, долл, и т.д.)"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Название (грн)")

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self):
        return self.name


class Service(models.Model):
    """Справочник услуг (Холодная вода, Электроэнергия)"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Название услуги")
    show_in_counters = models.BooleanField(default=True, verbose_name="Показывать в счетчиках")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name="Ед. измерения")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class Tariff(models.Model):
    """Тариф, который является набором услуг с ценами"""
    name = models.CharField(max_length=255, verbose_name="Название тарифа")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    services = models.ManyToManyField(Service, through='TariffService', verbose_name="Услуги")

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"

    def __str__(self):
        return self.name


class TariffService(models.Model):
    """Промежуточная модель для связи Тарифа и Услуги с указанием цены"""
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name="Тариф")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Услуга")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, verbose_name="Валюта")

    class Meta:
        verbose_name = "Услуга в тарифе"
        verbose_name_plural = "Услуги в тарифах"
        unique_together = ('tariff', 'service')  # Услуга может быть в тарифе только один раз

    def __str__(self):
        return f"{self.service.name} в {self.tariff.name}"


class Counter(models.Model):
    """Физический прибор-счетчик в квартире"""
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Серийный номер")
    apartment = models.ForeignKey('building.Apartment', on_delete=models.CASCADE, related_name="counters", verbose_name="Квартира")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name="Услуга (что измеряет)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Счетчик"
        verbose_name_plural = "Счетчики"

    def __str__(self):
        return f"{self.service.name} ({self.serial_number}) в {self.apartment}"


class CounterReading(models.Model):
    """История показаний для каждого счетчика"""
    STATUS_CHOICES = (
        ('new', 'Новое'),
        ('considered', 'Учтено'),
        ('zero', 'Нулевое'),
    )
    counter = models.ForeignKey(Counter, on_delete=models.CASCADE, related_name="readings", verbose_name="Счетчик")
    date = models.DateField(verbose_name="Дата снятия")
    value = models.DecimalField(max_digits=12, decimal_places=3, verbose_name="Показание")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")

    class Meta:
        verbose_name = "Показание счетчика"
        verbose_name_plural = "Показания счетчиков"
        ordering = ['-date']

    def __str__(self):
        return f"Показание {self.value} от {self.date}"


class Receipt(models.Model):
    """Квитанция на оплату за определенный период"""
    STATUS_CHOICES = (
        ('unpaid', 'Не оплачено'),
        ('partially_paid', 'Частично оплачено'),
        ('paid', 'Оплачено'),
    )
    apartment = models.ForeignKey('building.Apartment', on_delete=models.PROTECT, related_name="receipts", verbose_name="Квартира")
    month = models.PositiveIntegerField(verbose_name="Месяц (число)")
    year = models.PositiveIntegerField(verbose_name="Год")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid', verbose_name="Статус оплаты")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    services = models.ManyToManyField(Service, through='ReceiptItem', verbose_name="Услуги в квитанции")

    class Meta:
        verbose_name = "Квитанция"
        verbose_name_plural = "Квитанции"
        unique_together = ('apartment', 'month', 'year')

    def __str__(self):
        return f"Квитанция для {self.apartment} за {self.month}.{self.year}"


class ReceiptItem(models.Model):
    """Строка в квитанции - начисление по конкретной услуге"""
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, verbose_name="Квитанция")
    service = models.ForeignKey(Service, on_delete=models.PROTECT, verbose_name="Услуга")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма начисления")
    consumption = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True,
                                      verbose_name="Потребление")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                         verbose_name="Цена за ед.")

    class Meta:
        verbose_name = "Строка квитанции"
        verbose_name_plural = "Строки квитанций"
        unique_together = ('receipt', 'service')


class Article(models.Model):
    """Справочник статей приходов/расходов"""
    TYPE_CHOICES = (
        ('income', 'Приход'),
        ('expense', 'Расход'),
    )
    name = models.CharField(max_length=255, verbose_name="Название статьи")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип")

    class Meta:
        verbose_name = "Статья прихода/расхода"
        verbose_name_plural = "Статьи приходов/расходов"

    def __str__(self):
        return self.name


class CashBox(models.Model):
    """Запись о движении средств (транзакция)"""
    personal_account = models.ForeignKey('building.PersonalAccount', on_delete=models.PROTECT, verbose_name="Лицевой счет")
    article = models.ForeignKey(Article, on_delete=models.PROTECT, verbose_name="Статья")
    receipt = models.ForeignKey(Receipt, on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name="Квитанция (если оплата)")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма")
    date = models.DateTimeField(default=timezone.now, verbose_name="Дата транзакции")
    comment = models.TextField(blank=True, verbose_name="Комментарий")

    class Meta:
        verbose_name = "Транзакция по кассе"
        verbose_name_plural = "Транзакции по кассе"

    def __str__(self):
        return f"{self.article.get_type_display()} на {self.amount} по счету {self.personal_account}"
