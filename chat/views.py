from django.http import JsonResponse
from chat.models import Chat,Message
from chat.forms import MessageForm
from django.shortcuts import render
from django.db.models import Q
from user.models import User
from json import loads

def send(request,reciever_id):
    try:
        reciever = User.objects.exclude(id=request.user.id).get(id=reciever_id)
        try:
            chat = Chat.objects.get(sender=request.user,reciever=reciever)
        except:
            chat = Chat.objects.create(sender=request.user,reciever=reciever)

        form = MessageForm(loads(request.body))
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.owner = request.user
            message.save()
        else:
            return JsonResponse({'result':False,'errors':form.errors})

        return JsonResponse({'result':True,'chatId':chat.id})
    except Exception as e:
        return JsonResponse({'result':False,'error':str(e)})

def messages(request):
    context = {
        'chats':Chat.objects.filter(reciever=request.user)
    }
    return render(request,'messages/main.html',context)

def chat(request,id):
    context = {
        'chat': Chat.objects.get(id=id),
    }

    return render(request,'messages/chat.html',context)