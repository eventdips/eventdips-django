from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name="student-homepage"),
	path('profile',views.profile,name="student-profile"),
	path('acheivements',views.my_acheivements,name="student-acheivements"),
	path('<int:event_id>',views.subevents,name="student-subevents"),
	path('<int:event_id>/<int:subevent_id>',views.subevent,name="student-subevent"),
	path('<int:event_id>/<int:subevent_id>/registration',views.registration,name="student-registration")
]