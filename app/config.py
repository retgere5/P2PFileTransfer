#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulaması yapılandırma modülü.
"""

import os
import secrets
from datetime import timedelta

class Config:
    """Temel yapılandırma sınıfı."""
    
    # Genel ayarlar
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli-anahtar-buraya'
    
    # Uygulama ayarları
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB maksimum dosya boyutu
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'zip', 'rar', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx'}
    
    # P2P ayarları
    P2P_STUN_SERVERS = [
        'stun:stun.l.google.com:19302',
        'stun:stun1.l.google.com:19302',
        'stun:stun2.l.google.com:19302',
        'stun:stun3.l.google.com:19302',
        'stun:stun4.l.google.com:19302',
    ]
    
    # Oturum ayarları
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    
    # SocketIO
    CORS_HEADERS = 'Content-Type'
    
    @staticmethod
    def init_app(app):
        """Uygulama başlatma işlemleri."""
        # Yükleme klasörünü oluştur
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class DevelopmentConfig(Config):
    """Geliştirme ortamı yapılandırması."""
    
    DEBUG = True
    TESTING = False
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Geliştirme ortamına özel ayarlar
        app.config['TEMPLATES_AUTO_RELOAD'] = True

class ProductionConfig(Config):
    """Üretim ortamı yapılandırması."""
    
    DEBUG = False
    TESTING = False
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Üretim ortamına özel güvenlik ayarları
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['SESSION_COOKIE_HTTPONLY'] = True
        app.config['REMEMBER_COOKIE_SECURE'] = True
        app.config['REMEMBER_COOKIE_HTTPONLY'] = True

class TestingConfig(Config):
    """Test ortamı yapılandırması."""
    
    DEBUG = True
    TESTING = True
    
    # Test için geçici klasör
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'test_uploads')

# Yapılandırma sözlüğü
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 