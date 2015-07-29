from django.contrib import admin
from models import Artist, ArtistDetailLine

class ArtistDetailLineInline(admin.TabularInline):
    model = ArtistDetailLine

class ArtistAdmin(admin.ModelAdmin):
    inlines = [ArtistDetailLineInline]

admin.site.register(Artist, ArtistAdmin)
admin.site.register(ArtistDetailLine)
