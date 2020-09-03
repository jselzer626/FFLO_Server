from django.contrib import admin

# Register your models here.

from .models import Player, Roster, Owner

admin.site.register(Player)
admin.site.register(Owner)
admin.site.register(Roster)