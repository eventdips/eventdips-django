from django.shortcuts import render, redirect
from .models import Events,SubEvents,Status
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from studentview.models import Registrations
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import EventCreationForm, SingleEventInformationForm, SubEventCreationForm, LoginForm
from django.contrib.auth.decorators import login_required

def date_conversion(date):
    date = str(date)
    if len(date.split())>1:
        l = date.split(" to ")
        month = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
        if l[0]==l[1]:
            date = l[0].split("-")
            mon=date[1]
            if int(date[2]) in [1,21,31]:
                date[2] = str(date[2]) + "st"
            elif int(date[2]) in [2,22]:
                date[2] = str(date[2]) + "nd"
            elif int(date[2]) in [3,23]:
                date[2] = str(date[2]) + "rd"
            elif int(date[2]) in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,29,30]:
                date[2] = str(date[2]) + "th"
            return "{} {}, {}".format(date[2],month[int(mon)],str(date[0]))
        else:
            date1 = l[0].split("-")
            mon=date1[1]
            date2 = l[1].split("-")
            mon2=date2[1]
            if int(date1[2]) in [1,21,31]:
                date1[2] = str(date1[2]) + "st"
            elif int(date1[2]) in [2,22]:
                date1[2] = str(date1[2]) + "nd"
            elif int(date1[2]) in [3,23]:
                date1[2] = str(date1[2]) + "rd"
            elif int(date1[2]) in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,29,30]:
                date1[2] = str(date1[2]) + "th"

            if int(date2[2]) in [1,21,31]:
                date2[2] = str(date2[2]) + "st"
            elif int(date2[2]) in [2,22]:
                date2[2] = str(date2[2]) + "nd"
            elif int(date2[2]) in [3,23]:
                date2[2] = str(date2[2]) + "rd"
            elif int(date2[2]) in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,29,30]:
                date2[2] = str(date2[2]) + "th"
            s1 = "{} {}, {}".format(str(date1[2]),month[int(mon)],str(date1[0]))
            s2 = "{} {}, {}".format(str(date2[2]),month[int(mon2)],str(date2[0]))
            return s1 + " to " + s2
    else:
        l = date.split()
        month = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
        date = l[0].split("-")
        mon = date[1]
        if int(date[2]) in [1,21,31]:
            date[2] = str(date[2]) + "st"
        elif int(date[2]) in [2,22]:
            date[2] = str(date[2]) + "nd"
        elif int(date[2]) in [3,23]:
            date[2] = str(date[2]) + "rd"
        elif int(date[2]) in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,24,25,26,27,28,29,30]:
            date[2] = str(date[2]) + "th"
        return "{} {}, {}".format(str(date[2]),month[int(mon)],str(date[0]))

def teacher_event_sort(events):
    #By Event Deadline- Teachers
    #By Registration Deadline- Students

    months = ["January","February","March","April","May","June","July","August","Septemeber","October","November","December"]
    j = 0
    while j<=(10000):
        for i in range(0,len(events)-1):
            base1 = events[i]['event_dates'].split(" to ")
            base2 = events[i+1]['event_dates'].split(" to ")
            if len(base1)>1:
                y1 = int(events[i]['event_dates'].split(" to ")[1].split(", ")[1])
                m1 = months.index(events[i]['event_dates'].split(" to ")[1].split()[1].split(",")[0])
                d1 = int(events[i]['event_dates'].split(" to ")[1].split()[0][:-2])
            else:
                y1 = int(events[i]['event_dates'].split(" to ")[0].split(", ")[1])
                m1 = months.index(events[i]['event_dates'].split(" to ")[0].split()[1].split(",")[0])
                d1 = int(events[i]['event_dates'].split(" to ")[0].split()[0][:-2])

            if len(base2)>1:
                y2 = int(events[i+1]['event_dates'].split(" to ")[1].split(", ")[1])
                m2 = months.index(events[i+1]['event_dates'].split(" to ")[1].split()[1].split(",")[0])
                d2 = int(events[i+1]['event_dates'].split(" to ")[1].split()[0][:-2])
            else:
                y2 = int(events[i+1]['event_dates'].split(" to ")[0].split(", ")[1])
                m2 = months.index(events[i+1]['event_dates'].split(" to ")[0].split()[1].split(",")[0])
                d2 = int(events[i+1]['event_dates'].split(" to ")[0].split()[0][:-2])

            if y1>y2:
                events[i],events[i+1]=events[i+1],events[i]
            else:
                if m1>m2:
                    events[i],events[i+1]=events[i+1],events[i]
                else:
                    if d1>d2:
                        events[i],events[i+1]=events[i+1],events[i]

        j+=1

    return events

def student_check(request):
    if not request.user.is_anonymous:
        ret = Status.objects.get(user=request.user)
        if ret.status=="S":
            return True 
        else:
            return False
    else:
        return False

