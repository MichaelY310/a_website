import datetime
import os
from datetime import date

from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from accounts.models import Users, Projects
from cookie_project.settings import STATICFILES_DIRS
from post.forms import registerform


def postproject(request):
    userid = request.session.get("userid")
    user = Users.objects.get(userid=userid)
    username = user.username
    form = registerform()
    if request.method == "POST":
        form = registerform(request.POST)
        if not form.is_valid():
            return render(request, "post/postproject.html", locals())
        # 获取除了文字和图片以外的信息
        creatorid = userid
        createtime = datetime.datetime.now()
        title = request.POST.get("title")
        description = request.POST.get("description")
        pagenumber = int(request.POST.get("pagecount"))

        # 通过这些信息创建project
        project = Projects.objects.create(creatorid=creatorid, createtime=createtime, title=title, description=description, pagenumber=pagenumber)

        # 获取生成出来的projectid， 用它来创建project的文件夹
        projectid = project.projectid

        # 获取当前用户，即创建者的id
        myprojects = user.myprojects
        # 在后面加上projectid
        myprojects += "|" + str(projectid)
        user.myprojects = myprojects
        user.save()

        # 创建文件夹
        filesdir = STATICFILES_DIRS[0] + "\\projects\\" + str(projectid)
        os.mkdir(filesdir)

        # 计算非空的page的数量，之后放进project当中
        truepagenumber = 0
        for i in range(pagenumber):
            detailtext = request.POST.get("t"+str(i))
            picture = request.FILES.get(str(i))
            # 如果 text 和 picture 都没有，那么就跳过
            if not detailtext and not picture:
                continue
            if detailtext:
                with open(filesdir+"/"+str(truepagenumber)+".txt", "w") as container:
                    container.write(detailtext)
            if picture:
                with open(filesdir+"/"+str(truepagenumber)+".png", "wb") as container:
                    container.write(picture.read())
            truepagenumber += 1
        project.pagenumber = truepagenumber

        # 保存封面
        if request.FILES.get("cover"):
            cover = request.FILES.get("cover")
            with open(filesdir + "/cover.png", "wb") as c:
                c.write(cover.read())
        elif request.FILES.get("0"):
            copied = filesdir + "\\0.png"
            target = filesdir + "\cover.png"
            os.system("copy " + copied + " " + target)
        else:
            copied = STATICFILES_DIRS[0] + "\defaultcover.png"
            target = filesdir + "\cover.png"
            os.system("copy " + copied + " " + target)

        # 保存封面地址
        project.coveraddress = "\\projects\\" + str(projectid) + "\\cover.png"

        project.save()
        return redirect(reverse("post:postsuccessful", kwargs={"projectid": str(project.projectid)}))

    return render(request, "post/postproject.html", locals())


def postsuccessful(request, projectid=0):
    if projectid == 0:
        return redirect(reverse("mainpage:mainpage"))
    return render(request, "post/postsuccessful.html", {"projectid":str(projectid)})