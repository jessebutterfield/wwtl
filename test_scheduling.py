from collections import defaultdict
from typing import List, Set


def make_roster(league_list: List[int], num_matches: int):
    matches: List[Set[int]] = [set() for i in range(len(league_list))]
    next_match = len(league_list) - 1
    home = True
    for i in league:
        if len(matches[i]) < num_matches:
            for j in range(len(matches[i]), num_matches):
                if next_match <= i:
                    next_match = len(league_list) - 1
                print(i, next_match)
                matches[i].add(next_match)
                matches[next_match].add(i)
                next_match -= 1
                home = not home
    return matches


league_size = 15
league = list(range(league_size))
n = 0
total_matches = [[] for i in range(league_size)]
while n < 6:
    next_count = min(6-n, league_size-1)
    next_matches = make_roster(league, next_count)
    for k, m in enumerate(next_matches):
        total_matches[k].extend(m)
    n += next_count


for k, m in enumerate(total_matches):
    print(k, m)
    assert len(m) == 6
    assert k not in m
