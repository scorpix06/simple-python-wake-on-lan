from cx_Freeze import setup, Executable




# On appelle la fonction setup
setup(
    name = "Wake On Lan Windows",
    version = "1",
    description = "WOL PC",
    executables = [Executable("main.pyw", targetName="WakeOnLan"), ],
)


import sys
from cx_Freeze import setup, Executable

import os
PYTHON_INSTALL_DIR = os.path.dirname(sys.executable)
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

include_files = [(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join('lib', 'tk86t.dll')),
                 (os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'), os.path.join('lib', 'tcl86t.dll'))]

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [Executable('SimpleTkApp.py', base=base)]

setup(name='simple_Tkinter',
      version='0.1',
      description='Sample cx_Freeze Tkinter script',
      options={'build_exe': {'include_files': include_files}},
      executables=executables)