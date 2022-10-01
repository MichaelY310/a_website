from django.urls import path

from displayprojects import views

app_name = "displayprojects"

urlpatterns = [
    path("project/<int:projectid>/", views.project, name="project"),
    path("<int:page>/", views.allprojects, name="allprojects"),
    path("", views.allprojects, name="allprojects"),
]