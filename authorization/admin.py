from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'user_folder')  # Укажите поля, которые вы хотите видеть в админке
    search_fields = ('user__username', 'birth_date')  # Поля для поиска
    # Вы можете добавить другие опции, такие как list_filter, ordering и т.д.

admin.site.register(Profile, ProfileAdmin)