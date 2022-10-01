import os

from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from accounts.models import Projects, Users
from cookie_project.settings import STATICFILES_DIRS


def project(request, projectid):
    # if not projectid:
    #     return
    project = Projects.objects.get(projectid=projectid)
    projectid = project.projectid
    pagenumber = project.pagenumber
    creatorid = project.creatorid
    creator = Users.objects.get(userid=creatorid)
    title = project.title
    description = project.description
    pages = [["", ""] for i in range(pagenumber)]
    basedir = STATICFILES_DIRS[0] + "/"
    cover = "/projects/" + str(projectid) + "/cover.png"
    for i in range(pagenumber):
        textfile = "projects/" + str(projectid) + "/" + str(i) + ".txt"
        picturefile = "projects/" + str(projectid) + "/" + str(i) + ".png"
        if os.path.exists(basedir + textfile):
            with open(basedir + textfile) as f:
                pages[i][0] = f.read()
        if os.path.exists(basedir + picturefile):
            pages[i][1] = picturefile
    return render(request, "displayprojects/project.html", locals())


def allprojects(request, page=1):
    projects = Projects.objects.all()
    paginator = Paginator(projects, 3)
    pager = paginator.page(page)
    return render(request, "displayprojects/allprojects.html", locals())
