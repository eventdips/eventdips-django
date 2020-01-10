from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse
from .models import Events,SubEvents,Status
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from studentview.models import Registrations
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import EventCreationForm, SingleEventInformationForm, SubEventCreationForm, LoginForm, ForgotPassword, ResetPassword
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from studentview.views import get_device
import hashlib  
from datetime import date
from random import shuffle

teacher_hash = "teachers/"
student_hash = "students/"

def date_conversion(date):
    months = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
    try:
        dates = date.split(" to ")
        if dates[0]==dates[1]:
            base = dates[0].split("-")
            YYYY,M,DD = int(base[0]),months[int(base[1])],int(base[2])
            suffix = "st" if DD%10==1 else ("nd" if DD%10==2 else ("rd" if DD%10==3 else "th"))
            if len(str(DD))==1:
                DD = "0"+str(DD)
            final = "{}{} {},{}".format(DD,suffix,M,YYYY)
        else:
            final = ""
            for i in range(2):
                base = dates[i].split("-")
                YYYY,M,DD = int(base[0]),months[int(base[1])],int(base[2])
                suffix = "st" if DD%10==1 else ("nd" if DD%10==2 else ("rd" if DD%10==3 else "th"))
                if len(str(DD))==1:
                    DD = "0"+str(DD)
                if i==0:
                    final += "{}{} {},{} to ".format(DD,suffix,M,YYYY)
                else:
                    final += "{}{} {},{}".format(DD,suffix,M,YYYY)

        return final
    except:
        YYYY,MM,DD = date.year,date.month,date.day
        suffix = "st" if DD%10==1 else ("nd" if DD%10==2 else ("rd" if DD%10==3 else "th"))
        if len(str(DD))==1:
            sDD = "0"+str(DD)
        final = "{}{} {},{}".format(DD,suffix,months[MM],YYYY)

        return final

def encrypt(string):
    string = string.upper()
    final = ""
    for i in string:
        final += str(ord(i))
    
    return final

def decrypt(string):
    final = ""
    for i in range(0,len(string),2):
        char = chr(int(string[i]+string[i+1]))
        final += char.lower()

    return final

def student_check(request):
    user = User.objects.get(pk=int(request.COOKIES.get("id")))
    ret = Status.objects.get(user=user)
    if ret.status=="S":
        return True 
    else:
        return False

def finalize_check(request,pk,sub_pk):
    if SubEvents.objects.get(pk=sub_pk).confirmation_status=="Y":
        return True
    else:
        return False

def login_check(request):
    ret = request.COOKIES.get("logged_in")
    if not ret:
        return redirect('login')

