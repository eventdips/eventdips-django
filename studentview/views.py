from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Registrations
from teacherview.models import Events,SubEvents,Status
from teacherview.views import login_check, student_check, student_hash, date_conversion
from django.http import HttpResponseRedirect
from django.contrib import messages
from .forms import RegistrationSingleForm, AchievementForm

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

def my_achievements(request):
    login_check(request)

    try:
        if not student_check(request):
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
    
    for i in range(list_achievements.count("")):
        list_achievements.remove("")

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

    context ={
        "achievements":final,
        "url_redirect2":"achievements/add"}
    return render(request,'studentview/my_achievements.html',context)

def add_achievement(request):
    login_check(request)

    try:
        if not student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')
    
    user = User.objects.get(pk=int(request.COOKIES.get('id')))
    status = Status.objects.get(user=user)
    achievements = status.achievements
    list_achievements = achievements[1:-1].split("666")
    list_achievements.pop(-1)
    latest_id = int(list_achievements[-1][1:-1].split(":")[-1])

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

            messages.success(request,"Achievement Has Been Successfully Edited!")
            return redirect('student-achievements')
    else:
        form = AchievementForm()

    context = {
        "form":form
    }

    return render(request,"studentview/add_achievement.html",context)


def achievements_edit(request,achievement_id):
    login_check(request)

    try:
        if not student_check(request):
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
        "title":title
    }

    return render(request,"studentview/add_achievement.html",context)

def achievements_delete(request,achievement_id):
    login_check(request)

    try:
        if not student_check(request):
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
    login_check(request)

    try:
        if not student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')

    events = list(SubEvents.objects.filter(category=category))

    final = []
    for i in events:
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
        sub["url_redirect"] = "/{}{}/{}".format(student_hash,str(i.event_id),str(i.subevent_id))
        sub["event_attachment"] = i.subevent_attachment
        final.append(sub)

    context = {"title": category,
                "subevents":final}

    return render(request, "studentview/event_by_category.html", context)

def my_applications(request):
    login_check(request)

    try:
        if not student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')
    except:
        return redirect('login')
    
    pk = int(request.COOKIES.get('id'))
    registrations = list(Registrations.objects.filter(user=User.objects.get(pk=pk)))
    final = []
    for i in registrations:
        sub = {}
        sub["event_name"] = SubEvents.objects.get(pk=i.subevent_id).subevent_name
        sub["teacher_incharge"] = SubEvents.objects.get(pk=i.subevent_id).subevent_teacher_incharge
        sub["date_applied"] = date_conversion(i.date_applied)
        if not i.reg_status:
            sub["status"] = "Pending"
        elif i.reg_status=="A":
            sub["status"] = "Accepted"
        else:
            sub["status"] = "Rejected"
        final.append(sub)


    context={
        "Registrations":final,
    }

    return render(request,'studentview/my_applications.html',context)


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
        try:        
            if Registrations.objects.get(user=User.objects.get(pk=int(request.COOKIES.get('id'))),subevent_id=subevent_id) in list(Registrations.objects.filter(subevent_id=subevent_id)):
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
                sub["my_registered_event"] = True
                sub["completed_check"] = False
                final.append(sub)
        except:
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
            sub["my_registered_event"] = False
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
    
    #TEACHER CHECK
    try:
        if not student_check(request):
            messages.warning(request,'Illegal Action Attempted!')
            return redirect('teacher-homepage')        
    except:
        return redirect('login')

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
                reg.reg_info = form.cleaned_data.get('additional_Information')
                reg.save()

                msg = "Successfully Registered For '{}'".format("{}- {}".format(Events.objects.get(pk=event_id).event_name,SubEvents.objects.get(pk=subevent_id).subevent_name) if Events.objects.get(pk=event_id).event_name!=SubEvents.objects.get(pk=subevent_id).subevent_name else "{}".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
                messages.success(request,msg)
                return redirect('student-homepage')
            else:
                messages.warning(request,'Form Entry Error.')
                return HttpResponseRedirect("{}{}/{}/registration".format(student_hash,str(event_id),str(subevent_id)))

        else:
            form = RegistrationSingleForm()
    else:
        if request.method=="POST":
            form = RegistrationSingleForm(request.POST,subevent_id)
            if form.is_valid():
                reg = form.save(commit=False)
                reg.user = User.objects.get(pk=int(request.COOKIES.get('id')))
                reg.student_name = User.objects.get(pk=int(request.COOKIES.get('id'))).first_name + " " +  User.objects.get(pk=int(request.COOKIES.get('id'))).last_name
                reg.student_class = form.cleaned_data.get('grade')
                reg.student_section = form.cleaned_data.get('section')
                reg.event_id = event_id
                reg.subevent_id = subevent_id
                reg.reg_info = form.cleaned_data.get('additional_Information')
                reg.save()

                msg = "Successfully Registered For '{}'".format("{}- {}".format(Events.objects.get(pk=event_id).event_name,SubEvents.objects.get(pk=subevent_id).subevent_name) if Events.objects.get(pk=event_id).event_name!=SubEvents.objects.get(pk=subevent_id).subevent_name else "{}".format(SubEvents.objects.get(pk=subevent_id).subevent_name))
                messages.success(request,msg)
                return redirect('student-homepage')
            else:
                messages.warning(request,'Form Entry Error.')
                return HttpResponseRedirect("{}{}/{}/registration".format(student_hash,str(event_id),str(subevent_id)))

        else:
            form = RegistrationSingleForm()

    context = {
        "title": SubEvents.objects.get(pk=subevent_id).subevent_name,
        "event_name": Events.objects.get(pk=event_id).event_name,
        'form': form
    }

    return render(request,'studentview/registration.html',context)

    



    

    
