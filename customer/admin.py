
# Register your models here.
from datetime import datetime
from django.contrib import admin
from customer.models import Customer
from django.utils.html import format_html


def change_public_day(modeladmin, request, queryset):
    queryset.update(public_day=datetime.now())


change_public_day.short_description = 'Change public_day to now'


class CustomerAdmin(admin.ModelAdmin):
  # Loai bo cac fields khong can hitn thi (insert/update)
    # exclude = ('public_day',)

  # Hien thi cac fields chi dinh
    list_display = ('customer_name', 'username',
                    'email', 'tel', 'address',)

  # Filter theo cac fields chi dinh
    list_filter = ('username',)

  # Tim kiem
    search_fields = ('username__contains',)

  # Action
    actions = [change_public_day]


admin.site.register(Customer, CustomerAdmin)

# Thay doi tieu de

admin.site.site_header = 'Cozastore Administation'
