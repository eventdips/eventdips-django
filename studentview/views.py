from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Registrations
from teacherview.models import Events,SubEvents,Status
from teacherview import views as t_views
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import RegistrationSingleForm, AchievementForm, RegistrationsGroupForm
from datetime import date
from django_user_agents.utils import get_user_agent

def event_finalized_check(event_id,subevent_id):
    sub = SubEvents.objects.get(pk=subevent_id)
    if sub.confirmation_status == "Y":
        return True
    else:
        return False
    
def registration_deadline_passed(event_id,subevent_id):
    reg_deadline = SubEvents.objects.get(pk=subevent_id).last_date
    today = date.today()

    if today>reg_deadline:
        return True
    else:
        return False
    

def get_device(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return "mobile"
    else:
        return "pc"

def home(request):
    t_views.login_check(request)

    try:
        if not t_views.student_check(request):
            return redirect('teacher-homepage')
    except:
        pass

    events = list(Events.objects.all())
    final2 = []
    for i in events:
        if t_views.event_over_check(i.event_id,False):
            sub = {}
            if i.single_check=="True":
                sub_event = SubEvents.objects.filter(event_id=i.event_id)
                subevent_id = sub_event.first().subevent_id
                sub["url_redirect"] = "/{}{}/{}".format(t_views.student_hash,str(i.event_id),str(subevent_id))
                sub["registration_deadline"] = t_views.date_conversion(sub_event.first().last_date)
                #sub["valid"] = t_views.event_over_check(i.event_id,False)
                if sub_event.first().total_slots==sub_event.first().total_registrations:
                    sub["completed_check"] = True
                else:
                    sub["completed_check"] = False
                sub["finalized"] = True if sub_event.first().confirmation_status == "Y" else False
            else:
                sub["url_redirect"] = "/{}{}".format(t_views.student_hash,str(i.event_id))
            sub["name"] = i.event_name
            sub["teacher_incharge"] = i.teacher_incharge
            sub["event_information"]= i.event_information
            sub["event_dates"] = t_views.date_conversion(i.event_dates)

            final2.append(sub)

    subevents = list(SubEvents.objects.all())
    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    final=[]
    for s_event in subevents:
        if t_views.event_over_check(s_event.event_id,s_event.subevent_id):
            r = list(Registrations.objects.filter(subevent_id=s_event.subevent_id))
            for i in r:
                if i.user==user:
                    if s_event.total_slots>s_event.total_registrations:
                        sub = {}
                        sub["url_redirect"] = "/{}{}/{}".format(t_views.student_hash,str(s_event.event_id),str(s_event.subevent_id))
                        sub["name"] = s_event.subevent_name
                        sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                        sub["registration_deadline"]= t_views.date_conversion(s_event.last_date)
                        sub["event_dates"] = t_views.date_conversion(s_event.subevent_dates)
                        sub["category"] = s_event.category
                        #sub["valid"] = t_views.event_over_check(s_event.event_id,s_event.subevent_id)
                        sub["completed_check"] = False
                        sub["finalized"] = True if s_event.confirmation_status == "Y" else False
                        final.append(sub)
                    else:
                        sub = {}
                        sub["url_redirect"] = "/{}{}/{}".format(t_views.student_hash,str(s_event.event_id),str(s_event.subevent_id))
                        sub["name"] = s_event.subevent_name
                        sub["teacher_incharge"] = s_event.subevent_teacher_incharge
                        sub["registration_deadline"]= t_views.date_conversion(s_event.last_date)
                        sub["event_dates"] = t_views.date_conversion(s_event.subevent_dates)
                        sub["category"] = s_event.category
                        #sub["valid"] = t_views.event_over_check(s_event.event_id,s_event.subevent_id)
                        sub["completed_check"] = True
                        sub["finalized"] = True if s_event.confirmation_status == "Y" else False
                        final.append(sub)
            
    context = {
        "MyEvents": final,
        "OngoingEvents": final2,
        "Title": "Home",
        "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
        "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,0)[0],
        "notifications_decisions":get_current_notifications_students(request,0)[2][:3]
    }
    
    if get_device(request)=="pc":
        return render(request,'studentview/desktop/home.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/home.html',context)

def profile(request):
    t_views.login_check(request)

    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        pass

    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    final = []
    for s_event in list(SubEvents.objects.all()):
        if t_views.event_over_check(s_event.event_id,s_event.subevent_id):
            registrations = list(Registrations.objects.filter(subevent_id=s_event.subevent_id))
            if user in [reg.user for reg in registrations]:
                sub = {}
                if s_event.total_slots>s_event.total_registrations:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(t_views.student_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["event_dates"] = t_views.date_conversion(s_event.subevent_dates)
                    sub["registration_deadline"] = t_views.date_conversion(s_event.last_date)
                    sub["category"] = s_event.category
                    sub["event_information"] = s_event.subevent_information
                    sub["completed_check"] = False
                    sub["finalized"] = True if s_event.confirmation_status == "Y" else False
                    final.append(sub)
                else:
                    sub = {}
                    sub["url_redirect"] = "/{}{}/{}".format(t_views.student_hash,str(s_event.event_id),str(s_event.subevent_id))
                    sub["name"] = s_event.subevent_name
                    sub["event_dates"] = t_views.date_conversion(s_event.subevent_dates)
                    sub["registration_deadline"] = t_views.date_conversion(s_event.last_date)
                    sub["category"] = s_event.category
                    sub["completed_check"] = True
                    sub["event_information"] = s_event.subevent_information
                    sub["finalized"] = True if s_event.confirmation_status == "Y" else False
                    final.append(sub)

    context = {
        "username": user.username,
        "name": user.first_name + " " + user.last_name,
        "email": user.email,
        "MyEvents": final,
        "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
        "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,0)[0],
        "notifications_decisions":get_current_notifications_students(request,0)[2][:3]
    }
    
    if get_device(request)=="pc":
        return render(request,'studentview/desktop/myProfile.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/myProfile.html',context)

def my_achievements(request):
    t_views.login_check(request)

    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        pass
    
    id_ = int(request.COOKIES.get('id')) 
    user = User.objects.get(pk=id_)
    status = Status.objects.get(user=user)

    final=[]
    pre_achievements = status.achievements #will be all the acheivements in a list stored as a string
    list_achievements = pre_achievements[1:-1].split("666")
    if pre_achievements != "None":
        for i in range(list_achievements.count("")):
            list_achievements.remove("")

        for pre in list_achievements:
            pre = pre[1:-1]
            ach = pre.split(":")
            sub = {}
            sub["name"] = ach[1]
            sub["info"] = ach[3]
            sub["date"] = t_views.date_conversion(ach[5])
            sub["category"] = ach[7]
            sub["event_edit_redirect"] = "achievements/edit/{}".format(ach[9])
            sub["event_delete_redirect"] = "achievements/delete/{}".format(ach[9])
            final.append(sub)

    context ={
        "achievements":final,
        "url_redirect2":"achievements/add",
        "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
        "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,0)[0],
        "notifications_decisions":get_current_notifications_students(request,0)[2][:3]}
    
    if get_device(request)=="pc":
        return render(request,'studentview/desktop/my_achievements.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/my_achievements.html',context)

def add_achievement(request):
    t_views.login_check(request)

    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')
    
    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    status = Status.objects.get(user=user)
    achievements = status.achievements
    list_achievements = achievements[1:-1].split("666")
    list_achievements.pop(-1)
    latest_id = int(list_achievements[-1][1:-1].split(":")[-1]) if achievements != "None" else 0

    if request.method=="POST":
        form = AchievementForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("achievement_title")
            date = form.cleaned_data.get("start_date_of_achievement") + " to " + form.cleaned_data.get("last_date_of_achievement")
            category = form.cleaned_data.get("achievement_type")         
            info = form.cleaned_data.get("achievement_info")
            new_achievement = '''
            "name":{}:"information":{}:"Registration Date":{}:"category":{}:"id":{}
            '''.format(title,info,date,category,str(latest_id+1))

            new_achievement = "{"+new_achievement+"}"
            list_achievements.append(new_achievement)
            final = "["
            for ach in list_achievements:
                final += ach 
                final +="666"
            final += "]"

            status.achievements = final
            status.save()

            messages.success(request,"Achievement Has Been Successfully Added!")
            return redirect('student-achievements')
    else:
        form = AchievementForm()

    context = {
        "form":form,
        "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
        "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,0)[0],
        "notifications_decisions":get_current_notifications_students(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'studentview/desktop/add_achievement.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/add_achievement.html',context)

def achievements_edit(request,achievement_id):
    t_views.login_check(request)

    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')

    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    status = Status.objects.get(user=user)
    achievements = status.achievements
    list_achievements = achievements[1:-1].split("666")
    list_achievements.pop(-1)

    current_achievement = list_achievements[achievement_id-1][1:-1]
    ach = current_achievement.split(":")
    title = ach[1]

    if request.method=="POST":
        form = AchievementForm(request.POST,initial={"achievement_title":ach[1],"start_date_of_achievement":ach[5].split(" to ")[0],"last_date_of_achievement":ach[5].split(" to ")[1],"achievement_type":ach[7],"achievement_info":ach[3]})
        if form.is_valid():
            title = form.cleaned_data.get("achievement_title")
            date = form.cleaned_data.get("start_date_of_achievement") + " to " + form.cleaned_data.get("last_date_of_achievement")
            category = form.cleaned_data.get("achievement_type")         
            info = form.cleaned_data.get("achievement_info")
            list_achievements[achievement_id-1] = '''
            "name":{}:"information":{}:"Registration Date":{}:"category":{}:"id":{}
            '''.format(title,info,date,category,str(achievement_id))

            list_achievements[achievement_id-1] = "{"+list_achievements[achievement_id-1]+"}"
            final = "["
            for ach in list_achievements:
                final += ach 
                final +="666"
            final += "]"

            status.achievements = final
            status.save()

            messages.success(request,"Achievement Has Been Successfully Edited!")
            return redirect('student-achievements')
    else:
        form = AchievementForm(initial={"achievement_title":ach[1],"start_date_of_achievement":ach[5].split(" to ")[0],"last_date_of_achievement":ach[5].split(" to ")[1],"achievement_type":ach[7],"achievement_info":ach[3]})        

    context = {
        "form":form,
        "title":title,
        "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
        "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,0)[0],
        "notifications_decisions":get_current_notifications_students(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'studentview/desktop/add_achievement.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/add_achievement.html',context)

def achievements_delete(request,achievement_id):
    t_views.login_check(request)

    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')

    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    status = Status.objects.get(user=user)
    achievements = status.achievements
    list_achievements = achievements[1:-1].split("666")
    list_achievements.pop(-1)
    list_achievements.pop(achievement_id-1)

    final = "["
    for ach in list_achievements:
        final += ach 
        final +="666"
    final += "]" 

    status.achievements = final
    status.save()

    messages.success(request,"Achievement Has Been Successfully Deleted!")
    return redirect('student-achievements')


def event_by_category(request,category):
    t_views.login_check(request)

    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')

    events = list(SubEvents.objects.filter(category=category))

    final = []
    for i in events:
        if t_views.event_over_check(i.event_id,False):
            sub = {}
            if i.total_slots>i.total_registrations:
                sub["completed_check"] = False
            else:
                sub["completed_check"] = True
     
            ssub["finalized"] = True if i.confirmation_status == "Y" else False
            sub["name"] = i.subevent_name
            sub["dates"] = t_views.date_conversion(i.subevent_dates)
            sub["available_slots"] = str(i.total_slots-i.total_registrations)
            sub["registration_deadline"] = t_views.date_conversion(i.last_date)
            sub["total_registrations"] = str(i.total_registrations)
            sub["teacher_incharge"] = i.subevent_teacher_incharge   
            sub["url_redirect"] = "/{}{}/{}".format(t_views.student_hash,str(i.event_id),str(i.subevent_id))
            sub["event_attachment"] = i.subevent_attachment
            final.append(sub)

    context = {"title": category,
                "subevents":final,
                "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
                "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,0)[0],
                "notifications_decisions":get_current_notifications_students(request,0)[2][:3]
            }

    if get_device(request)=="pc":
        return render(request,'studentview/desktop/event_by_category.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/event_by_category.html',context)

def my_applications(request):
    t_views.login_check(request)

    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')
    
    pk = int(request.COOKIES.get('id'))
    registrations = list(Registrations.objects.filter(user=User.objects.get(pk=pk)))
    final = []
    for i in registrations:
        if t_views.event_over_check(False,i.subevent_id):
            sub = {}
            sub["event_name"] = SubEvents.objects.get(pk=i.subevent_id).subevent_name
            sub["teacher_incharge"] = SubEvents.objects.get(pk=i.subevent_id).subevent_teacher_incharge
            sub["date_applied"] = t_views.date_conversion(i.date_applied)
            if not i.reg_status:
                sub["status"] = "Pending"
            elif i.reg_status=="A":
                sub["status"] = "Accepted"
            else:
                sub["status"] = "Rejected"
            final.append(sub)


    context={
        "Registrations":final,
        "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
        "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,0)[0],
        "notifications_decisions":get_current_notifications_students(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'studentview/desktop/my_applications.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/my_applications.html',context)


def subevents(request,event_id):
    t_views.login_check(request)

    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')

    event = Events.objects.filter(pk=event_id).first()
    subevents = list(SubEvents.objects.filter(event_id=event_id))

    final = []
    for i in subevents:
        if t_views.event_over_check(False,i.subevent_id):
            sub = {}
            if i.total_slots>i.total_registrations:
                sub["completed_check"] = False
            else:
                sub["completed_check"] = True
            sub["name"] = i.subevent_name
            sub["dates"] = t_views.date_conversion(i.subevent_dates)
            sub["available_slots"] = str(i.total_slots-i.total_registrations)
            sub["registration_deadline"] = t_views.date_conversion(i.last_date)
            sub["total_registrations"] = str(i.total_registrations)
            sub["teacher_incharge"] = i.subevent_teacher_incharge   
            sub["url_redirect"] = "/{}{}/{}".format(t_views.student_hash,str(event_id),str(i.subevent_id))
            sub["event_attachment"] = i.subevent_attachment
            sub["finalized"] = True if i.confirmation_status == "Y" else False
            final.append(sub)

    context = {"title":event.event_name,
                "event_name": event.event_name,
                "subevents":final,
                "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
                "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,0)[0],
        "notifications_decisions":get_current_notifications_students(request,0)[2][:3]}

    if get_device(request)=="pc":
        return render(request,'studentview/desktop/subevents.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/subevents.html',context)

def subevent(request,event_id,subevent_id):
    t_views.login_check(request)

    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')
    
    if not t_views.event_over_check(event_id,subevent_id):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('student-homepage')
    
    if event_finalized_check(event_id,subevent_id):
        messages.warning(request,"Decisions Regarding Event '{}' Is Already Finalized!".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('student-homepage')

    final = []
    event = Events.objects.get(event_id=event_id)
    subevent = SubEvents.objects.get(subevent_id=subevent_id)

    regs = [reg for reg in Registrations.objects.all() if reg.event_type=="G"]

    try:
        if regs[-1].group_id:
            group_id = regs[-1].group_id+1
        else:
            group_id = 1
    except:
        group_id=1

    if subevent.total_slots>subevent.total_registrations:
        try:        
            if Registrations.objects.get(user=User.objects.get(pk=int(request.COOKIES.get('id'))),subevent_id=subevent_id) in list(Registrations.objects.filter(subevent_id=subevent_id)):
                sub = {}
                sub["url_redirect"] = "/{}{}/{}/registration".format(t_views.student_hash,str(event_id),str(subevent_id))
                sub["name"] = subevent.subevent_name
                sub["dates"] = t_views.date_conversion(subevent.subevent_dates)
                sub["type"] = "Group" if subevent.subevent_type != "I" else "Individual"
                sub["available_slots"] = str(subevent.total_slots-subevent.total_registrations)
                sub["event_information"] = subevent.subevent_information
                sub["event_requirements"] = subevent.subevent_requirements
                sub["teacher_incharge"] = subevent.subevent_teacher_incharge
                sub["last_date"] = t_views.date_conversion(subevent.last_date)
                sub["allowed_grades"] = subevent.allowed_grades  
                sub["event_attachment"] = subevent.subevent_attachment
                sub["category"] = subevent.category
                sub["my_registered_event"] = True
                sub["completed_check"] = False
                final.append(sub)
        except:
            sub = {}
            if subevent.subevent_type == "G":
                sub["url_redirect"] = "/{}{}/{}/add-group/{}".format(t_views.student_hash,event_id,subevent_id,group_id)
            else:
               sub["url_redirect"] = "/{}{}/{}/registration".format(t_views.student_hash,str(event_id),str(subevent_id))
            
            sub["name"] = subevent.subevent_name
            sub["dates"] = t_views.date_conversion(subevent.subevent_dates)
            sub["type"] = "Group" if subevent.subevent_type != "I" else "Individual"
            sub["available_slots"] = str(subevent.total_slots-subevent.total_registrations)
            sub["event_information"] = subevent.subevent_information
            sub["event_requirements"] = subevent.subevent_requirements
            sub["teacher_incharge"] = subevent.subevent_teacher_incharge
            sub["last_date"] = t_views.date_conversion(subevent.last_date)
            sub["allowed_grades"] = subevent.allowed_grades  
            sub["event_attachment"] = subevent.subevent_attachment
            sub["category"] = subevent.category
            sub["my_registered_event"] = False
            sub["completed_check"] = False
            final.append(sub)
    else:
        sub = {}
        sub["url_redirect"] = "/{}{}/{}/registration".format(t_views.student_hash,str(event_id),str(subevent_id))
        sub["name"] = subevent.subevent_name
        sub["dates"] = t_views.date_conversion(subevent.subevent_dates)
        sub["type"] = "Group" if subevent.subevent_type != "I" else "Individual"
        sub["available_slots"] = str(subevent.total_slots-subevent.total_registrations)
        sub["event_information"] = subevent.subevent_information
        sub["event_requirements"] = subevent.subevent_requirements
        sub["teacher_incharge"] = subevent.subevent_teacher_incharge
        sub["last_date"] = t_views.date_conversion(subevent.last_date)
        sub["allowed_grades"] = subevent.allowed_grades  
        sub["event_attachment"] = subevent.subevent_attachment
        sub["category"] = subevent.category
        sub["completed_check"] = True
        final.append(sub)
        
    context = {"title":subevent.subevent_name,
                "event_name": event.event_name,
                "subevents":final,
                "header_redirect":"/{}{}".format(t_views.student_hash,str(event_id)),
                "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
                "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,0)[0],
        "notifications_decisions":get_current_notifications_students(request,0)[2][:3]}
                
    if get_device(request)=="pc":
        return render(request,'studentview/desktop/subevent.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/subevent.html',context)

def add_reg_for_group(request,event_id,subevent_id,current_group_id):
    t_views.login_check(request)
    
    #TEACHER CHECK
    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')        
    except:
        return redirect('login')
    
    if not t_views.event_over_check(event_id,subevent_id):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('student-homepage')
    
    if event_finalized_check(event_id,subevent_id):
        messages.warning(request,"Decisions Regarding Event '{}' Is Already Finalized!".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('student-homepage')

    if registration_deadline_passed(event_id,subevent_id):
        messages.warning(request,"Registration Deadline for '{}' Has Passed.".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('student-homepage')

    subevent = SubEvents.objects.get(pk=subevent_id)
    if subevent.total_registrations==subevent.total_slots:
        messages.warning(request,"Registrations Are Complete For '{}'".format(subevent.subevent_name))
        return redirect('student-homepage')

    regs = [reg for reg in Registrations.objects.all() if reg.event_type=="G"]

    count = 0
    for reg in regs:
        if reg.group_id==current_group_id:
            count+=1
        
    if count==subevent.group_size:
        messages.success(request,"Registration Successful for '{}'".format(subevent.subevent_name))
        return redirect('student-homepage')

    final = []
    sub = {}
    sub["name"] = subevent.subevent_name
    sub["dates"] = t_views.date_conversion(subevent.subevent_dates)
    sub["event_information"] = subevent.subevent_information
    sub["teacher_incharge"] = subevent.subevent_teacher_incharge
    sub["group_size"] = subevent.group_size
    sub["current_count"] = str(count)+"/"+str(subevent.group_size)
    final.append(sub)

    context = {"title":subevent.subevent_name,
                "event":final,
                "url_redirect":"/{}{}/{}/add-group/{}/registration".format(t_views.student_hash,event_id,subevent_id,current_group_id),
                "notifications_days_left":get_current_notifications_students(request,0)[1],
                "notifications_count":get_current_notifications_students(request,0)[0]
            }

    if get_device(request)=="pc":
        return render(request,'studentview/desktop/add_reg_for_group.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/add_reg_for_group.html',context)
 
def group_registration(request,event_id,subevent_id,current_group_id):
    t_views.login_check(request)
    
    #TEACHER CHECK
    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')        
    except:
        return redirect('login')
    
    if not t_views.event_over_check(event_id,subevent_id):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('student-homepage')
    
    if event_finalized_check(event_id,subevent_id):
        messages.warning(request,"Decisions Regarding Event '{}' Is Already Finalized!".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('student-homepage')

    if registration_deadline_passed(event_id,subevent_id):
        messages.warning(request,"Registration Deadline for '{}' Has Passed.".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('student-homepage')

    #REGISTRATION COMPLETE CHECK
    subevent = SubEvents.objects.get(pk=subevent_id)
    if subevent.total_registrations==subevent.total_slots:
        messages.warning(request,"Registrations Are Complete For '{}'".format(subevent.subevent_name))
        return redirect('student-homepage')
    
    if request.method=="POST":
        form = RegistrationsGroupForm(request.POST)
        if form.is_valid():
            reg = form.save(commit=False)
            reg.user = User.objects.get(pk=int(form.cleaned_data.get('user')))
            
            try:    
                if Registrations.objects.get(user=reg.user,subevent_id=subevent_id) in list(Registrations.objects.filter(subevent_id=subevent_id)):
                    messages.warning(request,"'{}' Has Already Registered For '{}'!".format(reg.user.first_name+" "+reg.user.last_name,subevent.subevent_name))
                    return HttpResponseRedirect("/{}{}/{}/add-group/{}".format(t_views.student_hash,event_id,subevent_id,current_group_id))
            except:
                pass

            if reg.user in [r.user for r in Registrations.objects.filter(group_id=current_group_id)]:
                msg = "{} Has Already Registered for '{}'".format(reg.user.first_name+ " "+reg.user.last_name,SubEvents.objects.get(pk=subevent_id).subevent_name)
                messages.warning(request,msg)
                return HttpResponseRedirect("/{}{}/{}/add-group/{}".format(t_views.student_hash,event_id,subevent_id,current_group_id))

            reg.student_name = reg.user.first_name + " " + reg.user.last_name
            reg.student_class = form.cleaned_data.get('grade')
            reg.student_section = form.cleaned_data.get('section')
            reg.event_id = event_id
            reg.subevent_id = subevent_id
            reg.group_id = current_group_id
            reg.event_type = "G"
            reg.reg_info = form.cleaned_data.get('additional_Information')
            reg.save()

            msg = "'{}' Has Been Successfully Registered For '{}'".format(reg.user.first_name+ " "+reg.user.last_name,SubEvents.objects.get(pk=subevent_id).subevent_name) 
            messages.success(request,msg)
            return HttpResponseRedirect("/{}{}/{}/add-group/{}".format(t_views.student_hash,event_id,subevent_id,current_group_id))
        else:
            messages.warning(request,'Form Entry Error.')
            return HttpResponseRedirect("/{}{}/{}/add-group/{}/registration".format(t_views.student_hash,event_id,subevent_id,current_group_id))

    else:
        form = RegistrationsGroupForm()


    context = {
        "title": SubEvents.objects.get(pk=subevent_id).subevent_name,
        "event_name": Events.objects.get(pk=event_id).event_name,
        'form': form,
        "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
        "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,0)[0],
        "notifications_decisions":get_current_notifications_students(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'studentview/desktop/group_registration.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/group_registration.html',context)


def registration(request,event_id,subevent_id):
    t_views.login_check(request)
    
    #TEACHER CHECK
    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')        
    except:
        return redirect('login')
    
    if not t_views.event_over_check(event_id,subevent_id):
        messages.warning(request,"Event '{}' Is Already Complete!".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('student-homepage')
    
    if event_finalized_check(event_id,subevent_id):
        messages.warning(request,"Decisions Regarding Event '{}' Is Already Finalized!".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('student-homepage')
    
    if registration_deadline_passed(event_id,subevent_id):
        messages.warning(request,"Registration Deadline for '{}' Has Passed.".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
        return redirect('student-homepage')

    #REGISTRATION COMPLETE CHECK
    subevent = SubEvents.objects.get(pk=subevent_id)
    if subevent.total_registrations==subevent.total_slots:
        messages.warning(request,"Registrations Are Complete For '{}'".format(subevent.subevent_name))
        return redirect('student-homepage')

    #ALREADY REGISTERED FOR EVENT CHECK
    try:
        if Registrations.objects.get(user=User.objects.get(pk=int(request.COOKIES.get('id'))),subevent_id=subevent_id) in list(Registrations.objects.filter(subevent_id=subevent_id)):
            messages.warning(request,"You Have Already Registered For '{}'!".format(subevent.subevent_name))
            return redirect('student-homepage')
    except:
        pass
    
    if subevent.subevent_type=="I":
        if request.method=="POST":
            form = RegistrationSingleForm(request.POST)
            if form.is_valid():
                reg = form.save(commit=False)
                reg.user = User.objects.get(pk=int(request.COOKIES.get('id')))
                reg.student_name = User.objects.get(pk=int(request.COOKIES.get('id'))).first_name + " " +  User.objects.get(pk=int(request.COOKIES.get('id'))).last_name
                reg.student_class = form.cleaned_data.get('grade')
                reg.student_section = form.cleaned_data.get('section')
                reg.event_id = event_id
                reg.subevent_id = subevent_id
                reg.event_type = "I"
                reg.reg_info = form.cleaned_data.get('additional_Information')
                reg.group_id = 0
                reg.save()

                msg = "Successfully Registered For '{}'".format("{}- {}".format(Events.objects.get(pk=event_id).event_name,SubEvents.objects.get(pk=subevent_id).subevent_name) if Events.objects.get(pk=event_id).event_name!=SubEvents.objects.get(pk=subevent_id).subevent_name else "{}".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
                messages.success(request,msg)
                return redirect('student-homepage')
            else:
                messages.warning(request,'Form Entry Error.')
                return HttpResponseRedirect("{}{}/{}/registration".format(t_views.student_hash,str(event_id),str(subevent_id)))

        else:
            form = RegistrationSingleForm()
    else:
        if request.method=="POST":
            form = RegistrationsGroupForm(request.POST)
            if form.is_valid():
                reg = form.save(commit=False)
                reg.user = User.objects.get(pk=int(form.cleaned_data.get('user')))
                reg.student_name = reg.user.first_name + " " + reg.user.last_name
                reg.student_class = form.cleaned_data.get('grade')
                reg.student_section = form.cleaned_data.get('section')
                reg.event_id = event_id
                reg.subevent_id = subevent_id
                reg.event_type = "G"
                reg.reg_info = form.cleaned_data.get('additional_Information')
                reg.save()

                msg = "Successfully Registered For '{}'".format("{}- {}".format(Events.objects.get(pk=event_id).event_name,SubEvents.objects.get(pk=subevent_id).subevent_name) if Events.objects.get(pk=event_id).event_name!=SubEvents.objects.get(pk=subevent_id).subevent_name else "{}".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
                messages.success(request,msg)
                return redirect('student-homepage')
            else:
                messages.warning(request,'Form Entry Error.')
                return HttpResponseRedirect("{}{}/{}/registration".format(t_views.student_hash,str(event_id),str(subevent_id)))

        else:
            form = RegistrationSingleForm()

    context = {
        "title": SubEvents.objects.get(pk=subevent_id).subevent_name,
        "event_name": Events.objects.get(pk=event_id).event_name,
        'form': form,
        "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
        "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,0)[0],
        "notifications_decisions":get_current_notifications_students(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'studentview/desktop/registration.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/registration.html',context)

def show_all_notifications(request):
    t_views.login_check(request)
    
    try:
        if not t_views.student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')
        
    cnt,days_left,decision_received = get_current_notifications_students(request,1)

    context = {
        "title":"Notifications",
        "Days_Left": days_left,
        "Decisions_Received": decision_received,
        "notifications_days_left":get_current_notifications_students(request,0)[1][:3],
        "notification_count":"6+" if get_current_notifications_students(request,0)[0]>6 else get_current_notifications_students(request,1)[0],
        "notifications_decisions":get_current_notifications_students(request,0)[2][:3]
    }

    if get_device(request)=="pc":
        return render(request,'studentview/desktop/show_all_notifications.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/show_all_notifications.html',context)

def get_current_notifications_students(request,typ):
    '''two types
    1- Days Left to Deadline
    2- New Application
    '''
    
    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    final = []
    final2 = []
    regs = Registrations.objects.filter(user=user)

    for reg in regs:
        if t_views.event_over_check(reg.event_id,reg.subevent_id):
            s_event = SubEvents.objects.get(pk=reg.subevent_id)
            sub={}

            sub["notification_header"] = "Days Left"
            sub["event_name"] = s_event.subevent_name
            cur = date.today()
            d = s_event.subevent_dates.split(" to ")[1]
            date_obj = date(int(d.split("-")[0]),int(d.split("-")[1]),int(d.split("-")[2]))
            if typ==0:
                sub["days_left"] = "- " + str((date_obj-cur).days)
            else:
                sub["days_left"] = str((date_obj-cur).days)

            final.append(sub)

    for reg in regs:
        if t_views.event_over_check(reg.event_id,reg.subevent_id):
            if s_event.confirmation_status=="Y":
                s_event = SubEvents.objects.get(pk=reg.subevent_id)
                sub={}

                sub["decision"] = "- Accepted" if reg.reg_status=="A" else "- Rejected"
                sub["notification_header"] = "Final Decision"
                sub["reason"] = reg.rej_reason if reg.reg_status=="R" else ""
                sub["event_name"] = s_event.subevent_name
                sub["teacher_incharge"] = s_event.subevent_teacher_incharge
        
                final2.append(sub)
    

    return len(final)+len(final2),final,final2

def searchpage(request):
    t_views.login_check(request)
    
    try:
        if not t_views.student_check(request):
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
                    "url_redirect": "/{}{}/{}".format(t_views.student_hash,subevent_data.event_id, subevent_data.subevent_id),
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

    context["notifications_days_left"]=get_current_notifications_students(request,0)[1][:3]
    context["notification_count"]=get_current_notifications_students(request,0)[0]

    if get_device(request)=="pc":
        return render(request,'studentview/desktop/searchpage.html',context)
    elif get_device(request)=="mobile":
        return render(request,'studentview/mobile/searchpage.html',context)

def search(query, min_accuracy=0.5, limit=None):
    all_subevents = list(SubEvents.objects.all())
    search_results = []
    for subevent_data in all_subevents:
        if t_views.event_over_check(subevent_data.event_id,subevent_data.subevent_id):
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