"""src/users/models.py."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    """Role."""

    name = models.CharField(max_length=100, unique=True, verbose_name="Name role")
    has_statistics = models.BooleanField(
        default=False, verbose_name="Access to statistics"
    )
    has_cashbox = models.BooleanField(default=False, verbose_name="Access to cashbox")
    has_receipt = models.BooleanField(default=False, verbose_name="Access to receipt")
    has_personal_account = models.BooleanField(
        default=False, verbose_name="Access to personal account"
    )
    has_apartment = models.BooleanField(
        default=False, verbose_name="Access to apartment"
    )
    has_owner = models.BooleanField(default=False, verbose_name="Access to owner")
    has_house = models.BooleanField(default=False, verbose_name="Access to house")
    has_message = models.BooleanField(default=False, verbose_name="Access to message")
    has_ticket = models.BooleanField(default=False, verbose_name="Access to ticket")
    has_counters = models.BooleanField(default=False, verbose_name="Access to counters")
    has_management = models.BooleanField(
        default=False, verbose_name="Access to management site"
    )
    has_service = models.BooleanField(default=False, verbose_name="Access to service")
    has_tariff = models.BooleanField(default=False, verbose_name="Access to tariff")
    has_role = models.BooleanField(default=False, verbose_name="Access to role")
    has_user = models.BooleanField(default=False, verbose_name="Access to user")
    has_payment_details = models.BooleanField(
        default=False, verbose_name="Access to payment details"
    )

    class Meta:
        """Meta class."""

        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        """__str__."""
        return self.name


class User(AbstractUser):
    """User."""

    class UserType(models.TextChoices):
        """User type."""

        EMPLOYEE = "employee", "Сотрудник"
        OWNER = "owner", "Владелец"

    class UserStatus(models.TextChoices):
        """User status."""

        ACTIVE = "active", "Активен"
        INACTIVE = "inactive", "Отключен"
        NEW = "new", "Новый"

    user_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        verbose_name="ID Владельца (ручной ввод)",
    )

    middle_name = models.CharField(
        max_length=150, blank=True, verbose_name="Middle name"
    )
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.OWNER,
        verbose_name="Type of user",
    )
    status = models.CharField(
        max_length=10,
        choices=UserStatus.choices,
        default=UserStatus.NEW,
        verbose_name="Status",
    )
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, verbose_name="Profile image"
    )
    birthday = models.DateField(null=True, blank=True, verbose_name="Birthday")
    description = models.TextField(blank=True, verbose_name="Description")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    viber = models.CharField(max_length=20, blank=True, verbose_name="Viber")
    telegram = models.CharField(max_length=50, blank=True, verbose_name="Telegram")
    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Role"
    )

    def get_full_name(self):
        """Get full name."""
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()

    def __str__(self):
        """__str__."""
        return self.get_full_name() or self.username


class Ticket(models.Model):
    """A ticket for a master call."""

    class TicketStatus(models.TextChoices):
        """Ticket status."""

        NEW = "new", "Новое"
        IN_PROGRESS = "in_progress", "B работе"
        DONE = "done", "Выполнено"

    role = models.ForeignKey(
        Role, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Role"
    )
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.NEW,
        verbose_name="Status",
    )
    apartment = models.ForeignKey(
        "building.Apartment", on_delete=models.CASCADE, verbose_name="Apartment"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="User (author/master)"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    description = models.TextField(verbose_name="Description")
    date = models.DateField(auto_now_add=True, verbose_name="Date")
    time = models.TimeField(auto_now_add=True, verbose_name="Time")

    class Meta:
        """Meta class."""

        verbose_name = "Application"
        verbose_name_plural = "Applications"
        ordering = ["-date", "-time"]

    def __str__(self):
        """__str__."""
        return f"Application №{self.id}"


class Message(models.Model):
    """Message."""

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_messages",
        verbose_name="sender",
    )
    recipients = models.ManyToManyField(
        User,
        through="MessageRecipient",
        related_name="received_messages",
        verbose_name="Recipients",
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    text = models.TextField(verbose_name="Text")
    date = models.DateField(auto_now_add=True, verbose_name="Date")

    class Meta:
        """Meta class."""

        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["-date"]

    def __str__(self):
        """__str__."""
        return self.title


class MessageRecipient(models.Model):
    """MessageRecipient."""

    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Message"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Sender")

    class Meta:
        """Meta class."""

        verbose_name = "Message recipient"
        verbose_name_plural = "Messages recipients"
        unique_together = ("message", "user")

    def __str__(self):
        """__str__."""
        return f"Recipient '{self.user}' for message '{self.message.title}'"
