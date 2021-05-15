from collections import OrderedDict
from typing import Iterable, Dict

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.template import loader

from .models import Divisions, Doubles, Singles, Season


@user_passes_test(lambda user: user.is_superuser)
def singles_roster(request, year):
    players: Iterable[Singles] = Singles.objects.filter(player__year=year).all()
    divisions: Dict[int, Dict] = OrderedDict()
    for i, name in Divisions.choices:
        divisions[i] = {'name': name, 'list': []}
    for player in players:
        divisions[player.division]['list'].append(player)
    coaching: Iterable[Season] = Season.objects.filter(year=year, singles__isnull=True, a_players__isnull=True, b_players__isnull=True).all()
    template = loader.get_template('singles_roster.html')
    context = {'divisions': divisions, 'coaching': coaching}
    return HttpResponse(template.render(context, request))


@user_passes_test(lambda user: user.is_superuser)
def doubles_roster(request, year):
    teams: Iterable[Singles] = Doubles.objects.filter(playerA__year=year).all()
    divisions: Dict[int, Dict] = OrderedDict()
    for i, name in Divisions.choices:
        divisions[i] = {'name': name, 'list': []}
    for player in teams:
        divisions[player.division]['list'].append(player)
    template = loader.get_template('doubles_roster.html')
    context = {'divisions': divisions}
    return HttpResponse(template.render(context, request))
