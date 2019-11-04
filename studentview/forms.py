from django import forms
from .models import Registrations
from teacherview.models import SubEvents as S
from teacherview.models import Status 
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
    
'''
fields = { 'name': forms.CharField(max_length=50),
            'email': forms.EmailField(),
            'message': forms.CharField(widget=forms.Textarea) }
if not user.is_authenticated():
    fields['captcha'] = CaptchaField()
return type('RegistrationsGroupForm', (forms.BaseForm,), { 'base_fields': fields })
'''

'''
class RegistrationsGroupForm(forms.ModelForm,subevent_id):
    sub = SubEvents.objects.get(subevent_id=subevent_id)
    l=[]
    for i in range(sub.group_size):
        student = forms.CharField(help_text="Name of Student {}".format(str(i+1)),widget=forms.TextInput())
        grade = forms.IntegerField(help_text="Grade Of Student {} (Eg:11)".format(str(i+1)),widget=forms.NumberInput(attrs={'size': '20'}))
        section = forms.CharField(help_text="Section of Student {} (Eg:A)".format(str(i+1)),widget=forms.TextInput())
        l.append([student,grade,section])
    additional_Information = forms.CharField(help_text="Reason For Desire To Participate, Relevant Experience, etc..",widget=forms.Textarea(attrs={'rows':10, 'cols':50, 'placeholder':'Enter The Information Here...'}))
    #event_id = event_id
    #subevent_id = subevent_id
    
    class Meta:
        model = Registrations
        f = []
        for i in l:
            f.append(i[0])
            f.append(i[1])
            f.append(i[2])

        fields = [f,'additional_Information']
'''

class AchievementForm(forms.ModelForm):
    achievement_title = forms.CharField(help_text="Title For Achievement (Eg:Cisco Internship)",widget=forms.TextInput(attrs={'placeholder':'Enter The Name For Achievement Here...'}))
    start_date_of_achievement = forms.CharField(help_text="Start Date Of Achievement (Eg:1st January,2020)",widget=SelectDateWidget())
    last_date_of_achievement = forms.CharField(help_text="Late Date Of Achievement (Eg:3rd January,2020)",widget=SelectDateWidget())
    achievement_type = forms.CharField(help_text="Category Of Achievement (Eg:Technology)",widget=forms.TextInput())
    achievement_info = forms.CharField(help_text="Explain The Achievement",widget=forms.Textarea(attrs={'rows':10, 'cols':50, 'placeholder':'Enter The Information Here...'}))

    class Meta:
        model = Status
        fields = ["achievement_title","start_date_of_achievement","last_date_of_achievement","achievement_type","achievement_info"]