'''
SORT EVENTS BY DEADLINES- TEACHERVIEW
SORT EVENTS BY REGISTRATION DEADLINES- STUDENTVIEW
CREATE CUSTOM 404-PAGE
'''

@login_required
def home(request):
    if student_check(request):
        return redirect('student-homepage')

    events = list(Events.objects.all())
    teacher_id = request.user.id 
    final = []

    #There is also data available regarding: Total Slots, Date Posted, Time Posted, Event Type, Event Information.
    for i in events:
        sub = {}
        if i.single_check=="True":
            sub_event = SubEvents.objects.filter(event_id=i.event_id)
            subevent_id = sub_event.first().subevent_id
            sub["url_redirect"] = "/teachers/{}/{}".format(str(i.event_id),str(subevent_id))
        else:
            sub["url_redirect"] = "/teachers/{}".format(str(i.event_id))
        sub["name"] = i.event_name
        sub["teacher_incharge"] = i.teacher_incharge
        sub["event_information"]= i.event_information
        sub["event_dates"] = date_conversion(i.event_dates)

        final.append(sub)

    subevents = list(SubEvents.objects.all())
    final2=[]
    for s_event in subevents:
        if s_event.subevent_teacher_incharge_id==teacher_id:
            if s_event.selected_students<s_event.maximum_students and s_event.total_slots>s_event.total_registrations:
                sub = {}
                sub["url_redirect"] = "/teachers/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["name"] = s_event.subevent_name
                sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                sub["event_information"]= s_event.subevent_information
                sub["event_dates"] = date_conversion(s_event.subevent_dates)
                sub["event_edit_redirect"] = "/teachers/edit-event/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["event_delete_redirect"] = "/teachers/delete-event/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["category"] = s_event.category
                sub["completed_check"] = False
                final2.append(sub)
            else:
                sub = {}
                sub["url_redirect"] = "/teachers/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["name"] = s_event.subevent_name
                sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                sub["event_information"]= s_event.subevent_information
                sub["event_dates"] = date_conversion(s_event.subevent_dates)
                sub["event_edit_redirect"] = "/teachers/edit-event/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["event_delete_redirect"] = "/teachers/delete-event/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["category"] = s_event.category
                sub["completed_check"] = True
                final2.append(sub)
   
    for i in events:
        c=0
        if i.teacher_incharge_id==teacher_id:
            for s in final2:
                if s["name"]==i.event_name:
                    c+=1
            if c==0:
                sub = {}
                if i.single_check=="True":
                    sub_event = SubEvents.objects.filter(event_id=i.event_id)
                    subevent_id = sub_event.first().subevent_id
                    sub["url_redirect"] = "/teachers/{}/{}".format(str(i.event_id),str(subevent_id))
                else:
                    sub["url_redirect"] = "/teachers/{}".format(str(i.event_id))
                sub["name"] = i.event_name
                sub["teacher_incharge"] = i.teacher_incharge
                sub["event_information"]= i.event_information
                sub["event_dates"] = date_conversion(i.event_dates)
                sub["event_check"] = True
                final2.append(sub)
    
    final = teacher_event_sort(final)
    final2 = teacher_event_sort(final2)

    context = {"title":"Home",
        "AllEvents": final,
        "MyEvents":final2
    }
    return render(request, "teacherview/home.html", context)
 
def myevents(request):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')

    teacher_id = request.user.id
    subevents = list(SubEvents.objects.all())
    final=[]
    for s_event in subevents:
        if s_event.subevent_teacher_incharge_id==teacher_id:
            if s_event.selected_students<s_event.maximum_students and s_event.total_slots>s_event.total_registrations:
                sub = {}
                sub["url_redirect"] = "/teachers/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["name"] = s_event.subevent_name
                sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                sub["event_information"]= s_event.subevent_information
                sub["event_dates"] = date_conversion(s_event.subevent_dates)
                sub["event_edit_redirect"] = "/teachers/edit-event/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["event_delete_redirect"] = "/teachers/delete-event/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["completed_check"] = False
                final.append(sub)
            else:
                sub = {}
                sub["url_redirect"] = "/teachers/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["name"] = s_event.subevent_name
                sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                sub["event_information"]= s_event.subevent_information
                sub["event_dates"] = date_conversion(s_event.subevent_dates)
                sub["event_edit_redirect"] = "/teachers/edit-event/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["event_delete_redirect"] = "/teachers/delete-event/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
                sub["completed_check"] = True
                final.append(sub)

    context = {"title":"MyEvents",
        "MyEvents":final
    }
    return render(request, "teacherview/myevents.html", context)
 
