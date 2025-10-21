#!/usr/bin/env python
"""
Script para ejecutar el servidor Daphne (ASGI)
Soporta HTTP y WebSocket en el mismo puerto 8000
"""
import os
import sys
import subprocess

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sweetblaze_backend.settings')
    
    # Ejecutar Daphne en puerto 8000 (HTTP + WebSocket)
    # Daphne es un servidor ASGI que reemplaza a runserver para soportar WebSockets
    subprocess.run([
        sys.executable, '-m', 'daphne',
        '-b', '0.0.0.0',
        '-p', '8000',
        '--access-log', '-',
        'sweetblaze_backend.asgi:application'
    ])