from django.shortcuts import render, get_object_or_404, redirect

from src.core.forms import MainPageForm, SeoBlockForm, SliderImageFormSet, MainBlockFormSet, AboutUsPageForm, \
    DocumentFormSet
from src.core.models import MainPage, MainBlock, SeoBlock, Gallery, Image, Document, AboutUsPage


def admin_home_page(request):
    # Получаем объект главной страницы для редактирования
    main_page_instance = MainPage.objects.first()

    # Если объекта еще нет, нужно его создать. Это важный шаг для первого запуска.
    if not main_page_instance:
        seo = SeoBlock.objects.create(title="Главная страница")
        gallery = Gallery.objects.create(name="Слайдер главной страницы")
        # Создаем 3 пустых объекта Image для слайдера
        for _ in range(3):
            Image.objects.create(gallery=gallery)
        main_page_instance = MainPage.objects.create(
            title="Заголовок по умолчанию",
            description="Описание по умолчанию",
            seo_block=seo,
            gallery=gallery
        )
        for i in range(6):
            MainBlock.objects.create(main_page=main_page_instance, title=f"Блок {i + 1}")

    # Определяем queryset'ы для формсетов
    blocks_queryset = main_page_instance.blocks.all().order_by('id')
    slider_queryset = main_page_instance.gallery.images.all().order_by('id')

    if request.method == 'POST':
        # Создаем экземпляры форм и формсетов, передавая им данные из запроса
        main_page_form = MainPageForm(request.POST, instance=main_page_instance, prefix='main')
        seo_form = SeoBlockForm(request.POST, instance=main_page_instance.seo_block, prefix='seo')
        blocks_formset = MainBlockFormSet(request.POST, request.FILES, queryset=blocks_queryset, prefix='blocks')
        slider_formset = SliderImageFormSet(request.POST, request.FILES, queryset=slider_queryset, prefix='slider')

        # Проверяем валидность всех форм и формсетов
        if all([
            main_page_form.is_valid(),
            seo_form.is_valid(),
            blocks_formset.is_valid(),
            slider_formset.is_valid()
        ]):
            # Если все валидно, сохраняем
            main_page_form.save()
            seo_form.save()
            blocks_formset.save()
            slider_formset.save()

            # Можно добавить сообщение об успешном сохранении
            # messages.success(request, 'Данные главной страницы успешно обновлены!')
            return redirect('core:admin_home')
        else:
            # Если есть ошибки, Django автоматически передаст их в формы,
            # и они отобразятся в шаблоне.
            pass

    else:  # Для GET-запроса
        # Создаем "чистые" формы на основе данных из базы
        main_page_form = MainPageForm(instance=main_page_instance, prefix='main')
        seo_form = SeoBlockForm(instance=main_page_instance.seo_block, prefix='seo')
        blocks_formset = MainBlockFormSet(queryset=blocks_queryset, prefix='blocks')
        slider_formset = SliderImageFormSet(queryset=slider_queryset, prefix='slider')

    # Для GET-запроса (просто открываем страницу)
    context = {
        'main_page_form': main_page_form,
        'seo_form': seo_form,
        'blocks_formset': blocks_formset,
        'slider_formset': slider_formset,
    }

    return render(request, 'core/adminlte/admin_home_page.html', context)


def home_page(request):
    # Получаем ОДИН объект главной страницы. Предполагаем, что он всегда будет один.
    main_page_data = MainPage.objects.first()

    # Если в базе еще ничего нет, можно вернуть пустой контекст или обработать иначе
    if not main_page_data:
        return render(request, 'core/user/home.html', {})

    context = {
        'main_page': main_page_data,
        # Мы можем передать и другие данные, например, контакты, если они нужны на главной
    }
    return render(request, 'core/user/home.html', context)


def admin_about_page(request):
    # Получаем или создаем единственный экземпляр страницы "О нас"
    about_page_instance, created = AboutUsPage.objects.get_or_create(id=1, defaults={
        'title1': 'Заголовок по умолчанию',
        'description1': '',
        'title2': 'Доп. заголовок',
        'description2': '',
        'seo_block': SeoBlock.objects.create(title="О нас")
    })

    # Создаем галереи, если их нет
    if not about_page_instance.gallery1:
        about_page_instance.gallery1 = Gallery.objects.create(name="Галерея 1 'О нас'")
    if not about_page_instance.gallery2:
        about_page_instance.gallery2 = Gallery.objects.create(name="Галерея 2 'О нас'")
    about_page_instance.save()

    if request.method == 'POST':
        about_form = AboutUsPageForm(request.POST, request.FILES, instance=about_page_instance, prefix='about')
        seo_form = SeoBlockForm(request.POST, instance=about_page_instance.seo_block, prefix='seo')
        # Так как документы не привязаны напрямую к странице, queryset пустой
        docs_formset = DocumentFormSet(request.POST, request.FILES, prefix='docs')

        if about_form.is_valid() and seo_form.is_valid() and docs_formset.is_valid():
            about_form.save()
            seo_form.save()
            docs_formset.save()

            # Обработка загрузки в галереи (упрощенная)
            for file in request.FILES.getlist('gallery1_files'):
                Image.objects.create(gallery=about_page_instance.gallery1, image=file)
            for file in request.FILES.getlist('gallery2_files'):
                Image.objects.create(gallery=about_page_instance.gallery2, image=file)

            return redirect('core:admin_about')

    else:
        about_form = AboutUsPageForm(instance=about_page_instance, prefix='about')
        seo_form = SeoBlockForm(instance=about_page_instance.seo_block, prefix='seo')
        # Получаем все документы для редактирования
        docs_formset = DocumentFormSet(queryset=Document.objects.all(), prefix='docs')

    context = {
        'about_form': about_form,
        'seo_form': seo_form,
        'docs_formset': docs_formset,
        'gallery1_images': about_page_instance.gallery1.images.all(),
        'gallery2_images': about_page_instance.gallery2.images.all(),
    }

    return render(request, 'core/adminlte/admin_about_page.html', context)


def about(request):
    return render(request, "core/user/about.html")


def admin_services_page(request):
    return render(request, "core/adminlte/admin_services_page.html")


def services(request):
    return render(request, "core/user/services.html")


def admin_contacts_page(request):
    return render(request, "core/adminlte/admin_contacts_page.html")


def contacts(request):
    return render(request, "core/user/contacts.html")


def admin_tariff_page(request):
    return render(request, "core/adminlte/admin_tariff_page.html")


def admin_stats(request):
    """
    View для главной страницы админки (статистика).
    Пока это просто заглушка.
    """
    # Здесь в будущем будет логика для сбора статистики
    context = {}
    return render(request, 'core/adminlte/admin_stats.html', context)


