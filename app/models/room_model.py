#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulaması oda modeli.
"""

import time
import uuid
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional

@dataclass
class RoomModel:
    """Oda modeli."""
    
    id: str
    owner_id: str
    created_at: float = 0
    last_activity: float = 0
    is_active: bool = True
    peers: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Nesne oluşturulduktan sonra çalışır."""
        if not self.id:
            self.id = str(uuid.uuid4())[:8]
        
        if not self.created_at:
            self.created_at = time.time()
        
        if not self.last_activity:
            self.last_activity = time.time()
        
        # Oda sahibini peers listesine ekle
        if self.owner_id and self.owner_id not in self.peers:
            self.peers.append(self.owner_id)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RoomModel':
        """Sözlükten RoomModel nesnesi oluşturur."""
        return cls(
            id=data.get('id', str(uuid.uuid4())[:8]),
            owner_id=data.get('owner_id', ''),
            created_at=data.get('created_at', time.time()),
            last_activity=data.get('last_activity', time.time()),
            is_active=data.get('is_active', True),
            peers=data.get('peers', []),
            metadata=data.get('metadata', {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """RoomModel nesnesini sözlüğe dönüştürür."""
        return asdict(self)
    
    def update_activity(self):
        """Son aktivite zamanını günceller."""
        self.last_activity = time.time()
    
    def add_peer(self, peer_id: str):
        """Odaya peer ekler."""
        if peer_id not in self.peers:
            self.peers.append(peer_id)
            self.update_activity()
            return True
        return False
    
    def remove_peer(self, peer_id: str):
        """Odadan peer çıkarır."""
        if peer_id in self.peers:
            self.peers.remove(peer_id)
            self.update_activity()
            return True
        return False
    
    def is_empty(self) -> bool:
        """Odanın boş olup olmadığını kontrol eder."""
        return len(self.peers) == 0
    
    def is_owner(self, peer_id: str) -> bool:
        """Peer'ın oda sahibi olup olmadığını kontrol eder."""
        return peer_id == self.owner_id
    
    def deactivate(self):
        """Odayı devre dışı bırakır."""
        self.is_active = False
        self.update_activity()
    
    def activate(self):
        """Odayı etkinleştirir."""
        self.is_active = True
        self.update_activity()
    
    def update_metadata(self, metadata: Dict[str, Any]):
        """Oda meta verilerini günceller."""
        self.metadata.update(metadata)
        self.update_activity() 