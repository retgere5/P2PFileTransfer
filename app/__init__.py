#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulaması ana modülü.
"""

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from datetime import datetime
import os

# SocketIO nesnesini global olarak tanımla
socketio = SocketIO()

def create_app(config_name='development'):
    """
    Uygulama fabrika fonksiyonu.
    
    Args:
        config_name (str): Yapılandırma adı ('development', 'production', vb.)
    
    Returns:
        Flask: Flask uygulama nesnesi
    """
    # Flask uygulamasını oluştur
    app = Flask(__name__, static_folder='static', template_folder='templates')
    
    # Yapılandırmayı yükle
    from app.config import config_by_name
    app.config.from_object(config_by_name[config_name])
    
    # Gizli anahtarı ayarla
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'gizli-anahtar-buraya')
    
    # CORS'u etkinleştir
    CORS(app)
    
    # SocketIO'yu başlat
    socketio.init_app(app, cors_allowed_origins="*")
    
    # Context processor ekle
    @app.context_processor
    def utility_processor():
        """Template değişkenleri."""
        return {
            'now': datetime.now()
        }
    
    # Blueprint'leri kaydet
    from app.routes import main, p2p
    app.register_blueprint(main.bp)
    app.register_blueprint(p2p.bp, url_prefix='/p2p')
    
    # Hata işleyicilerini kaydet
    register_error_handlers(app)
    
    # Socket.IO olaylarını içe aktar
    from app import socket_events
    
    return app

def register_error_handlers(app):
    """
    Uygulama için hata işleyicilerini kaydeder.
    
    Args:
        app (Flask): Flask uygulama nesnesi
    """
    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def server_error(error):
        from flask import render_template
        return render_template('errors/500.html'), 500 