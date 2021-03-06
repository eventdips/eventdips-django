from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name='teacher-homepage'),
	path('myevents',views.myevents,name='teacher-myevents'),
	path('allevents',views.allevents,name='teacher-allevents'),
	path('profile',views.profile,name='teacher-profile'),
	path('notifications',views.show_all_notifications,name="teacher-notifications"),
	path('<int:pk>',views.subevents,name='teacher-subevents'),
	path('<int:pk>/<int:sub_pk>',views.subevent,name='teacher-subevent'),
	path('<int:pk>/<int:sub_pk>/rview',views.view_registrations,name='teacher-registers'),
	path('<int:pk>/<int:sub_pk>/rview/confirmation',views.confirmation,name='teacher-confirmation'),
	path('<int:pk>/<int:sub_pk>/reason-for-rejections',views.reason_for_rejection,name='teacher-reason'),
	path('<int:pk>/<int:sub_pk>/rview/<int:r_pk>',views.view_registration,name='teacher-register'),
	path('<int:pk>/<int:sub_pk>/rview/<int:r_pk>/view-achievement',views.view_achievement,name='teacher-achievement'),
	path('<int:pk>/<int:sub_pk>/rview/<int:r_pk>/view-previous',views.view_previous_events,name='teacher-previous'),
	path('<int:pk>/<int:sub_pk>/rview/view-selected',views.view_selected_students,name='selected-students'),
	path('<int:pk>/<int:sub_pk>/rview/view-registered',views.view_registered_students,name='registered-students'),
	path('<int:pk>/<int:sub_pk>/rview/<int:r_pk>/accept',views.accept,name='teacher-accept'),
	path('<int:pk>/<int:sub_pk>/rview/<int:r_pk>/reject',views.reject,name='teacher-reject'),
	path('add-event',views.add_event,name="add-event"),
	path('add-event/<int:event_id>/sub',views.subevent_addition_page,name='subevent-addition-page'),
	path('add-event/<int:event_id>/sub/add',views.add_subevent,name='add-subevent'),
	path('add-event/<int:event_id>',views.single_event_information,name="single-event-information"),
	path('edit-event/<int:event_id>/<int:subevent_id>',views.edit_event,name="edit-event"),
	path('delete-event/<int:event_id>/<int:subevent_id>',views.delete_event,name="delete-event"),
	path('search/', views.searchpage, name='teacher-search')
]

'''
teachers-ff1b4751894e267c4fe3e1c7025670929c15c05b033800e088f9ce931a377912
student-b90fa6a75b91609042515f892f39f7f3e584df5dbef91f6ea67dfaed32a0bab0
'''

'''
MAKE SINGLE EVENT FORM CHANGING THING
'''