from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path(r'singles/<int:year>', views.singles_roster),
    path(r'doubles/<int:year>', views.doubles_roster),
    path(r'roster_preview/<int:year>/<int:player_id>', views.preview_roster_email),
    path(r'test_email/<int:year>/<int:player_id>', views.send_test_email),
    path(r'roster/<int:year>', views.roster),
    path(r'send_season_emails/<int:year>', views.send_season_emails)
]
