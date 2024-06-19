from typing import List
import sys
from structure import Cell

INT_MIN = -sys.maxsize - 1
INT_MAX = sys.maxsize

def SUM(cells: List[int]):
    sum = 0
    for cell in cells:
        sum += cell
    return sum

def AVERAGE(cells):
    return SUM(cells) / len(cells)

def MAX(cells):
    mx = INT_MIN
    for cell in cells:
        mx = max(mx, cell)
    return mx

def MIN(cells):
    mn = INT_MAX
    for cell in cells:
        mn = min(mn, cell)
    return mn

def PRODUCT(cells):
    product = 1
    for cell in cells:
        product *= cell
    return product

def IF(condition, true_result, false_result):
    if eval(condition):
        return true_result
    else:
        return false_result

def AND(*args):
    return all(eval(arg) for arg in args if isinstance(arg, str))

def OR(*args):
    return any(eval(arg) for arg in args if isinstance(arg, str))

def NOT(arg):
    return not eval(arg)