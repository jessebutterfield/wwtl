from django.contrib import admin
from league.models import Season, Player, Doubles, Singles

admin.site.register(Season)
admin.site.register(Player)


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