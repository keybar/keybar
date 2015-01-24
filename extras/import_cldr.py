#!/bin/python
import os
import subprocess
import babel

babel_dir = os.path.join(os.path.dirname(babel.__file__), os.pardir)

subprocess.call(['python', '{0}/scripts/download_import_cldr.py'.format(babel_dir)])
