from django.urls import path

from userinfo import views

app_name="userinfo"

urlpatterns = [
    path("myinfo/", views.myinfo, name="myinfo"),
    path("space/<int:userid>/", views.space, name="space"),
    path("editaccount/", views.editaccount, name="editaccount"),
]