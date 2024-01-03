#!/bin/bash

# SHELL=/bin/bash
# PWD=/home/admin/documents/AutoPark
# LOGNAME=admin
# XDG_SESSION_TYPE=tty
# MOTD_SHOWN=pam
# HOME=/home/admin
# LANG=C.UTF-8
# VIRTUAL_ENV=/home/admin/documents/AutoPark/venv
# SSH_CONNECTION=66.81.164.95 3587 172.31.43.219 22
# XDG_SESSION_CLASS=user
# TERM=xterm-256color
# USER=admin
# SHLVL=1
# XDG_SESSION_ID=5
# VIRTUAL_ENV_PROMPT=(venv) 
# XDG_RUNTIME_DIR=/run/user/1000
# PS1=(venv) \[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ 
# SSH_CLIENT=66.81.164.95 3587 22
# PATH=/home/admin/documents/AutoPark/venv/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
# DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
# SSH_TTY=/dev/pts/0
# OLDPWD=/home/admin

# Cambiar al directorio del script y .env
cd /home/admin/documents/AutoPark

# Activar un entorno virtual
source venv/bin/activate

# Ejecutar script en el entorno
python3 main.py

deactivate
# # Ejecutar tu script compilado
# ./build/exe.linux-x86_64-3.11/main
