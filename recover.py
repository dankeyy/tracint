# [11, 11, 16, 18, 5, 5, 4, 7, 2, 2, 4, 9]


#   File "/home/dankey/dev/projects/traceback_recoverer/create.py", line 27, in <module>
#     g()
#   File "/home/dankey/dev/projects/traceback_recoverer/create.py", line 5, in g
#     f()
#   File "/home/dankey/dev/projects/traceback_recoverer/create.py", line 2, in f
#     [][1]
#     ~~^^^

# currently there's an issue in cpython causing the first frame numbers to be wrong,
# but just so we could continue on, i call the script with the first 4 numbers dropped
#
# sample run:
# python recover.py create.py "[5, 5, 4, 7, 2, 2, 4, 9]"
# Traceback (most recent call last):
# File "/home/dankey/dev/projects/traceback_recoverer/create.py", line 5, in <module>
#     f()
#     ^^^
# File "/home/dankey/dev/projects/traceback_recoverer/create.py", line 2, in f
#     [][1]
#     ^^^^^


import sys
import os
import ast
import linecache

import jedi

entrypoint = path = os.path.abspath(sys.argv[1])
locations = ast.literal_eval(sys.argv[2])

# with the assumption that recover is run from the top level project dir
j = jedi.Script(path=entrypoint)
res = None

print("Traceback (most recent call last):")

for i in range(0, len(locations), 4):
    # imagine slicing
    start_line = locations[i]
    end_line   = locations[i + 1]
    start_col  = locations[i + 2]
    end_col    = locations[i + 3]

    site = res[0].name if res else "<module>"
    print(f"File \"{path}\", line {start_line}, in {site} ")
    line = linecache.getline(path, start_line)
    print(line, end='')
    print(' ' * start_col + '^' * (end_col - start_col))

    res = j.goto(start_line, start_col, follow_imports=True, follow_builtin_imports=False)
    if res:
        path = str(res[0].module_path)
    else:
        break

    j = jedi.Script(path=path)
