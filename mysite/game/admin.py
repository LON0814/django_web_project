from django.contrib import admin
from .models import Game, Genre_list
from embed_video.admin import AdminVideoMixin

class GameAdmin(AdminVideoMixin, admin.ModelAdmin):
    list_display = ('title', 'video')


admin.site.register(Game, GameAdmin)
admin.site.register(Genre_list)

