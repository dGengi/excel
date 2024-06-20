import tkinter as tk
from tkinter import filedialog, messagebox,ttk
import csv
import matplotlib.pyplot as plt

class SpreadsheetApp:
    def __init__(self, root, rows=15, columns=10):
        self.root = root
        self.root.title("Spreadsheet")
        self.text_content = ""
        self.rows = rows
        self.columns = columns
        self.selected_cell = None
        self.previous_cell = None
        self.entries = {}
        self.variables = {}
        self.prevent_navigation = False

        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0

        self.create_widgets()
        self.root.bind("<Button-1>", self.start_drag)
        self.root.bind("<ButtonRelease-1>", self.end_drag) 

        self.update_window_position()

    def update_window_position(self):
        self.window_x = self.root.winfo_rootx()
        self.window_y = self.root.winfo_rooty()
        self.root.after(100, self.update_window_position)  

    def start_drag(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        #print(self.start_x,self.start_y)
        if self.start_y - self.window_y > 26 + 24.7 * (self.rows ) + 66 or self.start_x - self.window_x> 86 * (self.columns)+45 or self.start_x - self.window_x < 45 or self.start_y - self.window_y-66<26:
            return
        self.deselect_all_cells()

    def end_drag(self, event):
        self.end_x = event.x_root
        self.end_y = event.y_root
        if self.start_y - self.window_y > 26 + 24.7 * (self.rows ) +66 or self.start_x - self.window_x> 86 * (self.columns)+45 or self.start_x - self.window_x < 45 or self.start_y - self.window_y-66<26:
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

        for col in range(self.columns):
            label = tk.Label(self.root, text=chr(65 + col), relief=tk.RIDGE, width=10)
            label.grid(row=1, column=col + 1)

        for row in range(self.rows):
            label = tk.Label(self.root, text=str(row + 1), relief=tk.RIDGE, width=5)
            label.grid(row=row + 2, column=0)
            for col in range(self.columns):
                var = tk.StringVar()
                entry = tk.Entry(self.root, textvariable=var, relief=tk.RIDGE ,width=10, highlightcolor='gray', highlightthickness=1)
                entry.grid(row=row + 2, column=col + 1)
                self.entries[(row, col)] = entry
                self.variables[(row, col)] = var
                entry.bind("<Tab>", self.on_tab)
                entry.bind("<Return>", self.on_return)
                entry.bind("<Down>", self.on_down)
                entry.bind("<Up>", self.on_up)
                entry.bind("<Right>", self.on_right)
                entry.bind("<Left>", self.on_left)
                entry.bind("<KeyRelease>", self.update_text_box_content)

        

        self.deselect_all_cells()

    def update_text_content(self, event):
        self.text_content = self.text_box.get("1.0", tk.END).strip()
        if self.selected_cell:
            row, col = self.selected_cell
            self.variables[(row, col)].set(self.text_content)

    def on_tab(self, event):
        row, col = self.get_current_cell(event.widget)
        next_col = (col + 1) % self.columns
        self.focus_cell(row, next_col)
        self.selected_cell = (row, next_col)
        self.update_text_box_content(None)
        return "break"

    def on_return(self, event):
        row, col = self.get_current_cell(event.widget)
        next_row = (row + 1) % self.rows
        self.focus_cell(next_row, col)
        self.selected_cell = (next_row, col)
        self.update_text_box_content(None)
        return "break"

    def on_down(self, event):
        row, col = self.get_current_cell(event.widget)
        next_row = (row + 1) % self.rows
        self.focus_cell(next_row, col)
        self.selected_cell = (next_row, col)
        self.update_text_box_content(None)
        return "break"

    def on_up(self, event):
        row, col = self.get_current_cell(event.widget)
        prev_row = (row - 1) % self.rows
        self.focus_cell(prev_row, col)
        self.selected_cell = (prev_row, col)
        self.update_text_box_content(None)
        return "break"

    def on_right(self, event):
        row, col = self.get_current_cell(event.widget)
        next_col = (col + 1) % self.columns
        self.focus_cell(row, next_col)
        self.selected_cell = (row, next_col)
        self.update_text_box_content(None)
        return "break"

    def on_left(self, event):
        row, col = self.get_current_cell(event.widget)
        prev_col = (col - 1) % self.columns
        self.focus_cell(row, prev_col)
        self.selected_cell = (row, prev_col)
        self.update_text_box_content(None)
        return "break"

    def get_current_cell(self, widget):
        for (row, col), entry in self.entries.items():
            if entry == widget:
                return row, col
        return None, None

    def focus_cell(self, row, col):
        for entry in self.entries.values():
            entry.config(bg='white', highlightbackground='gray', highlightcolor='gray', highlightthickness=1)
        self.entries[(row, col)].config(bg='lightblue', highlightbackground='black', highlightcolor='black', highlightthickness=1)
        self.previous_cell = (row, col)
        self.entries[(row, col)].focus()
        val = self.variables[(row, col)].get()
        print(val)

    def update_text_box_content(self, event):
        if self.selected_cell:
            row, col = self.selected_cell
            content = self.variables[(row, col)].get()
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, content)

    def deselect_all_cells(self):
        for entry in self.entries.values():
            entry.config(bg='white', highlightbackground='gray', highlightcolor='gray', highlightthickness=1)

    def single_click_select(self):
        row, col = self.get_cell_from_position(self.start_x, self.start_y)
        if row is not None and col is not None:
            self.focus_cell(row, col)
            self.selected_cell = (row, col)
            self.update_text_box_content(None)

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
        row = int((y - self.window_y - 26-66) // 24.7)
        col = int((x - self.window_x - 45) // 86)
        if 0 <= row < self.rows and 0 <= col < self.columns:
            return row, col
        return None, None

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        with open(file_path, newline='') as file:
            reader = csv.reader(file)
            for r, row in enumerate(reader):
                if r >= self.rows:
                    break
                for c, value in enumerate(row):
                    if c >= self.columns:
                        break
                    self.variables[(r, c)].set(value)

    def save_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in range(self.rows):
                row_data = []
                for col in range(self.columns):
                    row_data.append(self.variables[(row, col)].get())
                writer.writerow(row_data)

    def clear_cells(self):
        for var in self.variables.values():
            var.set("")
        self.deselect_all_cells()
        self.text_box.delete("1.0", tk.END)

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
        
        if len(selected_cols) != 2:
            messagebox.showerror("Error", "Please select exactly two columns")
            return

        col1, col2 = list(selected_cols)
        
        names = []
        values = []
        
        col1_is_int = all(self.variables[(row, col1)].get().isdigit() for row in selected_rows if self.variables[(row, col1)].get())
        col2_is_int = all(self.variables[(row, col2)].get().isdigit() for row in selected_rows if self.variables[(row, col2)].get())
        
        if not col1_is_int and not col2_is_int:
            messagebox.showerror("Error", "One of the selected columns must contain only integers")
            return
        
        if col1_is_int and col2_is_int:
            for row in selected_rows:
                name = self.variables[(row, col1)].get()
                value = self.variables[(row, col2)].get()
                if name and value:
                    names.append(name)
                    values.append(int(value))
        elif col1_is_int:
            for row in selected_rows:
                value = self.variables[(row, col1)].get()
                name = self.variables[(row, col2)].get()
                if name and value:
                    names.append(name)
                    values.append(int(value))
        else:
            for row in selected_rows:
                name = self.variables[(row, col1)].get()
                value = self.variables[(row, col2)].get()
                if name and value:
                    names.append(name)
                    values.append(int(value))

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

if __name__ == "__main__":
    root = tk.Tk()
    app = SpreadsheetApp(root)  
    style = ttk.Style(root)
    style.theme_use('default') 
    font =('Arial',10)

    root.mainloop()
