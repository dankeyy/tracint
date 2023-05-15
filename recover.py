# [17, 17, 7, 10, 15, 15, 7, 10, 12, 12, 7, 12]

# Traceback (most recent call last):
#   File "/home/dankey/dev/projects/traceback_recoverer/create.py", line 16, in <module>
#     1, g()
#        ^^^
#   File "/home/dankey/dev/projects/traceback_recoverer/create.py", line 15, in g
#     1, f()
#        ^^^
#   File "/home/dankey/dev/projects/traceback_recoverer/create.py", line 12, in f
#     [];[][1]
#        ~~^^^
# IndexError: list index out of range

import sys
import ast

import jedi

entryfile = sys.argv[1]
locations = ast.literal_eval(sys.argv[2])

# with the assumption that recover is run from the top level project dir


print(entryfile, locations)
