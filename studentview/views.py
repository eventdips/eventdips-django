from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Registrations
from teacherview.models import Events,SubEvents,Status
from teacherview.views import login_check, student_check, student_hash, date_conversion
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import *

def home(request):
    login_check(request)

    try:
        if not student_check(request):
            return redirect('teacher-homepage')
    except:
        pass

    events = list(Events.objects.all())
    final2 = []
    for i in events:
        sub = {}
        if i.single_check=="True":
            sub_event = SubEvents.objects.filter(event_id=i.event_id)
            subevent_id = sub_event.first().subevent_id
            sub["url_redirect"] = "/{}{}/{}".format(student_hash,str(i.event_id),str(subevent_id))
            sub["registration_deadline"] = date_conversion(sub_event.first().last_date)
            if sub_event.first().total_slots==sub_event.first().total_registrations:
                sub["completed_check"] = True
            else:
                sub["completed_check"] = False
        else:
            sub["url_redirect"] = "/{}{}".format(student_hash,str(i.event_id))
        sub["name"] = i.event_name
        sub["teacher_incharge"] = i.teacher_incharge
        sub["event_information"]= i.event_information
        sub["event_dates"] = date_conversion(i.event_dates)

        final2.append(sub)

    subevents = list(SubEvents.objects.all())
    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    final=[]
    for s_event in subevents:
        r = list(Registrations.objects.filter(subevent_id=s_event.subevent_id))
        for i in r:
            if i.user==user:
                if s_event.total_slots>s_event.total_registrations:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(student_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                    sub["registration_deadline"]= date_conversion(s_event.last_date)
                    sub["event_dates"] = date_conversion(s_event.subevent_dates)
                    sub["category"] = s_event.category
                    sub["completed_check"] = False
                    final.append(sub)
                else:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(student_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                    sub["registration_deadline"]= date_conversion(s_event.last_date)
                    sub["event_dates"] = date_conversion(s_event.subevent_dates)
                    sub["category"] = s_event.category
                    sub["completed_check"] = True
                    final.append(sub)
            
    context = {
        "MyEvents": final,
        "OngoingEvents": final2,
        "Title": "Home"
    }
                    
    return render(request,'studentview/home.html',context)

def profile(request):
    login_check(request)

    try:
        if not student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        pass

    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    final = []
    for s_event in list(SubEvents.objects.all()):
        registrations = list(Registrations.objects.filter(subevent_id=s_event.subevent_id))
        if user in [reg.user for reg in registrations]:
            sub = {}
            if s_event.total_slots>s_event.total_registrations:
                sub = {}
                sub["url_redirect"] = "/{}{}/{}".format(student_hash,str(s_event.event_id),str(s_event.subevent_id))
                sub["name"] = s_event.subevent_name
                sub["event_dates"] = date_conversion(s_event.subevent_dates)
                sub["registration_deadline"] = date_conversion(s_event.last_date)
                sub["category"] = s_event.category
                sub["event_information"] = s_event.subevent_information
                sub["completed_check"] = False
                final.append(sub)
            else:
                sub = {}
                sub["url_redirect"] = "/{}{}/{}".format(student_hash,str(s_event.event_id),str(s_event.subevent_id))
                sub["name"] = s_event.subevent_name
                sub["event_dates"] = date_conversion(s_event.subevent_dates)
                sub["registration_deadline"] = date_conversion(s_event.last_date)
                sub["category"] = s_event.category
                sub["completed_check"] = True
                sub["event_information"] = s_event.subevent_information
                final.append(sub)

    context = {
        "username": user.username,
        "name": user.first_name + " " + user.last_name,
        "email": user.email,
        "MyEvents": final
    }
    
    return render(request,'studentview/myProfile.html',context)

def my_acheivements(request):
    login_check()

    try:
        if not student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        pass
    
    id_ = int(request.COOKIES.get('id')) 
    user = User.objects.get(pk=id_)
    status = Status.objects.get(user=user)
    #status.status == "S", status.acheivements = "(acheivement_name,acheivement_category,acheivement_description,acheivement_date);(achei....)"
    
    context ={

    }
    return render(request,'studentview/my_acheivements.html',context)

def subevents(request,event_id):
    login_check(request)

    try:
        if not student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')

    event = Events.objects.filter(pk=event_id).first()
    subevents = list(SubEvents.objects.filter(event_id=event_id))

    final = []
    for i in subevents:
        sub = {}
        if i.total_slots>i.total_registrations:
            sub["completed_check"] = False
        else:
            sub["completed_check"] = True
        sub["name"] = i.subevent_name
        sub["dates"] = date_conversion(i.subevent_dates)
        sub["available_slots"] = str(i.total_slots-i.total_registrations)
        sub["registration_deadline"] = date_conversion(i.last_date)
        sub["total_registrations"] = str(i.total_registrations)
        sub["teacher_incharge"] = i.subevent_teacher_incharge   
        sub["url_redirect"] = "/{}{}/{}".format(student_hash,str(event_id),str(i.subevent_id))
        sub["event_attachment"] = i.subevent_attachment
        final.append(sub)

    context = {"title":event.event_name,
                "event_name": event.event_name,
                "subevents":final}

    return render(request, "studentview/subevents.html", context)

def subevent(request,event_id,subevent_id):
	login_check(request)

	try:
		if not student_check(request):
			messages.warning(request,'Illegal Action Attempted!')
			return redirect('teacher-homepage')
	except:
		return redirect('login')

	final = []
	event = Events.objects.get(event_id=event_id)
	subevent = SubEvents.objects.get(subevent_id=subevent_id)

	if subevent.total_slots>subevent.total_registrations:
		sub = {}
		sub["url_redirect"] = "/{}{}/{}/registration".format(student_hash,str(event_id),str(subevent_id))
		sub["name"] = subevent.subevent_name
		sub["dates"] = date_conversion(subevent.subevent_dates)
		sub["type"] = "Group" if subevent.subevent_type != "I" else "Individual"
		sub["available_slots"] = str(subevent.total_slots-subevent.total_registrations)
		sub["event_information"] = subevent.subevent_information
		sub["event_requirements"] = subevent.subevent_requirements
		sub["teacher_incharge"] = subevent.subevent_teacher_incharge
		sub["last_date"] = date_conversion(subevent.last_date)
		sub["allowed_grades"] = subevent.allowed_grades  
		sub["event_attachment"] = subevent.subevent_attachment
		sub["category"] = subevent.category
		sub["completed_check"] = False
		final.append(sub)
	else:
		sub = {}
		sub["url_redirect"] = "/{}{}/{}/registration".format(student_hash,str(event_id),str(subevent_id))
		sub["name"] = subevent.subevent_name
		sub["dates"] = date_conversion(subevent.subevent_dates)
		sub["type"] = "Group" if subevent.subevent_type != "I" else "Individual"
		sub["available_slots"] = str(subevent.total_slots-subevent.total_registrations)
		sub["event_information"] = subevent.subevent_information
		sub["event_requirements"] = subevent.subevent_requirements
		sub["teacher_incharge"] = subevent.subevent_teacher_incharge
		sub["last_date"] = date_conversion(subevent.last_date)
		sub["allowed_grades"] = subevent.allowed_grades  
		sub["event_attachment"] = subevent.subevent_attachment
		sub["category"] = subevent.category
		sub["completed_check"] = True
		final.append(sub)
		
	context = {"title":subevent.subevent_name,
                "event_name": event.event_name,
                "subevents":final,
                "header_redirect":"/{}{}".format(student_hash,str(event_id))}
				
	return render(request, "studentview/subevent.html", context)

def registration(request,event_id,subevent_id):
    login_check(request)
    
    try:
        if not student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')        
    except:
        return redirect('login')

    subevent = SubEvents.objects.get(pk=subevent_id)
    if subevent.total_registrations==subevent.total_slots:
        messages.warning("Registrations Are Complete For '{}'".format(subevent.subevent_name))
        return redirect('student-homepage')

    
