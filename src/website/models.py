"""src/website/models.py."""

from django.db import models


class Gallery(models.Model):
    """Gallery."""

    name = models.CharField(max_length=100, verbose_name="Name of Gallery")

    class Meta:
        """Meta class."""

        verbose_name = "Gallery"
        verbose_name_plural = "Gallery"

    def __str__(self):
        """__str__."""
        return self.name


class Image(models.Model):
    """Image."""

    gallery = models.ForeignKey(
        Gallery, on_delete=models.CASCADE, related_name="images", verbose_name="Gallery"
    )
    image = models.ImageField(upload_to="gallery_images/", verbose_name="Image")

    class Meta:
        """Meta class."""

        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        """__str__."""
        return f"Image {self.id} for {self.gallery.name}"


class SeoBlock(models.Model):
    """Seo."""

    title = models.CharField(max_length=255, verbose_name="SEO Title")
    description = models.TextField(blank=True, verbose_name="SEO Description")
    keywords = models.CharField(max_length=255, blank=True, verbose_name="SEO Keywords")

    class Meta:
        """Meta class."""

        verbose_name = "Seo Block"
        verbose_name_plural = "Seo Blocks"

    def __str__(self):
        """__str__."""
        return f"SEO Block: {self.title}"


class Document(models.Model):
    """Document."""

    name = models.CharField(
        max_length=100,
        verbose_name="name",
        default="Document",
    )
    document = models.FileField(upload_to="documents/", verbose_name="File")

    class Meta:
        """Meta class."""

        verbose_name = "Name of Document"
        verbose_name_plural = "Name of Documents"

    def __str__(self):
        """__str__."""
        return self.name


class MainPage(models.Model):
    """Main page."""

    title = models.CharField(max_length=200, verbose_name="Slider title")
    description = models.TextField(verbose_name="Slider description")
    gallery = models.OneToOneField(
        Gallery,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Slider Gallery",
    )
    is_show_apps = models.BooleanField(default=True, verbose_name="is show apps")
    seo_block = models.OneToOneField(
        SeoBlock, on_delete=models.CASCADE, verbose_name="SEO"
    )

    class Meta:
        """Meta class."""

        verbose_name = "home page"
        verbose_name_plural = "home pages"

    def __str__(self):
        """__str__."""
        return "Content home pages"


class MainBlock(models.Model):
    """Main block."""

    main_page = models.ForeignKey(
        MainPage,
        on_delete=models.CASCADE,
        related_name="blocks",
        verbose_name="home pages",
    )
    image = models.ImageField(upload_to="main_page/blocks/", verbose_name="Image")
    title = models.CharField(max_length=150, verbose_name="title")
    description = models.TextField(verbose_name="description")

    class Meta:
        """Meta class."""

        verbose_name = "Main block"
        verbose_name_plural = "Main blocks"

    def __str__(self):
        """__str__."""
        return self.title


class AboutUsPage(models.Model):
    """About us page."""

    title1 = models.CharField(max_length=200, verbose_name="title 1", blank=True)
    description1 = models.TextField(verbose_name="description 1", blank=True)
    image = models.ImageField(
        upload_to="about_us/avatar", verbose_name="image", null=True, blank=True
    )

    gallery1 = models.OneToOneField(
        Gallery,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="about_us_gallery1",
        verbose_name="Gallery 1",
    )
    gallery2 = models.OneToOneField(
        Gallery,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="about_us_gallery2",
        verbose_name="Gallery 2",
    )

    title2 = models.CharField(max_length=200, verbose_name="title 2", blank=True)
    description2 = models.TextField(verbose_name="description 2", blank=True)

    seo_block = models.OneToOneField(
        SeoBlock, on_delete=models.CASCADE, verbose_name="SEO"
    )

    class Meta:
        """Meta class."""

        verbose_name = "About us page"
        verbose_name_plural = "About us pages"

    def __str__(self):
        """__str__."""
        return "Content about us page"


class ServicePage(models.Model):
    """Service page."""

    seo_block = models.OneToOneField(
        SeoBlock, on_delete=models.CASCADE, verbose_name="SEO"
    )

    class Meta:
        """Meta class."""

        verbose_name = "Service page"
        verbose_name_plural = "Service pages"

    def __str__(self):
        """__str__."""
        return "Content service page"


class ServiceBlock(models.Model):
    """Service block."""

    service_page = models.ForeignKey(
        ServicePage,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="Service page",
    )
    image = models.ImageField(upload_to="services/service_block", verbose_name="image")
    title = models.CharField(max_length=150, verbose_name="title")
    description = models.TextField(verbose_name="description")

    class Meta:
        """Meta class."""

        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        """__str__."""
        return self.title


class ContactPage(models.Model):
    """Contact page."""

    title = models.CharField(max_length=200, verbose_name="title")
    description = models.TextField(blank=True, verbose_name="description")

    url = models.URLField(blank=True, verbose_name="URL")
    fullname = models.CharField(max_length=255, blank=True, verbose_name="fullname")
    location = models.CharField(max_length=255, blank=True, verbose_name="location")
    address = models.CharField(max_length=255, verbose_name="address", blank=True)
    phone = models.CharField(max_length=50, verbose_name="phone", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)

    map = models.TextField(blank=True, verbose_name="map")
    seo_block = models.OneToOneField(
        SeoBlock, on_delete=models.CASCADE, verbose_name="SEO"
    )

    class Meta:
        """Meta class."""

        verbose_name = "Contact page"
        verbose_name_plural = "Contact page"

    def __str__(self):
        """__str__."""
        return "Content contact page"
