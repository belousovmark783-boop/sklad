from django.contrib import admin
from .models import Room, Rack, Client, Item

admin.site.site_header = "СкладОзон — Управление"
admin.site.site_title = "СкладОзон"
admin.site.index_title = "Панель управления складом"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name',)


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ('number', 'room', 'slots_count', 'max_load')
    list_filter = ('room',)
    search_fields = ('number',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'client', 'rack', 'position', 'arrival_date', 'contract_end_date')
    list_filter = ('client', 'rack', 'arrival_date')
    search_fields = ('contract_number', 'client__name')
    date_hierarchy = 'arrival_date'
