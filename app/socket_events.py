#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulaması Socket.IO olayları.
"""

import secrets
from flask import request
from flask_socketio import emit, join_room, leave_room
from app import socketio

# Aktif odalar ve kullanıcılar
active_rooms = {}
active_users = {}

@socketio.on('connect')
def handle_connect():
    """Kullanıcı bağlantı olayı."""
    client_id = request.sid
    active_users[client_id] = {
        'id': client_id,
        'name': f'Kullanıcı{secrets.randbelow(1000)}',
        'color': f'hsl({secrets.randbelow(360)}, 70%, 50%)'
    }
    
    emit('connected', {'client_id': client_id})
    print(f'Kullanıcı bağlandı: {client_id}')

@socketio.on('disconnect')
def handle_disconnect():
    """Kullanıcı bağlantı kesme olayı."""
    client_id = request.sid
    
    # Kullanıcının bulunduğu odaları bul
    rooms_to_leave = []
    for room_id, room_data in active_rooms.items():
        if client_id in room_data['users']:
            rooms_to_leave.append(room_id)
    
    # Odalardan çık
    for room_id in rooms_to_leave:
        handle_leave_room(room_id)
    
    # Kullanıcıyı sil
    if client_id in active_users:
        del active_users[client_id]
    
    print(f'Kullanıcı ayrıldı: {client_id}')

@socketio.on('join_room')
def handle_join_room(data):
    """Odaya katılma olayı."""
    client_id = request.sid
    room_id = data.get('room_id')
    
    if not room_id:
        # Oda ID'si yoksa yeni oda oluştur
        room_id = secrets.token_urlsafe(8)
    
    # Odaya katıl
    join_room(room_id)
    
    # Oda yoksa oluştur
    if room_id not in active_rooms:
        active_rooms[room_id] = {
            'id': room_id,
            'users': [client_id],
            'initiator': client_id
        }
        is_initiator = True
    else:
        # Odaya kullanıcı ekle
        if client_id not in active_rooms[room_id]['users']:
            active_rooms[room_id]['users'].append(client_id)
        is_initiator = client_id == active_rooms[room_id]['initiator']
    
    # Odadaki diğer kullanıcıları bul
    peers = []
    for user_id in active_rooms[room_id]['users']:
        if user_id != client_id and user_id in active_users:
            peers.append(active_users[user_id])
    
    # Kullanıcıya odaya katıldığını bildir
    emit('room_joined', {
        'room_id': room_id,
        'peers': peers,
        'is_initiator': is_initiator
    })
    
    # Diğer kullanıcılara yeni kullanıcı katıldığını bildir
    for user_id in active_rooms[room_id]['users']:
        if user_id != client_id:
            emit('new_peer', {
                'peer_id': client_id,
                'user': active_users.get(client_id)
            }, room=user_id)
    
    print(f'Kullanıcı odaya katıldı: {client_id} -> {room_id}')

@socketio.on('leave_room')
def handle_leave_room(room_id=None):
    """Odadan ayrılma olayı."""
    client_id = request.sid
    
    if not room_id:
        room_id = request.args.get('room_id')
    
    if not room_id or room_id not in active_rooms:
        return
    
    # Odadan ayrıl
    leave_room(room_id)
    
    # Kullanıcıyı odadan çıkar
    if client_id in active_rooms[room_id]['users']:
        active_rooms[room_id]['users'].remove(client_id)
    
    # Odada kullanıcı kalmadıysa odayı sil
    if not active_rooms[room_id]['users']:
        del active_rooms[room_id]
    else:
        # Başlatıcı ayrıldıysa yeni başlatıcı belirle
        if client_id == active_rooms[room_id]['initiator'] and active_rooms[room_id]['users']:
            active_rooms[room_id]['initiator'] = active_rooms[room_id]['users'][0]
    
    # Diğer kullanıcılara bildir
    emit('peer_disconnected', {
        'peer_id': client_id,
        'room_id': room_id
    }, room=room_id)
    
    print(f'Kullanıcı odadan ayrıldı: {client_id} -> {room_id}')

@socketio.on('signal')
def handle_signal(data):
    """WebRTC sinyal olayı."""
    client_id = request.sid
    
    # Kullanıcının bulunduğu odaları bul
    user_rooms = []
    for room_id, room_data in active_rooms.items():
        if client_id in room_data['users']:
            user_rooms.append(room_id)
    
    # Tüm odalardaki diğer kullanıcılara sinyal gönder
    for room_id in user_rooms:
        for user_id in active_rooms[room_id]['users']:
            if user_id != client_id:
                emit('signal', data, room=user_id)
    
    print(f'Sinyal gönderildi: {client_id} -> {data["type"]}') 