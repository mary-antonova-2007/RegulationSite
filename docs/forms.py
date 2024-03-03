from django import forms
from .models import WorkDocument

class WorkDocumentForm(forms.ModelForm):
    class Meta:
        model = WorkDocument
        fields = ['name', 'content', 'document_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название'}),
            'content': forms.FileInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
        }
