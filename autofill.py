from Parserdd import transform_cells
from spreadsheet import SpreadsheetApp
from column_conversion import *

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
            #t.append(",")



# x i y su krajnja selektovana polja recimo A1 i A5
#b je broj polja koje autofilujemo
def pattern(x,y,ss:SpreadsheetApp,b):
    a = transform_cells(selektovana_polja(x,y),ss)
    t=0
    p=[]
    for x in a:
        if not (x.isnumeric()):
            t=1
    if (t!=0):
        for i in range(b):
            p.append(a[i%len(a)-1])
    else:
        s=0
        for x in a:
            s=s+int(x)-int(a[0])
        s=s/len(a)
        c=int(a[len(a)-1])
        for i in range(b):
            c=c+s
            p.append(c)
    return(p)
#funkcija vraca listu stringova cime treba da upotpunimo autofilana polja