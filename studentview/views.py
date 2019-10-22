from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Registrations
from teacherview.models import Events,SubEvents,Status
from teacherview.views import login_check, student_check, student_hash, date_conversion

def home(request):
    login_check(request)

    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    subevents = list(SubEvents.objects.all())
    final=[]
    for s_event in subevents:
        r = list(Registrations.objects.get(subevent_id=s_event.subevent_id))
        for i in r:
            if r.user==user:
                if s_event.selected_students<s_event.maximum_students and s_event.total_slots>s_event.total_registrations:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(student_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                    sub["event_information"]= s_event.subevent_information
                    sub["event_dates"] = date_conversion(s_event.subevent_dates)
                    sub["category"] = s_event.category
                    sub["completed_check"] = False
                    final.append(sub)
                else:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(student_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                    sub["event_information"]= s_event.subevent_information
                    sub["event_dates"] = date_conversion(s_event.subevent_dates)
                    sub["event_edit_redirect"] = "/{}edit-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["event_delete_redirect"] = "/{}delete-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["category"] = s_event.category
                    sub["completed_check"] = True
                    final.append(sub)
                    
    return render(request,'studentview/home.html')

def profile(request):
	return render(request,'studentview/myProfile.html')

def my_acheivements(request):
	id_ = int(request.COOKIES.get('id')) 
	user = User.objects.get(pk=id_)
	status = Status.objects.get(user=user)
	#status.status == "S", status.acheivements = "(acheivement_name,acheivement_category,acheivement_description,acheivement_date);(achei....)"

	context ={

	}
	return render(request,'studentview/my_acheivements.html',context)