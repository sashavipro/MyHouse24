from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from src.core.forms import MainPageForm, SeoBlockForm, SliderImageFormSet, MainBlockFormSet, AboutUsPageForm, \
    DocumentFormSet, ServiceBlockFormSet, ContactPageForm
from src.core.models import MainPage, MainBlock, SeoBlock, Gallery, Image, Document, AboutUsPage, ServicePage, \
    ServiceBlock, ContactPage


def home_page(request):
    main_page_data = MainPage.objects.first()
    context = {'main_page': main_page_data}
    return render(request, 'core/user/home.html', context)


def about(request):
    about_page_data = AboutUsPage.objects.first()
    documents = Document.objects.all()
    context = {
        'about_page': about_page_data,
        'documents': documents
    }
    return render(request, "core/user/about.html", context)


def services(request):
    service_page = ServicePage.objects.first()
    all_services_list = ServiceBlock.objects.all().order_by('id')
    paginator = Paginator(all_services_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'service_page': service_page,
        'page_obj': page_obj,
    }
    return render(request, "core/user/services.html", context)


def contacts(request):
    # Эта view понадобится для отображения публичной страницы контактов
    # Пока оставим её простой
    contact_page_data = ContactPage.objects.first()
    context = {'contact_page': contact_page_data}
    return render(request, "core/user/contacts.html", context)


def admin_stats(request):
    """View для главной страницы админки (статистика)."""
    context = {}
    return render(request, 'core/adminlte/admin_stats.html', context)


def admin_home_page(request):
    main_page_instance = MainPage.objects.first()
    if not main_page_instance:
        seo = SeoBlock.objects.create(title="Главная страница")
        gallery = Gallery.objects.create(name="Слайдер главной страницы")
        for _ in range(3):
            Image.objects.create(gallery=gallery)
        main_page_instance = MainPage.objects.create(
            title="Заголовок по умолчанию", description="Описание по умолчанию",
            seo_block=seo, gallery=gallery
        )
        for i in range(6):
            MainBlock.objects.create(main_page=main_page_instance, title=f"Блок {i + 1}")

    blocks_queryset = main_page_instance.blocks.all().order_by('id')
    slider_queryset = main_page_instance.gallery.images.all().order_by('id')

    if request.method == 'POST':
        main_page_form = MainPageForm(request.POST, instance=main_page_instance, prefix='main')
        seo_form = SeoBlockForm(request.POST, instance=main_page_instance.seo_block, prefix='seo')
        blocks_formset = MainBlockFormSet(request.POST, request.FILES, queryset=blocks_queryset, prefix='blocks')
        slider_formset = SliderImageFormSet(request.POST, request.FILES, queryset=slider_queryset, prefix='slider')

        if all([main_page_form.is_valid(), seo_form.is_valid(), blocks_formset.is_valid(), slider_formset.is_valid()]):
            main_page_form.save()
            seo_form.save()
            blocks_formset.save()
            slider_formset.save()
            return redirect('core:admin_home')
    else:
        main_page_form = MainPageForm(instance=main_page_instance, prefix='main')
        seo_form = SeoBlockForm(instance=main_page_instance.seo_block, prefix='seo')
        blocks_formset = MainBlockFormSet(queryset=blocks_queryset, prefix='blocks')
        slider_formset = SliderImageFormSet(queryset=slider_queryset, prefix='slider')

    context = {
        'main_page_form': main_page_form,
        'seo_form': seo_form,
        'blocks_formset': blocks_formset,
        'slider_formset': slider_formset,
    }
    return render(request, 'core/adminlte/admin_home_page.html', context)


