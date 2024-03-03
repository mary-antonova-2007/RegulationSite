from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'type', 'is_read', 'created_at', 'project', 'product', 'work_document')
    list_filter = ('is_read', 'type', 'created_at')
    search_fields = ('recipient__username', 'project__name', 'product__name', 'work_document__name')

    # Если требуется, можно настроить поля, доступные для редактирования
    # fields = ('recipient', 'type', 'is_read', ...)

admin.site.register(Notification, NotificationAdmin)
