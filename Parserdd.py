from column_conversion import *
#from structure import *
from funkcije import *
import re

funkcije = ['SUM', 'AVERAGE', 'MAX', 'MIN', 'PRODUCT', 'IF', 'AND', 'OR', 'NOT', 'MEDIAN', 'COUNT', 'COUNTA', 'VAR', 'MODE']
i = 0

def transform_intervals(tokens : list) -> list:
    new_list = []
    #j = 1 # ovo ne radi nista
    #last = tokens[0] # ovo se ne koristi
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
    
#def increment_char(char): # nije potrebno (koristis csti i cits)
#    ascii_value = ord(char)
#    incremented_ascii_value = ascii_value + 1
#    incremented_char = chr(incremented_ascii_value)
#    return incremented_char

def cell_range(range : str):
    left, right = split_string_by_colon(range)
    #print(left)
    x, y = split_letter_number(left)
    x1, y1 = split_letter_number(right)
    values = []

    x, x1 = cits(min(csti(x),csti(x1))), cits(max(csti(x),csti(x1)))
    y, y1 = min(y, y1), max(y, y1)

    while csti(x) <= csti(x1):
        i = y
        while i <= y1:
            values.append(f"{x}{i}")
            values.append(",")
            i+=1
        x = cits(csti(x)+1)
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

#expression = 'MAX(1, 3) - PRODUCT(1000, 20)'
#tokens = tokenize(expression)
#tokens = transform_intervals(tokens)
#print(tokens)
#sum = 0
#d = Spreadsheet()
#d.generate_cell('A', 1, 1)
#d.generate_cell('A', 2, 11)
#d.generate_cell('A', 3, 4)

def transform_cells(tokens, L, keys, graph):
    i=0
    l = len(tokens)
    while i<l:
        if is_excel_cell_format(tokens[i]):
            col, row = split_letter_number(tokens[i])
            col = csti(col) - 1
            row -= 1
            value = str(keys[(row, col)])
            if graph is not None:
                try:
                    graph[(row,col)]
                except KeyError:
                    graph[(row,col)] = []
                for cell in L:
                    if cell not in graph[(row, col)]:
                        graph[(row, col)].append(cell)
            if len(value)>0 and value[0] == "=":
                if (row, col) in L:
                    raise OverflowError()
                value = izvrsi(tokenize(value[1:]), L+[(row,col)], keys, graph)[0]
            
            tokens[i] = value
            if value == '' and i != 0 and i != len(tokens) - 1:
                if tokens[i-1] in "(," and tokens[i+1] in ",)":
                    if tokens[i-1] == ',':
                        tokens.pop(i-1)
                        tokens.pop(i-1)
                        i-=2
                        l-=2
                    elif tokens[i+1] == ',':
                        tokens.pop(i)
                        tokens.pop(i)
                        i-=1
                        l-=2
                    else:
                        tokens.pop(i)
                        i-=1
                        l-=1
        i+=1
    return (tokens, graph)

def transform_eq(tokens):
    for i in range(len(tokens)):
        if tokens[i] == "=" and tokens[i-1] not in "<>":
            tokens[i] = "=="
    return tokens

def transform(tokens, L, keys, graph):
    tokens = transform_intervals(tokens)
    tokens, graph = transform_cells(tokens, L, keys, graph)
    tokens = transform_eq(tokens)
    return (tokens, graph)

def izvrsi(tokens, L, keys, graph):
    tokens, graph = transform(tokens, L, keys, graph)
    tokens2 = []
    i = 0
    while i < len(tokens):
        if tokens[i] in funkcije:
            f = tokens[i]
            z=1
            for t in range(i+2, len(tokens)):
                if tokens[t] == '(': z+=1
                elif tokens[t] == ')':
                    z-=1
                    if z == 0:
                        kraj = t
                        break
            l1 = tokens[(i+2):kraj]
            print("l1 =", l1)
            l2 = []
            j = 0
            while j < len(l1):
                if l1[j] in funkcije:
                    z=1
                    for t in range(j+2, len(l1)):
                        if l1[t] == '(': z+=1
                        elif l1[t] == ')':
                            z-=1
                            if z == 0:
                                kraj2 = t
                                break
                    l2.append(l1[j:kraj2+1])
                    j = kraj2
                elif l1[j] != ',':
                    z = 0
                    zarez = j
                    while zarez < len(l1):
                        if l1[zarez] == '(': z += 1
                        elif l1[zarez] == ')':
                            z -= 1
                            if z<0: print("ne valja nesto")
                        elif l1[zarez] == ',' and z == 0:
                            break
                        zarez += 1
                    l2.append(l1[j:zarez])
                    j = zarez
                j+=1
            print("l2 =", l2)
            l3 = [izvrsi(token, L, keys, None)[0] for token in l2]
            print("l3 =", l3)
            if f == "SUM":
                tokens2.append(str(SUM(l3)))
            elif f == "AVERAGE":
                tokens2.append(str(AVERAGE(l3)))
            elif f == "MAX":
                tokens2.append(str(MAX(l3)))
            elif f == "MIN":
                tokens2.append(str(MIN(l3)))
            elif f == "PRODUCT":
                tokens2.append(str(PRODUCT(l3)))
            elif f == "IF":
                tokens2.append(str(IF(l3[0], l3[1], l3[2])))
            elif f == "AND":
                tokens2.append(str(AND(l3)))
            elif f == "OR":
                tokens2.append(str(OR(l3)))
            elif f == "NOT":
                tokens2.append(str(NOT(l3[0])))
            elif f == 'MEDIAN':
                tokens2.append(str(MEDIAN(l3)))
            elif f == 'COUNT':
                tokens2.append(str(COUNT(l3)))
            elif f == 'COUNTA':
                tokens2.append(str(COUNTA(l3)))
            elif f == 'VAR':
                tokens2.append(str(VAR(l3)))
            elif f == 'MODE':
                tokens2.append(str(MODE(l3)))
            i = kraj
        else:
            tokens2.append(tokens[i])
        i += 1
    new_expression = "".join(tokens2)
    return (str(eval(new_expression)), graph)

#e0 = "3+SUM(1,2)"
#e1 = "SUM(1,3*AVERAGE(3,2,1))"
#e2 = "PRODUCT(1, 2, SUM(3, 3, 5), 3)"
#e3 = "IF(2=3, 5, -1)"
#e4 = "NOT(AND(2=2, 3+3=6, OR(5+3=8, 2+2=5)))"

#print(izvrsi(tokenize(e0)))
#print(izvrsi(tokenize(e1)))
#print(izvrsi(tokenize(e2)))
#print(izvrsi(tokenize(e3)))
#print(izvrsi(tokenize(e4)))

def evaluate(formula: str, cell = None, keys = None, graph = None):
    value, graph = izvrsi(tokenize(formula), [cell], keys, graph)
    value = eval(value)
    if type(value)==float and round(value, 14) == round(value):
        value = round(value)
    return ( value, graph)


#print(evaluate(e4, None))
