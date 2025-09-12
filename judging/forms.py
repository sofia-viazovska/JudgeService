from django import forms
from .models import Score, Team, Criteria

class ScoreForm(forms.ModelForm):
    """Form for judges to score teams on criteria"""
    
    class Meta:
        model = Score
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 0, 'max': 10, 'class': 'form-control'})
        }