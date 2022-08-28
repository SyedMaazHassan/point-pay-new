from dataclasses import fields
from django.contrib import admin
from django.conf import settings
from payment.models import *
from django.utils.html import mark_safe # Newer versions



class RequestConfirmationAdmin(admin.ModelAdmin):
    model = RequestConfirmation
    list_display = ["created_at", "user", "voucher", "is_usable"]

    def is_usable(self, obj):
        return not obj.is_expired()

    is_usable.boolean = True 


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 1
    can_delete = False
    can_add = False
    can_edit = False
    readonly_fields = fields = ("transaction_id", "Amount", "type", "source", "note", "created_at", "account_id")

    def Amount(self, obj):
        color = "green" 
        symbol = "+"
        if obj.is_debit:
            color = "red"
            symbol = "-"

        return mark_safe(
            f'<span style="color:{color}">{symbol} {settings.CURRENCY_SYMBOL} {obj.amount}</span>'
        )

    def type(self, obj):
        return "Debit" if obj.is_debit else "Credit"

class AccountAdmin(admin.ModelAdmin):
    model = Account
    inlines = [TransactionInline] 
    list_display = ["account_id", "title", "balance", "type", "created_at"]
    search_fields = ["account_id","title"]


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = ["transaction_id", "account_title", "Amount", "type", "source", "note", "created_at"]

    def account_title(self, obj):
        return obj.account.title

    def Amount(self, obj):
        color = "green" 
        symbol = "+"
        if obj.is_debit:
            color = "red"
            symbol = "-"

        return mark_safe(
            f'<span style="color:{color}">{symbol} {settings.CURRENCY_SYMBOL} {obj.amount}</span>'
        )

    def type(self, obj):
        return "Debit" if obj.is_debit else "Credit"

    search_fields = ["account_id", "title"]

# Register your models here.
admin.site.register(FeeSubmission)
admin.site.register(Account, AccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(RequestConfirmation, RequestConfirmationAdmin)
admin.site.register(TopupRequest)

