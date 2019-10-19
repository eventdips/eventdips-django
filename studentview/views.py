from django.shortcuts import render

def home(request):
	return render(request,'studentview/home.html')

def profile(request):
	return render(request,'studentview/myProfile.html')
