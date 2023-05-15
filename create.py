def f():
    [][1]

def g():
    f()

try:
    g()
except Exception as e:
    tb = e.__traceback__
    locations = []
    positions = None

    while tb:
        # i-th positions tuple means i-th instruction
        # as explained in https://docs.python.org/3/reference/datamodel.html#codeobject.co_positions
        for i, positions in enumerate(tb.tb_frame.f_code.co_positions()):
            if i == tb.tb_lasti:
                break
        assert positions is not None # should _never_ be the case
        locations.extend(positions)
        tb = tb.tb_next

    print(locations)
