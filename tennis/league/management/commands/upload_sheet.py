from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import csv
from league.models import Player, Season, Divisions, Singles, Doubles
from typing import Dict


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('/Users/jessebutterfield/Downloads/roster.csv', newline='') as csvfile:
            csv_input = csv.DictReader(csvfile)
            doubles: Dict[str, Dict] = {}
            for row in csv_input:
                email = row['Email']
                first_name = row['Name'].strip()
                last_name = row['LastName'].strip()
                username = first_name.lower() + '_' + last_name.lower() if not email else email
                user, _ = User.objects.get_or_create(username=username, email=email, first_name=first_name,
                                                  last_name=last_name)
                player, _ = Player.objects.get_or_create(
                    address=row["Address"],
                    city=row["City"],
                    state=row["State"],
                    zipcode=row["Zipcode"],
                    home_phone=row["HomePhone"],
                    work_phone=row["WorkPhone"],
                    cell_phone=row["CellPhone"],
                    paper_mail=bool(row["Asked for paper"]),
                    user=user
                )
                if row["Leave or Coaching"] == 'L':
                    season, _ = Season.objects.get_or_create(player=player, year=0)
                elif row["Leave or Coaching"] == 'C':
                    Season.objects.get_or_create(player=player, year=2021)
                    season, _ = Season.objects.get_or_create(player=player, year=0)
                else:
                    season, _ = Season.objects.get_or_create(player=player, year=2021)
                if row['Singles Division']:
                    division = self.get_division(row['Singles Division'])
                    Singles.objects.get_or_create(player=season, division=division)
                if row['Doubles Partner']:
                    division_list = row['Doubles Division'].split(" | ")
                    partner_list = row['Doubles Partner'].split(" | ")
                    for i, divsion_str in enumerate(division_list):
                        name = first_name + ' ' + last_name
                        division = self.get_division(divsion_str)
                        partner = partner_list[i].strip()
                        if name in doubles and doubles[name]['division'] == division:
                            d = doubles.pop(name)
                            d['playerB'] = season
                            Doubles.objects.get_or_create(**d)
                        else:
                            doubles[partner] = {'playerA': season, 'division': division}
            for player, partner in doubles.items():
                partner_name = partner['playerA'].player.user.first_name + " " + partner['playerA'].player.user.last_name
                print(player + " | " + partner_name)


    def get_division(self, division_name: str) -> int:
        for i, name in Divisions.choices:
            if name == division_name.title():
                return i
        raise RuntimeError(f"Unknown division {division_name.title()}")