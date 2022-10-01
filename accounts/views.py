import os

from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse

from accounts.forms import registerform
from accounts.models import Users
from accounts.util import token_confirm
from cookie_project.settings import EMAIL_HOST_USER, STATICFILES_DIRS


def userregister(request):
    if request.method == "POST":
        form = registerform(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data.pop('confirm')
            data.pop('captcha')
            user = Users.objects.create_user(**data)
            user.myprojects = ""
            user.save()
            token = token_confirm.generate_validate_token(user.userid)
            url = "http://" + request.get_host() + reverse('accounts:activate', kwargs={'token': token})
            html = loader.get_template('accounts_pages/activatetemplate.html').render({'url': url})
            send_mail('activate your account', '', EMAIL_HOST_USER, [request.POST.get("email")], html_message=html)
            return HttpResponse('message send successfully, please check it')
        else:
            return render(request, 'accounts_pages/userregister.html', {'form': form})

    form = registerform()
    return render(request, 'accounts_pages/userregister.html', {'form': form})

def activate(request, token):
    try:
        userid = token_confirm.confirm_validate_token(token)
    except:
        userid = token_confirm.remove_validate_token(token)
        user = Users.objects.all(userid=userid)
        user.delete()
        user.save()
        return HttpResponse("Page expired. Please register again.")

    try:
        user = Users.objects.get(userid=userid)
    except Users.DoesNotExist:
        return HttpResponse("User doesn't exist.")
    user.is_active = 1
    user.profileaddress = "\\users\\" + str(userid) + "\\profile.png"
    copied = STATICFILES_DIRS[0] + "\defaultprofile.png"
    target = STATICFILES_DIRS[0] + user.profileaddress
    os.system("copy " + copied + " " + target)
    user.save()
    return render(request, "accounts_pages/activatesuccess.html")

def userlogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            request.session.flush()
            request.session['userid'] = user.userid
            return redirect(reverse('mainpage:mainpage'))
        else:
            return render(request, 'accounts_pages/userlogin.html', {"msg":"wrong username or password"})
    return render(request, 'accounts_pages/userlogin.html')


def logout(request):
    request.session.flush()
    return redirect(reverse("accounts:userlogin"))