from column_conversion import *
from structure import *
from funkcije import *
import re

funkcije = ['SUM', 'AVERAGE', 'MAX', 'MIN', 'PRODUCT', 'IF', 'AND', 'OR', 'NOT']

def tokenize(expression):
    tokens = []
    current_token = ''
    for char in expression:
        if char.isalnum() or char == '.':
            current_token += char
        else:
            if current_token:
                tokens.append(current_token)
                current_token = ''
            if char in '+-*/(),<>=:':
                tokens.append(char)
    if current_token:
        tokens.append(current_token)
    return tokens

def split_string_by_colon(input_string):
    left, right = input_string.split(':')
    return left.strip(), right.strip()

def split_letter_number(reference):
    match = re.search(r"\d", reference)
    if match:
        index = match.start()
        letter_part = reference[:index]
        number_part = int(reference[index:])
        return letter_part, number_part
    else:
        return None, None
    
def increment_char(char):
    ascii_value = ord(char)
    incremented_ascii_value = ascii_value + 1
    incremented_char = chr(incremented_ascii_value)
    return incremented_char

def cell_range(range : str):
    left, right = split_string_by_colon(range)
    x, y = split_letter_number(left)
    x1, y1 = split_letter_number(right)
    values = []
    while x <= x1:
        i = y
        while i <= y1:
            values.append(f"{x}{i}")
            values.append(",")
            i+=1
        x = increment_char(x)
    return values
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def is_excel_cell_format(s):
    pattern = re.compile(r'^[A-Z]+[0-9]+$')
    return bool(pattern.match(s))

def get_argument(tokens : str, i : int) -> tuple[str, int]: #sta ako 3 + sum(1,2)
    argument = ""
    while i < len(tokens) and tokens[i] != ',':
        if (is_excel_cell_format(tokens[i])):
            a, b = split_letter_number(tokens[i])
            argument += str(d.cells[a][b].value)
        elif (tokens[i] in "*/+-" or is_number(tokens[i])):
            argument += tokens[i]
        elif tokens[i] in funkcije:
            argument += str(calculate_expression(tokens, i))
            while tokens[i] != ')':
                i+=1
            i += 2
            #print(i)
            print(argument)
            continue
        i+=1
    #print(argument)
    return eval(argument), i


def get_args(tokens : str, i : int):
    arguments = []
    while i < len(tokens) and tokens[i] != ')':
        argument, i = get_argument(tokens, i)
        arguments.append(argument)
        i+=1
    return arguments, i
            

def calculate_expression(tokens : list, i : int) -> str:
    sum = 0
    if i >= len(tokens):
        return
    if is_number(tokens[i]):
        if i == len(tokens) - 1:
            return tokens[i]
        else:
            return eval(tokens[i] + "" + tokens[i] + calculate_expression(tokens, i + 2))
    if tokens[i] in funkcije:
        last = tokens[i]
        args, i = get_args(tokens, i + 2)
        if last == 'SUM':
            sum += SUM(args)
        elif last == 'AVERAGE':
            sum += AVERAGE(args)
        elif last == 'MAX':
            sum += MAX(args)
        elif last == 'MIN':
            sum += MIN(args)
        elif last == 'PRODUCT':
            sum += PRODUCT(args)
    return sum


expression = 'PRODUCT(SUM(A1, A2, A3), A2, A3)'
tokens = tokenize(expression)

print(tokens)

sum = 0

d = Spreadsheet(100, 100)
d.generate_cell('A', 1, 1)
d.generate_cell('A', 2, 3)
d.generate_cell('A', 3, 4)

print(calculate_expression(tokens, 0))