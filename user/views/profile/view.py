from django.shortcuts import render

def view(request):
    return render(request,'user/profile/view.html')