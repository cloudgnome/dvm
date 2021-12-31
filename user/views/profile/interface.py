from django.shortcuts import render

def interface(request):
    return render(request,'user/profile/interface.html')