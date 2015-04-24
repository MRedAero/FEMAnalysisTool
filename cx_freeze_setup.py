__author__ = 'Michael Redmond'

from cx_Freeze import setup, Executable

import sys

sys.argv.append('build')

includefiles = []
includes = []
excludes = ['PyQt4.uic.port_v3']
packages = ['fem_post', 'base_app', 'fem_utilities']

setup(
    name = 'fem_post',
    version = '0.1',
    description = 'Finite Element Analysis Tool',
    author = 'N/A',
    author_email = 'N/A',
    options = {'build_exe': {'excludes': excludes,'packages': packages,'include_files': includefiles}},
    executables = [Executable('fem_post.py')]
)