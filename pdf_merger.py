import os
from tkinter import Tk, Canvas, Button, filedialog, Frame, Label
from tkinter import ttk
from PyPDF2 import PdfReader, PdfWriter

pdf_files = []
selected_indices = []

def add_files():
    global pdf_files
    files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
    pdf_files.extend(files)
    draw_canvas_items()
    status_label.config(text=f"{len(files)} files added.")

def remove_file():
    global pdf_files, selected_indices
    selected_indices.sort(reverse=True)
    for index in selected_indices:
        pdf_files.pop(index)
    selected_indices.clear()
    draw_canvas_items()
    status_label.config(text="Selected files removed.")

def move_up():
    global pdf_files, selected_indices
    if not selected_indices:
        return
    for index in selected_indices:
        if index > 0:
            pdf_files[index], pdf_files[index - 1] = pdf_files[index - 1], pdf_files[index]
    selected_indices[:] = [i - 1 for i in selected_indices if i > 0]
    draw_canvas_items()
    status_label.config(text="Selected files moved up.")

def move_down():
    global pdf_files, selected_indices
    if not selected_indices:
        return
    for index in reversed(selected_indices):
        if index < len(pdf_files) - 1:
            pdf_files[index], pdf_files[index + 1] = pdf_files[index + 1], pdf_files[index]
    selected_indices[:] = [i + 1 for i in selected_indices if i < len(pdf_files) - 1]
    draw_canvas_items()
    status_label.config(text="Selected files moved down.")

def merge_pdfs():
    global pdf_files
    writer = PdfWriter()
    
    if not pdf_files:
        status_label.config(text="No PDF files to merge.")
        return
    
    try:
        for filename in pdf_files:
            reader = PdfReader(filename)
            for page in reader.pages:
                writer.add_page(page)
        
        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if output_path:
            with open(output_path, "wb") as f:
                writer.write(f)
            status_label.config(text=f"PDF files successfully merged into {output_path}.")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

def draw_canvas_items():
    canvas.delete("all")
    for index, file in enumerate(pdf_files):
        y0 = 10 + (index * 40)
        y1 = y0 + 30
        rect_color = "lightblue" if index in selected_indices else "lightgrey"
        rect_id = canvas.create_rectangle(10, y0, 290, y1, fill=rect_color, outline="black", tags=f"rect_{index}")
        text_id = canvas.create_text(150, y0 + 15, text=os.path.basename(file), fill="black", tags=f"text_{index}")
        canvas.tag_bind(f"rect_{index}", "<Button-1>", lambda e, idx=index: toggle_selection(idx))
        canvas.tag_bind(f"text_{index}", "<Button-1>", lambda e, idx=index: toggle_selection(idx))

def toggle_selection(index):
    global selected_indices
    if index in selected_indices:
        selected_indices.remove(index)
    else:
        selected_indices.append(index)
    draw_canvas_items()

# Tkinter arayüzünü oluşturma
root = Tk()
root.title("PDF Merger")

# Modern görünüm için ttk stili
style = ttk.Style()
style.theme_use('clam')

# Frame ve Canvas oluşturma
frame = Frame(root)
frame.pack(padx=10, pady=10)

canvas = Canvas(frame, width=300, height=400, bg="white")
canvas.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

add_button = ttk.Button(frame, text="Add PDF", command=add_files)
add_button.grid(row=1, column=0, padx=5, pady=5)

remove_button = ttk.Button(frame, text="Remove Selected", command=remove_file)
remove_button.grid(row=1, column=1, padx=5, pady=5)

up_button = ttk.Button(frame, text="Move Up", command=move_up)
up_button.grid(row=1, column=2, padx=5, pady=5)

down_button = ttk.Button(frame, text="Move Down", command=move_down)
down_button.grid(row=1, column=3, padx=5, pady=5)

merge_button = ttk.Button(frame, text="Merge and Save", command=merge_pdfs)
merge_button.grid(row=2, column=0, columnspan=4, padx=5, pady=10)

status_label = Label(frame, text="")
status_label.grid(row=3, column=0, columnspan=4, padx=5, pady=5)

root.mainloop()
