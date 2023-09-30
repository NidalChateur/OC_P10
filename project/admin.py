from django.contrib import admin

from project.models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "name")


admin.site.register(Project, ProjectAdmin)


class ContributorAdmin(admin.ModelAdmin):
    list_display = ("id", "contributor", "project")


admin.site.register(Contributor, ContributorAdmin)


class IssuerAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "name", "project")


admin.site.register(Issue, IssuerAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "issue")


admin.site.register(Comment, CommentAdmin)
