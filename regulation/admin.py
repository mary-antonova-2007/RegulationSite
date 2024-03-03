from django.contrib import admin
from .models import Section, Image, File
from django.forms import TextInput, Textarea
from django.db import models


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1  # Количество пустых форм для новых изображений


class FileInline(admin.TabularInline):
    model = File
    extra = 1  # Количество пустых форм для новых файлов


class SectionAdmin(admin.ModelAdmin):
    inlines = [ImageInline, FileInline]
    list_display = ('id', 'name', 'header', 'parent')
    list_display_links = ('name',)  # Делаем поле 'name' ссылкой на редактирование
    # Если нужно, можно добавить другие настройки админ-панели здесь
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


admin.site.register(Section, SectionAdmin)
admin.site.register(Image)
admin.site.register(File)
