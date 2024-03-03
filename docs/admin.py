from django.contrib import admin
from .models import Project, Product, WorkDocument, DocumentType, Room
from django import forms


class ProductInlineForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),  # Устанавливает размер поля
        }
# Опционально: настройка отображения моделей в админ-панели
class ProductInline(admin.TabularInline):
    model = Product
    form = ProductInlineForm
    extra = 1


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'room':
            if request._obj_ is not None:
                kwargs['queryset'] = Room.objects.filter(project=request._obj_)
            else:
                kwargs['queryset'] = Room.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class RoomInline(admin.TabularInline):  # or admin.StackedInline for a different layout
    model = Room
    extra = 1  # Specifies how many extra forms to display


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'project_manager', 'project_designer')
    search_fields = ('name', 'designation')
    inlines = [RoomInline, ProductInline]

    def get_form(self, request, obj=None, **kwargs):
        # Сохраняем объект для использования в ProductInline
        request._obj_ = obj
        return super(ProjectAdmin, self).get_form(request, obj, **kwargs)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'room', 'project', 'product_designer')
    search_fields = ('name', 'designation', 'room')

class WorkDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'document_type', 'product', 'project', 'isArchived', 'created_at', )
    search_fields = ('name',)

class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'isSingleton')
    search_fields = ('name',)

class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('project', 'room_name', 'room_designation')
    search_fields = ('room_name', 'room_designation')




# Регистрация моделей
admin.site.register(Project, ProjectAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(WorkDocument, WorkDocumentAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(Room, RoomTypeAdmin)