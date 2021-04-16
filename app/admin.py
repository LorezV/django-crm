from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .import models
from django.urls import reverse_lazy

admin.site.site_url = reverse_lazy('index')

# Register your models here.
@admin.register(models.User)
class UserAdmin(UserAdmin):
    readonly_fields = ('date_joined',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disables_fields = set()
        if not is_superuser:
            disables_fields |= {
                'username',
                'is_superuser',
                'user_permissions'
            }
        if (not is_superuser and obj is not None and obj == request.user):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }
        for f in disables_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form

@admin.register(models.Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'client_name', 'create_date', 'closing_date', 'comment')
    readonly_fields = ('create_date', 'closing_date')

@admin.register(models.TelegramProfile)
class MasterAdmin(ModelAdmin):
    readonly_fields = ('telegram_chat_id', )

@admin.register(models.City)
class OrderAdmin(ModelAdmin):
    list_display = ('title', )