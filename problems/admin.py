from django.contrib import admin

from problems.models import Problem, Test, Score

class ProblemAdmin(admin.ModelAdmin):
    prepopulated_fields = {"name_slug": ("name",)} 
    list_display = ('name', 'difficulty')
    list_filter = ['difficulty',]
    ordering = ('name',)


class TestAdmin(admin.ModelAdmin):
    list_filter = ['problem',]
    ordering = ('problem',)


class ScoreAdmin(admin.ModelAdmin):
    list_display = ( '__str__', 'problem',)
    list_filter = ['problem', 'user',]
    ordering = ('problem',)


admin.site.register(Problem, ProblemAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Score, ScoreAdmin)
