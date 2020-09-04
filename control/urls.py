from django.urls import path

from control import views

urlpatterns = [
    path('', views.HostList.as_view(), name='index'),
    path('host/<slug:pk>/detail', views.HostView.as_view(), name='host')
]