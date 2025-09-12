from django.contrib import admin
from .models import Team, Criteria, Score

# Register your models here.
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_total_score')
    search_fields = ('name',)

@admin.register(Criteria)
class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('judge', 'team', 'criteria', 'score', 'created_at')
    list_filter = ('judge', 'team', 'criteria')
    search_fields = ('judge__username', 'team__name', 'criteria__name')
