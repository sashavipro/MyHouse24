import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

from src import building



class Role(models.Model):
    """
    Модель Ролей. Определяет, что может делать пользователь в системе.
    Например: "Директор", "Бухгалтер", "Владелец квартиры".
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Название роли")

    # Здесь можно добавить поля с правами доступа, как на вашем макете
    has_statistics = models.BooleanField(default=False, verbose_name="Доступ к статистике")
    has_cashbox = models.BooleanField(default=False, verbose_name="Доступ к кассе")
    has_receipt = models.BooleanField(default=False, verbose_name="Доступ к квитанции")
    has_personal_account = models.BooleanField(default=False, verbose_name="Доступ к лицевому счету")
    has_apartment = models.BooleanField(default=False, verbose_name="Доступ к квартире")
    has_owner = models.BooleanField(default=False, verbose_name="Доступ к владельцу")
    has_house = models.BooleanField(default=False, verbose_name="Доступ к домам")
    has_messege = models.BooleanField(default=False, verbose_name="Доступ к сообщениям")
    has_ticket = models.BooleanField(default=False, verbose_name="Доступ к заявкам")
    has_counters = models.BooleanField(default=False, verbose_name="Доступ к счетчику")
    has_management = models.BooleanField(default=False, verbose_name="Доступ к управлению сайтом")
    has_service = models.BooleanField(default=False, verbose_name="Доступ к услуге")
    has_tariff = models.BooleanField(default=False, verbose_name="Доступ к тарифу")
    has_role = models.BooleanField(default=False, verbose_name="Доступ к роле")
    has_user = models.BooleanField(default=False, verbose_name="Доступ к пользователю")
    has_payment_details = models.BooleanField(default=False, verbose_name="Доступ к платежным реквизитам")

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"

    def __str__(self):
        return self.name


class User(AbstractUser):
    """
    Кастомная модель Пользователя. Расширяет стандартную модель Django.
    """
    USER_TYPE_CHOICES = (
        ('employee', 'Сотрудник'),
        ('owner', 'Владелец'),
    )
    USER_STATUS_CHOICES = (
        ('active', 'Активен'),
        ('inactive', 'Отключен'),
        ('new', 'Новый'),
    )

    middle_name = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='owner',
                                 verbose_name="Тип пользователя")
    status = models.CharField(max_length=10, choices=USER_STATUS_CHOICES, default='new', verbose_name="Статус")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Изображение профиля")
    birthday = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    description = models.TextField(blank=True, verbose_name="Заметки о владельце")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    viber = models.CharField(max_length=20, blank=True, verbose_name="Viber")
    telegram = models.CharField(max_length=50, blank=True, verbose_name="Telegram")

    # Связь с ролью. У одного пользователя - одна роль.
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Роль"
    )

    def get_full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()

    def __str__(self):
        return self.get_full_name() or self.username


class Ticket(models.Model):
    """Заявка на вызов мастера"""
    STATUS_CHOICES = (
        ('new', 'Новое'),
        ('in_progress', 'В работе'),
        ('done', 'Выполнено'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    apartment = models.ForeignKey('building.Apartment', on_delete=models.CASCADE, verbose_name="Квартира")
    author = models.ForeignKey(User, related_name="created_tickets", on_delete=models.PROTECT,
                               verbose_name="Автор заявки")
    master = models.ForeignKey(User, related_name="assigned_tickets", on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name="Назначенный мастер")
    description = models.TextField(verbose_name="Описание проблемы")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"Заявка №{self.id} от {self.apartment}"


class Message(models.Model):
    """Сообщение в системе"""
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_messages",
                               verbose_name="Отправитель")
    recipients = models.ManyToManyField(User, through='MessageRecipient', related_name="received_messages",
                                        verbose_name="Получатели")
    title = models.CharField(max_length=255, verbose_name="Тема")
    text = models.TextField(verbose_name="Текст сообщения")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.title


class MessageRecipient(models.Model):
    """Промежуточная модель для получателей сообщений"""
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name="Сообщение")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Получатель")

    class Meta:
        verbose_name = "Получатель сообщения"
        verbose_name_plural = "Получатели сообщений"
        unique_together = ('message', 'user')