from django.contrib import admin

from payment.models import *



class RequestConfirmationAdmin(admin.ModelAdmin):
    model = RequestConfirmation
    list_display = ["created_at", "user", "voucher", "is_usable"]

    def is_usable(self, obj):
        return not obj.is_expired()

    is_usable.boolean = True 


# Register your models here.
admin.site.register(FeeSubmission)
admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(RequestConfirmation, RequestConfirmationAdmin)

