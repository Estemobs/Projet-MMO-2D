#!/bin/bash
# Flatpak launcher for Projet MMO 2D
cd /app/game
export PYTHONPATH=/app/game:/app/lib/python3.11/site-packages${PYTHONPATH:+:$PYTHONPATH}
exec python3 main.py "$@"
