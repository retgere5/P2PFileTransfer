#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulaması dosya modeli.
"""

import os
import time
import uuid
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class FileModel:
    """Dosya modeli."""
    
    id: str
    name: str
    path: str
    size: int
    mime_type: Optional[str] = None
    last_modified: float = 0
    created_at: float = 0
    
    def __post_init__(self):
        """Nesne oluşturulduktan sonra çalışır."""
        if not self.id:
            self.id = str(uuid.uuid4())
        
        if not self.created_at:
            self.created_at = time.time()
        
        if not self.last_modified:
            self.last_modified = time.time()
    
    @classmethod
    def from_upload(cls, file_path: str, original_filename: str) -> 'FileModel':
        """Yüklenen dosyadan FileModel nesnesi oluşturur."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
        
        file_stats = os.stat(file_path)
        
        return cls(
            id=str(uuid.uuid4()),
            name=original_filename,
            path=file_path,
            size=file_stats.st_size,
            last_modified=file_stats.st_mtime,
            created_at=time.time()
        )
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FileModel':
        """Sözlükten FileModel nesnesi oluşturur."""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            name=data.get('name', ''),
            path=data.get('path', ''),
            size=data.get('size', 0),
            mime_type=data.get('mime_type'),
            last_modified=data.get('last_modified', time.time()),
            created_at=data.get('created_at', time.time())
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """FileModel nesnesini sözlüğe dönüştürür."""
        return asdict(self)
    
    def exists(self) -> bool:
        """Dosyanın var olup olmadığını kontrol eder."""
        return os.path.exists(self.path)
    
    def delete(self) -> bool:
        """Dosyayı siler."""
        if not self.exists():
            return False
        
        try:
            os.remove(self.path)
            return True
        except Exception:
            return False 