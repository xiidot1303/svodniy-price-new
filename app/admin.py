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



class OpeatorInline(admin.TabularInline):
    model = Operator
    list_display = ['name', 'tg_id']


class ProviderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'tg_id']
    inlines = [OpeatorInline]

class InfoAdmin(admin.ModelAdmin):
    list_display = ['about_ru', 'about_uz', 'site', 'edit_button']
    list_display_links = ['edit_button']
    def edit_button(self, obj):
        change_url = reverse('admin:app_info_change', args=[obj.id])
        return format_html('<a class="btn btn-primary" href="{}"><i class="fas fa-edit"></i> Редактировать</a>', change_url)
    edit_button.short_description = 'Действие'

class ExcelAdmin(admin.ModelAdmin):
    list_display = ['file', 'published', 'type', 'status', 'error']
    list_display_links = None
    list_filter = ['type']

    fieldsets = (
        ('', {
            'fields': ['file', 'type'],
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

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # readonly_fields = ['title', 'title_en', 'provider_name', 'price', 'count']
    verbose_name = 'Продукт'
    verbose_name_plural = 'Продукты'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['bot_user', 'payment_method', 'total_amount', 'datetime', 'sent_to_provider', 'open_button']
    inlines = [OrderItemInline]

    def open_button(self, obj):
        change_url = reverse('admin:app_order_change', args=[obj.id])
        return format_html('<a class="btn btn-primary" href="{}"><i class="fas fa-eye"></i></a>', change_url)
    open_button.short_description = 'Действие'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "order_bot_user_name", "title", "price", 
                    "manufacturer", "country", "count", "provider_name", "order_datetime"]
    list_filter = ["order", "order__bot_user__name", "title", "provider_name"]
    verbose_name = "Заказ"
    verbose_name_plural = "Заказы"

    
    def order_bot_user_name(self, obj):
        return obj.order.bot_user.name
    order_bot_user_name.short_description = "Заказчик"
    order_bot_user_name.admin_order_field = "order__bot_user__name"
    
    def order_datetime(self, obj):
        return obj.order.datetime
    order_datetime.short_description = "Дата"
    order_datetime.admin_order_field = "order__datetime"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("order")

# admin.site.register(Language, LanguageAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(Provider, ProviderAdmin)
admin.site.register(Info, InfoAdmin)
admin.site.register(Excel, ExcelAdmin)
admin.site.register(Usage, UsageAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
