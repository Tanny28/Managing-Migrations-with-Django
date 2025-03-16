from django.contrib import admin
from .models import Currency, Transaction, CurrencyHistory, Currencybalance, ExchangeGoal
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('exchange_date',)
class CurrencyHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

class CurrencybalanceAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    list_display = ('currency', 'shared_portfolio', 'value', 'created_at')


    
admin.site.register(Currency)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CurrencyHistory,CurrencyHistoryAdmin)
admin.site.register(Currencybalance, CurrencybalanceAdmin)
admin.site.register( ExchangeGoal ,CurrencyHistoryAdmin)
