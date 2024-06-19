from typing import List
from column_conversion import *
import csv
from matrix_inversion import invert

class Cell:
    def __init__(self, col: str, row: int, value):
        self.col = col
        self.row = row
        self.value = value

class Spreadsheet:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells: dict[dict[Cell]] = {}
    
    def generate_cell(self, col: str, row: int, value):
        if value != None:
            cell = Cell(col, row, value)
            try:
                self.cells[col][row] = cell
            except:
                self.cells[col] = {}
                self.cells[col][row] = cell
    
    def edit_cell(self, col: str, row: int, value):
        self.cells[col][row].value = value
        if value is None:
            self.remove_cell(col, row)

    def remove_cell(self, col: str, row: int):
        try:
            self.cells[col].pop(row)
            if len(self.cells[col]) == 0:
                self.cells.pop(col)
        except:
            pass # polje nije postojalo 
    
    def cell_range(self, cell1: Cell, cell2: Cell) -> List[Cell]:
        columns = (csti(cell1.col), csti(cell2.col))
        rows = (cell1.row, cell2.row)

        colMin, colMax = min(columns), max(columns)
        rowMin, rowMax = min(rows), max(rows)

        L = []

        for i in range(colMin, colMax+1):
            for j in range(rowMin, rowMax+1):
                try:
                    cell=self.cells[cits(i)][j]
                    #if cell.value is not None: # vrednost celije nikad ne bi trebalo da bude None
                    L.append(cell)
                except KeyError:
                    pass
        
        return L
    
    def importCSV(self, file_location: str):
        self.cells = {}
        with open(file_location, newline='') as f:
            lines = list(csv.reader(f))
            for i in range(len(lines)):
                line = lines[i]
                for j in range(len(line)):
                    if line[j] != "":
                        self.generate_cell(cits(j+1), i+1, line[j])
    
    def exportCSV(self, file_location: str):
        with open(file_location, 'w', newline='') as f:
            csvwriter = csv.writer(f)
            keys = list(self.cells.keys())
            for i in range(len(keys)):
                keys[i] = csti(keys[i])
            keys.sort()
            length = keys[-1]
            height = 0
            #self.cells = {k: self.cells[k] for k in keys}
            #l = len(self.cells)
            #k=0
            #i=1
            #while k<l:
            matrix = []
            pk = 0
            for k in keys:
                for i in range(pk+1, k):
                    matrix.append([])
                l = []
                #int_columns = []
                #for col in self.cells[k]:
                #    int_columns.append(csti(col))
                keys2=sorted(self.cells[cits(k)])
                if keys2[-1] > height:
                    height = keys2[-1]
                pk2=0
                for k2 in keys2:
                    l += [None]*(k2-pk2-1)
                    l.append(self.cells[cits(k)][k2].value)
                    pk2 = k2
                matrix.append(l)
                pk = k
            matrixInv = invert(matrix, length, height)
            for row in matrixInv:
                csvwriter.writerow(row)
            
            #zavrsi ovo sranje
                    


    
tabela = Spreadsheet(4, 4)

tabela.importCSV("tabela neka.csv")
tabela.generate_cell("A", 2, 1233)
tabela.remove_cell("D", 4)
for i in range(4):
    for j in range(4):
        try:
            print(tabela.cells[cits(j+1)][i+1].value, end=' ')
        except KeyError:
            print("/", end=' ')
    print()

tabela.exportCSV("export test.csv")


# nova_matrica[i][j] = stara_matrica[j][i]

