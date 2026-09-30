import tkinter as tk
from tkinter import ttk, messagebox
import math

# ----------------- Engineering Calculation Functions -----------------

def area_of_circle(radius):
    """Calculates area and circumference of a circle."""
    area = math.pi * (radius ** 2)
    circumference = 2 * math.pi * radius
    return area, circumference

def area_of_rectangle(length, width):
    """Calculates area and perimeter of a rectangle."""
    area = length * width
    perimeter = 2 * (length + width)
    return area, perimeter

def area_of_triangle(base, height):
    """Calculates area of a triangle."""
    area = 0.5 * base * height
    return area

def cylinder_properties(radius, height):
    """Calculates volume and total surface area of a cylinder."""
    base_area = math.pi * (radius ** 2)
    volume = base_area * height
    surface_area = (2 * math.pi * radius * height) + (2 * base_area)
    return volume, surface_area


# ----------------- GUI Application Class -----------------

class EngineeringCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Engineering Formula Calculator")
        self.geometry("540x640")
        self.resizable(False, False)
        self.configure(bg="#F0F4F8")

        # Configure TTK Styles
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        
        # Style Customizations
        self.style.configure("TNotebook", background="#F0F4F8")
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10, "bold"), padding=[12, 6])
        self.style.configure("TButton", font=("Helvetica", 10, "bold"), padding=6)
        self.style.configure("TCombobox", padding=4)
        
        # Header
        header_frame = tk.Frame(self, bg="#1E3A8A", pady=12)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="⚙️ Engineering Formula Toolkit", font=("Helvetica", 16, "bold"), fg="white", bg="#1E3A8A").pack()
        tk.Label(header_frame, text="Quick Geometric & Section Calculations for Engineers", font=("Helvetica", 9), fg="#93C5FD", bg="#1E3A8A").pack()

        # Settings bar (Precision & Units)
        settings_frame = tk.Frame(self, bg="#F0F4F8", pady=6, padx=15)
        settings_frame.pack(fill="x")

        tk.Label(settings_frame, text="Unit:", font=("Helvetica", 9, "bold"), bg="#F0F4F8").pack(side="left", padx=(0, 4))
        self.unit_var = tk.StringVar(value="mm")
        unit_combo = ttk.Combobox(settings_frame, textvariable=self.unit_var, values=["mm", "cm", "m", "in", "ft"], width=5, state="readonly")
        unit_combo.pack(side="left", padx=(0, 15))
        unit_combo.bind("<<ComboboxSelected>>", lambda e: self.recalculate_active())

        tk.Label(settings_frame, text="Decimals:", font=("Helvetica", 9, "bold"), bg="#F0F4F8").pack(side="left", padx=(0, 4))
        self.precision_var = tk.IntVar(value=4)
        prec_combo = ttk.Combobox(settings_frame, textvariable=self.precision_var, values=[2, 3, 4, 6], width=4, state="readonly")
        prec_combo.pack(side="left")
        prec_combo.bind("<<ComboboxSelected>>", lambda e: self.recalculate_active())

        # Calculation History Box (created before tabs so calculations can log to it)
        hist_frame = tk.LabelFrame(self, text=" Calculation History ", bg="#F0F4F8", font=("Helvetica", 9, "bold"), padx=10, pady=5)
        hist_frame.pack(side="bottom", fill="x", padx=15, pady=(5, 12))
        
        self.history_list = tk.Listbox(hist_frame, height=4, font=("Consolas", 9), relief="solid", bd=1)
        self.history_list.pack(side="left", fill="x", expand=True)

        hist_btn_frame = tk.Frame(hist_frame, bg="#F0F4F8")
        hist_btn_frame.pack(side="right", padx=(6, 0), fill="y")
        ttk.Button(hist_btn_frame, text="Copy", width=6, command=self.copy_selected_history).pack(pady=2)
        ttk.Button(hist_btn_frame, text="Clear", width=6, command=lambda: self.history_list.delete(0, tk.END)).pack(pady=2)

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(padx=15, pady=5, fill="both", expand=True)

        # Build Tabs
        self.create_circle_tab()
        self.create_rectangle_tab()
        self.create_triangle_tab()
        self.create_cylinder_tab()

    # ----------------- Circle Tab -----------------
    def create_circle_tab(self):
        tab = tk.Frame(self.notebook, bg="white", padx=15, pady=15)
        self.notebook.add(tab, text="⭕ Circle")

        tk.Label(tab, text="Formula: Area = π · r²  |  Circumference = 2 · π · r", 
                 font=("Helvetica", 9, "italic"), fg="#4B5563", bg="#F3F4F6", relief="flat", padx=8, pady=4).pack(fill="x", pady=(0, 10))

        tk.Label(tab, text="Radius (r):", font=("Helvetica", 10, "bold"), bg="white").pack(anchor="w")
        self.circle_r = tk.StringVar(value="5.0")
        r_entry = ttk.Entry(tab, textvariable=self.circle_r, font=("Helvetica", 11))
        r_entry.pack(fill="x", pady=(2, 10))
        r_entry.bind("<KeyRelease>", lambda e: self.calc_circle())

        ttk.Button(tab, text="Calculate Circle", command=self.calc_circle).pack(fill="x", pady=4)

        self.circle_result = tk.Label(tab, text="", font=("Helvetica", 10), justify="left", bg="#EFF6FF", fg="#1E40AF", relief="solid", bd=1, padx=10, pady=10)
        self.circle_result.pack(fill="x", pady=(10, 0))
        self.calc_circle()

    def calc_circle(self):
        try:
            r = float(self.circle_r.get())
            if r < 0:
                raise ValueError("Negative radius")
            area, circum = area_of_circle(r)
            u = self.unit_var.get()
            p = self.precision_var.get()

            res_text = (
                f"📐 Results:\n"
                f"• Area (A) = {area:.{p}f} {u}²\n"
                f"• Circumference (C) = {circum:.{p}f} {u}\n"
                f"• Diameter (D) = {2*r:.{p}f} {u}"
            )
            self.circle_result.config(text=res_text, fg="#1E40AF", bg="#EFF6FF")
            self.add_history(f"Circle [r={r}{u}]: Area={area:.{p}f} {u}²")
        except ValueError:
            self.circle_result.config(text="⚠️ Please enter a valid positive number for radius.", fg="#DC2626", bg="#FEE2E2")

    # ----------------- Rectangle Tab -----------------
    def create_rectangle_tab(self):
        tab = tk.Frame(self.notebook, bg="white", padx=15, pady=15)
        self.notebook.add(tab, text="▭ Rectangle")

        tk.Label(tab, text="Formula: Area = Length × Width  |  Perimeter = 2 × (L + W)", 
                 font=("Helvetica", 9, "italic"), fg="#4B5563", bg="#F3F4F6", padx=8, pady=4).pack(fill="x", pady=(0, 10))

        tk.Label(tab, text="Length (L):", font=("Helvetica", 10, "bold"), bg="white").pack(anchor="w")
        self.rect_l = tk.StringVar(value="4.0")
        l_entry = ttk.Entry(tab, textvariable=self.rect_l, font=("Helvetica", 11))
        l_entry.pack(fill="x", pady=(2, 6))
        l_entry.bind("<KeyRelease>", lambda e: self.calc_rectangle())

        tk.Label(tab, text="Width (W):", font=("Helvetica", 10, "bold"), bg="white").pack(anchor="w")
        self.rect_w = tk.StringVar(value="6.0")
        w_entry = ttk.Entry(tab, textvariable=self.rect_w, font=("Helvetica", 11))
        w_entry.pack(fill="x", pady=(2, 10))
        w_entry.bind("<KeyRelease>", lambda e: self.calc_rectangle())

        ttk.Button(tab, text="Calculate Rectangle", command=self.calc_rectangle).pack(fill="x", pady=4)

        self.rect_result = tk.Label(tab, text="", font=("Helvetica", 10), justify="left", bg="#EFF6FF", fg="#1E40AF", relief="solid", bd=1, padx=10, pady=10)
        self.rect_result.pack(fill="x", pady=(10, 0))

    def calc_rectangle(self):
        try:
            l = float(self.rect_l.get())
            w = float(self.rect_w.get())
            if l < 0 or w < 0:
                raise ValueError("Negative dimensions")
            area, perim = area_of_rectangle(l, w)
            diagonal = math.hypot(l, w)
            u = self.unit_var.get()
            p = self.precision_var.get()

            res_text = (
                f"📐 Results:\n"
                f"• Area (A) = {area:.{p}f} {u}²\n"
                f"• Perimeter (P) = {perim:.{p}f} {u}\n"
                f"• Diagonal = {diagonal:.{p}f} {u}"
            )
            self.rect_result.config(text=res_text, fg="#1E40AF", bg="#EFF6FF")
            self.add_history(f"Rect [L={l}{u}, W={w}{u}]: Area={area:.{p}f} {u}²")
        except ValueError:
            self.rect_result.config(text="⚠️ Please enter valid positive numbers.", fg="#DC2626", bg="#FEE2E2")

    # ----------------- Triangle Tab -----------------
    def create_triangle_tab(self):
        tab = tk.Frame(self.notebook, bg="white", padx=15, pady=15)
        self.notebook.add(tab, text="🔺 Triangle")

        tk.Label(tab, text="Formula: Area = 0.5 × Base × Height", 
                 font=("Helvetica", 9, "italic"), fg="#4B5563", bg="#F3F4F6", padx=8, pady=4).pack(fill="x", pady=(0, 10))

        tk.Label(tab, text="Base (b):", font=("Helvetica", 10, "bold"), bg="white").pack(anchor="w")
        self.tri_b = tk.StringVar(value="8.0")
        b_entry = ttk.Entry(tab, textvariable=self.tri_b, font=("Helvetica", 11))
        b_entry.pack(fill="x", pady=(2, 6))
        b_entry.bind("<KeyRelease>", lambda e: self.calc_triangle())

        tk.Label(tab, text="Height (h):", font=("Helvetica", 10, "bold"), bg="white").pack(anchor="w")
        self.tri_h = tk.StringVar(value="5.0")
        h_entry = ttk.Entry(tab, textvariable=self.tri_h, font=("Helvetica", 11))
        h_entry.pack(fill="x", pady=(2, 10))
        h_entry.bind("<KeyRelease>", lambda e: self.calc_triangle())

        ttk.Button(tab, text="Calculate Triangle", command=self.calc_triangle).pack(fill="x", pady=4)

        self.tri_result = tk.Label(tab, text="", font=("Helvetica", 10), justify="left", bg="#EFF6FF", fg="#1E40AF", relief="solid", bd=1, padx=10, pady=10)
        self.tri_result.pack(fill="x", pady=(10, 0))

    def calc_triangle(self):
        try:
            b = float(self.tri_b.get())
            h = float(self.tri_h.get())
            if b < 0 or h < 0:
                raise ValueError("Negative dimensions")
            area = area_of_triangle(b, h)
            u = self.unit_var.get()
            p = self.precision_var.get()

            res_text = (
                f"📐 Results:\n"
                f"• Area (A) = {area:.{p}f} {u}²\n"
                f"• Step: ½ × {b} × {h} = {area:.{p}f} {u}²"
            )
            self.tri_result.config(text=res_text, fg="#1E40AF", bg="#EFF6FF")
            self.add_history(f"Triangle [b={b}{u}, h={h}{u}]: Area={area:.{p}f} {u}²")
        except ValueError:
            self.tri_result.config(text="⚠️ Please enter valid positive numbers.", fg="#DC2626", bg="#FEE2E2")

    # ----------------- Cylinder Tab -----------------
    def create_cylinder_tab(self):
        tab = tk.Frame(self.notebook, bg="white", padx=15, pady=15)
        self.notebook.add(tab, text="🛢️ Cylinder")

        tk.Label(tab, text="Formula: Volume = π · r² · h  |  Surface = 2πrh + 2πr²", 
                 font=("Helvetica", 9, "italic"), fg="#4B5563", bg="#F3F4F6", padx=8, pady=4).pack(fill="x", pady=(0, 10))

        tk.Label(tab, text="Radius (r):", font=("Helvetica", 10, "bold"), bg="white").pack(anchor="w")
        self.cyl_r = tk.StringVar(value="3.0")
        r_entry = ttk.Entry(tab, textvariable=self.cyl_r, font=("Helvetica", 11))
        r_entry.pack(fill="x", pady=(2, 6))
        r_entry.bind("<KeyRelease>", lambda e: self.calc_cylinder())

        tk.Label(tab, text="Height (h):", font=("Helvetica", 10, "bold"), bg="white").pack(anchor="w")
        self.cyl_h = tk.StringVar(value="10.0")
        h_entry = ttk.Entry(tab, textvariable=self.cyl_h, font=("Helvetica", 11))
        h_entry.pack(fill="x", pady=(2, 10))
        h_entry.bind("<KeyRelease>", lambda e: self.calc_cylinder())

        ttk.Button(tab, text="Calculate Cylinder", command=self.calc_cylinder).pack(fill="x", pady=4)

        self.cyl_result = tk.Label(tab, text="", font=("Helvetica", 10), justify="left", bg="#EFF6FF", fg="#1E40AF", relief="solid", bd=1, padx=10, pady=10)
        self.cyl_result.pack(fill="x", pady=(10, 0))

    def calc_cylinder(self):
        try:
            r = float(self.cyl_r.get())
            h = float(self.cyl_h.get())
            if r < 0 or h < 0:
                raise ValueError("Negative dimensions")
            vol, surface = cylinder_properties(r, h)
            u = self.unit_var.get()
            p = self.precision_var.get()

            res_text = (
                f"📐 Results:\n"
                f"• Volume (V) = {vol:.{p}f} {u}³\n"
                f"• Total Surface Area = {surface:.{p}f} {u}²\n"
                f"• Cross-Section Base Area = {math.pi * (r**2):.{p}f} {u}²"
            )
            self.cyl_result.config(text=res_text, fg="#1E40AF", bg="#EFF6FF")
            self.add_history(f"Cylinder [r={r}{u}, h={h}{u}]: Vol={vol:.{p}f} {u}³")
        except ValueError:
            self.cyl_result.config(text="⚠️ Please enter valid positive numbers.", fg="#DC2626", bg="#FEE2E2")

    # ----------------- Utility Helpers -----------------
    def recalculate_active(self):
        self.calc_circle()
        self.calc_rectangle()
        self.calc_triangle()
        self.calc_cylinder()

    def add_history(self, entry):
        if self.history_list.size() > 0 and self.history_list.get(0) == entry:
            return  # avoid duplicate spam
        self.history_list.insert(0, entry)
        if self.history_list.size() > 50:
            self.history_list.delete(50, tk.END)

    def copy_selected_history(self):
        selected = self.history_list.curselection()
        if selected:
            text = self.history_list.get(selected[0])
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("Copied", f"Copied to clipboard:\n{text}")
        elif self.history_list.size() > 0:
            text = self.history_list.get(0)
            self.clipboard_clear()
            self.clipboard_append(text)
            messagebox.showinfo("Copied", f"Copied latest to clipboard:\n{text}")


# ----------------- Application Entry -----------------
if __name__ == "__main__":
    app = EngineeringCalculator()
    app.mainloop()
print("Area of rectangle with length 4 and width 6:", area_of_rectangle(4, 6))