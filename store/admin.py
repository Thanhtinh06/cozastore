
# Register your models here.
from datetime import datetime
from django.contrib import admin
from store.models import Product
from django.utils.html import format_html

# Register your models here.


def change_public_day(modeladmin, request, queryset):
    queryset.update(public_day=datetime.now())


change_public_day.short_description = 'Change public_day to now'


# Thay doi cac fields

class ProductAdmin(admin.ModelAdmin):
  # Loai bo cac fields khong can hitn thi (insert/update)
    # exclude = ('public_day',)

  # Hien thi cac fields chi dinh
    # list_display = ('name', 'price', 'price_origin', 'public_day', 'viewed')

  # Filter theo cac fields chi dinh
    list_filter = ('public_day',)

  # Tim kiem
    search_fields = ('name__contains',)

  # Action
    actions = [change_public_day]

  # Tham khao: https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
  # Doi ten fields - dinh dang
    @admin.display(description='Name Product')
    def edit_name(self, obj):
        return ("%s" % obj.name.upper())

    @admin.display(description='Price Buy')
    def edit_price(self, obj):
        return ("%s" % '{:,}'.format(int(obj.price_buy)))

    @admin.display(description='Price Sell')
    def edit_price_origin(self, obj):
        return ("%s" % '{:,}'.format(int(obj.price_sell)))

    @admin.display(description='Public day')
    # def edit_public_day(self, obj):
    #     return ("%s" % obj.public_day.strftime('%d-%m-%Y %H:%M:%S'))
    @admin.display(description='Image')
    def edit_image(self, obj):
        return format_html("<img src='{}' alt='{}' width='45px' height='45px' />".format(obj.image.url, obj.name))

    list_display = ('edit_image', 'edit_name',
                    'edit_price', 'edit_price_origin', 'inventory', 'status')
    # 'edit_public_day'


admin.site.register(Product, ProductAdmin)

# Thay doi tieu de

admin.site.site_header = 'Cozastore Administation'
