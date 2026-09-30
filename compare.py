import tkinter as tk
from tkinter import ttk, messagebox
import random

def evaluate_number(val_str):
    """Evaluates the number and updates the visual UI elements."""
    try:
        val = float(val_str)
    except ValueError:
        result_label.config(text="⚠️ Please enter a valid number", foreground="#D9534F")
        details_label.config(text="")
        card_frame.config(bg="#FADBD8")
        return

    # Check sign
    if val > 0:
        status_text = f"✅ {val:g} is Positive"
        card_color = "#D4EDDA"   # soft green
        text_color = "#155724"
    elif val < 0:
        status_text = f"🔻 {val:g} is Negative"
        card_color = "#F8D7DA"   # soft red
        text_color = "#721C24"
    else:
        status_text = "⚪ The number is Zero"
        card_color = "#D1ECF1"   # soft blue
        text_color = "#0C5460"

    # Additional properties
    details = [f"Absolute value: {abs(val):g}"]
    if val.is_integer():
        int_val = int(val)
        parity = "Even" if int_val % 2 == 0 else "Odd"
        details.append(f"Parity: {parity}")
    
    # Update UI card
    card_frame.config(bg=card_color)
    result_label.config(text=status_text, foreground=text_color, bg=card_color)
    details_label.config(text=" | ".join(details), foreground=text_color, bg=card_color)

    # Add to history
    history_box.insert(0, f"{val:g} ➔ {status_text.split()[-1]}")

def on_entry_change(event=None):
    evaluate_number(entry_var.get())

def on_slider_change(val):
    entry_var.set(str(int(float(val))))
    evaluate_number(val)

def adjust_by(step):
    try:
        cur = float(entry_var.get())
    except ValueError:
        cur = 0
    new_val = int(cur) + step
    entry_var.set(str(new_val))
    slider.set(new_val)
    evaluate_number(new_val)

def set_random():
    rnd = random.randint(-50, 50)
    entry_var.set(str(rnd))
    slider.set(rnd)
    evaluate_number(rnd)

def reset():
    entry_var.set("0")
    slider.set(0)
    evaluate_number(0)

# --- Window Setup ---
root = tk.Tk()
root.title("Number Classifier GUI")
root.geometry("420x520")
root.resizable(False, False)
root.configure(bg="#F7F9FB")

style = ttk.Style()
style.theme_use("clam")

# Title
title_lbl = tk.Label(root, text="Number Explorer", font=("Helvetica", 16, "bold"), bg="#F7F9FB", fg="#333333")
title_lbl.pack(pady=(15, 5))

# --- Input Section ---
input_frame = tk.Frame(root, bg="#F7F9FB")
input_frame.pack(pady=10, padx=20, fill="x")

entry_lbl = tk.Label(input_frame, text="Enter a number:", font=("Helvetica", 10), bg="#F7F9FB")
entry_lbl.pack(anchor="w")

entry_var = tk.StringVar(value="0")
entry = ttk.Entry(input_frame, textvariable=entry_var, font=("Helvetica", 13), justify="center")
entry.pack(fill="x", pady=5)
entry.bind("<KeyRelease>", on_entry_change)

# Quick Step & Action Buttons
btn_frame = tk.Frame(input_frame, bg="#F7F9FB")
btn_frame.pack(fill="x", pady=4)
ttk.Button(btn_frame, text="-1", width=5, command=lambda: adjust_by(-1)).pack(side="left", padx=2)
ttk.Button(btn_frame, text="+1", width=5, command=lambda: adjust_by(1)).pack(side="left", padx=2)
ttk.Button(btn_frame, text="🎲 Random", command=set_random).pack(side="left", expand=True, fill="x", padx=4)
ttk.Button(btn_frame, text="🔄 Reset", command=reset).pack(side="left", padx=2)

# Slider (Interactive scrub)
slider_lbl = tk.Label(input_frame, text="Or drag the slider (-50 to 50):", font=("Helvetica", 9), bg="#F7F9FB", fg="#666")
slider_lbl.pack(anchor="w", pady=(10, 0))

slider = ttk.Scale(input_frame, from_=-50, to=50, orient="horizontal", command=on_slider_change)
slider.set(0)
slider.pack(fill="x", pady=3)

# --- Output Result Card ---
card_frame = tk.Frame(root, bg="#D1ECF1", bd=1, relief="solid")
card_frame.pack(padx=20, pady=15, fill="x")

result_label = tk.Label(card_frame, text="⚪ The number is Zero", font=("Helvetica", 13, "bold"), bg="#D1ECF1", fg="#0C5460")
result_label.pack(pady=(10, 2))

details_label = tk.Label(card_frame, text="Absolute value: 0 | Parity: Even", font=("Helvetica", 9), bg="#D1ECF1", fg="#0C5460")
details_label.pack(pady=(0, 10))

# --- History Log Section ---
history_lbl = tk.Label(root, text="Evaluation History", font=("Helvetica", 10, "bold"), bg="#F7F9FB", fg="#555")
history_lbl.pack(anchor="w", padx=20)

history_box = tk.Listbox(root, height=5, font=("Consolas", 9), relief="solid", bd=1)
history_box.pack(padx=20, pady=5, fill="both", expand=True)

# Run initial evaluation
evaluate_number("0")

root.mainloop()