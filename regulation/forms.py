from django import forms
from .models import Section, Image, File


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['name', 'parent', 'header', 'content', 'footer']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'header': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'footer': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ImageForm(forms.ModelForm):
    current_image = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Image
        fields = ['image', 'caption', 'current_image']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
            'current_image': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.image:
            self.fields['current_image'].initial = self.instance.image.url


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file', 'description']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }