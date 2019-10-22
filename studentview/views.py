from django.shortcuts import render
from django.contrib.auth.models import User
from teacherview.models import Status

def home(request):
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