def login_auth(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                response = redirect('teacher-homepage')
                response.set_cookie('logged_in',True)
                response.set_cookie('id',User.objects.get(username=username).pk)
                return response
            else:
                messages.warning(request,"Entered Username Or Password Is Incorrect!")
                return redirect('login')
        else:
            messages.warning("Invalid Entries!")
            return redirect('login')
    else:
        form = LoginForm()
    
    context = {
        "form":form
    }

    return render(request,'studentview/desktop/login.html',context)    
    
def logout_auth(request):
    logout(request)
    response = render(request,"studentview/desktop/logout.html")
    response.delete_cookie('logged_in')
    response.delete_cookie('id')
    return response

def forgot_password(request):
    if request.method=='POST':
        form = ForgotPassword(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')  

        return HttpResponseRedirect("/security-questions/{}".format(email))       
    else:
        form = ForgotPassword()
    
    context = {
        "title":"Forgot Password",
        "form":form
    }

    if get_device(request)=="pc":
        return render(request,'studentview/desktop/forgot_password.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/forgot_password.html',context)

def security_questions(request,email):
    questions = Status.objects.get(user=User.objects.get(email=email)).security_questions.split("%%")

    final = []
    count = 0
    for question in questions:
        sub = {
            "question":question,
            "id":"{}".format(count)
        }

        final.append(sub)
        count +=1

    context = {
        "title":"Security Questions",
        "questions": final,
        "url_redirect": "/reset-password/{}/{}".format(email,encrypt(email))
    }

    print(encrypt(email))

    return render(request,'studentview/desktop/security_questions.html', context)

def reset_password(request,email,code):
    if decrypt(code)!=email:
        messages.warning(request,"Illegal Action Attempted!")
        return redirect('login')

    first_ans = request.GET.get('0').lower()
    second_ans = request.GET.get('1').lower()
    third_ans = request.GET.get('2').lower()

    status = Status.objects.get(user=User.objects.get(email=email))
    answers = status.security_answers.split("%%")

    if first_ans==decrypt(answers[0]) and second_ans==decrypt(answers[1]) and third_ans==decrypt(answers[2]):
        if request.method=='POST':
            form = ResetPassword(request.POST)
            if form.is_valid():
                password = form.cleaned_data.get('password')
                confirm_pass = form.cleaned_data.get('confirm_password')
                
                if password==confirm_pass:
                    user = User.objects.get(email=email)
                    if user.password == password:
                        messages.warning(request,"Entered Password Is Already In Use!")
                        return HttpResponseRedirect("/reset-password/{}".format(email))
                    else:
                        user.set_password(password)
                        user.save()
                        messages.success(request,"Your Password Has Been Changed!")
                        return redirect('login')
                else:
                    messages.warning(request,'Entered Passwords Do Not Match!')
                    return HttpResponseRedirect("/reset-password/{}".format(email))
        else:
            form = ResetPassword()
    
        context = {
            "form":form
        }

        return render(request,'studentview/desktop/reset_password.html',context) 
    else:
        messages.warning(request,"Answers Entered are Incorrect!")
        return HttpResponseRedirect("/security-questions/{}".format(email))

def event_over_check(event_id,subevent_id):
    if not subevent_id:
        event = Events.objects.get(pk=event_id)
        if event.event_dates.split(" to ")[1]>=str(date.today()):
            return True
        else:
            return False
    else:
        subevent = SubEvents.objects.get(pk=subevent_id)
        if subevent.subevent_dates.split(" to ")[1]>=str(date.today()):
            return True
        else:
            return False

def home(request):
    login_check(request)

    try:
        if student_check(request):
            return redirect('student-homepage')
    except:
        return redirect('login')
        
    events = list(Events.objects.all())
    teacher_id = int(request.COOKIES.get("id"))
    final = []

    #There is also data available regarding: Total Slots, Date Posted, Time Posted, Event Type, Event Information.
    for i in events:
        if event_over_check(i.event_id,False):
            sub = {}
            if i.single_check=="True":
                sub_event = SubEvents.objects.filter(event_id=i.event_id)
                subevent_id = sub_event.first().subevent_id
                sub["confirmation_status"] = sub_event.first().confirmation_status
                sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,str(i.event_id),str(subevent_id))
            else:
                sub["url_redirect"] = "/{}{}".format(teacher_hash,str(i.event_id))
            sub["name"] = i.event_name
            sub["teacher_incharge"] = i.teacher_incharge
            sub["event_information"]= i.event_information
            #sub["valid"] = event_over_check(i.event_id,False)
            sub["event_dates"] = date_conversion(i.event_dates)

            final.append(sub)

    subevents = list(SubEvents.objects.all())
    final2=[]
    for s_event in subevents:
        if event_over_check(s_event.event_id,s_event.subevent_id):
            if s_event.subevent_teacher_incharge_id==teacher_id or Status.objects.get(user=User.objects.get(pk=teacher_id)).status=="M":
                if s_event.selected_students<s_event.maximum_students and s_event.total_slots>s_event.total_registrations:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                    sub["event_information"]= s_event.subevent_information
                    sub["event_dates"] = date_conversion(s_event.subevent_dates)
                    sub["event_edit_redirect"] = "/{}edit-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["event_delete_redirect"] = "/{}delete-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["category"] = s_event.category
                    sub["valid"] = event_over_check(s_event.event_id,s_event.subevent_id)
                    sub["confirmation_status"] = s_event.confirmation_status
                    sub["completed_check"] = False
                    final2.append(sub)
                else:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                    sub["event_information"]= s_event.subevent_information
                    sub["event_dates"] = date_conversion(s_event.subevent_dates)
                    sub["event_edit_redirect"] = "/{}edit-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["event_delete_redirect"] = "/{}delete-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["category"] = s_event.category
                    #sub["valid"] = event_over_check(s_event.event_id,s_event.subevent_id)
                    sub["confirmation_status"] = s_event.confirmation_status
                    sub["completed_check"] = True
                    final2.append(sub)
   
    for i in events:
        if event_over_check(i.event_id,False):
            c=0
            if i.teacher_incharge_id==teacher_id or Status.objects.get(user=User.objects.get(pk=teacher_id)).status=="M":
                for s in final2:
                    if s["name"]==i.event_name:
                        c+=1
                if c==0:
                    sub = {}
                    if i.single_check=="True":
                        sub_event = SubEvents.objects.filter(event_id=i.event_id)
                        subevent_id = sub_event.first().subevent_id
                        sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,str(i.event_id),str(subevent_id))
                    else:
                        sub["url_redirect"] = "/{}{}".format(teacher_hash,str(i.event_id))
                    sub["name"] = i.event_name
                    sub["teacher_incharge"] = i.teacher_incharge
                    sub["event_information"]= i.event_information
                    #sub["valid"] = event_over_check(i.event_id,False)
                    sub["event_dates"] = date_conversion(i.event_dates)
                    sub["event_check"] = True
                    final2.append(sub)

    context = {"title":"Home",
        "AllEvents": final,
        "MyEvents":final2,
        "status": "M" if Status.objects.get(user=User.objects.get(pk=teacher_id)).status=="M" else "",
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count": "3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/home.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/home.html',context)

def myevents(request):
    login_check(request)

    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')

    teacher_id = int(request.COOKIES.get("id"))
    subevents = list(SubEvents.objects.all())
    status = Status.objects.get(user=User.objects.get(pk=teacher_id))
    final=[]
    for s_event in subevents:
        if event_over_check(s_event.event_id,s_event.subevent_id):
            if s_event.subevent_teacher_incharge_id==teacher_id or status.status=="M":
                if s_event.selected_students<s_event.maximum_students and s_event.total_slots>s_event.total_registrations:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                    sub["event_information"]= s_event.subevent_information
                    sub["event_dates"] = date_conversion(s_event.subevent_dates)
                    sub["event_edit_redirect"] = "/{}edit-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["event_delete_redirect"] = "/{}delete-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["completed_check"] = False
                    sub["confirmation_status"] = s_event.confirmation_status
                    final.append(sub)
                else:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                    sub["event_information"]= s_event.subevent_information
                    sub["event_dates"] = date_conversion(s_event.subevent_dates)
                    sub["event_edit_redirect"] = "/{}edit-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["event_delete_redirect"] = "/{}delete-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["completed_check"] = True
                    sub["confirmation_status"] = s_event.confirmation_status
                    final.append(sub)

    context = {"title":"MyEvents",
        "MyEvents":final,
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }
    
    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/myevents.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/myevents.html',context)

def allevents(request):
    login_check(request)

    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
        
    subevents = list(SubEvents.objects.all())
    final=[]
    for s_event in subevents:   
        if event_over_check(s_event.event_id,s_event.subevent_id):     
            sub = {}
            sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
            sub["name"] = s_event.subevent_name
            sub["teacher_incharge"] = s_event.subevent_teacher_incharge
            sub["event_information"]= s_event.subevent_information
            sub["event_dates"] = date_conversion(s_event.subevent_dates)
            sub["confirmation_status"] = s_event.confirmation_status
            final.append(sub)

    context = {"title":"AllEvents",
        "AllEvents":final,
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/allevents.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/allevents.html',context)

def profile(request):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')

    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    status = Status.objects.get(user=user)
    
    final = []
    for s_event in list(SubEvents.objects.all()):
        if event_over_check(s_event.event_id,s_event.subevent_id):
            if s_event.subevent_teacher_incharge_id==user.pk or status.status=="M":
                sub = {}
                if s_event.selected_students<s_event.maximum_students and s_event.total_slots>s_event.total_registrations:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["event_dates"] = date_conversion(s_event.subevent_dates)
                    sub["event_edit_redirect"] = "/{}edit-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["event_delete_redirect"] = "/{}delete-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["category"] = s_event.category
                    sub["event_information"] = s_event.subevent_information
                    sub["confirmation_status"] = s_event.confirmation_status
                    sub["completed_check"] = False
                    
                    final.append(sub)
                else:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["event_dates"] = date_conversion(s_event.subevent_dates)
                    sub["event_edit_redirect"] = "/{}edit-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["event_delete_redirect"] = "/{}delete-event/{}/{}".format(teacher_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["category"] = s_event.category
                    sub["completed_check"] = True
                    sub["event_information"] = s_event.subevent_information
                    sub["confirmation_status"] = s_event.confirmation_status
                    final.append(sub)

    stat = "Admin" if status.status=="M" else ""
    context = {
        "username": user.username,
        "name": user.first_name + " " + user.last_name,
        "email": user.email,
        "status": stat,
        "department": status.department,
        "MyEvents": final,
        "title": user.first_name + " " + user.last_name,
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/teacherProfile.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/teacherProfile.html',context)

def subevents(request,pk):
    login_check(request)

    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')

    event = Events.objects.get(pk=pk)
    subevents = list(SubEvents.objects.filter(event_id=event.event_id))
    teacher_id = int(request.COOKIES.get("id"))

    final = []
    for i in subevents:
        if event_over_check(i.event_id,i.subevent_id):
            sub = {}
            sub["name"] = i.subevent_name
            sub["dates"] = date_conversion(i.subevent_dates)
            sub["available_slots"] = str(i.total_slots-i.total_registrations)
            sub["total_registrations"] = str(i.total_registrations)
            sub["teacher_incharge"] = i.subevent_teacher_incharge   
            sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,str(event.event_id),str(i.subevent_id))
            sub["event_attachment"] = i.subevent_attachment
            sub["confirmation_status"] = i.confirmation_status
            final.append(sub)

    context = {"title":event.event_name,
                "event_name": event.event_name,
                "url_redirect2": "/{}add-event/{}/sub/add".format(teacher_hash,event.event_id),
                "my_event":True if event.teacher_incharge_id==teacher_id else False,
                "subevents":final,
                "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
                "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
                "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]}

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/subevents.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/subevents.html',context)

def subevent(request,pk,sub_pk):
    login_check(request)

    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')

    if not event_over_check(pk,sub_pk):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    if finalize_check(request,pk,sub_pk):
        messages.warning(request,"Event '{}' Has Already Been Finalized! No Changes Are Allowed".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    event = Events.objects.filter(pk=pk).first()
    subevent = SubEvents.objects.filter(subevent_id=sub_pk).first()
    teacher_id = int(request.COOKIES.get("id"))

    if subevent.subevent_teacher_incharge_id==teacher_id or Status.objects.get(user=User.objects.get(pk=teacher_id)).status=="M":
        if subevent.selected_students<subevent.maximum_students and subevent.total_slots>subevent.total_registrations:
            final = []
            sub = {}
            sub["url_redirect"] = "/{}{}/{}/rview".format(teacher_hash,str(pk),str(sub_pk))
            sub["name"] = subevent.subevent_name
            sub["dates"] = date_conversion(subevent.subevent_dates)
            sub["type"] = "Group" if subevent.subevent_type != "I" else "Individual"
            sub["size"] = str(subevent.group_size)
            sub["available_slots"] = str(subevent.total_slots-subevent.total_registrations)
            sub["total_registrations"] = str(subevent.total_registrations)
            sub["event_information"] = subevent.subevent_information
            sub["event_requirements"] = subevent.subevent_requirements
            sub["teacher_incharge"] = subevent.subevent_teacher_incharge
            sub["last_date"] = date_conversion(subevent.last_date)
            sub["allowed_grades"] = subevent.allowed_grades  
            sub["event_attachment"] = subevent.subevent_attachment
            sub["event_edit_redirect"] = "/{}edit-event/{}/{}".format(teacher_hash,str(subevent.event_id),str(subevent.subevent_id))
            sub["event_delete_redirect"] = "/{}delete-event/{}/{}".format(teacher_hash,str(subevent.event_id),str(subevent.subevent_id))
            sub["my_event"] = True
            sub["maximum_participants"] = str(subevent.maximum_students)
            sub["selected_students"] = str(subevent.selected_students)
            sub["category"] = subevent.category
            sub["completed_check"] = False
            final.append(sub)
        else:
            final = []
            sub = {}
            sub["url_redirect"] = "/{}{}/{}/rview".format(teacher_hash,str(pk),str(sub_pk))
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
            sub["event_edit_redirect"] = "/{}edit-event/{}/{}".format(teacher_hash,str(subevent.event_id),str(subevent.subevent_id))
            sub["event_delete_redirect"] = "/{}delete-event/{}/{}".format(teacher_hash,str(subevent.event_id),str(subevent.subevent_id))
            sub["my_event"] = True
            sub["maximum_participants"] = str(subevent.maximum_students)
            sub["selected_students"] = str(subevent.selected_students)
            sub["category"] = subevent.category
            sub["completed_check"] = True
            final.append(sub)
    else:
        final = []
        sub = {}
        sub["url_redirect"] = "/{}{}/{}/rview".format(teacher_hash,str(pk),str(sub_pk))
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
                "header_redirect":"/{}{}".format(teacher_hash,str(pk)),
                "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
                "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
                "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]}

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/subevent.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/subevent.html',context)

def view_registrations(request,pk,sub_pk):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
    
    if not event_over_check(pk,sub_pk):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    if finalize_check(request,pk,sub_pk):
        messages.warning(request,"Event '{}' Has Already Been Finalized! No Changes Are Allowed".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    '''if int(request.COOKIES.get("id"))!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')'''

    registrations = list(Registrations.objects.filter(subevent_id=sub_pk))
    final=[]

    for i in registrations:
        sub = {}
        sub["url_redirect"] = "/{}{}/{}/rview/{}".format(teacher_hash,str(pk),str(sub_pk),str(i.registration_id))
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
        "header_redirect":"/{}{}/{}".format(teacher_hash,str(pk),str(sub_pk)),
        "view_selected_students":"/{}{}/{}/rview/view-selected".format(teacher_hash,str(pk),str(sub_pk)),
        "view_registered_students":"/{}{}/{}/rview/view-registered".format(teacher_hash,str(pk),str(sub_pk)),
        "confirmation":"/{}{}/{}/rview/confirmation".format(teacher_hash,str(pk),str(sub_pk)),
        "title":"Registrations",
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/view_registrations.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/view_registrations.html',context)

def confirmation(request,pk,sub_pk):
    login_check(request)

    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
    
    if not event_over_check(pk,sub_pk):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    sub = SubEvents.objects.get(pk=sub_pk)
    if sub.confirmation_status=="N":
        sub.confirmation_status = "Y"
        sub.save()
        #REPORTLAB PDF GEN
        messages.success(request,"Decisions for '{}' have been finalized!".format(sub.subevent_name))

        regs = list(Registrations.objects.filter(subevent_id=sub_pk))
        rejected_students = []
        for reg in regs:
            if reg.reg_status=="R":
                sub = {}
                sub["name"] = reg.user.first_name + " " + reg.user.last_name
                sub["class"] = reg.student_class
                sub["section"] = reg.student_section
                sub["id"] = reg.registration_id
                rejected_students.append(sub)
        
        context = {
            "title": "Reason For Rejections",
            "Rejected_Students": rejected_students,
            "event_name": SubEvents.objects.get(pk=sub_pk).subevent_name,
            "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
            "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
            "notifications_applications":get_current_notifications_teachers(request,0)[2][:3],
            "url_redirect": "/{}{}/{}/reason-for-rejections".format(teacher_hash,pk,sub_pk)
        }

        if get_device(request)=="pc":
            return render(request,'teacherview/desktop/confirmation.html',context)
        elif get_device(request)=="mobile":
            return render(request,'teacherview/mobile/confirmation.html',context)

    else:
        messages.warning(request,"Decisions for '{}' have been already been finalized.".format(sub.subevent_name))
        return redirect('teacher-homepage')

def reason_for_rejection(request,pk,sub_pk):
    login_check(request)

    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
    
    if not event_over_check(pk,sub_pk):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    if SubEvents.objects.get(pk=sub_pk).confirmation_status == "N":
        messages.warning(request,"Decisions for the Event '{}' Are Yet To Be Confirmed.".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    regs = list(Registrations.objects.filter(subevent_id=sub_pk))
    for reg in regs:
        reason = request.GET.get(str(reg.registration_id))
        if reason!="":
            reg.rej_reason = reason
        else:
            reg.rej_reason = "Sorry, your application has not been accepted."
        reg.save()

    messages.success(request,"Students Will be Notified of the Decisions!")
    return redirect('teacher-homepage')


def view_registration(request,pk,sub_pk,r_pk):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
    
    if not event_over_check(pk,sub_pk):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')
    
    if finalize_check(request,pk,sub_pk):
        messages.warning(request,"Event '{}' Has Already Been Finalized! No Changes Are Allowed".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    '''if int(request.COOKIES.get("id"))!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')'''

    registration = Registrations.objects.filter(registration_id=r_pk).first()
    student = User.objects.get(pk=registration.user.pk) 

    sub = {}
    sub["name"]=registration.student_name
    sub["class"]=str(registration.student_class)
    sub["section"]=registration.student_section
    sub["info"]=registration.reg_info
    if registration.event_type=="G":
        sub["group_type"] = True
        regs = list(Registrations.objects.filter(subevent_id=sub_pk))
        members = ""
        for reg in regs:
            if reg.group_id==registration.group_id:
                members += (reg.user.first_name+" "+reg.user.last_name+"; ")
        sub["team_members"] = members
    else:
        sub["group_type"] = False
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
        "header_redirect":"/{}{}/{}/rview".format(teacher_hash,str(pk),str(sub_pk)),
        "url_redirect_1":"/{}{}/{}/rview/{}/accept".format(teacher_hash,str(pk),str(sub_pk),str(r_pk)),
        "url_redirect_2":"/{}{}/{}/rview/{}/reject".format(teacher_hash,str(pk),str(sub_pk),str(r_pk)),
        "view_achievement_redirect":"/{}{}/{}/rview/{}/view-achievement".format(teacher_hash,str(pk),str(sub_pk),str(r_pk)),
        "view_previous_redirect":"/{}{}/{}/rview/{}/view-previous".format(teacher_hash,str(pk),str(sub_pk),str(r_pk)),   
        "title": student.first_name + " " + student.last_name,
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/view_registration.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/view_registration.html',context)

def view_achievement(request,pk,sub_pk,r_pk):
    login_check(request)

    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        pass
    
    user = Registrations.objects.get(registration_id=r_pk).user
    status = Status.objects.get(user=user)

    final=[]
    pre_achievements = status.achievements #will be all the acheivements in a list stored as a string
    list_achievements = pre_achievements[1:-1].split("666")
    
    for i in range(list_achievements.count("")):
        list_achievements.remove("")

    if pre_achievements!="None":
        for pre in list_achievements:
            pre = pre[1:-1]
            ach = pre.split(":")
            sub = {}
            sub["name"] = ach[1]
            sub["info"] = ach[3]
            sub["date"] = date_conversion(ach[5])
            sub["category"] = ach[7]
            sub["event_edit_redirect"] = "achievements/edit/{}".format(ach[9])
            sub["event_delete_redirect"] = "achievements/delete/{}".format(ach[9])
            final.append(sub)
    else:
        final = []

    context ={
        "achievements":final,
        "student_name":user.first_name +" "+ user.last_name + "'s",
        "return_redirect":'/{}{}/{}/rview/{}'.format(teacher_hash,str(pk),str(sub_pk),str(r_pk)),
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
        }
    
    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/view_achievements.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/view_achievements.html',context)

def view_previous_events(request,pk,sub_pk,r_pk):
    login_check(request)

    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        pass

    user = Registrations.objects.get(pk=r_pk).user
    regs = Registrations.objects.all()
    
    final = []
    for reg in regs:
        sub = {}
        if reg.user == user:
            s_event = SubEvents.objects.get(pk=reg.subevent_id)
            sub["name"] = s_event.subevent_name
            sub["category"] = s_event.category
            sub["dates"] = date_conversion(s_event.subevent_dates)

            final.append(sub)

    context = {
        "Events":final,
        "title":user.first_name + " " + user.last_name + "'s Previous Events",
        "return_redirect":'/{}{}/{}/rview/{}'.format(teacher_hash,str(pk),str(sub_pk),str(r_pk)),
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/view_previous_events.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/view_previous_events.html',context)

def accept(request,pk,sub_pk,r_pk):  
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
    
    if not event_over_check(pk,sub_pk):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    if finalize_check(request,pk,sub_pk):
        messages.warning(request,"Event '{}' Has Already Been Finalized! No Changes Are Allowed".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    '''if int(request.COOKIES.get("id"))!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')'''

    registration = Registrations.objects.get(registration_id=r_pk)
    partcipated_in = SubEvents.objects.get(subevent_id=sub_pk)
    
    if registration.reg_status=="A":
        messages.warning(request,"{} has already been selected for '{}'!".format(str(registration.student_name),partcipated_in.subevent_name))
        return HttpResponseRedirect('/{}{}/{}/rview'.format(teacher_hash,str(pk),str(sub_pk)))
    elif partcipated_in.maximum_students == partcipated_in.selected_students:
        messages.warning(request,"Maximum Number of Participants have been selected!")
        return HttpResponseRedirect('/{}{}/{}/rview'.format(teacher_hash,str(pk),str(sub_pk)))
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
        return HttpResponseRedirect('/{}{}/{}/rview'.format(teacher_hash,str(pk),str(sub_pk)))
 
def reject(request,pk,sub_pk,r_pk):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
    
    if not event_over_check(pk,sub_pk):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')
    
    if finalize_check(request,pk,sub_pk):
        messages.warning(request,"Event '{}' Has Already Been Finalized! No Changes Are Allowed".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    '''if int(request.COOKIES.get("id"))!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')'''

    registration = Registrations.objects.get(registration_id=r_pk)
    partcipated_in = SubEvents.objects.get(subevent_id=sub_pk)
    
    if registration.reg_status=="R":
        messages.warning(request,"{} has already been rejected for '{}'.".format(str(registration.student_name),partcipated_in.subevent_name))
        return HttpResponseRedirect('/{}{}/{}/rview'.format(teacher_hash,str(pk),str(sub_pk)))
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
    return HttpResponseRedirect('/{}{}/{}/rview'.format(teacher_hash,str(pk),str(sub_pk)))
 
def view_selected_students(request,pk,sub_pk):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
    
    if not event_over_check(pk,sub_pk):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    if finalize_check(request,pk,sub_pk):
        messages.warning(request,"Event '{}' Has Already Been Finalized! No Changes Are Allowed".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    '''if int(request.COOKIES.get("id"))!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')'''

    registrations = list(Registrations.objects.filter(subevent_id=sub_pk))
    final=[]

    for i in registrations:
        if i.reg_status=="A":
            sub = {}
            sub["url_redirect"] = "/{}{}/{}/rview/{}".format(teacher_hash,str(pk),str(sub_pk),str(i.registration_id))
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
        "header_redirect":"/{}{}/{}/rview".format(teacher_hash,str(pk),str(sub_pk)),
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/view_selected_students.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/view_selected_students.html',context)

def view_registered_students(request,pk,sub_pk):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
    
    if not event_over_check(pk,sub_pk):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    if finalize_check(request,pk,sub_pk):
        messages.warning(request,"Event '{}' Has Already Been Finalized! No Changes Are Allowed".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
        return redirect('teacher-homepage')

    '''if int(request.COOKIES.get("id"))!=SubEvents.objects.get(subevent_id=sub_pk).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')'''

    registrations = list(Registrations.objects.filter(subevent_id=sub_pk))
    final=[]

    for i in registrations:
        sub = {}
        sub["url_redirect"] = "/{}{}/{}/rview/{}".format(teacher_hash,str(pk),str(sub_pk),str(i.registration_id))
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
        "header_redirect":"/{}{}/{}/rview".format(teacher_hash,str(pk),str(sub_pk)),
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/view_registered_students.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/view_registered_students.html',context)

def add_event(request):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')

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
                    try:
                        new_event.event_attachment = request.FILES['add_attachment']
                    except:
                        pass
                    options = []
                    users = User.objects.all()
                    for user in users:
                        try:
                            if Status.objects.get(user=user).status=="T" or Status.objects.get(user=user).status=="M":
                                options.append(user)
                        except:
                            pass
                    new_event.teacher_incharge_id = options[int(form.cleaned_data.get('teacher_incharge'))].pk
                    new_event.teacher_incharge = options[int(form.cleaned_data.get('teacher_incharge'))].first_name + " " + options[int(form.cleaned_data.get('teacher_incharge'))].last_name
                    new_event.save()
                    return HttpResponseRedirect('/{}add-event/{}'.format(teacher_hash,new_event.event_id))
                else:
                    new_event.event_dates = "{} to {}".format(start_date,last_date)
                    new_event.single_check = single_check
                    try:
                        new_event.event_attachment = request.FILES['add_attachment']
                    except:
                        pass
                    options = []
                    users = User.objects.all()
                    for user in users:
                        try:
                            if Status.objects.get(user=user).status=="T" or Status.objects.get(user=user).status=="M":
                                options.append(user)
                        except:
                            pass

                    new_event.teacher_incharge_id = options[int(form.cleaned_data.get('teacher_incharge'))].pk
                    new_event.teacher_incharge = options[int(form.cleaned_data.get('teacher_incharge'))].first_name + " " + options[int(form.cleaned_data.get('teacher_incharge'))].last_name
                    new_event.save()
                    messages.success(request,"Event {} has been successfully created!".format(new_event.event_name)) 
                    return HttpResponseRedirect('/{}add-event/{}/sub'.format(teacher_hash,new_event.event_id))
    else:
        form = EventCreationForm()

    context = {
        "form":form,
        "title":"New Event",
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }
    
    if get_device(request)=="pc":
        return render(request,"teacherview/desktop/add_event.html",context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/add_event.html',context)

def single_event_information(request,event_id):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')

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
                if form.cleaned_data.get('group_size'):
                    new_subevent.group_size = form.cleaned_data.get('group_size')
                else:
                    new_subevent.group_size = 1
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
            "title":Events.objects.get(pk=event_id).event_name,
            "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
            "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
            "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
        }

    if get_device(request)=="pc":
        return render(request,"teacherview/desktop/single_event_information.html",context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/single_event_information.html',context)

def subevent_addition_page(request,event_id):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')

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
                    "url_redirect":"/{}add-event/{}/sub/add".format(teacher_hash,event_id),
                    "event_redirect": "/{}{}".format(teacher_hash,event_id),
                    "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
                    "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
                    "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]}

        if get_device(request)=="pc":
            return render(request,'teacherview/desktop/subevent_addition_page.html',context)
        elif get_device(request)=="mobile":
            return render(request,'teacherview/mobile/subevent_addition_page.html',context)

def add_subevent(request,event_id):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')

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
                    return HttpResponseRedirect('/{}add-event/{}/sub/add'.format(teacher_hash,event_id))
                else:
                    event = Events.objects.get(event_id=event_id)
                    options = []
                    users = User.objects.all()
                    for user in users:
                        try:
                            if Status.objects.get(user=user).status=="T" or Status.objects.get(user=user).status=="M":
                                options.append(user)
                        except:
                            pass
                    new_subevent.subevent_teacher_incharge = options[int(form.cleaned_data.get('teacher_incharge'))].first_name + " " +options[int(form.cleaned_data.get('teacher_incharge'))].last_name
                    new_subevent.subevent_teacher_incharge_id = options[int(form.cleaned_data.get('teacher_incharge'))].pk
                    new_subevent.subevent_name = form.cleaned_data.get('event_name')
                    new_subevent.subevent_dates = form.cleaned_data.get('start_date') +" to " + form.cleaned_data.get("last_date")
                    new_subevent.event_id = event.event_id
                    new_subevent.subevent_information = form.cleaned_data.get('event_description')
                    new_subevent.subevent_type = "I" if form.cleaned_data.get('event_type')=="Individual" else "G"
                    if form.cleaned_data.get('group_size'):
                        new_subevent.group_size = form.cleaned_data.get('group_size')
                    else:
                        new_subevent.group_size = 1
                    new_subevent.total_slots = int(total_slots)
                    new_subevent.maximum_students = int(maximum_students)
                    new_subevent.subevent_requirements = form.cleaned_data.get('requirements')
                    new_subevent.last_date = form.cleaned_data.get('registration_deadline')
                    new_subevent.allowed_grades = form.cleaned_data.get('allowed_grades')
                    try:
                        new_subevent.subevent_attachment = request.FILES['add_attachment']
                    except:
                        pass
                    new_subevent.category = form.cleaned_data.get('category')
                    new_subevent.save()

                    messages.success(request,"Event '{}' has been successfully added to '{}'!".format(form.cleaned_data.get('event_name'),event.event_name))
                    return HttpResponseRedirect('/{}add-event/{}/sub'.format(teacher_hash,event_id))
        else:
            form = SubEventCreationForm()

        context = {
            "form":form,
            "title":Events.objects.get(pk=event_id).event_name,
            "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
            "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
            "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
        }
        
        if get_device(request)=="pc":
            return render(request,'teacherview/desktop/add_subevent.html',context)
        elif get_device(request)=="mobile":
            return render(request,'teacherview/mobile/add_subevent.html',context)

def edit_event(request,event_id,subevent_id):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
    
    if finalize_check(request,event_id,subevent_id):
        messages.warning(request,"Event '{}' Has Already Been Finalized! No Changes Are Allowed!".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('teacher-homepage')

    '''if int(request.COOKIES.get("id"))!=SubEvents.objects.get(subevent_id=subevent_id).subevent_teacher_incharge_id:
        messages.warning(request,'Illegal Action Attempted!')
        return redirect('teacher-homepage')'''

    sub = SubEvents.objects.get(subevent_id=subevent_id)
    if request.method=="POST":
        form = SubEventCreationForm(request.POST,request.FILES,initial={'event_name': sub.subevent_name,'event_type': sub.subevent_type,'start_date':sub.subevent_dates.split(" to ")[0],'last_date':sub.subevent_dates.split(" to ")[1],'maximum_applicants':sub.total_slots,'maximum_participants':sub.maximum_students,'requirements':sub.subevent_requirements,'teacher_incharge':sub.subevent_teacher_incharge,'registration_deadline':sub.last_date,'allowed_grades':sub.allowed_grades,'event_description':sub.subevent_information,'category':sub.category,'add_attachment':sub.subevent_attachment})
        if form.is_valid():
            edit_subevent = form.save(commit=False)
            total_slots = form.cleaned_data.get('maximum_applicants')
            maximum_students = form.cleaned_data.get('maximum_participants')
        
            options = []
            users = User.objects.all()
            for user in users:
                try:
                    if Status.objects.get(user=user).status=="T" or Status.objects.get(user=user).status=="M":
                        options.append(user)
                except:
                    pass

            sub.subevent_teacher_incharge = options[int(form.cleaned_data.get('teacher_incharge'))].first_name + " " + options[int(form.cleaned_data.get('teacher_incharge'))].last_name
            sub.subevent_teacher_incharge_id = options[int(form.cleaned_data.get('teacher_incharge'))].pk
            sub.subevent_name = form.cleaned_data.get('event_name')
            sub.subevent_dates = form.cleaned_data.get('start_date') +" to " + form.cleaned_data.get("last_date")
            sub.subevent_information = form.cleaned_data.get('event_description')
            sub.subevent_type = "I" if form.cleaned_data.get('event_type')=="Individual" else "G"
            if form.cleaned_data.get('group_size'):
                sub.group_size = form.cleaned_data.get('group_size')
            else:
                sub.group_size = 1
            sub.total_slots = int(total_slots)
            sub.event_id = event_id
            sub.maximum_students = int(maximum_students)
            sub.subevent_requirements = form.cleaned_data.get('requirements')
            sub.last_date = form.cleaned_data.get('registration_deadline')
            sub.allowed_grades = form.cleaned_data.get('allowed_grades')
            try:
                sub.subevent_attachment = request.FILES['add_attachment']
            except:
                pass
            sub.category = form.cleaned_data.get('category')
            sub.save()

            messages.success(request,"Event '{}' has been edited!".format(form.cleaned_data.get('event_name')))
            return redirect('teacher-homepage')
    else:
        form = SubEventCreationForm(initial={'event_name': sub.subevent_name,'event_type': sub.subevent_type,'start_date':sub.subevent_dates.split(" to ")[0],'last_date':sub.subevent_dates.split(" to ")[1],'maximum_applicants':sub.total_slots,'maximum_participants':sub.maximum_students,'requirements':sub.subevent_requirements,'teacher_incharge':sub.subevent_teacher_incharge,'registration_deadline':sub.last_date,'allowed_grades':sub.allowed_grades,'event_description':sub.subevent_information})

    context = {
        "form":form,
        "title":SubEvents.objects.get(pk=subevent_id).subevent_name,
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/add_subevent.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/add_subevent.html',context)

def delete_event(request,event_id,subevent_id):
    login_check(request)

    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
    
    if finalize_check(request,pk,sub_pk):
        messages.warning(request,"Event '{}' Has Already Been Finalized! No Changes Are Allowed".format(SubEvents.objects.get(pk=sub_pk).subevent_name))
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
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
        
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
                    "confirmation_status": subevent_data.confirmation_status,
                    "last_date": subevent_data.last_date,
                    "additional_information": subevent_data.subevent_information
                }
                context["search_results"].append(subevent_context)

    context["notifications_days_left"]=get_current_notifications_teachers(request,0)[1][:3]
    context["notifications_count"]="3+" if get_current_notifications_teachers(request,0)[0] > 3 else get_current_notifications_teachers(request,0)[0]
    context["notifications_applications"]=get_current_notifications_teachers(request,0)[2][:3]
    
    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/searchpage.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/searchpage.html',context)

def search(query, min_accuracy=0.5, limit=None):
    all_subevents = list(SubEvents.objects.all())
    search_results = []
    for subevent_data in all_subevents:
        if event_over_check(subevent_data.event_id,subevent_data.subevent_id):
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

def show_all_notifications(request):
    login_check(request)
    
    try:
        if student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('student-homepage')
    except:
        return redirect('login')
        
    cnt,days_left,application_sent = get_current_notifications_teachers(request,1)

    context = {
        "title":"Notifications",
        "Days_Left": days_left,
        "Application_Sent": application_sent,
        "notifications_days_left":get_current_notifications_teachers(request,0)[1][:3],
        "notifications_count":"3+" if get_current_notifications_teachers(request,0)[0]>3 else get_current_notifications_teachers(request,0)[0],
        "notifications_applications":get_current_notifications_teachers(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'teacherview/desktop/show_all_notifications.html',context)
    elif get_device(request)=="mobile":
        return render(request,'teacherview/mobile/show_all_notifications.html',context)

def get_current_notifications_teachers(request,typ):
    '''two types
    1- Days Left to Deadline
    2- New Application
    '''
    
    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    events = SubEvents.objects.filter(subevent_teacher_incharge_id=user.pk)

    final = []
    for event in events:
        sub = {}
        if event_over_check(event.event_id,event.subevent_id):
            cur = date.today()
            d = event.subevent_dates.split(" to ")[1]
            date_obj = date(int(d.split("-")[0]),int(d.split("-")[1]),int(d.split("-")[2]))
            if (date_obj-cur).days>0:
                sub["notification_header"] = "Days Left"
                if typ==0:
                    sub["days_left"] = "- " + str((date_obj-cur).days)
                else:
                    sub["days_left"] = str((date_obj-cur).days)
                sub["event_name"] = event.subevent_name
                sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,event.event_id,event.subevent_id)
            elif (date_obj-cur).days==0:
                sub["notification_header"] = "Deadline Today!"
                sub["event_name"] = event.subevent_name
                sub["days_left"] = ""
                sub["url_redirect"] = "/{}{}/{}".format(teacher_hash,event.event_id,event.subevent_id)
            final.append(sub)

    final2=[]
    for event in events:
        if event_over_check(event.event_id,event.subevent_id):
            if event.confirmation_status=="N":
                regs = Registrations.objects.filter(subevent_id=event.subevent_id)
                for reg in regs:
                    sub={}
                    sub["student_name"] = reg.student_name
                    sub["notification_header"] = "Application Submitted!"
                    sub["event_name"] = event.subevent_name
                    sub["url_redirect"] = "/{}{}/{}/rview/{}".format(teacher_hash,event.event_id,event.subevent_id,reg.registration_id)

                    final2.append(sub)

    shuffle(final)
    shuffle(final2)
    return len(final)+len(final2),final,final2