def allevents(request):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')

    subevents = list(SubEvents.objects.all())
    final=[]
    for s_event in subevents:        
        sub = {}
        sub["url_redirect"] = "/teachers/{}/{}".format(str(s_event.event_id),str(s_event.subevent_id))
        sub["name"] = s_event.subevent_name
        sub["teacher_incharge"] = s_event.subevent_teacher_incharge
        sub["event_information"]= s_event.subevent_information
        sub["event_dates"] = date_conversion(s_event.subevent_dates)
        final.append(sub)

    context = {"title":"AllEvents",
        "AllEvents":final
    }
    return render(request, "teacherview/allevents.html", context)
 
def subevents(request,pk):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')

    event = Events.objects.filter(pk=pk).first()
    e_id = event.event_id
    subevents = list(SubEvents.objects.filter(event_id=e_id))
    teacher_id = request.user.id

    final = []
    for i in subevents:
        sub = {}
        sub["name"] = i.subevent_name
        sub["dates"] = date_conversion(i.subevent_dates)
        sub["available_slots"] = str(i.total_slots-i.total_registrations)
        sub["total_registrations"] = str(i.total_registrations)
        sub["teacher_incharge"] = i.subevent_teacher_incharge   
        sub["url_redirect"] = "/teachers/{}/{}".format(str(e_id),str(i.subevent_id))
        sub["event_attachment"] = i.subevent_attachment
        final.append(sub)

    context = {"title":event.event_name,
                "event_name": event.event_name,
                "url_redirect2": "/teachers/add-event/{}/sub/add".format(e_id),
                "myevent":True if event.teacher_incharge_id==teacher_id else False,
                "subevents":final}

    return render(request, "teacherview/subevents.html", context)
 
def subevent(request,pk,sub_pk):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')
    
    event = Events.objects.filter(pk=pk).first()
    subevent = SubEvents.objects.filter(subevent_id=sub_pk).first()
    teacher_id = request.user.id

    if subevent.subevent_teacher_incharge_id==teacher_id:
        if subevent.selected_students<subevent.maximum_students and subevent.total_slots>subevent.total_registrations:
            final = []
            sub = {}
            sub["url_redirect"] = "/teachers/{}/{}/rview".format(str(pk),str(sub_pk))
            sub["name"] = subevent.subevent_name
            sub["dates"] = date_conversion(subevent.subevent_dates)
            sub["type"] = "Group" if subevent.subevent_type != "I" else "Individual"
            sub["available_slots"] = str(subevent.total_slots-subevent.total_registrations)
            sub["total_registrations"] = str(subevent.total_registrations)
            sub["event_information"] = subevent.subevent_information
            sub["event_requirements"] = subevent.subevent_requirements
            sub["teacher_incharge"] = subevent.subevent_teacher_incharge
            sub["last_date"] = date_conversion(subevent.last_date)
            sub["allowed_grades"] = subevent.allowed_grades  
            sub["event_attachment"] = subevent.subevent_attachment
            sub["event_edit_redirect"] = "/teachers/edit-event/{}/{}".format(str(subevent.event_id),str(subevent.subevent_id))
            sub["event_delete_redirect"] = "/teachers/delete-event/{}/{}".format(str(subevent.event_id),str(subevent.subevent_id))
            sub["my_event"] = True
            sub["maximum_participants"] = str(subevent.maximum_students)
            sub["selected_students"] = str(subevent.selected_students)
            sub["category"] = subevent.category
            sub["completed_check"] = False
            final.append(sub)
        else:
            final = []
            sub = {}
            sub["url_redirect"] = "/teachers/{}/{}/rview".format(str(pk),str(sub_pk))
            sub["name"] = subevent.subevent_name
            sub["dates"] = date_conversion(subevent.subevent_dates)
            sub["type"] = "Group" if subevent.subevent_type != "I" else "Individual"
            sub["available_slots"] = str(subevent.total_slots-subevent.total_registrations)
            sub["total_registrations"] = str(subevent.total_registrations)
            sub["event_information"] = subevent.subevent_information
            sub["event_requirements"] = subevent.subevent_requirements
            sub["teacher_incharge"] = subevent.subevent_teacher_incharge
            sub["last_date"] = date_conversion(subevent.last_date)
            sub["allowed_grades"] = subevent.allowed_grades  
            sub["event_attachment"] = subevent.subevent_attachment
            sub["event_edit_redirect"] = "/teachers/edit-event/{}/{}".format(str(subevent.event_id),str(subevent.subevent_id))
            sub["event_delete_redirect"] = "/teachers/delete-event/{}/{}".format(str(subevent.event_id),str(subevent.subevent_id))
            sub["my_event"] = True
            sub["maximum_participants"] = str(subevent.maximum_students)
            sub["selected_students"] = str(subevent.selected_students)
            sub["category"] = subevent.category
            sub["completed_check"] = True
            final.append(sub)
    else:
        final = []
        sub = {}
        sub["url_redirect"] = "/teachers/{}/{}/rview".format(str(pk),str(sub_pk))
        sub["name"] = subevent.subevent_name
        sub["dates"] = date_conversion(subevent.subevent_dates)
        sub["type"] = "Group" if subevent.subevent_type != "I" else "Individual"
        sub["available_slots"] = str(subevent.total_slots-subevent.total_registrations)
        sub["total_registrations"] = str(subevent.total_registrations)
        sub["event_information"] = subevent.subevent_information
        sub["event_requirements"] = subevent.subevent_requirements
        sub["teacher_incharge"] = subevent.subevent_teacher_incharge
        sub["last_date"] = date_conversion(subevent.last_date)
        sub["allowed_grades"] = subevent.allowed_grades   
        sub["event_attachment"] = subevent.subevent_attachment
        sub["category"] = subevent.category
        sub["my_event"] = False
        final.append(sub)

    context = {"title":subevent.subevent_name,
                "event_name": event.event_name,
                "subevents":final,
                "header_redirect":"/teachers/{}".format(str(pk))}

    return render(request, "teacherview/subevent.html", context)
 
