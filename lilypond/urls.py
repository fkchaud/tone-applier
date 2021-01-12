from django.urls import path

from divine_office.views import dummy
from lilypond import views


urlpatterns = [
    path('apply', views.ApplyToTextView.as_view(), name='apply-to-text'),
    path('', dummy, name='dummy2'),
]
