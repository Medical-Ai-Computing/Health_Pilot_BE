from django.contrib import admin
from .models import User, EmergencyContact, Disease, Tag, Category, Article, Medication, Language_Preference, \
                    PatientDoctor, Membership, Payment, UserProfile, HealthAssessmentSection  # Rating_Review

admin.site.site_header = "Health Pilot ADMIN"
admin.site.site_title = "Health Pilot Admin Portal"
admin.site.index_title = "Wellcome to Health Pilot System Portal"


@admin.register(User)
class CommunityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields]
    search_fields = ['id', 'username']
    list_filter = ['gender']

@admin.register(UserProfile)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields]

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

@admin.register(PatientDoctor)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PatientDoctor._meta.fields]

@admin.register(Payment)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Payment._meta.fields]

@admin.register(Membership)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Membership._meta.fields]

@admin.register(HealthAssessmentSection)
class HealthAssessmentSectionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HealthAssessmentSection._meta.fields]

@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Medication._meta.fields]

@admin.register(Language_Preference)
class LanguageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Language_Preference._meta.fields]
    
# @admin.register(Rating_Review)
# class RatingAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Rating_Review._meta.fields]