def view_registrations(request,pk,sub_pk):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')
    
    if request.user.id!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')

    registrations = list(Registrations.objects.filter(subevent_id=sub_pk))
    final=[]

    for i in registrations:
        sub = {}
        sub["url_redirect"] = "/teachers/{}/{}/rview/{}".format(str(pk),str(sub_pk),str(i.registration_id))
        sub["name"]=i.student_name
        sub["class"]=str(i.student_class)
        sub["section"]=i.student_section
        if i.reg_status=="R":
            sub["status"]="Rejected" 
        elif i.reg_status == "A":
            sub["status"]="Accepted"
        else:
            sub["status"]="Pending"
        final.append(sub)

    context={
        "event_name":Events.objects.filter(event_id=pk).first().event_name,
        "subevent_name":SubEvents.objects.filter(subevent_id=int(sub_pk)).first().subevent_name,
        "Registrations":final,
        "header_redirect":"/teachers/{}/{}".format(str(pk),str(sub_pk)),
        "view_selected_students":"/teachers/{}/{}/rview/view-selected".format(str(pk),str(sub_pk)),
        "view_registered_students":"/teachers/{}/{}/rview/view-registered".format(str(pk),str(sub_pk))
    }

    return render(request,'teacherview/view_registrations.html',context)

def view_registration(request,pk,sub_pk,r_pk):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')
    
    if request.user.id!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')

    registration = Registrations.objects.filter(registration_id=r_pk).first()
    sub = {}
    sub["name"]=registration.student_name
    sub["class"]=str(registration.student_class)
    sub["section"]=registration.student_section
    sub["info"]=registration.reg_info
    sub["ego_flex"]=registration.acheivements
    if registration.reg_status=="R":
        sub["status"]="Rejected" 
    elif registration.reg_status=="A":
        sub["status"]="Accepted"
    else:
        sub["status"]="Pending"
    final = [sub]

    context={
        "event_name":Events.objects.filter(event_id=pk).first().event_name,
        "subevent_name":SubEvents.objects.filter(subevent_id=int(sub_pk)).first().subevent_name,
        "Registration":final,
        "header_redirect":"/teachers/{}/{}/rview".format(str(pk),str(sub_pk)),
        "url_redirect_1":"/teachers/{}/{}/rview/{}/accept".format(str(pk),str(sub_pk),str(r_pk)),
        "url_redirect_2":"/teachers/{}/{}/rview/{}/reject".format(str(pk),str(sub_pk),str(r_pk))
    }

    return render(request,'teacherview/view_registration.html',context)
 
def accept(request,pk,sub_pk,r_pk):  
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')
    
    if request.user.id!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')

    registration = Registrations.objects.get(registration_id=r_pk)
    partcipated_in = SubEvents.objects.get(subevent_id=sub_pk)
    
    if registration.reg_status=="A":
        messages.warning(request,"{} has already been selected for '{}'!".format(str(registration.student_name),partcipated_in.subevent_name))
        return HttpResponseRedirect('/teachers/{}/{}/rview'.format(str(pk),str(sub_pk)))
    elif partcipated_in.maximum_students == partcipated_in.selected_students:
        messages.warning(request,"Maximum Number of Participants have been selected!")
        return HttpResponseRedirect('/teachers/{}/{}/rview'.format(str(pk),str(sub_pk)))
    else:
        if registration.reg_status=="R":
            registration.reg_status = "A"
            registration.save()        
            partcipated_in.selected_students+=1
            partcipated_in.save()
        elif len(registration.reg_status)==0:
            partcipated_in.total_registrations+=1 #CHANGE WHEN APPLICATION SUBMITTED, WHEN REGISTRATION FORM IS MADE
            registration.reg_status = "A"
            registration.save()
            partcipated_in.selected_students+=1  
            partcipated_in.save()
        
        messages.success(request,"{} will participate in '{}'!".format(registration.student_name,partcipated_in.subevent_name))
        return HttpResponseRedirect('/teachers/{}/{}/rview'.format(str(pk),str(sub_pk)))
 
