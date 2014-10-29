#!/bin/bash

path=$(python -c "import os, babel; print(os.path.join(os.path.dirname(babel.__file__), os.pardir))")
cd $path
python scripts/download_import_cldr.py
