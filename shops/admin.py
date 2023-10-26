from django.contrib import admin
from .models import Shops_net, Shop, Recipet, Measurement_unit, Unit_of_measurement, Product, RecipetProduct

class ShopAdmin(admin.ModelAdmin):
    search_fields = ['name', 'shops_net__name']

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'shops_net__name']

admin.site.register(Shops_net)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Recipet)
admin.site.register(Measurement_unit)
admin.site.register(Unit_of_measurement)
admin.site.register(Product, ProductAdmin)
admin.site.register(RecipetProduct)