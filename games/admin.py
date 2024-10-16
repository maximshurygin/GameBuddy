from django.contrib import admin

from games.models import Game, BuddyRequest

# Register your models here.


admin.site.register(Game)

admin.site.register(BuddyRequest)
