
from datetime import datetime
from django.contrib import admin
from cart.models import Order, OrderItem
from django.utils.html import format_html


def change_public_day(modeladmin, request, queryset):
    queryset.update(public_day=datetime.now())


change_public_day.short_description = 'Change public_day to now'


class OrderAdmin(admin.ModelAdmin):
  # Loai bo cac fields khong can hitn thi (insert/update)
    # exclude = ('public_day',)

  # Hien thi cac fields chi dinh
    list_display = ('customer', 'total',
                    'status', 'created',)

  # Filter theo cac fields chi dinh
    list_filter = ('created',)

  # Tim kiem
    search_fields = ('customer__contains',)

  # Action
    actions = [change_public_day]


class OrderItemAdmin(admin.ModelAdmin):
  # Loai bo cac fields khong can hitn thi (insert/update)
    # exclude = ('public_day',)

  # Hien thi cac fields chi dinh
    list_display = ('order', 'product',
                    'price', 'quantity',)

  # Filter theo cac fields chi dinh
    list_filter = ('order',)

  # Tim kiem
    search_fields = ('order__contains',)

  # Action
    actions = [change_public_day]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

# Thay doi tieu de

admin.site.site_header = 'Cozastore Administation'
