#!/bin/bash
# Installs dependencies and initializes permissions

pip3 install --user -r requirements.txt
chmod +x importers/img_importer.py
