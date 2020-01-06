from django import forms
from django.contrib.auth.models import User
from .models import Events,SubEvents, Status
from studentview.models import Registrations
from django.forms.widgets import SelectDateWidget

def name_sort(l):
	for m in range(len(l)):
		for i in range(len(l)-1):
			if l[i][1]<l[i+1][1]:
				l[i],l[i+1]=l[i+1],l[i]
	
	return l

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput())

class ForgotPassword(forms.Form):
	email = forms.CharField(widget=forms.TextInput())

class ResetPassword(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput())
	confirm_password = forms.CharField(widget=forms.PasswordInput())
	
class EventCreationForm(forms.ModelForm):
	event_name = forms.CharField(widget= forms.TextInput(attrs={'placeholder':'Event Name Here'}))
	
	teacher_options = []
	users = User.objects.all()
	c=0
	for user in users:
		try:
			if Status.objects.get(user=user).status=="T" or Status.objects.get(user=user).status=="M":
				teacher_options.append((c,user.first_name + " " +user.last_name))
				c+=1
		except:
			pass

	teacher_options = name_sort(teacher_options)

	teacher_incharge = forms.CharField(widget=forms.Select(choices=teacher_options,attrs={'class':'form-control'}))
	event_information = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','rows':5, 'cols':50, 'placeholder':'Enter The Information Here...'}))
	start_date = forms.CharField(widget=SelectDateWidget(attrs={'class':'form-control'}))
	last_date = forms.CharField(widget=SelectDateWidget(attrs={'class':'form-control'}))
	options = (
		("True",'True'),
		("False",'False')
	)
	single_event = forms.CharField(help_text='''Enter True If The Event Does Not Have Any Events Under It.
												Example: Invictus- False, Debate Competition-True''',widget=forms.Select(choices=options,attrs={'class':'form-control'})) 

	add_attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'card-link'}))

	class Meta:
		model = Events
		fields = ['event_name','teacher_incharge','event_information','start_date','last_date','single_event']

class SingleEventInformationForm(forms.ModelForm):
	#subevent_name = event_name
	#subevent_dates = event_dates
	options = (
		("Individual",'Individual'),
		("Group",'Group')
	)
	event_type = forms.CharField(help_text='Individual Event or Group Event',widget=forms.Select(choices=options))
	group_size = forms.IntegerField(required=False,help_text="Number Of Students Per Group (If Individual Participation: Leave Blank)",widget=forms.NumberInput(attrs={'size': '20'}))
	maximum_applicants = forms.CharField(help_text='Maximum Number Of Applications',widget=forms.TextInput(attrs={'placeholder': '50'}))
	maximum_participants = forms.CharField(help_text='Maximum Number Of Students Who Can Participate In An Event',widget=forms.TextInput(attrs={'placeholder': '5'}))
	#subevent_information = event_information
	requirements = forms.CharField(help_text='Requirements or Selection Criteria.',widget=forms.Textarea(attrs={'rows':5, 'cols':50,'placeholder': '''Must Be From Class 10 \nMust have attended atleast 2 debate competetions... '''}))
	#subevent_teacher_incharge=event_incharge
	registration_deadline = forms.DateField(help_text="Last Date Of Registration (eg: 03/12/2019)",widget=SelectDateWidget())
	allowed_grades = forms.CharField(help_text='Grades Allowed. (Eg: 9th,10th)',widget=forms.TextInput(attrs={'placeholder': '9th,10th,11th'}))
	
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
	category = forms.CharField(help_text='Event Category',widget=forms.Select(choices=cat_options))

	class Meta:
		model = SubEvents
		fields = ['event_type','group_size','maximum_applicants','maximum_participants','requirements','registration_deadline','allowed_grades']

class SubEventCreationForm(forms.ModelForm):
	event_name = forms.CharField(help_text='Name Of The Event',widget=forms.TextInput(attrs={'placeholder': 'Debate'}))
	options = (
		("Individual",'Individual'),
		("Group",'Group')
	)
	event_type = forms.CharField(help_text='Individual Event or Group Event',widget=forms.Select(choices=options))
	group_size = forms.IntegerField(required=False,help_text="Number Of Students Per Group (If Individual Participation: Leave Blank)",widget=forms.NumberInput(attrs={'size': '20'}))
	start_date = forms.CharField(help_text="Start Date Of The Event (eg: 01/01/2020)",widget=SelectDateWidget())
	last_date = forms.CharField(help_text="Last Date Of The Event (eg: 03/01/2020)",widget=SelectDateWidget())
	maximum_applicants = forms.CharField(help_text='Maximum Number Of Applications',widget=forms.TextInput(attrs={'placeholder': '50'}))
	maximum_participants = forms.CharField(help_text='Maximum Number Of Students Who Can Participate In An Event',widget=forms.TextInput(attrs={'placeholder': '5'}))
	event_description = forms.CharField(help_text="Information About the Event (eg: Website Links)",widget=forms.Textarea(attrs={'rows':5, 'cols':50, 'placeholder':'Enter The Information Here...'}))
	requirements = forms.CharField(help_text='Requirements or Selection Criteria.',widget=forms.Textarea(attrs={'rows':5, 'cols':50,'placeholder': '''Must Be From Class 10\nMust have attended atleast 2 debate competetions... '''}))
	
	teacher_options = []
	users = User.objects.all()
	c=0
	for user in users:
		try:
			if Status.objects.get(user=user).status=="T" or Status.objects.get(user=user).status=="M":
				teacher_options.append((c,user.first_name + " " +user.last_name))
				c+=1
		except:
			pass

	teacher_options = name_sort(teacher_options)

	teacher_incharge = forms.CharField(widget=forms.Select(choices=teacher_options,attrs={'class':'form-control'}))	
	registration_deadline = forms.DateField(help_text="Last Date Of Registration (eg: 03/12/2019)",widget=SelectDateWidget())
	allowed_grades = forms.CharField(help_text='Grades Allowed. (Eg: 9th,10th)',widget=forms.TextInput(attrs={'placeholder': '9th,10th,11th'}))
	
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
	category = forms.CharField(help_text='Event Category',widget=forms.Select(choices=cat_options))
	add_attachment = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'btn btn-success green'}))

	class Meta:
		model = SubEvents
		fields = ['event_name','event_type','group_size','start_date','last_date','maximum_applicants','maximum_participants','requirements','teacher_incharge','registration_deadline','allowed_grades']
