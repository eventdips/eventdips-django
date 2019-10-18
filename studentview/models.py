from django.db import models
from django.contrib.auth.models import User

class Registrations(models.Model):
	registration_id = models.AutoField(primary_key=True)
	student_name = models.CharField(max_length=64)
	student_class = models.IntegerField()
	student_section = models.CharField(max_length=1)
	event_id = models.IntegerField(null=False)
	subevent_id = models.IntegerField()
	reg_info = models.TextField()
	acheivements = models.TextField()
	reg_status = models.CharField(max_length=1) #R- Rejected, A- Accepted
	group_ids = models.CharField(max_length=256)
	#acheivements will be pulled from the users db
	
	def __str__(self):
		return self.student_name + " " + str(self.event_id) + " " + str(self.registration_id)

		 