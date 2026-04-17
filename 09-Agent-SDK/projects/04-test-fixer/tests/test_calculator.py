"""calculator 模块的测试"""

import sys
import os

# 把 src/ 加入路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from calculator import add, subtract, multiply, divide, average


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0


def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 5) == 0


def test_divide():
    assert divide(10, 2) == 5.0
    assert divide(7, 2) == 3.5


def test_divide_by_zero():
    try:
        divide(1, 0)
        assert False, "应该抛出 ValueError"
    except ValueError:
        pass


def test_average():
    """这个测试会失败 —— 因为 average() 有 bug"""
    assert average([1, 2, 3]) == 2.0
    assert average([10, 20]) == 15.0
    assert average([]) == 0
