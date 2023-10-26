from django.contrib import admin
from .models import Shops_net, Shop, Recipet, Measurement_unit, Unit_of_measurement, Product, RecipetProduct

admin.site.register(Shops_net)
admin.site.register(Shop)
admin.site.register(Recipet)
admin.site.register(Measurement_unit)
admin.site.register(Unit_of_measurement)
admin.site.register(Product)
admin.site.register(RecipetProduct)