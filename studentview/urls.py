from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name="student-homepage"),
	path('profile',views.profile,name="student-profile")
]