def reject(request,pk,sub_pk,r_pk):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')
    
    if request.user.id!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')

    registration = Registrations.objects.get(registration_id=r_pk)
    partcipated_in = SubEvents.objects.get(subevent_id=sub_pk)
    
    if registration.reg_status=="R":
        messages.warning(request,"{} has already been rejected for '{}'.".format(str(registration.student_name),partcipated_in.subevent_name))
        return HttpResponseRedirect('/teachers/{}/{}/rview'.format(str(pk),str(sub_pk)))
    elif registration.reg_status=="A":
        registration.reg_status = "R"
        registration.save()
        partcipated_in.selected_students-=1
        partcipated_in.save()
    elif len(registration.reg_status)==0:
        partcipated_in.total_registrations+=1 #CHANGE WHEN APPLICATION SUBMITTED, WHEN REGISTRATION FORM IS MADE
        registration.reg_status = "R"
        registration.save()
        partcipated_in.save()
    

    messages.warning(request,"{} will not participate in '{}'.".format(registration.student_name,partcipated_in.subevent_name))
    return HttpResponseRedirect('/teachers/{}/{}/rview'.format(str(pk),str(sub_pk)))
 
def view_selected_students(request,pk,sub_pk):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')
    
    if request.user.id!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')

    registrations = list(Registrations.objects.filter(subevent_id=sub_pk))
    final=[]

    for i in registrations:
        if i.reg_status=="A":
            sub = {}
            sub["url_redirect"] = "/teachers/{}/{}/rview/{}".format(str(pk),str(sub_pk),str(i.registration_id))
            sub["name"]=i.student_name
            sub["class"]=str(i.student_class)
            sub["section"]=i.student_section
            if i.reg_status=="R":
                sub["status"]="Rejected" 
            elif i.reg_status == "A":
                sub["status"]="Accepted"
            else:
                sub["status"]="Pending"
            final.append(sub)

    context={
        "event_name":Events.objects.filter(event_id=pk).first().event_name,
        "subevent_name":SubEvents.objects.filter(subevent_id=int(sub_pk)).first().subevent_name,
        "Registrations":final,
        "header_redirect":"/teachers/{}/{}/rview".format(str(pk),str(sub_pk))
    }

    return render(request,'teacherview/view_selected_students.html',context)
 
def view_registered_students(request,pk,sub_pk):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')
    
    if request.user.id!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')

    registrations = list(Registrations.objects.filter(subevent_id=sub_pk))
    final=[]

    for i in registrations:
        sub = {}
        sub["url_redirect"] = "/teachers/{}/{}/rview/{}".format(str(pk),str(sub_pk),str(i.registration_id))
        sub["name"]=i.student_name
        sub["class"]=str(i.student_class)
        sub["section"]=i.student_section
        if i.reg_status=="R":
            sub["status"]="Rejected" 
        elif i.reg_status == "A":
            sub["status"]="Accepted"
        else:
            sub["status"]="Pending"
        final.append(sub)

    context={
        "event_name":Events.objects.filter(event_id=pk).first().event_name,
        "subevent_name":SubEvents.objects.filter(subevent_id=int(sub_pk)).first().subevent_name,
        "Registrations":final,
        "header_redirect":"/teachers/{}/{}/rview".format(str(pk),str(sub_pk))
    }

    return render(request,'teacherview/view_registered_students.html',context)
 
def add_event(request):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')

    if request.method == "POST":
        form = EventCreationForm(request.POST, request.FILES)
        if form.is_valid():
            new_event = form.save(commit=False)
            start_date = form.cleaned_data.get('start_date')
            last_date = form.cleaned_data.get('last_date')
            if last_date<start_date:
                messages.warning(request,"The Entered Event Dates Are Invalid!")
                return redirect('add-event')
            else:
                single_check = form.cleaned_data.get('single_event')
                if single_check=="True":
                    new_event.event_dates = "{} to {}".format(start_date,last_date)
                    new_event.single_check = single_check
                    new_event.event_attachment = request.FILES['add_attachment']
                    new_event.teacher_incharge_id = User.objects.get(user=form.cleaned_data.get("teacher_incharge")).id
                    new_event.save()
                    return HttpResponseRedirect('/teachers/add-event/{}'.format(new_event.event_id))
                else:
                    new_event.event_dates = "{} to {}".format(start_date,last_date)
                    new_event.single_check = single_check
                    new_event.event_attachment = request.FILES['add_attachment']
                    new_event.teacher_incharge_id = User.objects.get(user=form.cleaned_data.get("teacher_incharge")).id
                    new_event.save()
                    messages.success(request,"Event {} has been successfully created!".format(new_event.event_name)) 
                    return HttpResponseRedirect('/teachers/add-event/{}/sub'.format(new_event.event_id))
    else:
        form = EventCreationForm()

    context = {
        "form":form,
        "title":"New Event"
    }
    return render(request,'teacherview/add_event.html',context)
 
