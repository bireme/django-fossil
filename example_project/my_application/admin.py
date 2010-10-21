from django.contrib import admin

from models import Supplier, Purchase

class AdminSupplier(admin.ModelAdmin):
    pass

class AdminPurchase(admin.ModelAdmin):
    list_display = ('date','supplier','user')

admin.site.register(Supplier, AdminSupplier)
admin.site.register(Purchase, AdminPurchase)

