from django import forms
from docs.models import  WorkDocument, Product
from .models import Task


class TaskForm(forms.ModelForm):
    work_document = forms.ModelChoiceField(
        queryset=WorkDocument.objects.all(),
        required=False,
        label="Рабочий документ"
    )

    class Meta:
        model = Task
        exclude = ['comments', 'files']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'completion_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        self.product = kwargs.pop('product', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if self.project:
            self.fields['predecessors'].queryset = Task.objects.filter(project=self.project)
            if not self.product:
                self.fields['product'].queryset = Product.objects.filter(project=self.project)
        if self.product:
            self.fields['project'].initial = self.product.project
