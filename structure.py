from typing import List
from column_conversion import *

class Cell:
    def __init__(self, col: str, row: int, value: any | None = None): # ako ne napisemo vrednost racunamo None
        self.col = col
        self.row = row
        self.value = value

class Spreadsheet:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        cells: dict[dict[Cell]] = {}
    
    def generate_cell(self, col: str, row: int, value: any | None = None):
        cell = Cell(col, row, value)
        self.cells[col][row] = cell
    
    # generate_all_cells generise sve celije u tabeli sto trosi memoriju
    # i vreme, najbolje je da se ovo koristi samo za male tabele
    # a za vece tabele generisati celiju tek kad nam je ona potrebna
    def generate_all_cells(self):
        for i in range(1, self.height+1):
            for j in range(1, self.width+1):
                self.generate_cell(cits(i), j)
    
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
                    if cell.value is not None:
                        L.append(cell)
                except:
                    pass
        
        return L