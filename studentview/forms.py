from django import forms
from .models import Registrations
from django.forms.widgets import SelectDateWidget

class RegistrationSingleForm(forms.ModelForm):
    #user = current_user
    #name = current_user.first_name  + " " + current_user.last_name
    grade = forms.IntegerField(help_text="Grade Of Student (Eg:11)",widget=forms.NumberInput(attrs={'size': '20'}))
    section = forms.CharField(help_text="Section of Student (Eg:A)",widget=forms.TextInput())
    additional_Information = forms.CharField(help_text="Reason For Desire To Participate, Relevant Experience, etc..",widget=forms.Textarea(attrs={'rows':10, 'cols':50, 'placeholder':'Enter The Information Here...'}))
    #event_id = event_id
    #subevent_id = subevent_id
    
    class Meta:
        model = Registrations
        fields = ['grade','section','additional_Information']
