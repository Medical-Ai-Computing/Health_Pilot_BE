from django.contrib import admin
from .models import User

admin.site.site_header = "Health Pilot ADMIN"
admin.site.site_title = "Health Pilot Admin Portal"
admin.site.index_title = "Wellcome to Health Pilot System Portal"


@admin.register(User)
class CommunityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]
    search_fields = ['id', 'username']
    list_filter = ['gender']