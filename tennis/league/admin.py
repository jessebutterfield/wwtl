from django.contrib import admin
from league.models import Season, Player, Doubles, Singles, SinglesMatch, DoublesMatch, ScoreKeepers

admin.site.register(Season)
admin.site.register(SinglesMatch)
admin.site.register(DoublesMatch)
admin.site.register(ScoreKeepers)


class PlayerAdmin(admin.ModelAdmin):
    ordering = ['user__last_name', 'user__first_name']
    search_fields = ['user__first_name', 'user__last_name']
    list_filter = ['paper_mail']
    list_display = ['name', 'cell_phone', 'home_phone', 'work_phone']


admin.site.register(Player, PlayerAdmin)


class SinglesAdmin(admin.ModelAdmin):
    ordering = ['division', 'player__player__user__last_name', 'player__player__user__first_name']
    search_fields = ['player__player__user__first_name', 'player__player__user__last_name']
    list_filter = ['player__year']


admin.site.register(Singles, SinglesAdmin)


class DoublesAdmin(admin.ModelAdmin):
    ordering = ['division', 'playerA__player__user__last_name', 'playerA__player__user__first_name']
    search_fields = [
        'playerA__player__user__first_name',
        'playerA__player__user__last_name',
        'playerB__player__user__first_name',
        'playerB__player__user__last_name'
    ]
    list_filter = ['playerA__year']


admin.site.register(Doubles, DoublesAdmin)

class SinglesMatchAdmin(admin.ModelAdmin):
    ordering = ['home__division']
    list_filter = ['home__division', 'home__year']