def single_event_information(request,event_id):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')

    if Events.objects.get(event_id=event_id).single_check=="False":
        messages.warning(request,"Invalid Request.")
        return redirect('teacher-homepage')
    else:
        if request.method=="POST":
            form = SingleEventInformationForm(request.POST, request.FILES)
            if form.is_valid():
                new_subevent = form.save(commit=False)
                total_slots = form.cleaned_data.get('maximum_applicants')
                maximum_students = form.cleaned_data.get('maximum_participants')
                event = Events.objects.get(event_id=event_id)
                new_subevent.subevent_teacher_incharge = event.teacher_incharge
                new_subevent.subevent_teacher_incharge_id = event.teacher_incharge_id
                new_subevent.subevent_attachment = event.event_attachment
                new_subevent.subevent_name = event.event_name
                new_subevent.subevent_dates = event.event_dates
                new_subevent.event_id = event.event_id
                new_subevent.subevent_information = event.event_information
                new_subevent.subevent_type = "I" if form.cleaned_data.get('event_type')=="Individual" else "G"
                new_subevent.total_slots = int(total_slots)
                new_subevent.maximum_students = int(maximum_students)
                new_subevent.subevent_requirements = form.cleaned_data.get('requirements')
                new_subevent.last_date = form.cleaned_data.get('registration_deadline')
                new_subevent.allowed_grades = form.cleaned_data.get('allowed_grades')
                new_subevent.category = form.cleaned_data.get('category')
                new_subevent.save()

                messages.success(request,"Event '{}' has been successfully created!".format(event.event_name))
                return redirect('teacher-homepage')
        else:
            form = SingleEventInformationForm()

        context = {
            "form":form,
            "title":Events.objects.get(pk=event_id).event_name
        }
        return render(request,'teacherview/single_event_information.html',context)
 
def subevent_addition_page(request,event_id):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')

    if Events.objects.get(event_id=event_id).single_check=="True":
        messages.warning(request,"Invalid Request.")
        return redirect('teacher-homepage')
    else:
        event = Events.objects.filter(event_id=event_id).first()

        final = []
        sub = {}
        sub["name"] = event.event_name
        sub["dates"] = date_conversion(event.event_dates)
        sub["event_information"] = event.event_information
        sub["teacher_incharge"] = event.teacher_incharge
        final.append(sub)

        context = {"title":event.event_name,
                    "event":final,
                    "url_redirect":"/teachers/add-event/{}/sub/add".format(event_id),
                    "event_redirect": "/teachers/{}".format(event_id)}

        return render(request, "teacherview/subevent_addition_page.html", context)
 
def add_subevent(request,event_id):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')

    if Events.objects.get(event_id=event_id).single_check=="True":
        messages.warning(request,"Invalid Request.")
        return redirect('teacher-homepage')
    else:
        if request.method=="POST":
            form = SubEventCreationForm(request.POST,request.FILES)
            if form.is_valid():
                new_subevent = form.save(commit=False)
                total_slots = form.cleaned_data.get('maximum_applicants')
                maximum_students = form.cleaned_data.get('maximum_participants')
                start_date = form.cleaned_data.get('start_date')
                last_date = form.cleaned_data.get('last_date')
                if int(total_slots)<int(maximum_students) or start_date>last_date:
                    messages.warning(request,"Error: Invalid Entry.")
                    return HttpResponseRedirect('/teachers/add-event/{}/sub/add'.format(event_id))
                else:
                    event = Events.objects.get(event_id=event_id)
                    new_subevent.subevent_teacher_incharge = form.cleaned_data.get('teacher_incharge')
                    new_subevent.subevent_teacher_incharge_id = User.objects.get(first_name=form.cleaned_data.get('teacher_incharge').split()[0],last_name=form.cleaned_data.get('teacher_incharge').split()[1]).id
                    new_subevent.subevent_name = form.cleaned_data.get('event_name')
                    new_subevent.subevent_dates = form.cleaned_data.get('start_date') +" to " + form.cleaned_data.get("last_date")
                    new_subevent.event_id = event.event_id
                    new_subevent.subevent_information = form.cleaned_data.get('event_description')
                    new_subevent.subevent_type = "I" if form.cleaned_data.get('event_type')=="Individual" else "G"
                    new_subevent.total_slots = int(total_slots)
                    new_subevent.maximum_students = int(maximum_students)
                    new_subevent.subevent_requirements = form.cleaned_data.get('requirements')
                    new_subevent.last_date = form.cleaned_data.get('registration_deadline')
                    new_subevent.allowed_grades = form.cleaned_data.get('allowed_grades')
                    new_subevent.subevent_attachment = request.FILES['add_attachment']
                    new_subevent.category = form.cleaned_data.get('category')
                    new_subevent.save()

                    messages.success(request,"Event '{}' has been successfully added to '{}'!".format(form.cleaned_data.get('event_name'),event.event_name))
                    return HttpResponseRedirect('/teachers/add-event/{}/sub'.format(event_id))
        else:
            form = SubEventCreationForm()

        context = {
            "form":form,
            "title":Events.objects.get(pk=event_id).event_name
        }
        return render(request,'teacherview/add_subevent.html',context)
 
