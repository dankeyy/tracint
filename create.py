def f():
    [];[][1]

def g():
    1, f()


try:
    1, g()
except Exception as e:
    tb = e.__traceback__


    # there's this small annoyance that the last -last-instruction- is relevant only in the context of the first frame
    # so we need to preserve a stack for the traces and walk backwards with the lasti-s
    # feels bad to be needing to allocate here, c'est la vie
    traces = []
    last_instructions = []
    while tb:
        traces.append(tb)
        last_instructions.append(tb.tb_lasti)
        tb = tb.tb_next
    frames_count = len(last_instructions)

    locations = []
    positions = None
    for ti, t in enumerate(traces):
        # i-th positions tuple means i-th instruction
        # as explained in https://docs.python.org/3/reference/datamodel.html#codeobject.co_positions
        for i, positions in enumerate(t.tb_frame.f_code.co_positions()):
            if i == last_instructions[frames_count - ti - 1]:
                break
        assert positions is not None # should _never_ be the case
        locations.extend(positions)

    print(locations)
