import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Активен'
        DISABLED = 'DISABLED', 'Отключен'
        NEW = 'NEW', 'Новый'

    # Переопределяем поле username, чтобы сделать email основным идентификатором
    username = None  # Мы не будем использовать username
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Поля, обязательные при создании superuser

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус"
    )
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,
                               verbose_name="Уникальный ID пользователя")
    image = models.ImageField(upload_to='users/images/', null=True, blank=True, verbose_name="Аватар")
    middle_name = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    birthday = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    description = models.TextField(blank=True, verbose_name="Описание")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    viber = models.CharField(max_length=20, blank=True, verbose_name="Viber")
    telegram = models.CharField(max_length=50, blank=True, verbose_name="Telegram")

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.email})"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

