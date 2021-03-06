from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path(r'singles/<int:year>', views.singles_roster),
    path(r'doubles/<int:year>', views.doubles_roster),
    path(r'roster_preview/<int:year>/<int:player_id>', views.preview_roster_email),
    path(r'test_email/<int:year>/<int:player_id>', views.send_test_email),
    path(r'roster/<int:year>', views.roster),
    path(r'send_season_emails/<int:year>', views.send_season_emails),
    path(r'singles_match_card/<int:year>/division/<int:division>', views.match_card),
    path(r'send_singles_match_card/<int:year>/division/<int:division>', views.send_singles_match_cards),
    path(r'doubles_match_card/<int:year>/division/<int:division>', views.doubles_match_card),
    path(r'send_doubles_match_card/<int:year>/division/<int:division>', views.send_doubles_match_card),
    path(r'score_keeper/<int:year>', views.scorer_view, name="score_keeper"),
    path(r'<str:match_type>/scores/<int:team_id>', views.show_scores, name="show_scores"),
    path(r'<str:match_type>/report_scores/<int:team_id>', views.update_scores, name="report_scores"),
    path(r'<str:match_type>/<int:year>/division/<int:division>/results', views.season_results, name="season_results"),
    path(r'new_season/<int:year>', views.new_season, name="new_season"),
    path(r'sign_up/<int:year>/players/<int:player_id>', views.sign_up, name="sign_up"),
    path(r'players', views.create_player, name="create_player"),

]
