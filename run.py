#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
P2P File Transfer uygulamasını başlatan ana dosya.
"""

import os
from app import create_app, socketio

def main():
    """
    Uygulamayı başlatır.
    """
    # Uygulamayı oluştur
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    
    # Uygulama ayarlarını al
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')
    
    # SocketIO ile uygulamayı başlat
    print(f"\nP2P Dosya Transferi uygulaması başlatılıyor...")
    print(f"Adres: http://{host if host != '0.0.0.0' else 'localhost'}:{port}")
    print(f"Debug modu: {'Açık' if debug else 'Kapalı'}\n")
    
    socketio.run(app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    main() 