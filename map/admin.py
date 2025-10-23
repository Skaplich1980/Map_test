from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from .models import *

class PhotoInline(SortableTabularInline): # SortableTabularInline класс для перетаскивания
    """
    Встроенное редактирование фотографий прямо на странице Place.
    Показывает превью и позволяет менять порядок.
    """
    model = Photo
    extra = 1
    fields = ("preview", "image",)
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "—"
    preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    """
    Админка для мест:
    - список с названием и координатами
    - поиск по названию
    - inline‑фотографии
    """
    list_display = ("title", "latitude", "longitude", "short_desc")
    search_fields = ("title", "short_desc", "long_desc")
    inlines = [PhotoInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """
    Админка для фотографий:
    - превью картинки
    - сортировка по order
    """
    list_display = ("id", "place", "order", "preview")
    list_filter = ("place",)
    ordering = ("place", "order")
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image and hasattr(obj.image, "url"):
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "—"
    preview.short_description = "Превью"