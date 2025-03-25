from django.contrib import admin
from .models import Company, Transaction

class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "main_product")

class TransactionAdmin(admin.ModelAdmin):
    list_display = ("company", "partner", "transaction_type")

admin.site.register(Company, CompanyAdmin)
admin.site.register(Transaction, TransactionAdmin)
