from django.contrib import admin
from study.models import Subject, AccessSubjectGroup, Part, UsefulLink

# Register your models here.
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'description',)


@admin.register(AccessSubjectGroup)
class AccessSubjectGroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'user')
    list_filter = ('subject', 'user',)
    search_fields = ('subject', 'user',)


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'subject', 'title')
    list_filter = ('subject', )
    # list_filter = ('subject', 'title', 'description', 'content')
    search_fields = ('subject', 'title', 'description', 'content', )


@admin.register(UsefulLink)
class UsefulLinkAdmin(admin.ModelAdmin):
    list_display = ('pk', 'part', 'title')
    list_filter = ('part', )
    search_fields = ('part', 'title', 'description', )