from django import forms
from .models import Events,SubEvents
from studentview.models import Registrations
from django.forms.widgets import SelectDateWidget

class EventCreationForm(forms.ModelForm):
	event_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Invictus'}))
	teacher_incharge = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Vikranti Ashtikar'}))
	event_information = forms.CharField(help_text="Information About the Event (eg: Website Links)",widget=forms.Textarea(attrs={'rows':5, 'cols':50, 'placeholder':'Enter The Information Here...'}))
	start_date = forms.CharField(help_text="Start Date Of The Event (eg: 01/01/2020)",widget=SelectDateWidget())
	last_date = forms.CharField(help_text="Last Date Of The Event (eg: 03/01/2020)",widget=SelectDateWidget())
	options = (
		("True",'True'),
		("False",'False')
	)
	single_event = forms.CharField(help_text='''Enter True If The Event Does Not Have Any Events Under It.
												Example: Invictus- False, Debate Competition-True''',widget=forms.Select(choices=options)) 

	add_attachment = forms.FileField(widget=forms.ClearableFileInput())

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
	maximum_applicants = forms.CharField(help_text='Maximum Number Of Applications',widget=forms.TextInput(attrs={'placeholder': '50'}))
	maximum_participants = forms.CharField(help_text='Maximum Number Of Students Who Can Participate In An Event',widget=forms.TextInput(attrs={'placeholder': '5'}))
	#subevent_information = event_information
	requirements = forms.CharField(help_text='Requirements or Selection Criteria.',widget=forms.Textarea(attrs={'rows':5, 'cols':50,'placeholder': '''Must Be From Class 10 \n Must have attended atleast 2 debate competetions... '''}))
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
	add_attachment = forms.FileField(widget=forms.ClearableFileInput())


	class Meta:
		model = SubEvents
		fields = ['event_type','maximum_applicants','maximum_participants','requirements','registration_deadline','allowed_grades']

class SubEventCreationForm(forms.ModelForm):
	event_name = forms.CharField(help_text='Name Of The Event',widget=forms.TextInput(attrs={'placeholder': 'Debate'}))
	options = (
		("Individual",'Individual'),
		("Group",'Group')
	)
	event_type = forms.CharField(help_text='Individual Event or Group Event',widget=forms.Select(choices=options))
	start_date = forms.CharField(help_text="Start Date Of The Event (eg: 01/01/2020)",widget=SelectDateWidget())
	last_date = forms.CharField(help_text="Last Date Of The Event (eg: 03/01/2020)",widget=SelectDateWidget())
	maximum_applicants = forms.CharField(help_text='Maximum Number Of Applications',widget=forms.TextInput(attrs={'placeholder': '50'}))
	maximum_participants = forms.CharField(help_text='Maximum Number Of Students Who Can Participate In An Event',widget=forms.TextInput(attrs={'placeholder': '5'}))
	event_description = forms.CharField(help_text="Information About the Event (eg: Website Links)",widget=forms.Textarea(attrs={'rows':5, 'cols':50, 'placeholder':'Enter The Information Here...'}))
	requirements = forms.CharField(help_text='Requirements or Selection Criteria.',widget=forms.Textarea(attrs={'rows':5, 'cols':50,'placeholder': '''Must Be From Class 10\nMust have attended atleast 2 debate competetions... '''}))
	teacher_incharge= forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Vikranti Ashtikar'}))
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
	add_attachment = forms.FileField(widget=forms.ClearableFileInput())

	class Meta:
		model = SubEvents
		fields = ['event_name','event_type','start_date','last_date','maximum_applicants','maximum_participants','requirements','teacher_incharge','registration_deadline','allowed_grades']
