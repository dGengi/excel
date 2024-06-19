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
def slovo(a):
    s=""
    for i in range(len(a)):
        if (a[i].isnumeric()):
            break
        s=s+a[i]
    return s
def broj(a):
    s=""
    for i in range(len(slovo(a)),len(a)):
        s=s+a[i]
    return s


def select(a,b):
    slovo1=a[0]
    slovo2=b[1]
    broj1

def selektovana_polja(a,b):
    t=[]
    slova1=slovo(a)
    slova2=slovo(b)
    broj1=int(broj(a))
    broj2=int(broj(b))
    vrednost1=csti(slova1)
    vrednost2=csti(slova2)
    for i in range(abs(vrednost1-vrednost2)+1):
        for j in range(abs(broj1-broj2)+1):
            p=cits(i+1)+str(j+1)
            t.append(p)
            t.append(",")