def admin_about_page(request):
    about_page_instance, created = AboutUsPage.objects.get_or_create(id=1, defaults={
        'title1': 'Заголовок по умолчанию', 'description1': '', 'title2': 'Доп. заголовок',
        'description2': '', 'seo_block': SeoBlock.objects.create(title="О нас")
    })
    if not about_page_instance.gallery1:
        about_page_instance.gallery1 = Gallery.objects.create(name="Галерея 1 'О нас'")
    if not about_page_instance.gallery2:
        about_page_instance.gallery2 = Gallery.objects.create(name="Галерея 2 'О нас'")
    about_page_instance.save()

    if request.method == 'POST':
        about_form = AboutUsPageForm(request.POST, request.FILES, instance=about_page_instance, prefix='about')
        seo_form = SeoBlockForm(request.POST, instance=about_page_instance.seo_block, prefix='seo')
        docs_formset = DocumentFormSet(request.POST, request.FILES, prefix='docs')

        if about_form.is_valid() and seo_form.is_valid() and docs_formset.is_valid():
            about_form.save()
            seo_form.save()
            docs_formset.save()
            for file in request.FILES.getlist('gallery1_files'):
                Image.objects.create(gallery=about_page_instance.gallery1, image=file)
            for file in request.FILES.getlist('gallery2_files'):
                Image.objects.create(gallery=about_page_instance.gallery2, image=file)
            return redirect('core:admin_about')
    else:
        about_form = AboutUsPageForm(instance=about_page_instance, prefix='about')
        seo_form = SeoBlockForm(instance=about_page_instance.seo_block, prefix='seo')
        docs_formset = DocumentFormSet(queryset=Document.objects.all(), prefix='docs')

    context = {
        'about_form': about_form,
        'seo_form': seo_form,
        'docs_formset': docs_formset,
        'gallery1_images': about_page_instance.gallery1.images.all(),
        'gallery2_images': about_page_instance.gallery2.images.all(),
    }
    return render(request, 'core/adminlte/admin_about_page.html', context)


def admin_services_page(request):
    service_page, created = ServicePage.objects.get_or_create(id=1, defaults={
        'seo_block': SeoBlock.objects.create(title="Услуги")
    })

    if request.method == 'POST':
        formset = ServiceBlockFormSet(request.POST, request.FILES, prefix='services')
        seo_form = SeoBlockForm(request.POST, instance=service_page.seo_block, prefix='seo')

        if formset.is_valid() and seo_form.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.service_page = service_page
                instance.save()
            formset.save_m2m()
            for form in formset.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()
            seo_form.save()
            return redirect('core:admin_services')
    else:
        formset = ServiceBlockFormSet(queryset=ServiceBlock.objects.filter(service_page=service_page),
                                      prefix='services')
        seo_form = SeoBlockForm(instance=service_page.seo_block, prefix='seo')

    context = {
        'formset': formset,
        'seo_form': seo_form
    }
    return render(request, 'core/adminlte/admin_services_page.html', context)


def admin_contacts_page(request):
    contacts_page, created = ContactPage.objects.get_or_create(id=1, defaults={
        'title': 'Контакты', 'seo_block': SeoBlock.objects.create(title="Контакты")
    })

    if request.method == 'POST':
        form = ContactPageForm(request.POST, instance=contacts_page, prefix='contact')
        seo_form = SeoBlockForm(request.POST, instance=contacts_page.seo_block, prefix='seo')

        if form.is_valid() and seo_form.is_valid():
            form.save()
            seo_form.save()
            return redirect('core:admin_contacts')
    else:
        form = ContactPageForm(instance=contacts_page, prefix='contact')
        seo_form = SeoBlockForm(instance=contacts_page.seo_block, prefix='seo')

    context = {
        'form': form,
        'seo_form': seo_form
    }
    return render(request, 'core/adminlte/admin_contacts_page.html', context)


@require_POST
def delete_gallery_image(request, image_id):

    # if not request.user.is_staff:
    #     return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)

    try:
        image_to_delete = Image.objects.get(id=image_id)
        image_to_delete.delete()
        return JsonResponse({'status': 'success', 'message': 'Image deleted successfully'})
    except Image.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Image not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@require_POST
def delete_document(request, doc_id):
    try:
        doc_to_delete = Document.objects.get(id=doc_id)
        doc_to_delete.delete() # Удалит объект и связанный с ним файл
        return JsonResponse({'status': 'success', 'message': 'Document deleted successfully'})
    except Document.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Document not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)