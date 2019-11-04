from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name="student-homepage"),
	path('profile',views.profile,name="student-profile"),
	path('/achievements',views.my_achievements,name="student-achievements"),
	path('/achievements/add',views.add_achievement,name="student-achievement-add"),
	path('/achievements/edit/<int:achievement_id>',views.achievements_edit,name="student-achievements-edit"),
	path('/achievements/delete/<int:achievement_id>',views.achievements_delete,name="student-achievements-delete"),
	path('//<str:category>',views.event_by_category,name="event-category"),
	path('/applications',views.my_applications,name="my-applications"),
	path('<int:event_id>',views.subevents,name="student-subevents"),
	path('<int:event_id>/<int:subevent_id>',views.subevent,name="student-subevent"),
	path('<int:event_id>/<int:subevent_id>/registration',views.registration,name="student-registration")
]

'''
ADD REMOVING OF EVENTS IF LAST_DATE OF EVENT PASSES 
MAKE TEACHER EVENT INCHARGE AS A DROPDOWN
USE MAIL SERVICE AND NOTIFICATIONS TO INFORM TEACHERS ABOUT NEW APPLICATIONS
USE MAIL SERVICE AND NOTIFICATIONS TO INFORM STUDENTS ABOUT NEW EVENTS
'''