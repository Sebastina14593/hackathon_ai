from django import forms
from messanger.models import Chat, MultiChoiceOption

class FormResultForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['user_email', 'problem_description', 'detailed_description', 'multiple_choice']

        widgets = {
            'multiple_choice': forms.CheckboxSelectMultiple(attrs={'class': 'form-checkbox'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control full-width'}),
            'problem_description': forms.RadioSelect(attrs={'class': 'form-control'}),
            'detailed_description': forms.Textarea(attrs={'class': 'form-control full-text-area'}),
        }