from django.contrib import admin
from league.models import Season, Player, Doubles, Singles
# Register your models here.
admin.site.register(Season)
admin.site.register(Player)
admin.site.register(Doubles)
admin.site.register(Singles)