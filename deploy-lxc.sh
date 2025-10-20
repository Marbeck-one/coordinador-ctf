#!/bin/bash

# Crear contenedor
lxc launch ubuntu:22.04 ctf-coordinador

# Instalar dependencias
lxc exec ctf-coordinador -- apt update
lxc exec ctf-coordinador -- apt install -y python3 python3-pip

# Crear directorios
lxc exec ctf-coordinador -- mkdir -p /root/desafio-coordinador/templates

# Copiar archivos
lxc file push app.py ctf-coordinador/root/desafio-coordinador/
lxc file push -r templates/ ctf-coordinador/root/desafio-coordinador/

# Instalar Flask
lxc exec ctf-coordinador -- pip3 install flask

# Iniciar servicio
lxc exec ctf-coordinador -- bash -c \
  "cd /root/desafio-coordinador && nohup python3 app.py > /tmp/ctf.log 2>&1 &"

# Obtener IP
IP=$(lxc list ctf-coordinador --format=json | grep -oP '"eth0".*?"address": "\K[^"]+')
echo "✅ Desafío disponible en: http://$IP:5000"