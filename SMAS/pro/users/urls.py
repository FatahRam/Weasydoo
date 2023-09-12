from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('signin', views.signin,name="signin"),
    path('profile', views.profile,name="profile"),
    path('register', views.register,name="register"),
    path('deco', views.deco,name="deco")
]