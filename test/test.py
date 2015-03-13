
import numba

@numba.autojit
def add(a, b):
    return a + b

print add(5, 9)