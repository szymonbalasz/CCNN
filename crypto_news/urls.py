from django.urls import path
from . import views
from . import viewsAuth

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', viewsAuth.loginUser, name="login"),
    path('logout/',  viewsAuth.logoutUser, name="logout"),
    path('register/', viewsAuth.registerUser, name="register"),
    path('editProfile/', viewsAuth.editProfile, name="editProfile"),
    path('changePassword/', viewsAuth.changePassword, name="changePassword"),
]