from django.contrib import admin
from .models import Shops_net, Shop, Receipt, Payment_type, Measurement_unit, Unit_of_measurement, Product, ReceiptProduct
from django.utils.translation import gettext as _

class ShopAdmin(admin.ModelAdmin):
    search_fields = ['name', 'shops_net__name']

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'shops_net__name']

class ReceiptProductAdmin(admin.ModelAdmin):
    actions = ['duplicate_selected']

    def duplicate_selected(self, request, queryset):
        for receipt_product in queryset:
            receipt_product.pk = None
            receipt_product.save()

        self.message_user(request, _('{} receiptProduct(s) were duplicated successfully.'.format(len(queryset))))

    duplicate_selected.short_description = _("Duplicate selected ReceiptProducts")

admin.site.register(Shops_net)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Receipt)
admin.site.register(Payment_type)
admin.site.register(Measurement_unit)
admin.site.register(Unit_of_measurement)
admin.site.register(Product, ProductAdmin)
admin.site.register(ReceiptProduct, ReceiptProductAdmin)
