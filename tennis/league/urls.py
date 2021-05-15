from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path(r'singles/<int:year>', views.singles_roster),
    path(r'doubles/<int:year>', views.doubles_roster),
]
