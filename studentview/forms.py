from django import forms
from .models import Registrations
from teacherview.models import SubEvents as S
from teacherview.models import Status 
from django.forms.widgets import SelectDateWidget
from django.contrib.auth.models import User

class UserSignUpStudentForm(forms.ModelForm):
    first_name = forms.CharField(help_text="First Name",widget=forms.TextInput())
    last_name = forms.CharField(help_text="Last Name",widget=forms.TextInput())
    email = forms.CharField(help_text="Email Address",widget=forms.TextInput())
    #status = S
    #achievements = None
    #Department = None
    password = forms.CharField(help_text="Maintain a strong password for security purposes", widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    security_questions = (
		("What was your childhood nickname?","What was your childhood nickname?"),
        ("What is the name of your favorite childhood friend?","What is the name of your favorite childhood friend?"),
        ("What street did you live on in third grade?","What street did you live on in third grade?"),
        ("What is your oldest sibling's middle name?","What is your oldest sibling's middle name?"),
        ("What school did you attend for sixth grade?","What school did you attend for sixth grade?"),
        ("In what city does your nearest sibling live?","In what city does your nearest sibling live?")
	)

    security_question_1 = forms.CharField(help_text="Security Question 1",widget=forms.Select(choices=security_questions,attrs={'class':'form-control'}))
    response_1 = forms.CharField(help_text="Answer to Question 1",widget=forms.TextInput())
    security_question_2 = forms.CharField(help_text="Security Question 2",widget=forms.Select(choices=security_questions,attrs={'class':'form-control'}))
    response_2 = forms.CharField(help_text="Answer to Question 2",widget=forms.TextInput())
    security_question_3 = forms.CharField(help_text="Security Question 3",widget=forms.Select(choices=security_questions,attrs={'class':'form-control'}))
    response_3 = forms.CharField(help_text="Answer to Question 3",widget=forms.TextInput())

    class Meta:
        model = User
        fields = ['first_name','last_name','email']

class UserSignUpTeacherForm(forms.ModelForm):
    first_name = forms.CharField(help_text="First Name",widget=forms.TextInput())
    last_name = forms.CharField(help_text="Last Name",widget=forms.TextInput())
    email = forms.CharField(help_text="Email Address",widget=forms.TextInput())
    #status = S
    #achievements = None
    department = forms.CharField(help_text="Current Teaching Department. Eg: Head of Computer Science",widget=forms.TextInput())
    password = forms.CharField(help_text="Maintain a strong password for security purposes", widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    security_questions = (
		("What was your childhood nickname?","What was your childhood nickname?"),
        ("What is the name of your favorite childhood friend?","What is the name of your favorite childhood friend?"),
        ("What street did you live on in third grade?","What street did you live on in third grade?"),
        ("What is your oldest sibling's middle name?","What is your oldest sibling's middle name?"),
        ("What school did you attend for sixth grade?","What school did you attend for sixth grade?"),
        ("In what city does your nearest sibling live?","In what city does your nearest sibling live?")
	)

    security_question_1 = forms.CharField(help_text="Security Question 1",widget=forms.Select(choices=security_questions,attrs={'class':'form-control'}))
    response_1 = forms.CharField(help_text="Answer to Question 1",widget=forms.TextInput())
    security_question_2 = forms.CharField(help_text="Security Question 2",widget=forms.Select(choices=security_questions,attrs={'class':'form-control'}))
    response_2 = forms.CharField(help_text="Answer to Question 2",widget=forms.TextInput())
    security_question_3 = forms.CharField(help_text="Security Question 3",widget=forms.Select(choices=security_questions,attrs={'class':'form-control'}))
    response_3 = forms.CharField(help_text="Answer to Question 3",widget=forms.TextInput())

    class Meta:
        model = User
        fields = ['first_name','last_name','email']


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

class RegistrationsGroupForm(forms.ModelForm):
    user = forms.IntegerField(help_text="ID Of The User",widget=forms.TextInput())
    #name = current_user.first_name  + " " + current_user.last_name
    grade = forms.IntegerField(help_text="Grade Of Student (Eg:11)",widget=forms.NumberInput(attrs={'size': '20'}))
    section = forms.CharField(help_text="Section of Student (Eg:A)",widget=forms.TextInput())
    additional_Information = forms.CharField(help_text="Reason For Desire To Participate, Relevant Experience, etc..",widget=forms.Textarea(attrs={'rows':10, 'cols':50, 'placeholder':'Enter The Information Here...'}))
    #event_id = event_id
    #subevent_id = subevent_id
    
    class Meta:
        model = Registrations
        fields = ['grade','section','additional_Information']

class AchievementForm(forms.ModelForm):
    achievement_title = forms.CharField(help_text="Title For Achievement (Eg:Cisco Internship)",widget=forms.TextInput(attrs={'placeholder':'Name of Achievement...','class':'form-control'}))
    start_date_of_achievement = forms.CharField(help_text="Start Date Of Achievement (Eg:1st January,2020)",widget=forms.TextInput(attrs={'class':'form-control','type':'date'}))
    last_date_of_achievement = forms.CharField(help_text="Late Date Of Achievement (Eg:3rd January,2020)",widget=forms.TextInput(attrs={'class':'form-control','type':'date'}))
    cat_options = (
		("IT",'IT'),
		("Sport",'Sport'),
		("Debate",'Debate'),
		("Public Speaking",'Public Speaking'),
		("Educational",'Educational'),
		("Technology",'Technology'),
		("Literature",'Literature'),
		("Design",'Design'),
		("Science",'Science')
	)
    achievement_type = forms.CharField(help_text="Category Of Achievement (Eg:Technology)",widget=forms.Select(choices=cat_options,attrs={'class':'form-control'}))
    achievement_info = forms.CharField(help_text="Explain The Achievement",widget=forms.Textarea(attrs={'rows':10, 'cols':50, 'placeholder':'Enter The Information Here...','class':'form-control'}))

    class Meta:
        model = Status
        fields = ["achievement_title","start_date_of_achievement","last_date_of_achievement","achievement_type","achievement_info"]