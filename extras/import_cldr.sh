#!/bin/bash

path=$(python -c "import os, babel; print(os.path.join(os.path.dirname(babel.__file__), os.pardir))")
cd $path
python setup.py import_cldr
