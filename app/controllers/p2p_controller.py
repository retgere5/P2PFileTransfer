#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulaması P2P controller'ı.
Bu modül, P2P bağlantıları ve dosya transferi ile ilgili rotaları yönetir.
"""

import os
import json
import uuid
from flask import Blueprint, render_template, jsonify, request, current_app, session, abort, send_file
from werkzeug.utils import secure_filename
from app.services.p2p_service import P2PService

# Blueprint oluştur
p2p_bp = Blueprint('p2p', __name__)

# P2P servisi
p2p_service = P2PService()

@p2p_bp.route('/room')
def room():
    """P2P oda sayfası."""
    room_id = request.args.get('id')
    if not room_id:
        return render_template('p2p/create_room.html')
    
    return render_template('p2p/room.html', room_id=room_id)

@p2p_bp.route('/api/stun-servers')
def get_stun_servers():
    """STUN sunucularını döndürür."""
    return jsonify({
        'stun_servers': p2p_service.get_stun_servers()
    })

@p2p_bp.route('/api/upload', methods=['POST'])
def upload_file():
    """Dosya yükleme işlemi."""
    # Dosya kontrolü
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'Dosya bulunamadı'
        }), 400
    
    file = request.files['file']
    
    # Dosya adı kontrolü
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'Dosya seçilmedi'
        }), 400
    
    # Dosya uzantısı kontrolü
    if not p2p_service.is_allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'Bu dosya türüne izin verilmiyor'
        }), 400
    
    # Dosyayı kaydet
    filename = secure_filename(file.filename)
    file_path = p2p_service.get_file_path(filename)
    file.save(file_path)
    
    # Dosya bilgilerini döndür
    file_info = p2p_service.get_file_info(file_path)
    
    return jsonify({
        'success': True,
        'file_info': file_info
    })

@p2p_bp.route('/api/download/<path:filename>')
def download_file(filename):
    """Dosya indirme işlemi."""
    # Dosya yolunu oluştur
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    # Dosya kontrolü
    if not os.path.exists(file_path):
        abort(404)
    
    # Dosya bilgilerini al
    file_info = p2p_service.get_file_info(file_path)
    
    # Dosyayı gönder
    return send_file(
        file_path,
        as_attachment=True,
        download_name=file_info['name'],
        mimetype='application/octet-stream'
    )

@p2p_bp.route('/api/file-info/<path:filename>')
def get_file_info(filename):
    """Dosya bilgilerini döndürür."""
    # Dosya yolunu oluştur
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    # Dosya kontrolü
    if not os.path.exists(file_path):
        return jsonify({
            'success': False,
            'error': 'Dosya bulunamadı'
        }), 404
    
    # Dosya bilgilerini al
    file_info = p2p_service.get_file_info(file_path)
    
    return jsonify({
        'success': True,
        'file_info': file_info
    })

@p2p_bp.route('/api/delete-file/<path:filename>', methods=['DELETE'])
def delete_file(filename):
    """Dosya silme işlemi."""
    # Dosya yolunu oluştur
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    # Dosya kontrolü
    if not os.path.exists(file_path):
        return jsonify({
            'success': False,
            'error': 'Dosya bulunamadı'
        }), 404
    
    # Dosyayı sil
    try:
        os.remove(file_path)
        return jsonify({
            'success': True,
            'message': 'Dosya başarıyla silindi'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Dosya silinirken hata oluştu: {str(e)}'
        }), 500 