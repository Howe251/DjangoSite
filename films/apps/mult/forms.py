from django import forms
from .models import Genre


class ListForm(forms.Form):
    ordering = forms.ChoiceField(label="сортировка", required=False, initial=["-name", "По убыванию"], choices=[
        ["name", "По алфавиту А-Я"],
        ["-name", "По алфавиту Я-А"],
        ["-create_date", "Сначала новые"],
        ["create_date", "Сначала старые"]
    ])
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), label='жанры', empty_label="Выберите жанр",
                                   initial=1, required=False)
