import time

try:
    import timeout_decorator
except ImportError:
    raise ImportError(
        "Requires Package timeout_decorator!\nYou can install it by pip install timeout-decorator")
try:
    from timeout import timeout
except ImportError("Requires Package timeout!\nYou can install it by pip install timeout")


def main():
    try:
        info2()
    except Exception as e:
        print(e)

    try:
        info1()
    except Exception as e:
        print(e)

    return


@timeout_decorator.timeout(3)
def info1():
    while(True):
        continue


@timeout_decorator.timeout(3)
def info2():
    time.sleep(2)
    print("func info2 didn't timeout")
    return


main()
