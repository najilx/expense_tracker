from django.contrib import admin
from .models import Transaction

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'amount', 'category', 'description')
    list_filter = ('category','date','user')
    search_fields = ('category','description',)
