def f():
    [];[][1]

def g():
    1, f()


try:
    1, g()

except Exception as e:
    l = []
    t = e.__traceback__
    positions = None
    while t:
        for i, positions in enumerate(t.tb_frame.f_code.co_positions()):
            if t.tb_next and i == t.tb_next.tb_lasti:
                break
        l.extend(positions)
        t = t.tb_next
    print(l)
