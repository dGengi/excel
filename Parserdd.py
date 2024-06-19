from column_conversion import *
from structure import *
from funkcije import *
import re

funkcije = ['SUM', 'AVERAGE', 'MAX', 'MIN', 'PRODUCT', 'IF', 'AND', 'OR', 'NOT']
i = 0

def transform_intervals(tokens : list) -> list:
    new_list = []
    j = 1
    last = tokens[0]
    for j in range(len(tokens)):
        if tokens[j] == ':':
            simplified = cell_range(str(tokens[j - 1]) + str(tokens[j]) + str(tokens[j + 1]))
            simplified.pop(len(simplified) - 1)
            #print(tokens)
            #print(simplified)
            new_list.extend(simplified)
        else:
            if j == 0 or j == len(tokens) - 1:
                new_list.append(tokens[j])
                continue
            if tokens[j - 1] != ':' and tokens[j + 1] != ':':
                new_list.append(tokens[j])

    return new_list

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
    print(left)
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

def get_argument(tokens : list):
    global i
    argument = ""
    while i < len(tokens):
        if tokens[i] == ',':
            break
        if is_number(tokens[i]) or tokens[i] in "*/+-":
            argument += tokens[i]
        elif is_excel_cell_format(tokens[i]):
            alpha, digit = split_letter_number(tokens[i])
            argument += str(d.cells[alpha][digit].value)
        elif tokens[i] in funkcije:
            last_i = i
            tokens_copy = ""
            j = i
            while j < len(tokens):
                if tokens[j] == ')':
                    tokens_copy += ')'
                    break
                tokens_copy += tokens[j]
                j+=1
            tokens_copy = tokenize(tokens_copy)
            #print(tokens_copy)
            i = 0
            argument += str(evaluate_expression(tokens_copy))
            i = last_i
            while tokens[i] != ')':
                i+=1
            #print(i)
            continue
        i+=1
    return eval(argument)

def get_arguments(tokens : list):
    global i
    arguments = []
    while i < len(tokens):
        if tokens[i] == ')':
            break
        arguments.append(get_argument(tokens))
        i+=1
    return arguments

def evaluate_expression(tokens : list):
    sum = 0
    global i
    while i < len(tokens):
        if tokens[i] in funkcije:
            function_name = tokens[i]
            i+=2
            arguments = get_arguments(tokens)
            print(arguments)
            if function_name == 'SUM':
                sum += SUM(arguments)
            elif function_name == 'AVERAGE':
                sum += AVERAGE(arguments)
            elif function_name == 'MAX':
                sum += MAX(arguments)
            elif function_name == 'MIN':
                sum += MIN(arguments)
            elif function_name == 'PRODUCT':
                sum += PRODUCT(arguments)
        i+=1
    return sum

expression = 'PRODUCT(A1:A3) + MAX(A1, A2)'
tokens = tokenize(expression)
print(tokens)
tokens = transform_intervals(tokens)
print(tokens)
sum = 0
d = Spreadsheet(100, 100)
d.generate_cell('A', 1, 1)
d.generate_cell('A', 2, 11)
d.generate_cell('A', 3, 4)
print(evaluate_expression(tokens))