def edit_event(request,event_id,subevent_id):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')
    
    if request.user.id!=SubEvents.objects.get(subevent_id=subevent_id).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')

    sub = SubEvents.objects.get(subevent_id=subevent_id)
    if request.method=="POST":
        form = SubEventCreationForm(request.POST,request.FILES,initial={'event_name': sub.subevent_name,'event_type': sub.subevent_type,'start_date':sub.subevent_dates.split(" to ")[0],'last_date':sub.subevent_dates.split(" to ")[1],'maximum_applicants':sub.total_slots,'maximum_participants':sub.maximum_students,'requirements':sub.subevent_requirements,'teacher_incharge':sub.subevent_teacher_incharge,'registration_deadline':sub.last_date,'allowed_grades':sub.allowed_grades,'event_description':sub.subevent_information,'category':sub.category,'add_attachment':sub.subevent_attachment})
        if form.is_valid():
            edit_subevent = form.save(commit=False)
            total_slots = form.cleaned_data.get('maximum_applicants')
            maximum_students = form.cleaned_data.get('maximum_participants')
            event = Events.objects.get(event_id=event_id)
            sub.subevent_teacher_incharge = form.cleaned_data.get('teacher_incharge')
            sub.subevent_name = form.cleaned_data.get('event_name')
            sub.subevent_dates = form.cleaned_data.get('start_date') +" to " + form.cleaned_data.get("last_date")
            sub.subevent_information = form.cleaned_data.get('event_description')
            sub.subevent_type = "I" if form.cleaned_data.get('event_type')=="Individual" else "G"
            sub.total_slots = int(total_slots)
            sub.event_id = event_id
            sub.maximum_students = int(maximum_students)
            sub.subevent_requirements = form.cleaned_data.get('requirements')
            sub.last_date = form.cleaned_data.get('registration_deadline')
            sub.allowed_grades = form.cleaned_data.get('allowed_grades')
            sub.subevent_attachment = request.FILES['add_attachment']
            sub.category = form.cleaned_data.get('category')
            sub.save()

            messages.success(request,"Event '{}' has been edited!".format(form.cleaned_data.get('event_name')))
            return redirect('teacher-homepage')
    else:
        form = SubEventCreationForm(initial={'event_name': sub.subevent_name,'event_type': sub.subevent_type,'start_date':sub.subevent_dates.split(" to ")[0],'last_date':sub.subevent_dates.split(" to ")[1],'maximum_applicants':sub.total_slots,'maximum_participants':sub.maximum_students,'requirements':sub.subevent_requirements,'teacher_incharge':sub.subevent_teacher_incharge,'registration_deadline':sub.last_date,'allowed_grades':sub.allowed_grades,'event_description':sub.subevent_information})

    context = {
        "form":form,
        "title":SubEvents.objects.get(pk=subevent_id).subevent_name
    }
    return render(request,'teacherview/add_subevent.html',context)
 
def delete_event(request,event_id,subevent_id):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')

    event = Events.objects.get(event_id=event_id)

    if event.single_check=="True":
        sub = SubEvents.objects.get(subevent_id=subevent_id)
        sub.delete()
        event.delete()
        messages.success(request,"'{}' has been successfully deleted.".format(sub.subevent_name))
    else:
        sub = SubEvents.objects.get(subevent_id=subevent_id)
        sub.delete()
        messages.success(request,"'{}' has been successfully deleted.".format(sub.subevent_name))
    return redirect('teacher-homepage')
 
