from django.contrib import admin
# from mptt.admin import MPTTModelAdmin
from gallery.models import Category, Photo

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name', )
    }
admin.site.register(Category, CategoryAdmin)

class PhotoAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name', )
    }
admin.site.register(Photo, PhotoAdmin)