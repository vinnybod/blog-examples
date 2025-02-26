from src import lib_b, lib_c

lib_b.foo()
lib_c.foo()


def foo():
    print("foo from lib_a")