def searchpage(request):
    if student_check(request):
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('teacher-homepage')

    query = str(request.GET.get('query'))
    context = {
        "page_title": "Search",
        "search_query": query,
        "search_results": []
    }
    if len(context["search_query"]) > 0:
        result_subevent_ids = search(context["search_query"])
        all_subevents_data = SubEvents.objects.all()
        for subevent_data in all_subevents_data:
            if subevent_data.subevent_id in result_subevent_ids:               
                subevent_context = {
                    "url_redirect": "../{}/{}".format(subevent_data.event_id, subevent_data.subevent_id),
                    "event_id": subevent_data.event_id,
                    "event_name": Events.objects.get(event_id=subevent_data.event_id).event_name,
                    "subevent_name": subevent_data.subevent_name,
                    "subevent_type": "Individual" if subevent_data.subevent_type == "I" else "Group",
                    "subevent_dates": subevent_data.subevent_dates.split("to"), #.strftime("%m/%d/%Y").replace(' ', ', '),
                    "subevent_requirements": subevent_data.subevent_requirements,
                    "teacher_incharge": subevent_data.subevent_teacher_incharge,
                    "available_slots": subevent_data.total_slots - subevent_data.total_registrations,
                    "occupied_slots": subevent_data.total_registrations,
                    "publish_date": subevent_data.published_date,
                    "last_date": subevent_data.last_date,
                    "additional_information": subevent_data.subevent_information
                }
                context["search_results"].append(subevent_context)
    return render(request, "teacherview/searchpage.html", context)

def search(query, min_accuracy=0.5, limit=None):
    all_subevents = list(SubEvents.objects.all())
    search_results = []
    for subevent_data in all_subevents:
        resultant_data = {
            "accuracy": 0,
            "subevent_id": subevent_data.subevent_id
        }
        search_criteria = [
            subevent_data.event_id,
            subevent_data.subevent_name,
            subevent_data.subevent_id,
            subevent_data.subevent_name,
            subevent_data.subevent_teacher_incharge,
            subevent_data.subevent_requirements,
            subevent_data.subevent_information
        ]
        for criteria in search_criteria:
            match = get_search_accuracy(query, criteria)
            if match > min_accuracy and match > resultant_data["accuracy"]:
                resultant_data["accuracy"] = match
        if resultant_data["accuracy"] > min_accuracy:
            search_results.append(resultant_data)
    search_results = [data["subevent_id"] for data in sorted(search_results, key=lambda res:res["accuracy"])][:limit if limit else len(search_results)]
    return search_results

def get_ordered_results(raw_data, key, limit=None, descending=True):
    raw_data.sort(key=lambda data:data[key], reverse=descending)
    sorted_data = raw_data[:limit if limit else len(raw_data)]
    return sorted_data

def get_search_accuracy(query, result):
    result = str(result)
    computed_accuracy = 0
    if query in result:
        computed_accuracy = 100
    elif query.lower() in result.lower():
        ind = result.lower().index(query.lower())
        substring = result[ind: ind+len(query)]
        computed_accuracy = 90
    else:
        for occurence_index in [ind for (ind, char) in enumerate(result) if char.lower() == query[0].lower()]:
            loss, ctr, substring = 0, 0, ''
            for ind in range(occurence_index, len(result)):
                if ctr >= len(query):
                    break
                elif query[ctr].lower() == result[ind].lower():
                    substring += result[ind]
                    ctr += 1
                else:
                    loss += 1
            instance_accuracy = 0
            if substring.lower() == query.lower():
                instance_accuracy = 80-(loss*30)
            if instance_accuracy > computed_accuracy:
                computed_accuracy = instance_accuracy
    return round(computed_accuracy, 2)

def get_current_notifications():
    profile_name = ''
    res = {
        "unread": [],
        "read": [],
    }
    date_info = datetime.datetime.now()
    event_ids = [event.subevent_id for event in SubEvents.objects.filter(subevent_teacher_incharge="Vikranti Ashtikar")]
    txt = []
    for subevent_data in SubEvents.objects.all():
        if subevent_data.subevent_id in event_ids:
            datetime_str = subevent_data.subevent_dates.split(" to ")[0] + ' 00:00:00'
            subevent_date = datetime.datetime.strptime(datetime_str, '%d/%m/%Y %H:%M:%S')
            time_diff = int((subevent_date - date_info).days)
            cat = 'unread' if time_diff >= 2 else "read"
            timestamp = ''
            dt = 'Less than a day' if time_diff <= 1 else '{} days'.format(time_diff)
            text = '{} until {}'.format(dt, subevent_data.subevent_name)
            url = '//{}/teachers/{}/{}'.format(website_url, subevent_data.event_id, subevent_data.subevent_id)
            raw_txt = "{}::{}::{}::{}".format(cat, timestamp, text, url)
            txt.append(raw_txt)
        for notification_text in txt:#user_data.notifications:
            cat, timestamp, text, redirect = notification_text.split("::")
            notification_data = {
                "url_redirect": redirect,
                "timestamp": timestamp,
                "text": text
            }
            res[cat].append(notification_data)
    cnt = len(res["unread"])
    if cnt > 9:
        cnt = "9+"
    res["count"] = str(cnt)
    return res

