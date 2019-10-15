from django import forms


class InputForm(forms.Form):
    Input_Word = forms.CharField(max_length=5000)
