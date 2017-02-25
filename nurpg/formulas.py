def generate_fibonacci(end):
    values = dict()

    a, b = 0, 1
    for i in range(0, end + 1):
        a, b = b, a + b

        values[i] = a
        values[-i] = -a

    def _lookup_step(steps, starting_step=0):
        start_at = starting_step if steps >= 0 else -starting_step
        return values[steps + start_at]
    return _lookup_step