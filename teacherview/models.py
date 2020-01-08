from django.db import models
from django.contrib.auth.models import User

class Events(models.Model):
	event_id = models.AutoField(primary_key=True)
	event_name = models.CharField(max_length=64)
	teacher_incharge = models.CharField(max_length=64)
	teacher_incharge_id = models.IntegerField()
	date_published = models.DateField(auto_now_add=True)
	event_information = models.TextField(blank=True)
	event_dates = models.TextField()
	single_check = models.CharField(max_length=5)
	event_attachment = models.FileField(blank=True,upload_to='Attachments')

	def __str__(self):
		return self.event_name + " " + str(self.event_id) + " " + self.teacher_incharge
 
class SubEvents(models.Model):
	subevent_id = models.AutoField(primary_key=True)
	subevent_name = models.CharField(max_length=64)
	subevent_dates = models.CharField(max_length=64)
	subevent_type = models.CharField(max_length=1, default='I')
	group_size = models.IntegerField(null=True)
	event_id = models.IntegerField(null=False)
	total_slots = models.IntegerField(default=0) #MAX ALLOWED SLOTS
	total_registrations = models.IntegerField(default=0)
	maximum_students = models.IntegerField(default=0) 
	selected_students = models.IntegerField(default=0) 
	subevent_information = models.TextField(blank=True)
	subevent_requirements = models.TextField(blank=True)
	subevent_teacher_incharge = models.CharField(max_length=64)
	subevent_teacher_incharge_id = models.IntegerField()
	published_date = models.DateField(auto_now_add=True)
	last_date = models.DateField()
	allowed_grades = models.CharField(default="ALL", max_length=32)
	subevent_attachment = models.FileField(blank=True,upload_to='Attachments')
	category = models.CharField(max_length=32)
	confirmation_status = models.CharField(default="N",max_length=1) #"Y"-Yes

	def __str__(self):
		return self.subevent_name + " " + str("Event Id: {}".format(str(self.event_id))) + " " + self.subevent_teacher_incharge

class Status(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	status = models.CharField(default="",max_length=1)
	achievements = models.TextField(default="") #stores STUDENT ACHEIVEMENTS- Teacher=="None"
	department = models.CharField(max_length=64) #stored TEACHER DEPT- Student=="None"
	#notifications - notification and read/unread

	def __str__(self):
		return self.user.first_name + " " + self.user.last_name + ": " + self.status

#TEACHERS TABLE- TEACHER ID, TEACHER NAME, TEACHER EVENTS(SUBEVENT_IDS SEPERATED BY A COLON)