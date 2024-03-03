from django.contrib import admin
from django.forms import models

from .models import Task, Comment


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'product', 'status', 'start_date', 'deadline')
    list_filter = ('status', 'project', 'product')
    search_fields = ('name', 'description')
    raw_id_fields = ('responsible',)
    filter_horizontal = ('subscribers', 'predecessors',)
    date_hierarchy = 'start_date'




class CommentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'created_at')
    search_fields = ('comment',)
    date_hierarchy = 'created_at'

# Регистрация моделей
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)
