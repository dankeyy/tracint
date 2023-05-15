from create import print_list
import tests.a

try:
    tests.a.g()
except Exception as e:
    print_list(e)

# [5, 5, 4, 15, 4, 4, 4, 7, 2, 2, 4, 9]
