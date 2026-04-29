import re
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Room, Rack, Client, Item
from datetime import date


def _initials(name):
    clean = re.sub(r'^(ООО|АО|ЗАО|ПАО|ИП|ОАО|НКО)\s*[«"]?', '', name).strip().strip('»"')
    words = [w for w in clean.split() if w]
    if not words:
        return name[:2].upper()
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[1][0]).upper()


def index(request):
    today = date.today()
    context = {
        'rooms': Room.objects.prefetch_related('racks').all(),
        'racks': Rack.objects.select_related('room').all(),
        'clients': Client.objects.all(),
        'items': Item.objects.select_related('client', 'rack', 'rack__room').all(),
        'today': today,
        'total_rooms': Room.objects.count(),
        'total_racks': Rack.objects.count(),
        'total_clients': Client.objects.count(),
        'total_items': Item.objects.count(),
    }
    return render(request, 'wb/index.html', context)


@require_GET
def api_data(request):
    """JSON API — all warehouse data for the React frontend."""
    today = date.today()

    rooms = []
    for room in Room.objects.prefetch_related('racks').all():
        racks_in_room = []
        for rack in room.racks.all():
            racks_in_room.append({
                'id': rack.id,
                'number': rack.number,
                'slots_count': rack.slots_count,
                'slot_height': rack.slot_height,
                'slot_width': rack.slot_width,
                'slot_length': rack.slot_length,
                'max_load': rack.max_load,
                'items_count': rack.items.count(),
            })
        rooms.append({
            'id': room.id,
            'name': room.name,
            'capacity': room.capacity,
            'racks': racks_in_room,
            'racks_count': len(racks_in_room),
        })

    clients = []
    for client in Client.objects.all():
        clients.append({
            'id': client.id,
            'name': client.name,
            'bank_details': client.bank_details,
            'items_count': client.items.count(),
            'initials': _initials(client.name),
        })

    items = []
    for item in Item.objects.select_related('client', 'rack', 'rack__room').all():
        is_expired = item.contract_end_date < today
        items.append({
            'id': item.id,
            'contract': item.contract_number,
            'client': item.client.name,
            'rack': item.rack.number,
            'position': item.position,
            'room': item.rack.room.name,
            'dimensions': f'{item.height}×{item.width}×{item.length} м',
            'weight': f'{item.weight} кг',
            'received': item.arrival_date.strftime('%d.%m.%Y'),
            'expires_at': item.contract_end_date.strftime('%d.%m.%Y'),
            'is_expired': is_expired,
        })

    all_racks = []
    for rack in Rack.objects.select_related('room').all():
        all_racks.append({
            'id': rack.id,
            'number': rack.number,
            'room': rack.room.name,
            'slots_count': rack.slots_count,
            'slot_height': rack.slot_height,
            'slot_width': rack.slot_width,
            'slot_length': rack.slot_length,
            'max_load': rack.max_load,
            'items_count': rack.items.count(),
        })

    data = {
        'stats': {
            'rooms': Room.objects.count(),
            'racks': Rack.objects.count(),
            'clients': Client.objects.count(),
            'items': Item.objects.count(),
        },
        'rooms': rooms,
        'racks': all_racks,
        'clients': clients,
        'items': items,
    }
    return JsonResponse(data)
