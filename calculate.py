#v0.3

## TODO:
# open another window (GUI) to display defined variables
# store variables persistently
#   add clear function to clear stored variables

import sys
from time import time

start = time()
print("Intializing.", end="", flush=True)

def autoinstall(import_statement):
    try:
        exec(import_statement, globals())
    except ModuleNotFoundError as missing_pkg:
        inp = input(f"\nPackage '{missing_pkg.name}' required. Install it now? (y/N): ")
        if "y" in inp.lower():
            try:
                import subprocess
                subprocess.check_call([sys.executable, "-m", "pip", "install", missing_pkg.name])
                print("\n")
                exec(import_statement, globals())
            except Exception as e:
                print(e)
                input("Press any key to exit")
                exit()
        else:
            exit()
    finally:
        print(".", end="", flush=True)



# Load dependencies
autoinstall("import IPython")
autoinstall("import sympy as sp")
#autoinstall("import matplotlib")


from IPython import get_ipython
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



# Util functions
def clear(opt=None):
    try:
        opt = opt.__name__ # dirty hack
    except:
        pass

    if not opt:
        get_ipython().run_line_magic("reset", "-fs")
    elif opt.lower() == "all": 
        get_ipython().run_line_magic("reset", "-fs in out")

def vars():
    get_ipython().run_line_magic("whos", "")


# IPython config
from traitlets.config import Config
c = Config()
c.StoreMagics.autorestore = True
c.InteractiveShell.autocall = 2
c.InteractiveShell.ast_node_interactivity='last_expr_or_assign'

end = time()
print(f"\nDone in {end - start} seconds")

IPython.start_ipython(argv=[], user_ns=globals(), config=c)
