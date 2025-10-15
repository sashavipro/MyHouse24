from django.db import models


# =============================================================================
# ОБЩИЕ / ПЕРЕИСПОЛЬЗУЕМЫЕ МОДЕЛИ
# =============================================================================

class SeoBlock(models.Model):
    """Модель для SEO-данных (Title, Description, Keywords)."""
    title = models.CharField(max_length=255, verbose_name="SEO Title")
    description = models.TextField(blank=True, verbose_name="SEO Description")
    keywords = models.CharField(max_length=255, blank=True, verbose_name="SEO Keywords")

    def __str__(self):
        return f"SEO Block: {self.title}"

    class Meta:
        verbose_name = "SEO блок"
        verbose_name_plural = "SEO блоки"


class Gallery(models.Model):
    """Модель галереи, которая может содержать несколько изображений."""
    name = models.CharField(max_length=100, verbose_name="Название галереи для админки")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Галерея"
        verbose_name_plural = "Галереи"


class Image(models.Model):
    """Модель отдельного изображения, связанного с галереей."""
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='images', verbose_name="Галерея")
    image = models.ImageField(upload_to='gallery_images/', verbose_name="Изображение")

    def __str__(self):
        return f"Изображение {self.id} для {self.gallery.name}"

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"


class Document(models.Model):
    """Модель для загрузки документа/файла."""
    name = models.CharField(max_length=100, verbose_name="Название документа для админки", default="Документ")
    document = models.FileField(upload_to='documents/', verbose_name="Файл")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


# =============================================================================
# МОДЕЛИ ДЛЯ СТРАНИЦ САЙТА
# =============================================================================

# --- Главная страница (Main) ---

class MainPage(models.Model):
    """Модель для контента главной страницы."""
    title = models.CharField(max_length=200, verbose_name="Заголовок слайдера")
    description = models.TextField(verbose_name="Описание слайдера")
    gallery = models.OneToOneField(Gallery, on_delete=models.SET_NULL, null=True, blank=True,
                                   verbose_name="Галерея для слайдера")
    is_show_apps = models.BooleanField(default=True, verbose_name="Показать ссылки на приложения")
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, verbose_name="SEO блок")

    def __str__(self):
        return "Контент главной страницы"

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"


class MainBlock(models.Model):
    """Блок с картинкой, заголовком и описанием для главной страницы."""
    main_page = models.ForeignKey(MainPage, on_delete=models.CASCADE, related_name='blocks',
                                  verbose_name="Главная страница")
    image = models.ImageField(upload_to='main_page/blocks/', verbose_name="Изображение")
    title = models.CharField(max_length=150, verbose_name="Заголовок блока")
    description = models.TextField(verbose_name="Описание блока")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блок на главной"
        verbose_name_plural = "Блоки на главной"


# --- Страница "О нас" (About Us) ---

class AboutUsPage(models.Model):
    """Модель для контента страницы 'О нас'."""
    title1 = models.CharField(max_length=200, verbose_name="Заголовок 1")
    description1 = models.TextField(verbose_name="Описание 1")
    image = models.ImageField(upload_to='about_us/avatar', verbose_name="Изображение")

    gallery1 = models.OneToOneField(Gallery, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='about_us_gallery1', verbose_name="Галерея 1")
    gallery2 = models.OneToOneField(Gallery, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='about_us_gallery2', verbose_name="Галерея 2")

    title2 = models.CharField(max_length=200, verbose_name="Заголовок 2")
    description2 = models.TextField(verbose_name="Описание 2")

    document = models.OneToOneField(Document, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Документ")
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, verbose_name="SEO блок")

    def __str__(self):
        return "Контент страницы 'О нас'"

    class Meta:
        verbose_name = "Страница 'О нас'"
        verbose_name_plural = "Страница 'О нас'"


# --- Страница "Услуги" (Services) ---

class ServicePage(models.Model):
    """Модель-контейнер для страницы 'Услуги'."""
    # У этой модели может не быть своих полей, она служит для группировки блоков услуг.
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, verbose_name="SEO блок")

    def __str__(self):
        return "Контент страницы 'Услуги'"

    class Meta:
        verbose_name = "Страница 'Услуги'"
        verbose_name_plural = "Страница 'Услуги'"


class ServiceBlock(models.Model):
    """Модель отдельного блока услуги."""
    service_page = models.ForeignKey(ServicePage, on_delete=models.CASCADE, related_name='services',
                                     verbose_name="Страница услуг")
    image = models.ImageField(upload_to='services/service_block', verbose_name="Изображение услуги")
    title = models.CharField(max_length=150, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание услуги")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


# --- Страница "Контакты" (Contact) ---

class ContactPage(models.Model):
    """Модель для контента страницы контактов."""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")

    url = models.URLField(blank=True, verbose_name="URL (например, ссылка на соцсеть)")
    fullname = models.CharField(max_length=255, blank=True, verbose_name="ФИО / Название компании")
    location = models.CharField(max_length=255, blank=True, verbose_name="Город / Местоположение")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=50, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")

    map = models.TextField(blank=True, verbose_name="Код для вставки карты (HTML/JS)")
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE, verbose_name="SEO блок")

    def __str__(self):
        return "Контент страницы 'Контакты'"

    class Meta:
        verbose_name = "Страница 'Контакты'"
        verbose_name_plural = "Страница 'Контакты'"
