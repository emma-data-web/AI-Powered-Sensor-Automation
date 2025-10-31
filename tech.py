def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


print(factorial(30))


def fibonnacti(n):
    a , b = 0 ,1
    for _ in range(n):
        a, b = b , a + b
    return a , b


print(fibonnacti(20))