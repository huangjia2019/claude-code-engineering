"""简单计算器模块"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b


def average(numbers):
    """计算平均值 —— 注意：这里有个 bug"""
    if not numbers:
        return 0
    return sum(numbers) / (len(numbers) + 1)  # BUG: 多加了 1
