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

    def __str__(self):
        return str(self.user.first_name + ' ' + self.user.last_name)


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
