#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulaması peer modeli.
"""

import time
import uuid
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional

@dataclass
class PeerModel:
    """Peer modeli."""
    
    id: str
    socket_id: str
    room_id: Optional[str] = None
    connected_at: float = 0
    last_activity: float = 0
    is_connected: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Nesne oluşturulduktan sonra çalışır."""
        if not self.id:
            self.id = str(uuid.uuid4())
        
        if not self.connected_at:
            self.connected_at = time.time()
        
        if not self.last_activity:
            self.last_activity = time.time()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PeerModel':
        """Sözlükten PeerModel nesnesi oluşturur."""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            socket_id=data.get('socket_id', ''),
            room_id=data.get('room_id'),
            connected_at=data.get('connected_at', time.time()),
            last_activity=data.get('last_activity', time.time()),
            is_connected=data.get('is_connected', True),
            metadata=data.get('metadata', {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """PeerModel nesnesini sözlüğe dönüştürür."""
        return asdict(self)
    
    def update_activity(self):
        """Son aktivite zamanını günceller."""
        self.last_activity = time.time()
    
    def disconnect(self):
        """Peer'ı bağlantısını keser."""
        self.is_connected = False
        self.update_activity()
    
    def reconnect(self, socket_id: str):
        """Peer'ı yeniden bağlar."""
        self.socket_id = socket_id
        self.is_connected = True
        self.update_activity()
    
    def join_room(self, room_id: str):
        """Peer'ı bir odaya ekler."""
        self.room_id = room_id
        self.update_activity()
    
    def leave_room(self):
        """Peer'ı odadan çıkarır."""
        self.room_id = None
        self.update_activity()
    
    def update_metadata(self, metadata: Dict[str, Any]):
        """Peer meta verilerini günceller."""
        self.metadata.update(metadata)
        self.update_activity() 