import os
import pandas as pd
import tkinter as tk  
from tkinter import ttk, filedialog
from tkcalendar import DateEntry 
import csv  
import datetime  
from uctove_tridy import ACCOUNTS  

# Třída pro účetní doklady
class Doklad:
    STANDARDNI_DOKLADY = [  # Seznam standardních účetních dokladů
        "VBÚ - Výpis z bankovního účtu",
        "VÚÚ - Výpis z úvěrového účtu",
        "VPD - Výdajový pokladní doklad",
        "PPD - Příjmový pokladní doklad",
        "FAD - Faktura došlá (přijatá)",
        "FAV - Faktura vydaná",
        "INT - Interní (vnitřní) účetní doklad",
        "ZVL - Zúčtovací a výplatní listina",
        "VPDc - Výdajový pokladní doklad - ceniny",
        "PPDc - Příjmový pokladní doklad - ceniny",
        "PŘJ - Příjemka",
        "VÝD - Výdejka"
    ]


class AccountingJournalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Účetní deník")  # Nastavení titulku okna aplikace

        self.accounts_MD_DAL = []  # Inicializace seznamu účetních dokladů MD a DAL

        self.md_combobox = ttk.Combobox(self, values=list(range(711)), state="readonly")  # Vytvoření kombinovaného pole pro MD účet
        self.dal_combobox = ttk.Combobox(self, values=list(range(711)), state="readonly")  # Vytvoření kombinovaného pole pro DAL účet

        self.create_widgets()  # Vytvoření widgetů GUI

        self.last_valid_date = None  # Inicializace proměnné pro poslední platné datum

    def create_widgets(self):
        # Vytvoření hlavního rámu
        main_frame = ttk.Frame(self, padding=(10, 10, 10, 10), style="Main.TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # Vytvoření rámu pro vstupy
        entry_frame = ttk.Frame(main_frame, padding=(10, 10, 10, 10), style="Entry.TFrame")
        entry_frame.grid(row=0, column=0, sticky="nsew")

        # Posisek a vstupní pole
        ttk.Label(entry_frame, text="Datum", style="Entry.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Label(entry_frame, text="Číslo faktury", style="Entry.TLabel").grid(row=0, column=1, padx=5, pady=5, sticky="e")
        ttk.Label(entry_frame, text="Text", style="Entry.TLabel").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        ttk.Label(entry_frame, text="Doklad", style="Entry.TLabel").grid(row=0, column=3, padx=5, pady=5, sticky="e")
        ttk.Label(entry_frame, text="MD", style="Entry.TLabel").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        ttk.Label(entry_frame, text="DAL", style="Entry.TLabel").grid(row=0, column=5, padx=5, pady=5, sticky="e")
        ttk.Label(entry_frame, text="Částka", style="Entry.TLabel").grid(row=0, column=6, padx=5, pady=5, sticky="e")

        # Vytvoření vstupních polí
        self.date_entry = DateEntry(entry_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.invoice_number_entry = ttk.Entry(entry_frame)
        self.text_entry = ttk.Entry(entry_frame)
        self.doklad_entry = ttk.Combobox(entry_frame, values=Doklad.STANDARDNI_DOKLADY, state="readonly")
        self.md_button = ttk.Button(entry_frame, text="Vybrat účet", command=self.open_account_window_MD)
        self.dal_button = ttk.Button(entry_frame, text="Vybrat účet", command=self.open_account_window_DAL)
        self.amount_entry = ttk.Entry(entry_frame)

        # Rozmístění vstupních polí
        self.date_entry.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.invoice_number_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.text_entry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        self.doklad_entry.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.md_button.grid(row=1, column=4, padx=5, pady=5, sticky="ew")
        self.dal_button.grid(row=1, column=5, padx=5, pady=5, sticky="ew")
        self.amount_entry.grid(row=1, column=6, padx=5, pady=5, sticky="ew")

        # Vytvoření tlačítek pro přidání, odstranění a uložení
        ttk.Button(entry_frame, text="Přidat", command=self.add_entry, style="Entry.TButton").grid(row=2, column=0, columnspan=8, pady=10,
                                                                                                   sticky="ew")
        ttk.Button(entry_frame, text="Odstranit", command=self.delete_entry, style="Entry.TButton").grid(row=3, column=0, columnspan=8,
                                                                                                         pady=10, sticky="ew")
        ttk.Button(entry_frame, text="Uložit do CSV", command=self.save_to_csv, style="Entry.TButton").grid(row=4, column=0, columnspan=8,
                                                                                                           pady=10, sticky="ew")

        # Vytvoření rámu pro tabulku
        table_frame = ttk.Frame(main_frame, padding=(10, 0, 10, 10), style="Main.TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew")

        # Nastavení sloupců tabulky
        columns = ("Datum", "Číslo faktury", "Text", "Doklad", "MD", "DAL", "Částka")
        self.treeview = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, stretch=True)

        self.treeview.pack(fill=tk.BOTH, expand=True)

        self.treeview.bind("<Configure>", self.adjust_treeview_columns)
        self.treeview.bind("<Double-1>", self.edit_selected_row)
        self.treeview.bind("<MouseWheel>", self.on_mousewheel)  # Přidání možnosti scrollovat myší

        # Nastavení vlastností gridu
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=0)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        entry_frame.grid_rowconfigure(1, weight=1)
        entry_frame.grid_columnconfigure(0, weight=1)
        entry_frame.grid_columnconfigure(1, weight=1)
        entry_frame.grid_columnconfigure(2, weight=1)
        entry_frame.grid_columnconfigure(3, weight=1)
        entry_frame.grid_columnconfigure(4, weight=1)
        entry_frame.grid_columnconfigure(5, weight=1)
        entry_frame.grid_columnconfigure(6, weight=1)

    def add_entry(self):
        # Získání hodnot z vstupních polí
        date = self.date_entry.get()
        if date:
            self.last_valid_date = date  # Uložení posledního platného data
        else:
            date = self.last_valid_date  # Použití posledního platného data, pokud není zadáno nové datum
        invoice_number = self.invoice_number_entry.get()
        text = self.text_entry.get()
        doklad = self.doklad_entry.get()
        md = self.md_combobox.get()
        dal = self.dal_combobox.get()
        amount = self.amount_entry.get()

        # Vložení nového záznamu do tabulky
        self.treeview.insert("", "end", values=(date, invoice_number, text, doklad, md, dal, amount))

        if doklad not in self.accounts_MD_DAL:
            self.accounts_MD_DAL.append(doklad)

        # Vyčištění vstupních polí
        self.date_entry.delete(0, tk.END)
        self.invoice_number_entry.delete(0, tk.END)
        self.text_entry.delete(0, tk.END)
        self.doklad_entry.set("")
        self.md_combobox.set("")
        self.dal_combobox.set("")
        self.amount_entry.delete(0, tk.END)

        self.md_button.config(text="Vybrat účet")
        self.dal_button.config(text="Vybrat účet")

    def delete_entry(self):
        selected_item = self.treeview.selection()
        if selected_item:
            self.treeview.delete(selected_item)

    def adjust_treeview_columns(self, event=None):
        total_width = self.treeview.winfo_width()
        for col in self.treeview["columns"]:
            self.treeview.column(col, width=int(total_width / len(self.treeview["columns"])))

    def save_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                data = []
                for row_id in self.treeview.get_children():
                    row_data = self.treeview.item(row_id, "values")
                    data.append(row_data)

                df = pd.DataFrame(data, columns=["Datum", "Číslo faktury", "Text", "Doklad", "MD", "DAL", "Částka"])
                df.to_csv(file_path, index=False, encoding="utf-8-sig")  # Uložení dat do CSV souboru
            except Exception as e:
                print("Chyba při uložení souboru formátu CSV:", e)

    def open_account_window_MD(self):
        self.open_account_window("MD")

    def open_account_window_DAL(self):
        self.open_account_window("DAL")

    def open_account_window(self, target):
        account_window = AccountWindow(parent=self, accounts=ACCOUNTS, target=target, callback=self.set_account_entry)
        main_width = self.winfo_width()
        main_height = self.winfo_height()
        window_width = account_window.winfo_reqwidth()
        window_height = account_window.winfo_reqheight()
        x = self.winfo_rootx() + main_width // 2 - window_width // 2
        y = self.winfo_rooty() + main_height // 2 - window_height // 2
        account_window.geometry("+{}+{}".format(x, y))

    def edit_selected_row(self, event):
        item = self.treeview.selection()[0]
        column = self.treeview.identify_column(event.x)
        if column:
            self.treeview.focus(item)
            self.treeview.selection_set(item)
            cell_value = self.treeview.item(item, 'values')[int(column.replace('#', '')) - 1]
            self.edit_cell_popup(item, column, cell_value)

    def edit_cell_popup(self, item, column, cell_value):
        def save_changes():
            new_value = entry.get()
            self.treeview.set(item, column, new_value)
            popup.destroy()

        popup = tk.Toplevel(self)
        popup.title("Upravit buňku")
        popup.geometry("200x100+{}+{}".format(self.winfo_rootx() + self.winfo_width() // 2 - 100, self.winfo_rooty() + self.winfo_height() // 2 - 50))
        popup.resizable(False, False)

        entry = ttk.Entry(popup)
        entry.insert(0, cell_value)
        entry.pack(pady=10)

        save_button = ttk.Button(popup, text="Save", command=save_changes)
        save_button.pack(pady=5)

    def on_mousewheel(self, event):
        self.treeview.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def set_account_entry(self, selected_account, target):
        if selected_account:
            if target == "MD":
                self.md_combobox.set(selected_account)
                self.md_button.config(text=selected_account)
            elif target == "DAL":
                self.dal_combobox.set(selected_account)
                self.dal_button.config(text=selected_account)


class AccountWindow(tk.Toplevel):
    def __init__(self, parent, accounts, target, callback):
        super().__init__(parent)
        self.title("Select Account")  # Nastavení titulku okna
        self.parent = parent
        ttk.Label(self, text="Select Account:").pack(pady=10)  # Popisek pro výběr účtu
        self.account_combobox = ttk.Combobox(self, values=accounts, state="readonly")  # Vytvoření kombinovaného pole pro výběr účtu
        self.account_combobox.pack(pady=10)
        self.account_combobox.bind("<<ComboboxSelected>>", self.update_selected_account_label)  # Nastavení události pro výběr účtu
        ttk.Button(self, text="OK", command=lambda: self.ok_button_clicked(callback, target)).pack(pady=10)  # Tlačítko OK pro potvrzení výběru

    def update_selected_account_label(self, event):
        selected_account = self.account_combobox.get()
        md_combobox = self.parent.md_combobox
        dal_combobox = self.parent.dal_combobox
        if md_combobox == event.widget:
            md_combobox.set(selected_account)
            self.parent.md_button.config(text=selected_account)
        elif dal_combobox == event.widget:
            dal_combobox.set(selected_account)
            self.parent.dal_button.config(text=selected_account)

    def ok_button_clicked(self, callback, target):
        selected_account = self.account_combobox.get()
        if selected_account:
            callback(selected_account, target)
        self.destroy()


if __name__ == "__main__":
    try:
        app = AccountingJournalApp()  # Vytvoření instance aplikace
        app.geometry("900x600")  
        app.style = ttk.Style()  
        app.style.theme_use("clam")  
        app.style.configure("Main.TFrame", background="#f0f0f0")  
        app.style.configure("Entry.TFrame", background="#e0e0e0")
        app.style.configure("Entry.TLabel", background="#e0e0e0")  
        app.style.configure("Entry.TButton", background="#f0f0f0")  
        app.mainloop() 
    except Exception as e:
        print("Chyba:", e)  # Vypsání chyby, pokud došlo k výjimce
