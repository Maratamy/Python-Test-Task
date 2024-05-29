from django import forms

from .models import CurrencyRate


class DateRangeForm(forms.Form):
    choices = [('USD', 'Доллар США'),
    ('EUR', 'Евро'),
    ('GBP', 'Фунт стерлингов'),
    ('JPY', 'Японская йена'),
    ('TRY', 'Турецкая лира'),
    ('INR', 'Индийская рупия'),
    ('CNY', 'Китайский юань'),
    ]
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label="Начало отсчёта")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),label="Конец отсчёта")
    currency = forms.ChoiceField(choices=choices,label="Выбор валюты")
class DataGraph(forms.Form):
    choices = [('USD', 'Доллар США'),
               ('EUR', 'Евро'),
               ('GBP', 'Фунт стерлингов'),
               ('JPY', 'Японская йена'),
               ('TRY', 'Турецкая лира'),
               ('INR', 'Индийская рупия'),
               ('CNY', 'Китайский юань'),
               ]
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Начало отсчёта")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Конец отсчёта")
    currencies = forms.MultipleChoiceField(choices=choices,  label="Построить графики для следующих валют", widget=forms.CheckboxSelectMultiple())
