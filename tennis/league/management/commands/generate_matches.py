from django.core.management.base import BaseCommand, CommandError
from league.models import Singles, Doubles, SinglesMatch, DoublesMatch
from collections import defaultdict
from typing import List, Set
import random


class Command(BaseCommand):
    help = 'Generates a season of matches'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)

    def handle(self, *args, **options):
        year: int = options['year']
        SinglesMatch.objects.filter(home__player__year=year).delete()
        DoublesMatch.objects.filter(home__playerA__year=year).delete()
        singles = list(Singles.objects.filter(player__year=year).all())
        singles_by_division = defaultdict(list)
        for s in singles:
            singles_by_division[s.division].append(s)
        for d, player_list in singles_by_division.items():
            matches = self.generate_league(len(player_list))
            for i, match_list in enumerate(matches):
                assert len(match_list) == 6
                assert i not in match_list
            random.shuffle(player_list)
            for i, match_list in enumerate(matches):
                home_player = player_list[i]
                for match in match_list:
                    if match < i:
                        SinglesMatch.objects.create(home=home_player, away=player_list[match])
        doubles = list(Doubles.objects.filter(playerA__year=year).all())
        doubles_by_division = defaultdict(list)
        for d in doubles:
            doubles_by_division[d.division].append(d)
        for d, player_list in doubles_by_division.items():
            matches = self.generate_league(len(player_list))
            for i, match_list in enumerate(matches):
                assert len(match_list) == 6
                assert i not in match_list
            random.shuffle(player_list)
            for i, match_list in enumerate(matches):
                home_player = player_list[i]
                for match in match_list:
                    if match < i:
                        DoublesMatch.objects.create(home=home_player, away=player_list[match])

    def make_roster(self, league_list: List[int], num_matches: int):
        matches: List[Set[int]] = [set() for i in range(len(league_list))]
        next_match = len(league_list) - 1
        home = True
        for i in league_list:
            if len(matches[i]) < num_matches:
                for j in range(len(matches[i]), num_matches):
                    if next_match <= i:
                        next_match = len(league_list) - 1
                    matches[i].add(next_match)
                    matches[next_match].add(i)
                    next_match -= 1
                    home = not home
        return matches

    def generate_league(self, league_size: int) -> List[List[int]]:
        league = list(range(league_size))
        n = 0
        total_matches = [[] for i in range(league_size)]
        while n < 6:
            next_count = min(6 - n, league_size - 1)
            next_matches = self.make_roster(league, next_count)
            for k, m in enumerate(next_matches):
                total_matches[k].extend(m)
            n += next_count
        return total_matches
