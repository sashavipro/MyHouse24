"""src/building/models.py."""

from django.db import models


class House(models.Model):
    """House."""

    title = models.CharField(max_length=255, verbose_name="Название")
    address = models.TextField(verbose_name="Адрес")
    image1 = models.ImageField(
        upload_to="houses/", null=True, blank=True, verbose_name="Image 1"
    )
    image2 = models.ImageField(
        upload_to="houses/", null=True, blank=True, verbose_name="Image 2"
    )
    image3 = models.ImageField(
        upload_to="houses/", null=True, blank=True, verbose_name="Image 3"
    )
    image4 = models.ImageField(
        upload_to="houses/", null=True, blank=True, verbose_name="Image 4"
    )
    image5 = models.ImageField(
        upload_to="houses/", null=True, blank=True, verbose_name="Image 5"
    )
    staff = models.ManyToManyField(
        "users.User", through="HouseStaff", verbose_name="Service staff"
    )

    class Meta:
        """Meta class."""

        verbose_name = "House"
        verbose_name_plural = "Houses"

    def __str__(self):
        """__str__."""
        return self.title


class HouseStaff(models.Model):
    """House staff."""

    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name="House")
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, verbose_name="Employee"
    )
    role_in_house = models.CharField(max_length=100, verbose_name="Role in house")

    class Meta:
        """Meta class."""

        verbose_name = "House staff"
        verbose_name_plural = "House staff"
        unique_together = ("house", "user")

    def __str__(self):
        """__str__."""
        # Используем f-строку для форматирования
        return f"{self.user.get_full_name()} в доме '{self.house.title}'"


class Section(models.Model):
    """Section."""

    name = models.CharField(max_length=100, verbose_name="Name")
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="sections", verbose_name="House"
    )

    class Meta:
        """Meta class."""

        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        """__str__."""
        return f"{self.name} ({self.house.title})"


class Floor(models.Model):
    """Floor."""

    name = models.CharField(max_length=100, verbose_name="Number floor")
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="floors", verbose_name="house"
    )

    class Meta:
        """Meta class."""

        verbose_name = "Floor"
        verbose_name_plural = "Floors"

    def __str__(self):
        """__str__."""
        return f"{self.name} ({self.house.title})"


class PersonalAccount(models.Model):
    """Personal account."""

    number = models.CharField(
        max_length=20, unique=True, verbose_name="Personal account number"
    )
    status = models.CharField(max_length=20, default="active", verbose_name="Status")
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, verbose_name="Balance"
    )

    class Meta:
        """Meta class."""

        verbose_name = "Personal account"
        verbose_name_plural = "Personals accounts"

    def __str__(self):
        """__str__."""
        return self.number


class Apartment(models.Model):
    """Apartment."""

    number = models.CharField(max_length=10, verbose_name="Number")
    area = models.FloatField(verbose_name="Area", null=True, blank=True)

    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name="House")
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, verbose_name="Section", null=True, blank=True
    )
    floor = models.ForeignKey(
        Floor, on_delete=models.CASCADE, verbose_name="Floor", null=True, blank=True
    )

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apartments",
        verbose_name="Owner",
    )
    tariff = models.ForeignKey(
        "finance.Tariff",
        on_delete=models.PROTECT,
        verbose_name="Tariff",
        null=True,
        blank=True,
    )
    personal_account = models.OneToOneField(
        PersonalAccount,
        on_delete=models.CASCADE,
        verbose_name="Personal account",
        null=True,
        blank=True,
    )

    class Meta:
        """Meta class."""

        verbose_name = "Apartment"
        verbose_name_plural = "Apartments"
        unique_together = (
            "house",
            "number",
        )

    def __str__(self):
        """__str__."""
        return f"Apartment {self.number}, {self.house.title}"
