from django.shortcuts import render
from user.forms import BusinessForm

def business(request):
    if request.POST:
        form = BusinessForm(request.POST,instance=request.user.business if hasattr(request.user,'business') else None)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = request.user
            business.save()

        context = {'form':form}

    else:
        context = {
            'form': BusinessForm(instance=request.user.business if hasattr(request.user,'business') else None)
        }

    return render(request,'user/profile/business.html',context)