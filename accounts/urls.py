from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("userregister/", views.userregister, name="userregister"),
    path("userlogin/", views.userlogin, name="userlogin"),
    path("activate/<token>/", views.activate, name="activate"),
    path("logout/", views.logout, name="logout"),
]