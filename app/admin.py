from django.contrib import admin
from app.models import *
from app.forms import *
from django import forms
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect

class LanguageAdmin(admin.ModelAdmin):
    list_display = ['user_ip', 'lang']

class DrugAdmin(admin.ModelAdmin):
    list_display = ['title', 'title_en', 'price', 'provider_name', 'published', 'edit_button']
    list_filter = ['title', 'title_en', 'provider_name']
    search_fields = ['title']
    list_display_links = ['edit_button']

    def edit_button(self, obj):
        change_url = reverse('admin:app_drug_change', args=[obj.id])
        return format_html('<a class="btn btn-primary" href="{}"><i class="fas fa-edit"></i></a>', change_url)
    edit_button.short_description = 'Действие'

class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address']

class InfoAdmin(admin.ModelAdmin):
    list_display = ['about_ru', 'about_uz', 'site', 'edit_button']
    list_display_links = ['edit_button']
    def edit_button(self, obj):
        change_url = reverse('admin:app_info_change', args=[obj.id])
        return format_html('<a class="btn btn-primary" href="{}"><i class="fas fa-edit"></i> Редактировать</a>', change_url)
    edit_button.short_description = 'Действие'

class ExcelAdmin(admin.ModelAdmin):
    list_display = ['file', 'published', 'status', 'error']
    list_display_links = None

    fieldsets = (
        ('', {
            'fields': ['file'],
        }),
    )

    # def edit_button(self, obj):
    #     change_url = reverse('admin:app_excel_change', args=[obj.id])
    #     return format_html('<a class="btn btn-primary" href="{}"><i class="fas fa-edit"></i> Редактировать</a>', change_url)
    # edit_button.short_description = 'Действие'

class UsageAdmin(admin.ModelAdmin):
    list_display = ['bot_user', 'drug_title', 'lang', 'datetime']
    def changelist_view(self, request, extra_context=None):
        return redirect('usage_rate')

# admin.site.register(Language, LanguageAdmin)
admin.site.register(Drug, DrugAdmin)
# admin.site.register(Provider, ProviderAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(Excel, ExcelAdmin)
admin.site.register(Usage, UsageAdmin)
