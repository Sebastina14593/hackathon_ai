from django.urls import path
from . import views
import messanger

urlpatterns = [
    path('', views.index, name="home"), # не надо указывать круглых скобок (т.к. нужно лишь обратиться к нему без его выполнения)
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name="logout")
]