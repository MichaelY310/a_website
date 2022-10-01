from django.urls import path

from post import views

app_name = "post"

urlpatterns = [
    path("postproject/", views.postproject, name="postproject"),
    path("postsuccessful/<str:projectid>", views.postsuccessful, name="postsuccessful"),
]