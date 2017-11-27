import cx_Freeze
import sys
import os

os.environ['TCL_LIBRARY'] = sys.executable[:-10] + "tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = sys.executable[:-10] + "tcl\\tk8.6"

base = None

if sys.platform == "win32":
	base = "Win32GUI"

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
	name = "main",
	options = {"build_exe": {"packages":["tkinter"], "include_files":["plans.json", "systems.json"]}},
	version = "1.0",
	description = "Access System",
	executables = executables
)