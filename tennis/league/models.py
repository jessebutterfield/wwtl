from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    home_phone = models.CharField(max_length=20, blank=True)
    work_phone = models.CharField(max_length=20, blank=True)
    cell_phone = models.CharField(max_length=20, blank=True)
    paper_mail = models.BooleanField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def name(self):
        return str(self.user.first_name + ' ' + self.user.last_name)

    def __str__(self):
        return self.name()


class Season(models.Model):
    year = models.IntegerField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def doubles(self):
        self.doublesA + self.doublesB

    def __str__(self):
        return f'{self.player}({self.year})'


class Divisions(models.IntegerChoices):
    HIGH_ADVANCED = 1
    ADVANCED = 2
    HIGH_INTERMEDIATE = 3
    INTERMEDIATE = 4
    LOW_INTERMEDIATE = 5
    BEGINNER = 6

    @classmethod
    def get_name(cls, index) -> str:
        for i, name in cls.choices:
            if i == index:
                return name
        return ''


class Singles(models.Model):
    player = models.ForeignKey(Season, on_delete=models.CASCADE)
    division = models.IntegerField(choices=Divisions.choices)

    def __str__(self):
        return f'{self.player} - {Divisions.get_name(self.division)}'


class Doubles(models.Model):
    playerA = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='doublesA')
    playerB = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='doublesB')
    division = models.IntegerField(choices=Divisions.choices)

    def __str__(self):
        return f'{self.playerA.player}/{self.playerB.player}({self.playerA.year}) - {Divisions.get_name(self.division)}'


class SinglesMatch(models.Model):
    home = models.ForeignKey(Singles, on_delete=models.CASCADE, related_name='home_matches')
    away = models.ForeignKey(Singles, on_delete=models.CASCADE, related_name='away_matches')

    def __str__(self):
        return f'{self.home.player} v {self.away.player}'


class DoublesMatch(models.Model):
    home = models.ForeignKey(Doubles, on_delete=models.CASCADE, related_name='home_matches')
    away = models.ForeignKey(Doubles, on_delete=models.CASCADE, related_name='away_matches')

    def __str__(self):
        return f'{self.home.playerA.player}/{self.home.playerB.player} v {self.away.playerA.player}/{self.away.playerB.player}'

class MatchSet(models.Model):
    home = models.IntegerField()
    away = models.IntegerField()
    tie_break_home = models.IntegerField()
    tie_break_away = models.IntegerField()

    class Meta:
        abstract = True


class SingleSet(MatchSet):
    match = models.ForeignKey(SinglesMatch, on_delete=models.CASCADE)


class DoubleSet(MatchSet):
    match = models.ForeignKey(DoublesMatch, on_delete=models.CASCADE)


class ScoreKeepers(models.Model):
    SINGLES = 'S'
    DOUBLES = 'D'
    MATCH_TYPE = [
        (SINGLES, 'Singles'),
        (DOUBLES, 'Doubles'),
    ]
    year = models.IntegerField()
    division = models.IntegerField(choices=Divisions.choices)
    match_type = models.CharField(
        max_length=1,
        choices=MATCH_TYPE
    )
    player = models.ForeignKey(Player, on_delete=models.RESTRICT)

    def __str__(self):
        return f'{self.get_division_display()} {self.get_match_type_display()} {self.player}'
