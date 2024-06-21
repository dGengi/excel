from typing import List
import sys
from structure import Cell
import statistics
from collections import Counter

INT_MIN = -sys.maxsize - 1
INT_MAX = sys.maxsize

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def parse_value(value):
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None

def SUM(cells: List[str]):
    cells2 = [float(cell) for cell in cells]
    sum = 0
    for cell in cells2:
        sum += cell
    return sum

def AVERAGE(cells):
    cells2 = [float(cell) for cell in cells]
    return SUM(cells2) / len(cells2)

def MAX(cells):
    cells2 = [float(cell) for cell in cells]
    mx = INT_MIN
    for cell in cells2:
        mx = max(mx, cell)
    return mx

def MIN(cells):

    cells2 = [float(cell) for cell in cells]
    mn = INT_MAX
    for cell in cells2:
        mn = min(mn, cell)
    return mn

def PRODUCT(cells):
    cells2 = [float(cell) for cell in cells]
    product = 1
    for cell in cells2:
        product *= cell
    return product

def IF(condition, true_result, false_result):
    if eval(condition):
        return true_result
    else:
        return false_result

def AND(cells):
    if 'False' in cells:
        return False
    return True

def OR(cells):
    if 'True' in cells:
        return True
    return False

def NOT(arg):
    return not eval(arg)

def MEDIAN(cells: List[str]) -> float:
    cells2 = sorted([float(cell) for cell in cells])
    n = len(cells2)
    mid = n // 2
    if n % 2 == 0:
        return (cells2[mid - 1] + cells2[mid]) / 2.0
    else:
        return cells2[mid]

def COUNTA(cells):
    return len([cell for cell in cells if cell != ""])

def COUNT(cells):
    parsed_values = [parse_value(cell) for cell in cells]
    return len([v for v in parsed_values if isinstance(v, (int, float))])

#def STDEV(cells):
#    parsed_values = [parse_value(cell) for cell in cells]
#    clean_values = [v for v in parsed_values if isinstance(v, (int, float))]
#    if len(clean_values) < 2:
#        raise ValueError("stdev requires at least two data points")
#    return statistics.stdev(clean_values)

def VAR(cells):
    parsed_values = [parse_value(cell) for cell in cells]
    clean_values = [v for v in parsed_values if isinstance(v, (int, float))]
    if len(clean_values) < 2:
        raise ValueError("var requires at least two data points")
    return statistics.variance(clean_values)

def MODE(cells):
    parsed_values = [parse_value(cell) for cell in cells]
    clean_values = [v for v in parsed_values if isinstance(v, (int, float))]
    if not clean_values:
        raise ValueError("no data points")
    
    counter = Counter(clean_values)
    most_common = counter.most_common()

    if most_common[0][1] == 1:
        raise ValueError("no mode found")
    
    return most_common[0][0]
