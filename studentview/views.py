from django.shortcuts import render

def home(request):
	return render(request,'studentview/home.html')
