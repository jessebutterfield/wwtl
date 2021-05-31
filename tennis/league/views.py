from collections import OrderedDict
from typing import Iterable, Dict, List

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.template import loader
from .send_emails import send_roster_emails, send_match_cards

from .models import Divisions, Doubles, Singles, Season, SinglesMatch, ScoreKeepers


def singles_roster(request, year):
    players: Iterable[Singles] = Singles.objects.filter(player__year=year).all()
    singles = group_by_division(players)
    coaching: Iterable[Season] = Season.objects.filter(year=year, singles__isnull=True, doublesA__isnull=True, doublesB__isnull=True).all()
    template = loader.get_template('singles_roster.html')
    context = {'divisions': singles, 'coaching': coaching}
    return HttpResponse(template.render(context, request))


def doubles_roster(request, year):
    teams: Iterable[Doubles] = Doubles.objects.filter(playerA__year=year).all()
    doubles = group_by_division(teams)
    template = loader.get_template('doubles_roster.html')
    context = {'divisions': doubles}
    return HttpResponse(template.render(context, request))

def group_by_division(players):
    divisions: Dict[int, Dict] = OrderedDict()
    for i, name in Divisions.choices:
        divisions[i] = {'name': name, 'list': []}
    for player in players:
        divisions[player.division]['list'].append(player)
    return divisions


def roster(request, year):
    players: Iterable[Singles] = Singles.objects.filter(player__year=year).order_by('player__player__user__last_name').all()
    singles = group_by_division(players)
    teams: Iterable[Doubles] = Doubles.objects.filter(playerA__year=year).order_by('playerA__player__user__last_name').all()
    doubles = group_by_division(teams)
    template = loader.get_template('roster.html')
    context = {'doubles': doubles, 'singles': singles, 'year': year}
    return HttpResponse(template.render(context, request))


@user_passes_test(lambda user: user.is_superuser)
def match_card(request, year, division):
    all_singles = Singles.objects.filter(player__year=year, division=division)\
        .prefetch_related("home_matches",
                           "home_matches__away",
                           "home_matches__away__player",
                           "home_matches__away__player__player",
                           "home_matches__away__player__player__user",
                           "away_matches",
                           "away_matches__home",
                           "away_matches__home__player",
                           "away_matches__home__player__player",
                           "away_matches__home__player__player__user"
                           ).all()
    singles: Singles = all_singles[0]
    home_matches = singles.home_matches.all()
    away_matches = singles.away_matches.all()
    opponents = [m.away for m in home_matches] + [m.home for m in away_matches]
    score_keeper = ScoreKeepers.objects.get(year=singles.player.year,
                                            division=division,
                                            match_type=ScoreKeepers.SINGLES)
    context = {"opponents": opponents, "singles": singles, "score_keeper": score_keeper}
    template = loader.get_template('singles_match_card.html')
    return HttpResponse(template.render(context, request))


@user_passes_test(lambda user: user.is_superuser)
def send_singles_match_cards(request, year: int, division: int):
    score_keeper = ScoreKeepers.objects.get(year=year,
                                            division=division,
                                            match_type=ScoreKeepers.SINGLES)
    all_singles: List[Singles] = Singles.objects.filter(player__year=year, division=division) \
        .prefetch_related("home_matches",
                          "home_matches__away",
                          "home_matches__away__player",
                          "home_matches__away__player__player",
                          "home_matches__away__player__player__user",
                          "away_matches",
                          "away_matches__home",
                          "away_matches__home__player",
                          "away_matches__home__player__player",
                          "away_matches__home__player__player__user"
                          ).all()
    send_match_cards(all_singles, score_keeper)
    return HttpResponse("ok")


@user_passes_test(lambda user: user.is_superuser)
def check_emails(request, year: int):
    seasons = Season.objects.filter(year=year).exclude(player__user__email='').all()
    emails = "<br/>".join([s.player.user.email for s in seasons])
    return HttpResponse(f'{len(seasons)} {emails}')


@user_passes_test(lambda user: user.is_superuser)
def preview_roster_email(request, year, player_id):
    season = Season.objects.get(year=year, player_id=player_id)
    template = loader.get_template('roster_email.html')
    context = {'season': season, 'year': year}
    return HttpResponse(template.render(context, request))


@user_passes_test(lambda user: user.is_superuser)
def send_test_email(request, year, player_id):
    season: Season = Season.objects.get(year=year, player_id=player_id)
    send_roster_emails(year, [season])
    return HttpResponse("ok")


@user_passes_test(lambda user: user.is_superuser)
def send_season_emails(request, year):
    seasons: Iterable[Season] = Season.objects.filter(year=year).exclude(player__user__email='').all()
    send_roster_emails(year, seasons)
    return HttpResponse("ok")


