#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulaması için P2P servisi.
Bu modül, P2P bağlantıları ve dosya transferi işlemlerini yönetir.
"""

import os
import json
import uuid
import logging
from flask import current_app

# Loglama
logger = logging.getLogger(__name__)

class P2PService:
    """P2P işlemlerini yöneten servis sınıfı."""
    
    @staticmethod
    def get_stun_servers():
        """STUN sunucularını döndürür."""
        return current_app.config.get('P2P_STUN_SERVERS', [])
    
    @staticmethod
    def is_allowed_file(filename):
        """Dosya uzantısının izin verilen uzantılardan olup olmadığını kontrol eder."""
        if '.' not in filename:
            return False
        
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in current_app.config.get('ALLOWED_EXTENSIONS', set())
    
    @staticmethod
    def get_file_path(filename):
        """Dosya yolunu döndürür."""
        # Güvenli bir dosya adı oluştur
        safe_filename = str(uuid.uuid4()) + '_' + filename
        
        # Dosya yolunu oluştur
        return os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)
    
    @staticmethod
    def get_file_info(file_path):
        """Dosya bilgilerini döndürür."""
        if not os.path.exists(file_path):
            return None
        
        # Dosya bilgilerini al
        file_stats = os.stat(file_path)
        filename = os.path.basename(file_path)
        
        # Orijinal dosya adını al (UUID kısmını kaldır)
        original_filename = '_'.join(filename.split('_')[1:]) if '_' in filename else filename
        
        return {
            'name': original_filename,
            'path': file_path,
            'size': file_stats.st_size,
            'last_modified': file_stats.st_mtime
        }
    
    @staticmethod
    def cleanup_temp_files(file_paths):
        """Geçici dosyaları temizler."""
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    logger.info(f"Geçici dosya silindi: {file_path}")
                except Exception as e:
                    logger.error(f"Dosya silinirken hata oluştu: {file_path}, Hata: {str(e)}")
    
    @staticmethod
    def create_chunk_metadata(file_path, chunk_size=1024*1024):
        """Dosya parçalarının meta verilerini oluşturur."""
        if not os.path.exists(file_path):
            return None
        
        file_size = os.path.getsize(file_path)
        total_chunks = (file_size + chunk_size - 1) // chunk_size
        
        return {
            'file_size': file_size,
            'chunk_size': chunk_size,
            'total_chunks': total_chunks
        } 