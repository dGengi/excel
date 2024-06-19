import tkinter as tk

class SpreadsheetApp:
    def __init__(self, root, rows=10, columns=5):
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

    def start_drag(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root
        if self.start_y > 25 * (2 * (self.rows + 2)):
            return
        self.deselect_all_cells()

    def end_drag(self, event):
        self.end_x = event.x_root
        self.end_y = event.y_root
        if self.start_y > 25 * ((self.rows + 2) * 2):
            return
        if self.start_x == self.end_x and self.start_y == self.end_y:
            self.single_click_select()
        else:
            self.select_cells_in_rectangle(self.start_x, self.start_y, self.end_x, self.end_y)

    def create_widgets(self):
        for col in range(self.columns):
            label = tk.Label(self.root, text=chr(65 + col), relief=tk.RIDGE, width=10)
            label.grid(row=0, column=col + 1)

        for row in range(self.rows):
            label = tk.Label(self.root, text=str(row + 1), relief=tk.RIDGE, width=5)
            label.grid(row=row + 1, column=0)

            for col in range(self.columns):
                var = tk.StringVar()
                entry = tk.Entry(self.root, textvariable=var, relief=tk.RIDGE, width=10, highlightcolor='gray', highlightthickness=1)
                entry.grid(row=row + 1, column=col + 1)
                self.entries[(row, col)] = entry
                self.variables[(row, col)] = var
                entry.bind("<Tab>", self.on_tab)
                entry.bind("<Return>", self.on_return)
                entry.bind("<Down>", self.on_down)
                entry.bind("<Up>", self.on_up)
                entry.bind("<Right>", self.on_right)
                entry.bind("<Left>", self.on_left)
                entry.bind("<KeyRelease>", self.update_text_box_content)

        self.text_box = tk.Text(self.root, height=5, width=50)
        self.text_box.grid(row=self.rows + 2, column=0, columnspan=self.columns + 1, padx=5, pady=5)
        self.text_box.bind("<KeyRelease>", self.update_text_content)
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
        widget_x = self.root.winfo_rootx()
        widget_y = self.root.winfo_rooty()

        relative_x = x - widget_x
        relative_y = y - widget_y

        cell_width = self.entries[(0, 0)].winfo_width()
        cell_height = self.entries[(0, 0)].winfo_height()

        col = int((relative_x - 50) / cell_width)
        if col < 0:
            col = 0
        elif col >= self.columns:
            col = self.columns - 1

        row = int((relative_y - 25) / cell_height)
        if row < 0:
            row = 0
        elif row >= self.rows:
            row = self.rows - 1

        return row, col

if __name__ == "__main__":
    root = tk.Tk()
    app = SpreadsheetApp(root)
    root.mainloop()


