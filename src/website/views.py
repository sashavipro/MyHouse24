"""src/website/views.py."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic import View

from src.website.models import AboutUsPage
from src.website.models import ContactPage
from src.website.models import Document
from src.website.models import Gallery
from src.website.models import Image
from src.website.models import MainBlock
from src.website.models import MainPage
from src.website.models import SeoBlock
from src.website.models import ServiceBlock
from src.website.models import ServicePage

from .forms import AboutUsPageForm
from .forms import ContactPageForm
from .forms import DocumentFormSet
from .forms import MainBlockFormSet
from .forms import MainPageForm
from .forms import SeoBlockForm
from .forms import ServiceBlockFormSet
from .forms import SliderImageFormSet


class HomePageView(TemplateView):
    """Display the public home page."""

    template_name = "core/user/home.html"

    def get_context_data(self, **kwargs):
        """Add the main page object to the context."""
        context = super().get_context_data(**kwargs)
        context["main_page"] = MainPage.objects.first()
        return context


class AboutPageView(TemplateView):
    """Display the public 'About Us' page."""

    template_name = "core/user/about.html"

    def get_context_data(self, **kwargs):
        """Add the 'About Us' page object and all documents to context."""
        context = super().get_context_data(**kwargs)
        context["about_page"] = AboutUsPage.objects.first()
        context["documents"] = Document.objects.all()
        return context


class ServicesPageView(TemplateView):
    """Display the public 'Services' page with pagination."""

    template_name = "core/user/services.html"

    def get_context_data(self, **kwargs):
        """Add the 'Services' page object and paginated services to context."""
        context = super().get_context_data(**kwargs)
        context["service_page"] = ServicePage.objects.first()
        all_services_list = ServiceBlock.objects.all().order_by("id")
        paginator = Paginator(all_services_list, 1)
        page_number = self.request.GET.get("page")
        context["page_obj"] = paginator.get_page(page_number)

        return context


class ContactsPageView(TemplateView):
    """Display the public 'Contacts' page."""

    template_name = "core/user/contacts.html"

    def get_context_data(self, **kwargs):
        """Add the 'Contacts' page object to the context."""
        context = super().get_context_data(**kwargs)
        context["contact_page"] = ContactPage.objects.first()
        return context


class AdminHomePageView(LoginRequiredMixin, UpdateView):
    """Handle the editing of the main page content."""

    model = MainPage
    form_class = MainPageForm
    template_name = "core/adminlte/admin_home_page.html"
    success_url = reverse_lazy("website:admin_home")

    def get_object(self, queryset=None):
        """Return the single main page instance, creating if necessary."""
        obj, created = MainPage.objects.get_or_create(
            id=1,
            defaults={
                "title": "Default Title",
                "description": "Default description",
                "seo_block": SeoBlock.objects.create(title="Home Page"),
                "gallery": Gallery.objects.create(name="Home Page Slider"),
            },
        )
        if created:
            for _ in range(3):
                Image.objects.create(gallery=obj.gallery)
            for i in range(6):
                MainBlock.objects.create(main_page=obj, title=f"Block {i + 1}")
        return obj

    def get_context_data(self, **kwargs):
        """Add extra forms and formsets to the context."""
        context = super().get_context_data(**kwargs)

        slider_queryset = (
            self.object.gallery.images.all().order_by("id")
            if self.object.gallery
            else Image.objects.none()
        )

        if self.request.POST:
            context["seo_form"] = SeoBlockForm(
                self.request.POST,
                instance=self.object.seo_block,
                prefix="seo",
            )
            context["blocks_formset"] = MainBlockFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object,
                prefix="blocks",
            )
            context["slider_formset"] = SliderImageFormSet(
                self.request.POST,
                self.request.FILES,
                queryset=slider_queryset,
                prefix="slider",
            )
        else:
            context["seo_form"] = SeoBlockForm(
                instance=self.object.seo_block, prefix="seo"
            )
            context["blocks_formset"] = MainBlockFormSet(
                instance=self.object, prefix="blocks"
            )
            context["slider_formset"] = SliderImageFormSet(
                queryset=slider_queryset, prefix="slider"
            )
        return context

    def form_valid(self, form):
        """Validate and save the main form and all related formsets."""
        context = self.get_context_data()
        seo_form = context["seo_form"]
        blocks_formset = context["blocks_formset"]
        slider_formset = context["slider_formset"]

        if (
            seo_form.is_valid()
            and blocks_formset.is_valid()
            and slider_formset.is_valid()
        ):
            self.object = form.save()
            seo_form.save()
            blocks_formset.save()
            slider_formset.save()
            return super().form_valid(form)

        return self.form_invalid(form)


class AdminAboutPageView(LoginRequiredMixin, UpdateView):
    """Handle the editing of the 'About Us' page content."""

    model = AboutUsPage
    form_class = AboutUsPageForm
    template_name = "core/adminlte/admin_about_page.html"
    success_url = reverse_lazy("website:admin_about")

    def get_object(self, queryset=None):
        """Return the single page instance, creating galleries if needed."""
        obj, created = AboutUsPage.objects.get_or_create(
            id=1,
            defaults={"seo_block": SeoBlock.objects.create(title="About us")},
        )
        if created or not obj.gallery1:
            obj.gallery1 = Gallery.objects.create(name="Gallery 1 'About us'")
            obj.save()
        if created or not obj.gallery2:
            obj.gallery2 = Gallery.objects.create(name="Gallery 2 'About us'")
            obj.save()
        return obj

    def get_context_data(self, **kwargs):
        """Add the SEO form, document formset, and gallery images."""
        context = super().get_context_data(**kwargs)
        context["about_form"] = context.pop("form")

        if "seo_form" not in context:
            context["seo_form"] = SeoBlockForm(
                instance=self.object.seo_block, prefix="seo"
            )
        if "docs_formset" not in context:
            context["docs_formset"] = DocumentFormSet(
                queryset=Document.objects.all(), prefix="docs"
            )

        context["gallery1_images"] = self.object.gallery1.images.all()
        context["gallery2_images"] = self.object.gallery2.images.all()
        return context

    def post(self, request, *args, **kwargs):
        """Handle POST requests with form and formsets validation."""
        self.object = self.get_object()
        form = self.get_form()
        seo_form = SeoBlockForm(
            request.POST, instance=self.object.seo_block, prefix="seo"
        )
        docs_formset = DocumentFormSet(request.POST, request.FILES, prefix="docs")

        if form.is_valid() and seo_form.is_valid() and docs_formset.is_valid():
            return self.form_valid(form, seo_form, docs_formset)

        return self.form_invalid(form, seo_form, docs_formset)

    def form_valid(self, form, seo_form, docs_formset):
        """If the forms are valid, save the associated models."""
        form.save()
        seo_form.save()
        docs_formset.save()

        for file in self.request.FILES.getlist("gallery1_files"):
            Image.objects.create(gallery=self.object.gallery1, image=file)
        for file in self.request.FILES.getlist("gallery2_files"):
            Image.objects.create(gallery=self.object.gallery2, image=file)

        return redirect(self.get_success_url())

    def form_invalid(self, form, seo_form, docs_formset):
        """If any form is invalid, re-render with data-filled forms."""
        context = self.get_context_data()
        context["form"] = form
        context["seo_form"] = seo_form
        context["docs_formset"] = docs_formset
        return self.render_to_response(context)


class AdminServicesPageView(LoginRequiredMixin, View):
    """Handle the 'Services' admin page."""

    template_name = "core/adminlte/admin_services_page.html"
    success_url = reverse_lazy("website:admin_services")

    def get(self, request, *args, **kwargs):
        """Handle GET request: instantiate and display the forms."""
        service_page, _ = ServicePage.objects.get_or_create(
            id=1, defaults={"seo_block": SeoBlock.objects.create(title="Услуги")}
        )

        seo_form = SeoBlockForm(instance=service_page.seo_block, prefix="seo")
        formset = ServiceBlockFormSet(instance=service_page, prefix="services")

        context = {"form": seo_form, "formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Handle POST request: validate and save the form data."""
        service_page = ServicePage.objects.get(id=1)

        seo_form = SeoBlockForm(
            request.POST, instance=service_page.seo_block, prefix="seo"
        )
        formset = ServiceBlockFormSet(
            request.POST,
            request.FILES,
            instance=service_page,
            prefix="services",
        )

        if seo_form.is_valid() and formset.is_valid():
            seo_form.save()
            formset.save()
            return redirect(self.success_url)

        context = {"form": seo_form, "formset": formset}
        return render(request, self.template_name, context)


