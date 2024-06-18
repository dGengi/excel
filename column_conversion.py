from string import ascii_uppercase #niz A,B,C,...,Z

def col_str_to_int(col: str) -> int:
    result = 1
    l = len(col)
    for i in range(1, l):
        result += 26**i
    for i in range(l):
        ind = ascii_uppercase.index(col[i])
        result += ind * 26**(l-1-i)
    return result

def col_int_to_str(col: int) -> str:
    result = ""
    while(col>0):
        letterInd = (col-1)%26
        col = (col-1)//26
        result = ascii_uppercase[letterInd] + result
    return result

# mrzi me da pisem col_str_to_int i col_int_to_str svaki put
def csti(col: str) -> int:
    return col_str_to_int(col)
def cits(col: int) -> str:
    return col_int_to_str(col)
