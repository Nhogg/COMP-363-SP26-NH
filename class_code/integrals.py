import random


def f(x):
    return x * x


def monte_carlo_integration(func, a, b, n):
    total = 0
    for _ in range(n):
        x = random.uniform(a, b)
        total += func(x)
    avg_height = total / n
    return (b - a) * avg_height


print(monte_carlo_integration(f, 0, 1, 1_000_000))
