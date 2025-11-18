from django import forms 
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('text', 'email')
        labels = {
            'email': 'Email (Optional)'
        }