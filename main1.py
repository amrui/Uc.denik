import tkinter as tk
from tkinter import ttk

class UcetniDenikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Účetní deník")

        self.create_widgets()

    def create_widgets(self):
        # Hlavní rámec
        main_frame = ttk.Frame(self.root, padding=(10, 10, 10, 10), style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Pole pro zadávání informací
        entry_frame = ttk.Frame(main_frame, padding=(10, 10, 10, 10), style="TFrame")
        entry_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ttk.Label(entry_frame, text="Poř. č.").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(entry_frame, text="Text").grid(row=0, column=1, padx=5, pady=5, sticky="e")
        ttk.Label(entry_frame, text="Doklad").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Label(entry_frame, text="Kč").grid(row=0, column=3, padx=5, pady=5, sticky="e")
        ttk.Label(entry_frame, text="MD").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        ttk.Label(entry_frame, text="DAL").grid(row=0, column=5, padx=5, pady=5, sticky="e")

        self.poradi_entry = PlaceholderEntry(entry_frame, placeholder="1", readonly=True)
        self.text_entry = PlaceholderEntry(entry_frame, placeholder="...", readonly=True)
        self.doklad_entry = PlaceholderEntry(entry_frame, placeholder="PPD", readonly=True)
        self.kc_entry = PlaceholderEntry(entry_frame, placeholder="0.00 Kč", readonly=True)
        self.md_combobox = PlaceholderEntry(entry_frame, placeholder="001", readonly=True)
        self.dal_combobox = PlaceholderEntry(entry_frame, placeholder="001", readonly=True)

        self.poradi_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.text_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.doklad_entry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.kc_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.md_combobox.grid(row=1, column=4, padx=5, pady=5, sticky="ew")
        self.dal_combobox.grid(row=1, column=5, padx=5, pady=5, sticky="ew")

        ttk.Button(entry_frame, text="Přidat záznam", command=self.pridat_zaznam, style="TButton").grid(row=2, column=0, columnspan=6, pady=10, sticky="ew")

        # Tlačítko na smazání záznamu
        ttk.Button(entry_frame, text="Smazat záznam", command=self.smazat_zaznam, style="TButton").grid(row=3, column=0, columnspan=6, pady=10, sticky="ew")

        # Tabulka
        table_frame = ttk.Frame(main_frame, padding=(10, 0, 10, 10), style="TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        columns = ("Poř. č.", "Text", "Doklad", "Kč", "MD", "DAL")
        self.treeview = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, stretch=True)

        self.treeview.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.treeview.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.treeview.configure(yscrollcommand=scrollbar.set)

        # Změny ve vzhledu
        self.root.configure(bg="#FFFFFF")  # Bílá barva pozadí
        style = ttk.Style(self.root)
        style.configure("TFrame", background="#FFFFFF")  # Bílá barva pozadí
        style.configure("TButton", background="#A9A9A9", foreground="#000000", borderwidth=5, relief="flat", padding=(8, 8))  # Šedá barva pozadí, černý text, zaoblené hrany

        # Konfigurace pro umístění okna na střed
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        entry_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform="group1")  # Adjusted to make all columns resizable
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_rowconfigure(0, weight=1)

        # Přidání konfigurace pro elastic design záznamů
        self.treeview.bind("<Configure>", self.adjust_treeview_columns)

    def pridat_zaznam(self):
        # Získání hodnot z pole pro zadávání
        poradi = self.poradi_entry.get()
        text = self.text_entry.get()
        doklad = self.doklad_entry.get()
        kc = self.kc_entry.get()
        md = self.md_combobox.get()
        dal = self.dal_combobox.get()

        # Přidání záznamu do tabulky
        self.treeview.insert("", "end", values=(poradi, text, doklad, kc, md, dal))

        # Vynulování pole pro zadávání
        self.poradi_entry.delete(0, "end")
        self.text_entry.delete(0, "end")
        self.doklad_entry.delete(0, "end")
        self.kc_entry.delete(0, "end")
        self.md_combobox.delete(0, "end")
        self.dal_combobox.delete(0, "end")

    def smazat_zaznam(self):
        selected_item = self.treeview.selection()
        if selected_item:
            self.treeview.delete(selected_item)

    def adjust_treeview_columns(self, event):
        # Elastic design for treeview columns
        for col in self.treeview["columns"]:
            self.treeview.column(col, width=int(self.treeview.winfo_width()/len(self.treeview["columns"])))

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="", readonly=False, **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.readonly = readonly

        self.insert(0, self.placeholder)
        self.bind("<FocusIn>", self.on_entry_click)
        self.bind("<FocusOut>", self.on_focus_out)
        self.configure(state="readonly" if self.readonly else "normal")

    def on_entry_click(self, event):
        if self.readonly:
            self.configure(state="normal")
            if self.get() == self.placeholder:
                self.delete(0, "end")

    def on_focus_out(self, event):
        if self.readonly and not self.get():
            self.insert(0, self.placeholder)
            self.configure(state="readonly")

class PlaceholderCombobox(ttk.Combobox):
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.set(self.placeholder)
        self.bind("<FocusIn>", self.on_combobox_click)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_combobox_click(self, event):
        if self.get() == self.placeholder:
            self.set("")

    def on_focus_out(self, event):
        if not self.get():
            self.set(self.placeholder)

if __name__ == "__main__":
    root = tk.Tk()
    app = UcetniDenikApp(root)

    # Přidání konfigurace pro umístění okna na střed
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (800/2))
    y_cordinate = int((screen_height/2) - (600/2))
    root.geometry("{}x{}+{}+{}".format(800, 600, x_cordinate, y_cordinate))

    root.mainloop()
