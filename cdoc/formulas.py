def _generate_fibonacci_values(end):
    values = dict()
    
    a, b = 0, 1
    for i in range(0, end + 1):
        a, b = b, a + b
        values[i] = a
        
    return values


def Fibonacci(end):
    values = _generate_fibonacci_values(end)
    
    def _fib(step):
        return values[step]
    
    return _fib