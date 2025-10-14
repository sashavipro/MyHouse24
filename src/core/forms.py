from django import forms
from .models import MainPage, MainBlock, SeoBlock, Image


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control tinymce-editor'}),
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
    max_num=3 # Указываем, что форм должно быть не больше 3
)