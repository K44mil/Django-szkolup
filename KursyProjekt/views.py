from django.shortcuts import render, redirect
from adminp.models import AdminMessage
import datetime

def register(request):
    return render(request, 'register.html', {})

def sendMessage(request):

    if request.method == 'POST':
        name = request.POST['messageAuthorName']
        email = request.POST['messageAuthorEmail']
        content = request.POST['messageContent']

        adminMessage = AdminMessage.objects.create(
            name=name,
            email=email,
            content=content,
            time=datetime.datetime.now(),
            read=False
        )

        adminMessage.save()
    return render(request, 'sent_message.html', {})

    return redirect('/')