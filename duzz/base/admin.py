from django.contrib import admin

from models import Comment, DuzzUser, Topic


class CommentInline(admin.StackedInline):
    model = Comment


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated')
    inlines = [CommentInline]

admin.site.register(Topic, TopicAdmin)
admin.site.register(DuzzUser)
