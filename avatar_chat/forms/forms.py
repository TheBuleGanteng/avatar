from django import forms
from django.utils.translation import gettext_lazy as _

__all__ = ['InputForm']

#------------------------------------------------------------------------

# Uses standard django CharField
class InputForm(forms.Form):
    user_input = forms.CharField( 
        max_length=4096,
        widget=forms.Textarea(attrs={
            'autofocus': True,
            'rows': 2,
            'autocomplete': 'off',
            'class': 'form-control border border-2 border-secondary',
            'placeholder': _('ask your question here'),
        })
    )
    first_name = forms.CharField(widget=forms.HiddenInput()) # Included so it can be accessible to the JS via FormData
    timestamp = forms.CharField(widget=forms.HiddenInput()) # Included so it can be accessible to the JS via FormData

    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        # Set required=True for all fields in this form
        for field_name in self.fields:
            self.fields[field_name].required = True

    def clean(self):
        cleaned_data = super().clean() # Use of super().clean() allows Django's built-in validation to happen first, and then the additional custom validation below is applied to that cleaned data.
        user_input = cleaned_data.get("user_input")
        first_name = cleaned_data.get("first_name")
        timestamp = cleaned_data.get("timestamp")
        
        return cleaned_data


