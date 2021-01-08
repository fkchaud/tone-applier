from django.urls import path

from divine_office import views


urlpatterns = [
    path('find', views.FindLiturgy.as_view(), name='find'),
    path('', views.dummy, name='dummy'),
    # path('', views.Index.as_view(), name='index'),
]