class AdminContactsPageView(LoginRequiredMixin, UpdateView):
    """Handle the editing of the 'Contacts' page content."""

    model = ContactPage
    form_class = ContactPageForm
    template_name = "core/adminlte/admin_contacts_page.html"
    success_url = reverse_lazy("website:admin_contacts")

    def get_object(self, queryset=None):
        """Return the single 'Contacts' page instance."""
        obj, _ = ContactPage.objects.get_or_create(
            id=1,
            defaults={
                "title": "Contacts",
                "seo_block": SeoBlock.objects.create(title="Contacts"),
            },
        )
        return obj

    def get_context_data(self, **kwargs):
        """Add the SEO form to the context."""
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["seo_form"] = SeoBlockForm(
                self.request.POST, instance=self.object.seo_block
            )
        else:
            context["seo_form"] = SeoBlockForm(instance=self.object.seo_block)
        return context

    def form_valid(self, form):
        """Validate and save the main form and the SEO form."""
        context = self.get_context_data()
        seo_form = context["seo_form"]
        if seo_form.is_valid():
            self.object = form.save()
            seo_form.save()
            return super().form_valid(form)
        return self.form_invalid(form)


@method_decorator(require_POST, name="dispatch")
class DeleteDocumentView(LoginRequiredMixin, View):
    """Handle an AJAX request to delete a document."""

    def post(self, request, *args, **kwargs):
        """Find and delete a document by its ID."""
        doc_id = kwargs.get("doc_id")
        try:
            doc_to_delete = get_object_or_404(Document, id=doc_id)
            doc_to_delete.delete()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Document deleted successfully",
                }
            )
        except Document.DoesNotExist as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)


@method_decorator(require_POST, name="dispatch")
class DeleteGalleryImageView(LoginRequiredMixin, View):
    """Handle an AJAX request to delete an image from a gallery."""

    def post(self, request, *args, **kwargs):
        """Find and delete an image by its ID."""
        image_id = kwargs.get("image_id")
        try:
            image_to_delete = get_object_or_404(Image, id=image_id)
            image_to_delete.delete()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Image deleted successfully",
                }
            )
        except Image.DoesNotExist as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=404)
