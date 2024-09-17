import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to evaluate expressions
def evaluate_expression(expression):
    try:
        result = eval(expression)
        return result
    except Exception as e:
        messagebox.showerror("Error", f"Invalid Expression: {e}")
        return None

# Function to update the display
def update_display(value):
    display_var.set(value)

# Function to handle button clicks
def button_click(value):
    current_text = display_var.get()
    if value == "=":
        result = evaluate_expression(current_text)
        if result is not None:
            update_display(result)
            save_to_history(current_text, result)
    elif value == "C":
        update_display("")
    else:
        update_display(current_text + value)

# Function to save the expression and result to the history
def save_to_history(expression, result):
    conn = sqlite3.connect('calculator_history.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history (expression TEXT, result TEXT)')
    c.execute('INSERT INTO history (expression, result) VALUES (?, ?)', (expression, result))
    conn.commit()
    conn.close()

# Function to view history
def view_history():
    conn = sqlite3.connect('calculator_history.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history (expression TEXT, result TEXT)')
    c.execute('SELECT * FROM history')
    rows = c.fetchall()
    conn.close()
    
    history_window = tk.Toplevel(root)
    history_window.title("History")
    
    history_text = tk.Text(history_window, width=40, height=10)
    history_text.pack()
    
    for row in rows:
        history_text.insert(tk.END, f"{row[0]} = {row[1]}\n")

# Create the main window
root = tk.Tk()
root.title("Calculator")

# Create display variable
display_var = tk.StringVar()

# Create the display widget
display = tk.Entry(root, textvariable=display_var, font=('Arial', 20), bd=10, insertwidth=4, width=14, borderwidth=4, justify='right')
display.grid(row=0, column=0, columnspan=4)

# Button layout
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    'C', '0', '=', '+'
]

row = 1
col = 0
for button in buttons:
    tk.Button(root, text=button, padx=20, pady=20, font=('Arial', 18), command=lambda b=button: button_click(b)).grid(row=row, column=col)
    col += 1
    if col > 3:
        col = 0
        row += 1

# Add View History button
tk.Button(root, text="View History", padx=10, pady=10, command=view_history).grid(row=row, column=0, columnspan=4)

# Run the application
root.mainloop()
