# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ImageHandler, Tag


@admin.register(ImageHandler)
class ImageHandlerAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'updated_at',
        'user',
        'title',
        'original_image',
    )
    list_filter = ('created_at', 'updated_at', 'user')
    raw_id_fields = ('tags',)
    date_hierarchy = 'created_at'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'tag', 'slug')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('slug',)
    date_hierarchy = 'created_at'
