from django.db import models

from src import users, finance
from src.finance.models import Tariff
from src.users.models import User


class House(models.Model):
    """Модель дома/ЖК"""
    title = models.CharField(max_length=255, verbose_name="Название")
    address = models.TextField(verbose_name="Адрес")
    image1 = models.ImageField(upload_to='houses/', null=True, blank=True, verbose_name="Изображение 1")
    image2 = models.ImageField(upload_to='houses/', null=True, blank=True, verbose_name="Изображение 2")
    image3 = models.ImageField(upload_to='houses/', null=True, blank=True, verbose_name="Изображение 3")
    image4 = models.ImageField(upload_to='houses/', null=True, blank=True, verbose_name="Изображение 4")
    image5 = models.ImageField(upload_to='houses/', null=True, blank=True, verbose_name="Изображение 5")
    staff = models.ManyToManyField('users.User', through='HouseStaff', verbose_name="Обслуживающий персонал")

    class Meta:
        verbose_name = "Дом"
        verbose_name_plural = "Дома"

    def __str__(self):
        return self.title


class HouseStaff(models.Model):
    """Промежуточная модель для связи Дома и Пользователей-сотрудников"""
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name="Дом")
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name="Сотрудник")
    role_in_house = models.CharField(max_length=100, verbose_name="Должность в доме")

    class Meta:
        verbose_name = "Сотрудник дома"
        verbose_name_plural = "Сотрудники домов"
        unique_together = ('house', 'user')


class Section(models.Model):
    """Секция/подъезд в доме"""
    name = models.CharField(max_length=100, verbose_name="Название секции")
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name="sections", verbose_name="Дом")

    class Meta:
        verbose_name = "Секция"
        verbose_name_plural = "Секции"

    def __str__(self):
        return f"{self.name} ({self.house.title})"


class Floor(models.Model):
    """Этаж в секции"""
    name = models.CharField(max_length=100, verbose_name="Номер этажа")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="floors", verbose_name="Секция")

    class Meta:
        verbose_name = "Этаж"
        verbose_name_plural = "Этажи"

    def __str__(self):
        return f"Этаж {self.name} ({self.section.name})"


class PersonalAccount(models.Model):
    """Лицевой счет, привязанный к квартире"""
    number = models.CharField(max_length=20, unique=True, verbose_name="Номер лицевого счета")
    status = models.CharField(max_length=20, default='active', verbose_name="Статус")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Баланс")

    class Meta:
        verbose_name = "Лицевой счет"
        verbose_name_plural = "Лицевые счета"

    def __str__(self):
        return self.number


class Apartment(models.Model):
    """Модель квартиры"""
    number = models.CharField(max_length=10, verbose_name="Номер квартиры")
    area = models.FloatField(verbose_name="Площадь (кв.м.)")

    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name="Дом")
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name="Секция")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, verbose_name="Этаж")

    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apartments",
        verbose_name="Владелец"
    )
    tariff = models.ForeignKey(
        'finance.Tariff',
        on_delete=models.PROTECT,
        verbose_name="Тариф"
    )
    personal_account = models.OneToOneField(
        PersonalAccount,
        on_delete=models.CASCADE,
        verbose_name="Лицевой счет"
    )

    class Meta:
        verbose_name = "Квартира"
        verbose_name_plural = "Квартиры"
        unique_together = ('house', 'number')  # Номер квартиры должен быть уникальным в пределах дома

    def __str__(self):
        return f"Кв. {self.number}, {self.house.title}"
