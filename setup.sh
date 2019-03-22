#!/bin/bash
# Installs dependencies and initializes permissions

pip3 install -r requirements.txt
chmod +x importers/img_importer.py
export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
export PATH=$PATH:/usr/local/mysql/bin