from django.contrib import admin

from models import Attachment, Comment, DuzzUser, Topic


admin.site.register(Attachment)

class CommentInline(admin.StackedInline):
    model = Comment


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'creator', 'created', 'updated')
    search_fields = ('creator__username', 'creator__full_name', 'subject')
    inlines = [CommentInline]

admin.site.register(Topic, TopicAdmin)
admin.site.register(DuzzUser)
