#!/bin/sh
pip install --upgrade pip
pip install requests
pip install pyyaml
python /scripts/wiki_update.py "$1" $2 $3 $4 $5 $6 $7