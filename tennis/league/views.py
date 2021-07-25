import random
from collections import OrderedDict, defaultdict
from typing import Iterable, Dict, List, Tuple

from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.template import loader
from .send_emails import send_roster_emails, send_match_cards, send_doubles_match_cards, generate_singles_email, generate_doubles_email
from .models import Divisions, Doubles, DoubleSet, Singles, SingleSet, Season, ScoreKeepers, SinglesMatch, DoublesMatch


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


def prefetched_singles(year: int, division: int) -> List[Singles]:
    return Singles.objects.filter(player__year=year, division=division) \
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

@user_passes_test(lambda user: user.is_superuser)
def match_card(request, year, division):
    all_singles = prefetched_singles(year, division)
    score_keeper = ScoreKeepers.objects.get(year=year,
                                            division=division,
                                            match_type=ScoreKeepers.SINGLES)
    singles_id = request.GET.get('id')
    selected_singles = None
    if singles_id:
        for d in all_singles:
            if d.id == int(singles_id):
                selected_singles = d
    if not selected_singles:
        selected_singles = random.choice(all_singles)
    data_tuple = generate_singles_email(selected_singles, score_keeper)
    print(f"Would send to {data_tuple[4]}")
    return HttpResponse(data_tuple[2])


@user_passes_test(lambda user: user.is_superuser)
def send_singles_match_cards(request, year: int, division: int):
    score_keeper = ScoreKeepers.objects.get(year=year,
                                            division=division,
                                            match_type=ScoreKeepers.SINGLES)
    all_singles = prefetched_singles(year, division)
    send_match_cards(all_singles, score_keeper)
    return HttpResponse("ok")

def doubles_with_prefetch(year: int, division: int) -> List[Doubles]:
    return Doubles.objects.filter(playerA__year=year, division=division) \
        .prefetch_related("home_matches",
                          "home_matches__away",
                          "home_matches__away__playerA",
                          "home_matches__away__playerA__player",
                          "home_matches__away__playerA__player__user",
                          "home_matches__away__playerB",
                          "home_matches__away__playerB__player",
                          "home_matches__away__playerB__player__user",
                          "away_matches",
                          "away_matches__home",
                          "away_matches__home__playerA",
                          "away_matches__home__playerA__player",
                          "away_matches__home__playerA__player__user",
                          "away_matches",
                          "away_matches__home",
                          "away_matches__home__playerB",
                          "away_matches__home__playerB__player",
                          "away_matches__home__playerB__player__user"
                          ).all()


@user_passes_test(lambda user: user.is_superuser)
def doubles_match_card(request, year: int, division: int):
    all_doubles = doubles_with_prefetch(year, division)
    score_keeper = ScoreKeepers.objects.get(year=year,
                                            division=division,
                                            match_type=ScoreKeepers.DOUBLES)
    doubles_id = request.GET.get('id')
    selected_doubles = None
    if doubles_id:
        for d in all_doubles:
            if d.id == int(doubles_id):
                selected_doubles = d
    if not selected_doubles:
        selected_doubles = random.choice(all_doubles)
    data_tuple = generate_doubles_email(selected_doubles, score_keeper)
    print(f"Would send to {data_tuple[4]}")
    return HttpResponse(data_tuple[2])


@user_passes_test(lambda user: user.is_superuser)
def send_doubles_match_card(request, year, division):
    all_doubles = doubles_with_prefetch(year, division)
    score_keeper = ScoreKeepers.objects.get(year=year,
                                            division=division,
                                            match_type=ScoreKeepers.DOUBLES)
    send_doubles_match_cards(all_doubles, score_keeper)
    return HttpResponse('ok')


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


@login_required()
def scorer_view(request, year: int):
    if request.user.is_superuser:
        user_id = request.GET['user_id']
        score_keeper = ScoreKeepers.objects.get(player__user_id=user_id, year=year)
    else:
        try:
            score_keeper = ScoreKeepers.objects.get(player__user=request.user, year=year)
        except ScoreKeepers.DoesNotExist:
            raise PermissionDenied
    if score_keeper.match_type == ScoreKeepers.SINGLES:
        players = Singles.objects.filter(player__year=year, division=score_keeper.division).all()
    else:
        players = Doubles.objects.filter(playerA__year=year, division=score_keeper.division).all()
    template = loader.get_template('keeper_list.html')
    context = {'score_keeper': score_keeper, 'players': players}
    return HttpResponse(template.render(context, request))

@login_required()
def show_scores(request, match_type: str, team_id: int):
    if match_type == 'singles':
        team_model = Singles
        match_model = SinglesMatch
        set_model = SingleSet
    else:
        team_model = Doubles
        match_model = DoublesMatch
        set_model = DoubleSet
    us = team_model.objects.get(id=team_id)
    matches = match_model.objects.filter(Q(home_id=team_id) | Q(away_id=team_id)).all()
    all_sets = set_model.objects.filter(match__in=matches).all()
    template = loader.get_template('report_scores.html')
    opponents = {m.id: m.away if m.home_id == team_id else m.home for m in matches}
    parsed_sets = defaultdict(lambda: defaultdict(dict))
    for s in all_sets:
        set_data = {
            'us': s.home if s.match.home_id == team_id else s.away,
            'them': s.away if s.match.home_id == team_id else s.home,
            'usTB': s.tie_break_home if s.match.home_id == team_id else s.tie_break_away,
            'themTB': s.tie_break_away if s.match.home_id == team_id else s.tie_break_home
        }
        parsed_sets[s.match_id][s.set_number] = set_data
    context = {'sets': parsed_sets, 'opponents': opponents, 'us': us, 'team_id': team_id, "match_type": match_type}
    return HttpResponse(template.render(context, request))


@login_required()
def update_scores(request, match_type: str, team_id: int):
    scores = defaultdict(lambda: defaultdict(dict))
    for key, value in request.POST.items():
        if key.startswith("match"):
            split = key.split("/")
            scores[split[1]][int(split[2])][split[3]] = int(value) if value else None
    if match_type == 'singles':
        set_type = SingleSet
        team_model = Singles
    else:
        set_type = DoubleSet
        team_model = Doubles
    for match_id, set_map in scores.items():
        for set_number, score_map in set_map.items():
            if score_map['us'] is not None:
                old_set, _ = set_type.objects.get_or_create(match_id=match_id, set_number=set_number)
                if old_set.match.home_id == team_id:
                    old_set.home = score_map['us']
                    old_set.away = score_map['them']
                    old_set.tie_break_home = score_map['usTB']
                    old_set.tie_break_away = score_map['themTB']
                else:
                    old_set.home = score_map['them']
                    old_set.away = score_map['us']
                    old_set.tie_break_home = score_map['themTB']
                    old_set.tie_break_away = score_map['usTB']
                old_set.save()
            else:
                set_type.objects.filter(match_id=match_id, set_number=set_number).delete()
    team = team_model.objects.get(id=team_id)
    url = "/league/score_keeper/" + str(team.year())
    if request.user.is_superuser:
        score_keeper = ScoreKeepers.objects.get(year=team.year(), division=team.division, match_type=match_type[0].upper())
        url += "?user_id=" + str(score_keeper.player.user_id)
    return redirect(url)

