#v0.2

import sys
from time import time

start = time()
print("Intializing.", end="", flush=True)

def autoinstall(import_statement):
    try:
        exec(import_statement, globals())
    except ModuleNotFoundError as missing_pkg:
        inp = input(f"Package '{missing_pkg.name}' required. Install it now? (y/N): ")
        if "y" in inp.lower():
            import subprocess
            subprocess.check_call([sys.executable, "-m", "pip", "install", missing_pkg.name])
            print("\n")
            exec(import_statement, globals())
    finally:
        print(".", end="", flush=True)



# Load dependencies
autoinstall("import IPython")
autoinstall("import sympy as sp")
#autoinstall("import numpy")
#autoinstall("import matplotlib")

from IPython.core.magic import register_line_magic
from sympy import pi,sin,cos,tan


precision = 5

# Common Electromagnetic Constants
c = 2.998e8
e0 = 8.854e-12
u0 = pi*4e-7
n0 = 376.7

# Common Conductivities
Scu = 5.813e7
Sau = 4.098e7
Sag = 6.173e7

# Common Functions
SWR = lambda gamma: sp.N((1+abs(gamma))/(1-abs(gamma)), precision)
ZatD = lambda z0, zl, B, l: sp.N(z0*(zl+1j*z0*tan(B*l))/(z0+1j*zl*tan(B*l)), precision)

## TODO:
# show variables and their values
# store variables persistently
#   add clear function to clear stored variables
# override lamba function so calling it with no arguments in the REPL returns definition instead of memory position

# Util functions
def reset():
    from IPython import get_ipython
    get_ipython().run_line_magic("reset", "")


# IPython config
from traitlets.config import Config
c = Config()
c.StoreMagics.autorestore = True
c.InteractiveShell.autocall = 2
c.InteractiveShell.ast_node_interactivity='last_expr_or_assign'

end = time()
print(f"\nDone in {end - start} seconds")

IPython.start_ipython(argv=[], user_ns=globals(), config=c)
