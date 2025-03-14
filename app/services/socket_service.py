#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulaması için Socket.IO servisi.
Bu modül, gerçek zamanlı P2P iletişimi için gerekli socket işlemlerini yönetir.
"""

import os
import json
import uuid
import logging
from flask import request, session
from flask_socketio import SocketIO, emit, join_room, leave_room

# SocketIO nesnesi oluştur
socketio = SocketIO(cors_allowed_origins="*")

# Aktif odalar ve bağlantılar
active_rooms = {}
active_connections = {}

# Loglama
logger = logging.getLogger(__name__)

@socketio.on('connect')
def handle_connect():
    """Yeni bir istemci bağlandığında çalışır."""
    client_id = str(uuid.uuid4())
    session['client_id'] = client_id
    active_connections[client_id] = request.sid
    
    logger.info(f"Yeni bağlantı: {client_id}")
    emit('connected', {'client_id': client_id})

@socketio.on('disconnect')
def handle_disconnect():
    """İstemci bağlantısı kesildiğinde çalışır."""
    client_id = session.get('client_id')
    if client_id:
        # Aktif bağlantılardan kaldır
        if client_id in active_connections:
            del active_connections[client_id]
        
        # Odalardan kaldır
        for room_id, room_info in list(active_rooms.items()):
            if client_id in room_info['clients']:
                room_info['clients'].remove(client_id)
                
                # Odadaki diğer kullanıcılara bildir
                emit('peer_disconnected', {'client_id': client_id}, room=room_id)
                
                # Oda boşsa kaldır
                if not room_info['clients']:
                    del active_rooms[room_id]
                    logger.info(f"Oda silindi: {room_id}")
        
        logger.info(f"Bağlantı kesildi: {client_id}")

@socketio.on('create_room')
def handle_create_room():
    """Yeni bir oda oluşturur."""
    client_id = session.get('client_id')
    if not client_id:
        emit('error', {'message': 'Oturum bulunamadı'})
        return
    
    # Yeni oda ID'si oluştur
    room_id = str(uuid.uuid4())[:8]
    
    # Odayı oluştur
    active_rooms[room_id] = {
        'owner': client_id,
        'clients': [client_id]
    }
    
    # Odaya katıl
    join_room(room_id)
    session['room_id'] = room_id
    
    logger.info(f"Oda oluşturuldu: {room_id} (Sahibi: {client_id})")
    emit('room_created', {'room_id': room_id})

@socketio.on('join_room')
def handle_join_room(data):
    """Var olan bir odaya katılır."""
    room_id = data.get('room_id')
    client_id = session.get('client_id')
    
    if not client_id:
        emit('error', {'message': 'Oturum bulunamadı'})
        return
    
    if not room_id or room_id not in active_rooms:
        emit('error', {'message': 'Oda bulunamadı'})
        return
    
    # Odaya katıl
    join_room(room_id)
    session['room_id'] = room_id
    
    # Odaya ekle
    if client_id not in active_rooms[room_id]['clients']:
        active_rooms[room_id]['clients'].append(client_id)
    
    # Odadaki diğer kullanıcılara bildir
    for peer_id in active_rooms[room_id]['clients']:
        if peer_id != client_id:
            emit('new_peer', {'peer_id': client_id}, room=active_connections.get(peer_id))
    
    # Odadaki diğer kullanıcıları bildir
    peers = [peer for peer in active_rooms[room_id]['clients'] if peer != client_id]
    emit('room_joined', {'room_id': room_id, 'peers': peers})
    
    logger.info(f"Odaya katıldı: {room_id} (Kullanıcı: {client_id})")

@socketio.on('leave_room')
def handle_leave_room():
    """Odadan ayrılır."""
    client_id = session.get('client_id')
    room_id = session.get('room_id')
    
    if not client_id or not room_id:
        return
    
    if room_id in active_rooms and client_id in active_rooms[room_id]['clients']:
        # Odadan çıkar
        leave_room(room_id)
        active_rooms[room_id]['clients'].remove(client_id)
        
        # Odadaki diğer kullanıcılara bildir
        emit('peer_disconnected', {'client_id': client_id}, room=room_id)
        
        # Oda boşsa kaldır
        if not active_rooms[room_id]['clients']:
            del active_rooms[room_id]
            logger.info(f"Oda silindi: {room_id}")
        
        # Oturumdan kaldır
        session.pop('room_id', None)
        
        logger.info(f"Odadan ayrıldı: {room_id} (Kullanıcı: {client_id})")

@socketio.on('signal')
def handle_signal(data):
    """WebRTC sinyal mesajlarını iletir."""
    client_id = session.get('client_id')
    room_id = session.get('room_id')
    target_id = data.get('target_id')
    signal_data = data.get('signal')
    
    if not client_id or not room_id or not target_id or not signal_data:
        emit('error', {'message': 'Geçersiz sinyal verisi'})
        return
    
    if room_id not in active_rooms or target_id not in active_rooms[room_id]['clients']:
        emit('error', {'message': 'Hedef kullanıcı bulunamadı'})
        return
    
    # Hedef kullanıcıya sinyal gönder
    if target_id in active_connections:
        emit('signal', {
            'source_id': client_id,
            'signal': signal_data
        }, room=active_connections[target_id])
        
        logger.debug(f"Sinyal iletildi: {client_id} -> {target_id}")

@socketio.on('file_metadata')
def handle_file_metadata(data):
    """Dosya meta verilerini hedef kullanıcıya iletir."""
    client_id = session.get('client_id')
    room_id = session.get('room_id')
    target_id = data.get('target_id')
    file_info = data.get('file_info')
    
    if not client_id or not room_id or not target_id or not file_info:
        emit('error', {'message': 'Geçersiz dosya bilgisi'})
        return
    
    if room_id not in active_rooms or target_id not in active_rooms[room_id]['clients']:
        emit('error', {'message': 'Hedef kullanıcı bulunamadı'})
        return
    
    # Hedef kullanıcıya dosya bilgilerini gönder
    if target_id in active_connections:
        emit('file_metadata', {
            'source_id': client_id,
            'file_info': file_info
        }, room=active_connections[target_id])
        
        logger.info(f"Dosya bilgisi gönderildi: {client_id} -> {target_id}, Dosya: {file_info.get('name')}")

@socketio.on('transfer_status')
def handle_transfer_status(data):
    """Dosya transfer durumunu hedef kullanıcıya iletir."""
    client_id = session.get('client_id')
    room_id = session.get('room_id')
    target_id = data.get('target_id')
    status = data.get('status')
    
    if not client_id or not room_id or not target_id or not status:
        return
    
    if room_id not in active_rooms or target_id not in active_rooms[room_id]['clients']:
        return
    
    # Hedef kullanıcıya transfer durumunu gönder
    if target_id in active_connections:
        emit('transfer_status', {
            'source_id': client_id,
            'status': status
        }, room=active_connections[target_id])
        
        logger.debug(f"Transfer durumu iletildi: {client_id} -> {target_id}, Durum: {status}") 