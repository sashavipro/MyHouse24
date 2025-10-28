"""src/website/forms.py."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from src.website.models import AboutUsPage
from src.website.models import ContactPage
from src.website.models import Document
from src.website.models import Image
from src.website.models import MainBlock
from src.website.models import MainPage
from src.website.models import SeoBlock
from src.website.models import ServiceBlock
from src.website.models import ServicePage


class MainPageForm(forms.ModelForm):
    """Form for editing the content of the main page."""

    class Meta:
        """Meta class."""

        model = MainPage
        fields = ["title", "description", "is_show_apps"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control tinymce-editor"}
            ),
            "is_show_apps": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SeoBlockForm(forms.ModelForm):
    """Form for editing SEO data."""

    class Meta:
        """Meta class."""

        model = SeoBlock
        fields = ["title", "description", "keywords"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "keywords": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class MainBlockForm(forms.ModelForm):
    """Form for the 'Near us' block on the main page."""

    class Meta:
        """Meta class."""

        model = MainBlock
        fields = ["image", "title", "description"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control tinymce-editor", "rows": 5}
            ),
        }

    def __init__(self, *args, **kwargs):
        """Make image and description fields optional."""  # <-- ИСПРАВЛЕНО D401
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False
        self.fields["description"].required = False


class ImageForm(forms.ModelForm):
    """Form for one image in the gallery."""

    class Meta:
        """Meta class."""

        model = Image
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        """Make the image field optional."""  # <-- ИСПРАВЛЕНО D401
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False


class AboutUsPageForm(forms.ModelForm):
    """Form for editing the 'About Us' page."""

    class Meta:
        """Meta class."""

        model = AboutUsPage
        fields = ["title1", "description1", "image", "title2", "description2"]
        widgets = {
            "title1": forms.TextInput(attrs={"class": "form-control"}),
            "description1": forms.Textarea(
                attrs={"class": "form-control tinymce-editor"}
            ),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "title2": forms.TextInput(attrs={"class": "form-control"}),
            "description2": forms.Textarea(
                attrs={"class": "form-control tinymce-editor"}
            ),
        }


class DocumentForm(forms.ModelForm):
    """Form for one document."""

    class Meta:
        """Meta class."""

        model = Document
        fields = ["document", "name"]
        widgets = {
            "document": forms.FileInput(),
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


class ServiceBlockForm(forms.ModelForm):
    """Form for one service block."""

    class Meta:
        """Meta class."""

        model = ServiceBlock
        fields = ["image", "title", "description"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control tinymce-editor", "rows": 5}
            ),
        }


class ContactPageForm(forms.ModelForm):
    """Form for editing the 'Contacts' page."""

    class Meta:
        """Meta class."""

        model = ContactPage
        fields = [
            "title",
            "description",
            "url",
            "fullname",
            "location",
            "address",
            "phone",
            "email",
            "map",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control tinymce-editor"}
            ),
            "url": forms.URLInput(attrs={"class": "form-control"}),
            "fullname": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "map": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
        }


class LoginForm(AuthenticationForm):
    """Login form."""

    username = forms.CharField(
        label="Email или ID",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "E-mail или ID",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Пароль",
                "autocomplete": "current-password",
            }
        ),
    )


MainBlockFormSet = forms.inlineformset_factory(
    MainPage, MainBlock, form=MainBlockForm, extra=0
)


SliderImageFormSet = forms.modelformset_factory(
    Image,
    form=ImageForm,
    extra=0,
    max_num=3,
)

DocumentFormSet = forms.modelformset_factory(
    Document,
    form=DocumentForm,
    extra=1,
    can_delete=True,
)


ServiceBlockFormSet = forms.inlineformset_factory(
    ServicePage, ServiceBlock, form=ServiceBlockForm, extra=1, can_delete=True
)
