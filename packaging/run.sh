#!/bin/bash
# Flatpak launcher for Projet MMO 2D
cd /app/game
PYTHONPATH=/app/lib/python3.11/site-packages${PYTHONPATH:+:$PYTHONPATH} exec python3 main.py "$@"
