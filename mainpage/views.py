from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.models import Users
from cookie_project.settings import STATICFILES_DIRS


def check_login(func):
    def inner(*args, **kwargs):
        if "userid" in args[0].session:
            return func(*args, **kwargs)
        else:
            return redirect(reverse("accounts:userlogin"))
    return inner

# Create your views here.
@check_login
def mainpage(request):
    userid = request.session.get("userid")
    user = Users.objects.get(userid=userid)

    return render(request, "mainpage_pages/mainpage.html", locals())