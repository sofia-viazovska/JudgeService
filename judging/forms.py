from django import forms
from .models import Score, Team, Criteria, SERVICE_CHOICES

class ScoreForm(forms.ModelForm):
    """Form for judges to score teams on criteria"""

    class Meta:
        model = Score
        fields = ['checked']
        widgets = {
            'checked': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class TeamServiceForm(forms.ModelForm):
    """Form for admins to select a service vector for a team"""

    class Meta:
        model = Team
        fields = ['service']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-select'})
        }
