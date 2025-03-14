#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulaması ana controller'ı.
Bu modül, ana sayfa ve genel rotaları yönetir.
"""

from flask import Blueprint, render_template, jsonify, request, current_app

# Blueprint oluştur
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Ana sayfa."""
    return render_template('index.html')

@main_bp.route('/about')
def about():
    """Hakkında sayfası."""
    return render_template('about.html')

@main_bp.route('/health')
def health():
    """Sağlık kontrolü."""
    return jsonify({
        'status': 'ok',
        'version': '1.0.0'
    })

@main_bp.route('/config')
def get_config():
    """İstemci yapılandırmasını döndürür."""
    # Sadece istemcinin ihtiyacı olan yapılandırmaları gönder
    client_config = {
        'stun_servers': current_app.config.get('P2P_STUN_SERVERS', []),
        'max_file_size': current_app.config.get('MAX_CONTENT_LENGTH', 0),
        'allowed_extensions': list(current_app.config.get('ALLOWED_EXTENSIONS', []))
    }
    
    return jsonify(client_config)

@main_bp.errorhandler(404)
def page_not_found(e):
    """404 hata sayfası."""
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def server_error(e):
    """500 hata sayfası."""
    return render_template('errors/500.html'), 500 