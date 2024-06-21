import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar, Label, Button
from matplotlib import font_manager

root = tk.Tk()
root.geometry("800x600")

# probni tekst
text = Label(root, text="mjau", font=("Arial", 16))
text.pack()
ime_teksta = text

# da li je lista fontova ili velicina vidljiva
font_list_visible = False
size_list_visible = False

# menjanje fontova
def change_font(ime_fonta, ime_teksta):
    trenutna_velicina = get_current_font_size(ime_teksta)
    ime_teksta.config(font=(ime_fonta, trenutna_velicina))

def toggle_fonts(ime_teksta):
    global font_list_visible
    if font_list_visible:
        for widget in frame_font.winfo_children():
            widget.destroy()
        scrollbar_font.pack_forget()
        canvas_font.pack_forget()
        font_list_visible = False
    else:
        list_fonts(ime_teksta)
        font_list_visible = True

# pravi listu dugmica za svaki moguci font u pythonovoj biblioteci
def list_fonts(ime_teksta):
    available_fonts = sorted([f.name for f in font_manager.fontManager.ttflist])
    for widget in frame_font.winfo_children():
        widget.destroy()

    for font in available_fonts:
        myButton = Button(frame_font, text=font, command=lambda f=font: change_font(f, ime_teksta))
        myButton.pack()

    canvas_font.pack(side="left", fill="both", expand=True)
    scrollbar_font.pack(side="right", fill="y")

# isto kao ovo prethodno samo je za velicinu a ne font
def promena_velicine(velicina, ime_teksta):
    trenutni_font = get_current_font_family(ime_teksta)
    ime_teksta.config(font=(trenutni_font, velicina))

def toggle_sizes(ime_teksta):
    global size_list_visible
    if size_list_visible:
        # Clear existing widgets in frame_size and scrollbar
        for widget in frame_size.winfo_children():
            widget.destroy()
        scrollbar_size.pack_forget()
        canvas_size.pack_forget()
        size_list_visible = False
    else:
        lista_velicina(ime_teksta)
        size_list_visible = True

def lista_velicina(ime_teksta):
    # Clear existing widgets in frame_size
    for widget in frame_size.winfo_children():
        widget.destroy()

    for i in range(1, 73):
        myButton = Button(frame_size, text=str(i), command=lambda f=i: promena_velicine(f, ime_teksta))
        myButton.pack()

    # Pack the canvas and scrollbar after adding buttons
    canvas_size.pack(side="left", fill="both", expand=True)
    scrollbar_size.pack(side="right", fill="y")

# za dobijanje trenutnog fonta ili velicine obelezenog teksta
def get_current_font_size(ime_teksta):
    current_font = ime_teksta.cget("font")
    font_parts = current_font.split()
    if len(font_parts) > 1:
        font_size = int(font_parts[-1])
        return font_size

def get_current_font_family(ime_teksta):
    current_font = ime_teksta.cget("font")
    font_parts = current_font.split()
    if len(font_parts) > 1:
        font_family = " ".join(font_parts[:-1])
        return font_family
    return current_font

# scroler za font
font_frame = Frame(root)
canvas_font = Canvas(font_frame)
frame_font = Frame(canvas_font)
scrollbar_font = Scrollbar(font_frame, orient="vertical", command=canvas_font.yview)
canvas_font.configure(yscrollcommand=scrollbar_font.set)
canvas_font.create_window((0, 0), window=frame_font, anchor="nw")
frame_font.bind("<Configure>", lambda event, canvas=canvas_font: canvas.configure(scrollregion=canvas.bbox("all")))

# isto ovo prethodno samo za size umesto fonta 
size_frame = Frame(root)
canvas_size = Canvas(size_frame)
frame_size = Frame(canvas_size)
scrollbar_size = Scrollbar(size_frame, orient="vertical", command=canvas_size.yview)
canvas_size.configure(yscrollcommand=scrollbar_size.set)
canvas_size.create_window((0, 0), window=frame_size, anchor="nw")
frame_size.bind("<Configure>", lambda event, canvas=canvas_size: canvas.configure(scrollregion=canvas.bbox("all")))

font_frame.pack(side="left", fill="both", expand=True)
size_frame.pack(side="right", fill="both", expand=True)

# dugme za fontove
font_button = Button(root, text="Change Fonts", command=lambda: toggle_fonts(ime_teksta))
font_button.place(x=10, y=10)

# dugme za velicine
size_button = Button(root, text="Change Size", command=lambda: toggle_sizes(ime_teksta))
size_button.place(x=440, y=10)

root.mainloop()


