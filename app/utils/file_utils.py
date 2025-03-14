#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulaması dosya işlemleri yardımcı modülü.
"""

import os
import uuid
import mimetypes
from typing import Optional, Dict, Any, List, Tuple
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename: str) -> bool:
    """
    Dosya uzantısının izin verilen uzantılardan olup olmadığını kontrol eder.
    
    Args:
        filename (str): Dosya adı
    
    Returns:
        bool: Dosya uzantısı izin verilen uzantılardan ise True, değilse False
    """
    if '.' not in filename:
        return False
    
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in current_app.config.get('ALLOWED_EXTENSIONS', set())

def get_safe_filename(filename: str) -> str:
    """
    Güvenli bir dosya adı oluşturur.
    
    Args:
        filename (str): Orijinal dosya adı
    
    Returns:
        str: Güvenli dosya adı
    """
    # Güvenli bir dosya adı oluştur
    safe_filename = secure_filename(filename)
    
    # Benzersiz bir isim oluştur
    unique_filename = f"{uuid.uuid4()}_{safe_filename}"
    
    return unique_filename

def get_file_path(filename: str) -> str:
    """
    Dosya yolunu döndürür.
    
    Args:
        filename (str): Dosya adı
    
    Returns:
        str: Dosya yolu
    """
    # Güvenli bir dosya adı oluştur
    safe_filename = get_safe_filename(filename)
    
    # Dosya yolunu oluştur
    return os.path.join(current_app.config['UPLOAD_FOLDER'], safe_filename)

def get_file_info(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Dosya bilgilerini döndürür.
    
    Args:
        file_path (str): Dosya yolu
    
    Returns:
        Optional[Dict[str, Any]]: Dosya bilgileri
    """
    if not os.path.exists(file_path):
        return None
    
    # Dosya bilgilerini al
    file_stats = os.stat(file_path)
    filename = os.path.basename(file_path)
    
    # Orijinal dosya adını al (UUID kısmını kaldır)
    original_filename = '_'.join(filename.split('_')[1:]) if '_' in filename else filename
    
    # MIME türünü tahmin et
    mime_type, _ = mimetypes.guess_type(original_filename)
    
    return {
        'name': original_filename,
        'path': file_path,
        'size': file_stats.st_size,
        'mime_type': mime_type,
        'last_modified': file_stats.st_mtime
    }

def delete_file(file_path: str) -> bool:
    """
    Dosyayı siler.
    
    Args:
        file_path (str): Dosya yolu
    
    Returns:
        bool: Başarılı ise True, değilse False
    """
    if not os.path.exists(file_path):
        return False
    
    try:
        os.remove(file_path)
        return True
    except Exception:
        return False

def create_chunk_metadata(file_path: str, chunk_size: int = 1024*1024) -> Optional[Dict[str, Any]]:
    """
    Dosya parçalarının meta verilerini oluşturur.
    
    Args:
        file_path (str): Dosya yolu
        chunk_size (int, optional): Parça boyutu (bayt). Varsayılan 1MB.
    
    Returns:
        Optional[Dict[str, Any]]: Parça meta verileri
    """
    if not os.path.exists(file_path):
        return None
    
    file_size = os.path.getsize(file_path)
    total_chunks = (file_size + chunk_size - 1) // chunk_size
    
    return {
        'file_size': file_size,
        'chunk_size': chunk_size,
        'total_chunks': total_chunks
    }

def get_file_chunks(file_path: str, chunk_size: int = 1024*1024) -> List[bytes]:
    """
    Dosyayı parçalara ayırır.
    
    Args:
        file_path (str): Dosya yolu
        chunk_size (int, optional): Parça boyutu (bayt). Varsayılan 1MB.
    
    Returns:
        List[bytes]: Dosya parçaları
    """
    if not os.path.exists(file_path):
        return []
    
    chunks = []
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)
    
    return chunks

def read_chunk(file_path: str, chunk_index: int, chunk_size: int = 1024*1024) -> Tuple[bytes, bool]:
    """
    Dosyadan belirli bir parçayı okur.
    
    Args:
        file_path (str): Dosya yolu
        chunk_index (int): Parça indeksi
        chunk_size (int, optional): Parça boyutu (bayt). Varsayılan 1MB.
    
    Returns:
        Tuple[bytes, bool]: Parça verisi ve son parça olup olmadığı bilgisi
    """
    if not os.path.exists(file_path):
        return b'', True
    
    file_size = os.path.getsize(file_path)
    total_chunks = (file_size + chunk_size - 1) // chunk_size
    
    if chunk_index >= total_chunks:
        return b'', True
    
    with open(file_path, 'rb') as f:
        f.seek(chunk_index * chunk_size)
        chunk = f.read(chunk_size)
    
    is_last_chunk = chunk_index == total_chunks - 1
    
    return chunk, is_last_chunk 