from django import forms
from .models import Mult


class SearchForm(forms.ModelForm):
    class Meta:
        model = Mult
        fields = ("text", )
