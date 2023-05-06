from django.contrib import admin
from .models import User, EmergencyContact, Disease, Tag, Category, Article

admin.site.site_header = "Health Pilot ADMIN"
admin.site.site_title = "Health Pilot Admin Portal"
admin.site.index_title = "Wellcome to Health Pilot System Portal"


@admin.register(User)
class CommunityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]
    search_fields = ['id', 'username']
    list_filter = ['gender']

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EmergencyContact._meta.fields]

@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Disease._meta.fields]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tag._meta.fields]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Article._meta.fields]