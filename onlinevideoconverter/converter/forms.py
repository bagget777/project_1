# converter/forms.py

# Формы Django для приложения converter.

from django import forms
from .models import ConversionRequest

# Форма для создания конверсионного запроса.
class ConversionRequestForm(forms.ModelForm):
    class Meta:
        model = ConversionRequest
        fields = ['video_url', 'email']
