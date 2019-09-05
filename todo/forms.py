from django import forms
from datetime import datetime


class CreateTodoForm(forms.Form):
    name = forms.CharField(max_length=64)
    description = forms.CharField(max_length=256)
    deadline = forms.DateTimeField(input_formats=["%m/%d/%Y %I:%M %p"])

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        if deadline < datetime.now():
            raise forms.ValidationError('Please choose future date')
        return deadline
