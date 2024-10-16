
from django import forms

from games.models import BuddyRequest


class BuddyRequestForm(forms.ModelForm):
    class Meta:
        model = BuddyRequest
        fields = ('description', 'goal', 'min_age', 'max_age', 'voice')
