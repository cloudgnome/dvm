from django.shortcuts import render

def main(request):
    return render(request,'user/profile/main.html')