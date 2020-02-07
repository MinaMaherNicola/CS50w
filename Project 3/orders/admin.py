from django.contrib import admin

from .models import Topping, MenuItem, Address, OrderHeader, OrderLines, Type

# Register your models here.

class OrderLinesInline(admin.TabularInline):
    model = OrderLines
    ordering = ('id',)

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderLinesInline,
    ]

admin.site.register(Type)
admin.site.register(Topping)
admin.site.register(MenuItem)
admin.site.register(Address)
admin.site.register(OrderHeader, OrderAdmin)
admin.site.register(OrderLines)
