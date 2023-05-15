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

    relevant = line[start_col: end_col]
    actual_call = relevant.rfind('.')
    col = start_col if actual_call == -1 else actual_call + 1 + start_col # calls by some sort of namespace
    res = j.goto(start_line, col, follow_imports=True, follow_builtin_imports=True)
    if res:
        path = str(res[0].module_path)
    else:
        break

    j = jedi.Script(path=path)
