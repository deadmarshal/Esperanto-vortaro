#! /usr/bin/env python3
#EsperantoDict by Ali M
import sqlite3 as sqlite
import tkinter as tk
from tkinter import ttk
#GUI Widgets


class EsperantoDict:
    def __init__(self, master):

        master.title("EsperantoDict")
        master.iconbitmap("Esperanto.ico")
        master.resizable(False, False)
        master.configure(background='#EAFFCD')
        self.style = ttk.Style()
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.update_list())

        self.style = ttk.Style()
        self.style.configure("TFrame", background='#EAFFCD')
        self.style.configure("TButton", background='#C6FF02')
        self.style.configure("TLabel", background='#EAFFCD')

        self.frame_header = ttk.Frame(master, relief=tk.FLAT)
        self.frame_header.config(style="TFrame")
        self.frame_header.pack(side=tk.TOP, padx=5, pady=5)

        self.logo = tk.PhotoImage(file=r'C:\EsperantoDict\eo.png')
        self.small_logo = self.logo.subsample(10, 10)

        ttk.Label(self.frame_header, image=self.small_logo).grid(row=0, column=0, stick="ne", padx=5, pady=5, rowspan=2)
        ttk.Label(self.frame_header, text='EsperantoDict', font=('Arial', 18, 'bold')).grid(row=0, column=1)

        self.frame_content = ttk.Frame(master)
        self.frame_content.config(style="TFrame")
        self.frame_content.pack()

        self.entry_search = ttk.Entry(self.frame_content, textvariable=self.search_var, width=30)
        self.entry_search.bind('<FocusIn>', self.entry_delete)
        self.entry_search.bind('<FocusOut>', self.entry_insert)
        self.entry_search.grid(row=0, column=0, padx=5)
        self.entry_search.focus()
        self.entry_search.bind("<Key>", self.edit_input)

        self.button_search = ttk.Button(self.frame_content, text="Search")
        self.photo_search = tk.PhotoImage(file=r'C:\EsperantoDict\search.png')
        self.small_photo_search = self.photo_search.subsample(3, 3)
        self.button_search.config(image=self.small_photo_search, compound=tk.LEFT, style="TButton")
        self.button_search.grid(row=0, column=2, columnspan=1, sticky='nw', padx=5)

        self.listbox = tk.Listbox(self.frame_content, height=30, width=30)
        self.listbox.grid(row=1, column=0, padx=5)
        self.scrollbar = ttk.Scrollbar(self.frame_content, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=1, sticky='nsw')
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.bind('<<ListboxSelect>>', self.enter_meaning)

        self.textbox = tk.Text(self.frame_content, relief=tk.GROOVE, width=60, height=30, borderwidth=2)
        self.textbox.config(wrap='word')
        self.textbox.grid(row=1, column=2, sticky='w', padx=5)

        # SQLite
        self.db = sqlite.connect(r'C:\EsperantoDict\test.db')
        self.cur = self.db.cursor()
        self.cur.execute('SELECT Esperanto FROM Words ORDER BY Esperanto')
        for row in self.cur:
            self.listbox.insert(tk.END, row)
        for row in range(0, self.listbox.size(), 2):
            self.listbox.itemconfigure(row, background="#f0f0ff")
            self.update_list()

    def update_list(self):
        search_term = self.search_var.get()
        for item in self.listbox.get(0, tk.END):
            if search_term.lower() in item:
                self.listbox.delete(0, tk.END)
                self.listbox.insert(tk.END, item)

    def edit_input(self, tag):
        words = ["ĝ", "ĉ", "ĥ", "ĵ", "ŭ", "ŝ"]
        char = ["gx", "cx", "hx", "jx", "ux", "sx"]
        result = ''
        if True:
            user_in = self.search_var.get().lower()
            if user_in in char:
                if char[0] in user_in:
                    result = words[0]
                elif char[1] in user_in:
                    result = words[1]
                elif char[2] in user_in:
                    result = words[3]
                elif char[3] in user_in:
                    result = words[2]
                elif char[4] in user_in:
                    result = words[4]
            return self.entry_search.insert(tk.END, result)

    # SQLite
    def enter_meaning(self, tag):
        for index in self.listbox.curselection():
            esperanto = self.listbox.get(index)
            results = self.cur.execute("SELECT English FROM Words WHERE Esperanto = ?", esperanto)
            for row in results:
                self.textbox.delete(1.0, tk.END)
                self.textbox.insert(tk.END, row)

    def entry_delete(self, tag):
        self.entry_search.delete(0, tk.END)
        return None

    def entry_insert(self, tag):
        self.entry_search.delete(0, tk.END)
        self.entry_search.insert(0, "Type to Search")
        return None


def main():
    root = tk.Tk()
    esperantodict = EsperantoDict(root)
    root.mainloop()


if __name__ == '__main__': main()

# db tbl name: Words
# db first field name: Esperanto
# db second field name: English
