import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import matplotlib.pyplot as plt
import platform
from Parserdd import *
from column_conversion import *


class SpreadsheetApp:
    def __init__(self, root, rows=5, columns=10):
        self.root = root
        style = ttk.Style(root)
        style.theme_use('default')
        self.root.title("Spreadsheet")
        self.text_content = ""
        self.rows = rows
        self.columns = columns
        self.selected_cell = None
        self.previous_cell = None
        self.entries = {}
        self.variables = {}
        self.keys = {}
        self.prevent_navigation = False
        self.cell_height=0
        self.cell_width=0
        self.upper_distance=0
        self.left_distance=0
        
        if platform.system() == 'Windows':
            self.cell_height=20.86
            self.cell_width=76.3
            self.left_distance=40
            self.upper_distance=70
        if platform.system() == 'Linux':
            self.cell_height=24.7
            self.cell_width=85.8
            self.left_distance=45
            self.upper_distance=92

        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.counter=0

        self.create_widgets()
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<ButtonRelease-1>", self.end_drag)
        self.root.bind("<Return>",self.on_down)

        self.update_window_position()

    def update_window_position(self):
        self.window_x = self.root.winfo_rootx()
        self.window_y = self.root.winfo_rooty()
        self.root.after(100, self.update_window_position)

    def start_drag(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        if self.start_y - self.window_y - self.upper_distance > self.rows * self.cell_height or self.start_x - self.window_x - self.left_distance > self.cell_width * (self.columns) or self.start_x - self.window_x < self.left_distance or self.start_y - self.window_y < self.upper_distance:
            return
        

    def end_drag(self, event):
        self.end_x = event.x_root
        self.end_y = event.y_root
        if self.start_y - self.window_y - self.upper_distance > self.rows * self.cell_height or self.start_x - self.window_x - self.left_distance > self.cell_width * (self.columns) or self.start_x - self.window_x < self.left_distance or self.start_y - self.window_y < self.upper_distance:
            return
        if self.start_x == self.end_x and self.start_y == self.end_y:
            self.single_click_select()
        else:
            self.select_cells_in_rectangle(self.start_x, self.start_y, self.end_x, self.end_y)

    def create_widgets(self):
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=0, columnspan=self.columns + 1, padx=5, pady=5)

        self.text_box = tk.Text(button_frame, height=2, width=25)
        self.text_box.grid(row=0, column=0, padx=5, pady=1)
        self.text_box.bind("<KeyRelease>", self.update_text_content)

        self.load_button = tk.Button(button_frame, height=2, width=15, text='Load CSV file', command=self.load_csv)
        self.load_button.grid(row=0, column=2, padx=5, pady=1)

        self.save_button = tk.Button(button_frame, height=2, width=15, text='Save CSV file', command=self.save_csv)
        self.save_button.grid(row=0, column=3, padx=5, pady=1)

        self.clear_button = tk.Button(button_frame, height=2, width=15, text='Clear', command=self.clear_cells)
        self.clear_button.grid(row=0, column=4, padx=5, pady=1)

        self.save_chart_button = tk.Button(button_frame, height=2, width=15, text='Save Bar Chart', command=self.save_bar_chart)
        self.save_chart_button.grid(row=0, column=5, padx=5, pady=1)

        self.add_row_button = tk.Button(button_frame, height=2, width=15, text='Add Row', command=self.add_row)
        self.add_row_button.grid(row=0, column=6, padx=5, pady=1)

        self.add_column_button = tk.Button(button_frame, height=2, width=15, text='Add Column', command=self.add_column)
        self.add_column_button.grid(row=0, column=7, padx=5, pady=1)
        
        

        self.canvas = tk.Canvas(self.root)
        self.canvas.grid(row=1, column=0, sticky='nsew')

        self.v_scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.grid(row=1, column=1, sticky='ns')
        self.h_scrollbar = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.grid(row=2, column=0, sticky='ew')

        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        for col in range(self.columns):
            label = tk.Label(self.inner_frame, text=self.get_column_letter(col), relief=tk.RIDGE, width=10)
            label.grid(row=1, column=col + 1)

        for row in range(self.rows):
            label = tk.Label(self.inner_frame, text=str(row + 1), relief=tk.RIDGE, width=5)
            label.grid(row=row + 2, column=0)
            for col in range(self.columns):
                var = tk.StringVar()
                entry = tk.Entry(self.inner_frame, textvariable=var, relief=tk.RIDGE, width=10, highlightcolor='gray', highlightthickness=1)
                entry.grid(row=row + 2, column=col + 1)
                self.entries[(row, col)] = entry
                self.variables[(row, col)] = var
                
                entry.bind("<Down>", self.on_down)
                entry.bind("<Up>", self.on_up)
                entry.bind("<Right>", self.on_right)
                entry.bind("<Left>", self.on_left)
                entry.bind("<KeyRelease>", self.update_text_box_content)
                entry.bind("<Tab>", self.on_right)
                

        self.deselect_all_cells()

        
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def get_column_letter(self, col):
        letter = ''
        while col >= 0:
            letter = chr(col % 26 + ord('A')) + letter
            col = col // 26 - 1
        return letter
    
    

    def formula_eval(self,row=-1,col=-1):
    
        if(row,col)==self.previous_cell:
            self.counter+=1

        value = str(self.variables[(row, col)].get())
        
        
        for rows in range(self.rows):
            for columns in range(self.columns):
                if not (rows,columns) in self.keys and (rows,columns) in self.variables:
                    self.keys[(rows,columns)]=self.variables[(rows,columns)].get()
        
        
    
      #  print(value)
        if (row,col) and value:
            print("jel 2")
            #print(value)
            if(value[0] == '='):
                try:
                    self.keys[(row,col)]=self.variables[(row,col)].get()
                  #  print(value)
                    self.variables[(row,col)].set(evaluate(value[1:],(row,col),self.keys))
                   # print(self.keys)
                    
                except:
                    self.variables[(row,col)].set("#ERROR!")
            else:
                print("dajebeno")
                if (row,col) == self.previous_cell and self.counter==1:
                    self.keys[(row,col)]=self.variables[(row,col)].get()
                    
                elif (row,col)!= self.previous_cell:
                    pass

                    # print(self.keys)
                   # if self.keys[(row,col)] and self.keys[(row,col)][0]!='=':
                     #   self.keys[(row,col)]=(self.variables[(row,col)].get())
                        #print(self.keys)
                
                    
        

            
        

    def update_text_content(self, event):
        self.text_content = self.text_box.get("1.0", tk.END).strip()
        if self.selected_cell:
            row, col = self.selected_cell
            self.variables[(row, col)].set(self.text_content)

    def on_tab(self, event):
        row, col = self.get_current_cell(event.widget)
        next_col = (col + 1) % self.columns
        self.focus_cell(row, next_col)
        
        self.update_text_box_content(None)
        return "break"

    def on_return(self, event):
        row, col = self.get_current_cell(event.widget)
        next_row = (row + 1) % self.rows
        self.focus_cell(next_row, col)
        
        self.update_text_box_content(None)
        return "break"

    def on_down(self, event):
        row, col = self.selected_cell
        next_row = (row + 1) % self.rows
        self.focus_cell(next_row, col)
        
        self.update_text_box_content(None)
        return "break"

    def on_up(self, event):
        row, col = self.get_current_cell(event.widget)
        prev_row = (row - 1) % self.rows
        self.focus_cell(prev_row, col)
        
        self.update_text_box_content(None)
        return "break"

    def on_right(self, event):
        row, col = self.get_current_cell(event.widget)
        next_col = (col + 1) % self.columns
        self.focus_cell(row, next_col)
        
        self.update_text_box_content(None)
        return "break"

    def on_left(self, event):
        row, col = self.get_current_cell(event.widget)
        prev_col = (col - 1) % self.columns
        self.focus_cell(row, prev_col)
        
        self.update_text_box_content(None)
        return "break"

    def get_current_cell(self, widget):
        for (r, c), entry in self.entries.items():
            if entry == widget:
                return r, c
        return None, None

    def focus_cell(self, row, col):
        
            
        self.entries[(row, col)].focus_set()
        self.deselect_all_cells()
        self.entries[(row, col)].config(bg='lightblue', highlightbackground='black', highlightcolor='black', highlightthickness=1)
        self.selected_cell = (row, col)
        
        if self.selected_cell in self.keys:
            self.variables[self.selected_cell].set(self.keys[self.selected_cell])
      #  print(row,col)

    def update_text_box_content(self, event):
        if self.selected_cell:
            row, col = self.selected_cell
            self.text_content = self.variables[(row, col)].get()
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, self.text_content)

    def deselect_all_cells(self):
        if self.selected_cell:
            red,kol=self.selected_cell
            self.previous_cell=self.selected_cell
            self.counter=0
            self.formula_eval(red,kol)

        for entry in self.entries.values():
            entry.config(bg='white', highlightbackground='gray', highlightcolor='gray', highlightthickness=1)
        for row in range(self.rows):
            for col in range(self.columns):
                self.formula_eval(row,col)


    def select_cells_in_rectangle(self, x, y, z, g):
        start_row, start_col = self.get_cell_from_position(self.start_x, self.start_y)
        end_row, end_col = self.get_cell_from_position(self.end_x, self.end_y)
        if start_row is None:
            start_row = 0
        if start_col is None:
            start_col = 0
        if end_row is None:
            end_row = self.rows - 1
        if end_col is None:
            end_col = self.columns - 1
        self.focus_cell(start_row, start_col)
        self.selected_cell = (start_row, start_col)
        self.update_text_box_content(None)
        top_row = min(start_row, end_row)
        bottom_row = max(start_row, end_row)
        left_col = min(start_col, end_col)
        right_col = max(start_col, end_col)

        for entry in self.entries.values():
            entry.config(bg='white', highlightbackground='gray', highlightcolor='gray', highlightthickness=1)

        for row in range(top_row, bottom_row + 1):
            for col in range(left_col, right_col + 1):
                self.entries[(row, col)].config(bg='lightblue', highlightbackground='black', highlightcolor='black', highlightthickness=1)
    def get_cell_from_position(self, x, y):
        row = int((y - self.window_y - self.upper_distance) // self.cell_height)
        col = int((x - self.window_x - self.left_distance) // self.cell_width)
        if 0 <= row < self.rows and 0 <= col < self.columns:
            return row, col
        return None, None

    def single_click_select(self):
        row,col = self.get_cell_from_position(self.start_x,self.start_y)
        self.focus_cell(row, col)
        self.update_text_box_content(None)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                for r, row in enumerate(reader):
                    for c, val in enumerate(row):
                        if r < self.rows and c < self.columns:
                            self.variables[(r, c)].set(val)
                            self.keys[(r,c)]=val
                        

    def save_csv(self):
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                for r in range(self.rows):
                    row = [self.keys[(r, c)] for c in range(self.columns)]
                    writer.writerow(row)
            messagebox.showinfo("Save CSV", "CSV file saved successfully.")

    def is_decimal(self,value):
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    def save_bar_chart(self):
        selected_entries = []
        
        
        
        for (row, col), entry in self.entries.items():
            if entry.cget("bg") == 'lightblue':
                selected_entries.append((row, col))
            
        if len(selected_entries) < 2:
            messagebox.showerror("Error", "Please select at least two columns")
            return

        selected_cols = set(col for row, col in selected_entries)
        selected_rows = set(row for row, col in selected_entries)
        
        col1, col2 = list(selected_cols)
      #  print(col1)
        
        if len(selected_cols) != 2:
            messagebox.showerror("Error", "Please select exactly two columns")
            return

        col1, col2 = list(selected_cols)
        
        names = []
        values = []
        
        col1_is_int = all(self.is_decimal(self.variables[(row, col1)].get()) for row in selected_rows if self.variables[(row, col1)].get())
        col2_is_int = all(self.is_decimal(self.variables[(row, col2)].get()) for row in selected_rows if self.variables[(row, col2)].get())
        
        if not col1_is_int and not col2_is_int:
            messagebox.showerror("Error", "One of the selected columns must contain only integers")
            return
        
        if col1_is_int and col2_is_int:
            for row in selected_rows:
                name = self.variables[(row, col1)].get()
                value = self.variables[(row, col2)].get()
                if name and value:
                    names.append(name)
                    values.append(float(value))
        elif col1_is_int:
            for row in selected_rows:
                value = self.variables[(row, col1)].get()
                name = self.variables[(row, col2)].get()
                if name and value:
                    names.append(name)
                    values.append(float(value))
        else:
            for row in selected_rows:
                name = self.variables[(row, col1)].get()
                value = self.variables[(row, col2)].get()
                if name and value:
                    names.append(name)
                    values.append(float(value))

        plt.figure(figsize=(10, 6))
        plt.bar(names, values, color='blue')
        plt.xlabel('Names')
        plt.ylabel('Values')
        plt.title('Bar Chart')
        
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg")])
        if not file_path:
            return
        
        plt.savefig(file_path)
        plt.close()
        messagebox.showinfo("Success", f"Bar chart saved as {file_path}")

    def clear_cells(self):
        for var in self.variables.values():
            var.set("")
        for row in range(self.rows):
            for col in range(self.columns):
                self.keys[(row,col)]=''
     #   print(self.keys)
        self.update_text_box_content(None)
        

    def add_row(self):
        new_row = self.rows
        self.rows += 1
        label = tk.Label(self.inner_frame, text=str(new_row + 1), relief=tk.RIDGE, width=5)
        label.grid(row=new_row + 2, column=0)
        for col in range(self.columns):
            var = tk.StringVar()
            entry = tk.Entry(self.inner_frame, textvariable=var, relief=tk.RIDGE, width=10, highlightcolor='gray', highlightthickness=1)
            entry.grid(row=new_row + 2, column=col + 1)
            self.entries[(new_row, col)] = entry
            self.variables[(new_row, col)] = var
            entry.bind("<Tab>", self.on_tab)
            entry.bind("<Return>", self.on_return)
            entry.bind("<Down>", self.on_down)
            entry.bind("<Up>", self.on_up)
            entry.bind("<Right>", self.on_right)
            entry.bind("<Left>", self.on_left)
            entry.bind("<KeyRelease>", self.update_text_box_content)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.deselect_all_cells()

    def add_column(self):
        new_col = self.columns
        self.columns += 1
        label = tk.Label(self.inner_frame, text=self.get_column_letter(new_col), relief=tk.RIDGE, width=10)
        label.grid(row=1, column=new_col + 1)
        for row in range(self.rows):
            var = tk.StringVar()
            entry = tk.Entry(self.inner_frame, textvariable=var, relief=tk.RIDGE, width=10, highlightcolor='gray', highlightthickness=1)
            entry.grid(row=row + 2, column=new_col + 1)
            self.entries[(row, new_col)] = entry
            self.variables[(row, new_col)] = var
            entry.bind("<Tab>", self.on_tab)
            entry.bind("<Return>", self.on_return)
            entry.bind("<Down>", self.on_down)
            entry.bind("<Up>", self.on_up)
            entry.bind("<Right>", self.on_right)
            entry.bind("<Left>", self.on_left)
            entry.bind("<KeyRelease>", self.update_text_box_content)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.deselect_all_cells()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpreadsheetApp(root)
    root.mainloop()
