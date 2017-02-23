def generate_fibonacci(end):
    values = dict()

    a, b = 0, 1
    for i in range(0, end + 1):
        a, b = b, a + b
        values[i] = a

    return lambda s: values[s]
