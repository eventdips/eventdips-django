from django import forms
from .models import Registrations
from django.forms.widgets import SelectDateWidget

class RegistrationForm(forms.ModelForm):
    #user = current_user
    name = forms.CharField(widget=forms.TextInput())
    grade = forms.IntegerField(help_text="Grade Of Student (Eg:11)",widget=forms.NumberInput(attrs={'size': '20'}))
    section = forms.CharField(help_text="Section of Student (Eg:A)",widget=forms.TextInput())
    #
