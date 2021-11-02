from django import forms
from .models import Mult


class SortForm(forms.Form):
    # az = forms.ChoiceField(label="По алфавиту", required=False)
    ordering = forms.ChoiceField(label="сортировка", required=False, initial=["-name", "По убыванию"], choices=[
        ["name", "По алфавиту А-Я"],
        ["-name", "По алфавиту Я-А"],
        ["create_date", "Сначала новые"],
        ["-create_date", "Сначала старые"]
    ])
    # ordering = ModelForm.ChoiceField(label="Сортировка", required=False, choices=[
    #
    # ])
