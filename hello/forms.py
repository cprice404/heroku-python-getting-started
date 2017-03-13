from django import forms


class PersonForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
