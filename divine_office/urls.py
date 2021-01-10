from django.urls import path

from divine_office import views


urlpatterns = [
    path('find', views.FindLiturgy.as_view(), name='find-liturgy'),
    path('show', views.ShowLiturgyView.as_view(), name='show-liturgy'),
    path('', views.dummy, name='dummy'),
    # path('', views.Index.as_view(), name='index'),
]
