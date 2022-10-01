from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from accounts.models import Users, Projects
from cookie_project.settings import STATICFILES_DIRS
from userinfo.forms import registerform


def check_login(func):
    def inner(*args, **kwargs):
        if "userid" in args[0].session and Users.objects.get(userid=args[0].session.get("userid")):
            return func(*args, **kwargs)
        else:
            return redirect(reverse("accounts:userlogin"))
    return inner

@check_login
def myinfo(request):
    userid = request.session.get("userid")
    user = Users.objects.get(userid=userid)
    return render(request, "userinfo/userinformation.html", locals())

def space(request, userid):
    user = Users.objects.get(userid=userid)
    projectids = user.myprojects.split("|")[1:]
    projectlist = []
    for i in projectids:
        project = Projects.objects.get(projectid=i)
        projectlist.append(project)
    return render(request, "userinfo/userspace.html", locals())

@check_login
def editaccount(request):
    userid = request.session.get("userid")
    user = Users.objects.get(userid=userid)
    form = registerform()
    if request.method == "POST":
        form = registerform(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.username = data.get("username")
            user.password = data.get("password")
            if request.FILES.get("newprofile"):
                print("=====new profile got=====")
                newprofile = request.FILES.get("newprofile")
                with open(STATICFILES_DIRS[0] + user.profileaddress, "wb") as profile:
                    profile.write(newprofile.read())
            user.save()
            return redirect(reverse("userinfo:myinfo"))
        else:
            return render(request, "userinfo/editaccount.html", locals())
    return render(request, "userinfo/editaccount.html", locals())