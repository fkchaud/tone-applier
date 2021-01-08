from django.urls import path

from divine_office import views


urlpatterns = [
    path('', views.index, name='index'),
]
