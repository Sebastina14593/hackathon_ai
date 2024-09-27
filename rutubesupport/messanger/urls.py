from django.urls import path
from . import views

urlpatterns = [
    path('', views.requestsmenu, name="requestsmenu"),
    path('<int:pk>', views.messanger, name="messanger"),
    # path('<int:pk>', views.RequestsDetailView.as_view(), name = 'requestdetail'), # pk - primery key
]