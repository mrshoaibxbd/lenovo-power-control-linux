#!/usr/bin/env python3
import tkinter as tk
import subprocess
import webbrowser

FILE_PATH = "/sys/devices/pci0000:00/0000:00:1f.0/PNP0C09:00/VPC2004:00/conservation_mode"

# --- Hardware Logic ---
def read_status():
    try:
        with open(FILE_PATH, 'r') as file:
            return file.read().strip()
    except Exception:
        return "Error"

def toggle_hardware(event=None):
    current = read_status()
    new_status = "0" if current == "1" else "1"
    command = f'pkexec sh -c "echo {new_status} > {FILE_PATH}"'
    subprocess.run(command, shell=True)
    update_ui()

# --- About Window Logic ---
def open_about():
    about_win = tk.Toplevel(root)
    about_win.geometry("300x220")
    about_win.configure(bg="#1e1e1e")
    about_win.overrideredirect(True)
    
    # Center the popup relative to the main window
    x = root.winfo_x() + 50
    y = root.winfo_y() + 15
    about_win.geometry(f"+{x}+{y}")
    
    tk.Label(about_win, text="Developer: Md Shoaib Mahmud", fg="cyan", bg="#1e1e1e", font=("Helvetica", 11, "bold")).pack(pady=15)
    
    website_btn = tk.Button(about_win, text="Visit shoaib.pro.bd", fg="white", bg="blue", command=lambda: webbrowser.open_new("http://shoaib.pro.bd"), bd=0)
    website_btn.pack(pady=5)
    
    caution_text = "Caution: Just for Lenovo Ideapad Slim 3i\nor specific compatible motherboards."
    tk.Label(about_win, text=caution_text, fg="red", bg="#1e1e1e", font=("Helvetica", 9)).pack(pady=15)
    
    close_btn = tk.Button(about_win, text="Close", fg="white", bg="#aa0000", command=about_win.destroy, bd=0)
    close_btn.pack(pady=5)

# --- UI Drawing & Updating Logic ---
def draw_gradient(canvas, width, height):
    for i in range(height):
        r = 0
        g = int((i / height) * 200)
        b = int(100 + (i / height) * 155)
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, width, i, fill=color)

def update_ui():
    status = read_status()
    canvas.delete("dynamic") 
    
    if status == "1":
        status_text = "Status - ENABLED"
        text_color = "#00FF00" 
        switch_color = "#00FF00" 
        circle_x = 240 
    elif status == "0":
        status_text = "Status - DISABLED"
        text_color = "#FF0000" 
        switch_color = "gray"
        circle_x = 160 
    else:
        status_text = "Status - ERROR"
        text_color = "white"
        switch_color = "gray"
        circle_x = 160
        
    canvas.create_text(200, 100, text=status_text, fill=text_color, font=("Helvetica", 14, "bold"), tags="dynamic")
    
    canvas.create_oval(140, 130, 180, 170, fill=switch_color, outline="", tags=("dynamic", "switch"))
    canvas.create_oval(220, 130, 260, 170, fill=switch_color, outline="", tags=("dynamic", "switch"))
    canvas.create_rectangle(160, 130, 240, 170, fill=switch_color, outline="", tags=("dynamic", "switch"))
    
    canvas.create_oval(circle_x - 18, 132, circle_x + 18, 168, fill="white", outline="", tags=("dynamic", "switch"))

# --- Main Window Initialization ---
root = tk.Tk()
root.title("Power Control")
root.overrideredirect(True)

# Calculate screen center coordinates
window_width = 400
window_height = 250
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int((screen_width / 2) - (window_width / 2))
center_y = int((screen_height / 2) - (window_height / 2))

# Spawn the window perfectly centered
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

canvas = tk.Canvas(root, width=400, height=250, highlightthickness=0)
canvas.pack(fill="both", expand=True)

draw_gradient(canvas, 400, 250)
canvas.create_text(200, 60, text="Conservation Mode Toggle", fill="white", font=("Helvetica", 16, "bold"))

about_btn = tk.Button(root, text="About", command=open_about, bg="#004488", fg="cyan", bd=0, highlightthickness=0)
about_btn.place(x=10, y=10)

main_close_btn = tk.Button(root, text="Close", command=root.destroy, bg="#aa0000", fg="white", bd=0, highlightthickness=0)
main_close_btn.place(x=340, y=10)

canvas.tag_bind("switch", "<Button-1>", toggle_hardware)

update_ui()
root.mainloop()