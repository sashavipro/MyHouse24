"""src/users/models.py."""

import logging
import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.db import DatabaseError
from django.db import IntegrityError
from django.db import models

logger = logging.getLogger(__name__)


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
    has_article = models.BooleanField(default=False, verbose_name="Access to Articles")

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
        default=UserType.EMPLOYEE,
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

    def save(self, *args, **kwargs):
        """Auto-assign 'Director' role to superusers.

        Sync user's groups with their role.
        """
        if self.is_superuser and not self.role:
            try:
                all_permissions = {}
                # Using get_fields() instead of accessing _meta.fields directly
                for field in Role._meta.get_fields():  # noqa: SLF001
                    if hasattr(field, "name") and field.name.startswith("has_"):
                        all_permissions[field.name] = True

                director_role, _ = Role.objects.get_or_create(
                    name="Директор", defaults=all_permissions
                )

                self.role = director_role
                self.user_type = self.UserType.EMPLOYEE
            except (DatabaseError, IntegrityError):
                # logging.exception automatically includes exception info
                logger.exception("Auto-assign role error")

        super().save(*args, **kwargs)

        if self.role:
            try:
                group, _ = Group.objects.get_or_create(name=self.role.name)

                current_groups = set(self.groups.all())
                if current_groups != {group}:
                    self.groups.set([group])

            except (DatabaseError, IntegrityError):
                logger.exception(
                    "Failed to sync user %s with group %s due to a database error.",
                    self.username,
                    self.role.name,
                )
        elif self.groups.exists():
            self.groups.clear()

    def get_full_name(self):
        """Get full name."""
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()

    def __str__(self):
        """__str__."""
        return self.get_full_name() or self.username


class Owner(User):
    """Proxy model for the User model to represent apartment owners.

    This model does not create a new database table. It allows us to have
    a separate set of permissions for owners in the Django admin and for our
    custom permission system.
    """

    class Meta:
        """Meta class."""

        proxy = True
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"


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
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="tickets_created",
    )
    master = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Мастер",
        related_name="tickets_assigned",
        limit_choices_to={"user_type": "employee"},
    )
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Phone")
    description = models.TextField(verbose_name="Description")
    date = models.DateField(verbose_name="Желаемая дата")
    time = models.TimeField(verbose_name="Желаемое время")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        """Meta class."""

        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ["-created_at"]

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
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")

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
    is_read = models.BooleanField(default=False, verbose_name="Прочитано")
    is_hidden = models.BooleanField(default=False, verbose_name="Скрыто получателем")

    class Meta:
        """Meta class."""

        verbose_name = "Message recipient"
        verbose_name_plural = "Messages recipients"
        unique_together = ("message", "user")

    def __str__(self):
        """__str__."""
        return f"Recipient '{self.user}' for message '{self.message.title}'"


class Invitation(models.Model):
    """Model to store one-time invitation tokens."""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        """Str."""
        return f"Invitation for {self.user.email}"
