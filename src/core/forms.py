from django import forms
from .models import MainPage, MainBlock, SeoBlock, Image, AboutUsPage, Document, ServiceBlock


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = ['title', 'description', 'is_show_apps']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control tinymce-editor'}),
            'is_show_apps': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = ['title', 'description', 'keywords']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'keywords': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class MainBlockForm(forms.ModelForm):
    class Meta:
        model = MainBlock
        fields = ['image', 'title', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control tinymce-editor', 'rows': 5}),
        }


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class AboutUsPageForm(forms.ModelForm):
    class Meta:
        model = AboutUsPage
        # Включаем все поля, кроме внешних ключей, которые обработаем отдельно
        exclude = ['gallery1', 'gallery2', 'document', 'seo_block']
        widgets = {
            'title1': forms.TextInput(attrs={'class': 'form-control'}),
            'description1': forms.Textarea(attrs={'class': 'form-control tinymce-editor'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title2': forms.TextInput(attrs={'class': 'form-control'}),
            'description2': forms.Textarea(attrs={'class': 'form-control tinymce-editor'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document', 'name']
        widgets = {
            'document': forms.ClearableFileInput(),  # Уберем класс, чтобы стилизовать вручную
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ServiceBlockForm(forms.ModelForm):
    class Meta:
        model = ServiceBlock
        fields = ['image', 'title', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control tinymce-editor', 'rows': 5}),
        }


# --- ФОРМСЕТЫ ---
# FormSet для блоков "Рядом с нами". `extra=0` означает, что не будет создаваться пустых форм для добавления новых.
MainBlockFormSet = forms.modelformset_factory(
    MainBlock,
    form=MainBlockForm,
    extra=0
)

# FormSet для слайдов. Мы хотим редактировать ровно 3 слайда.
SliderImageFormSet = forms.modelformset_factory(
    Image,
    form=ImageForm,
    extra=0,
    max_num=3  # Указываем, что форм должно быть не больше 3
)

# Формсет для документов. `extra=1` - показывать одну пустую форму для добавления.
# `can_delete=True` - позволит удалять существующие документы.
DocumentFormSet = forms.modelformset_factory(
    Document,
    form=DocumentForm,
    extra=1,
    can_delete=True
)

# Формсет для Услуг. `extra=1` и `can_delete=True` позволят добавлять и удалять услуги.
ServiceBlockFormSet = forms.modelformset_factory(
    ServiceBlock,
    form=ServiceBlockForm,
    extra=0,
    can_delete=True
)
