#! /usr/bin/env python3
#GeologyDict by Ali M
import sqlite3 as sqlite
import tkinter as tk
from tkinter import Text
from tkinter import Entry
from tkinter import Scrollbar
from tkinter import ttk

#GUI Widgets


class GeologyDict:
    def __init__(self, master):

        master.title("EsperantoDict")
        master.resizable(False, False)
        master.configure(background='#EAFFCD')

        self.style = ttk.Style()
        self.style.configure("TFrame", background='#EAFFCD')
        self.style.configure("TButton", background='#EAFFCD')
        self.style.configure("TLabel", background='#EAFFCD')

        self.frame_header = ttk.Frame(master, relief=tk.FLAT)
        self.frame_header.pack(side=tk.TOP, padx=5, pady=5)

        self.logo = tk.PhotoImage(file=r'C:\Geologydict\eo.png')
        self.small_logo = self.logo.subsample(10, 10)

        ttk.Label(self.frame_header, image=self.small_logo).grid(row=0, column=0, stick="ne", padx=5, pady=5, rowspan=2)
        ttk.Label(self.frame_header, text='EsperantoDict', font=('Arial', 18, 'bold')).grid(row=0, column=1)

        self.frame_content = ttk.Frame(master)
        self.frame_content.pack()

        self.entry_search = ttk.Entry(self.frame_content)
        self.entry_search.grid(row=0, column=0)
        self.entry_search.insert(tk.END, "Type to Search")
        self.entry_search.bind('<Button-1>', self.entry_delete)

        self.button_search = ttk.Button(self.frame_content, text="Search")
        self.aks = tk.PhotoImage(file=r'C:\Geologydict\search.png')
        self.small_aks = self.aks.subsample(3, 3)
        self.button_search.config(image=self.small_aks, compound=tk.LEFT)
        self.button_search.grid(row=0, column=1, columnspan=2)

        self.listbox = tk.Listbox(self.frame_content, height=28)
        self.listbox.grid(row=1, column=0)
        self.scrollbar = ttk.Scrollbar(self.frame_content, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=1, sticky='ns')
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.bind('<<ListboxSelect>>', self.enter_meaning)

        self.textbox = tk.Text(self.frame_content, width=60, height=27)
        self.textbox.grid(row=1, column=2)

    # SQLite
        self.db = sqlite.connect(r'C:\Geologydict\test.db')
        self.cur = self.db.cursor()
        self.cur.execute('SELECT Esperanto FROM Words')
        for row in self.cur:
            self.listbox.insert(tk.END, row)

    # SQLite

    def enter_meaning(self, tag):
        self.textbox.delete(1.0, tk.END)
        if self.listbox.curselection():
            for row in self.cur.execute('SELECT English FROM Words'):
                self.textbox.insert(tk.END, row)

    def entry_delete(self, tag):
        self.entry_search.delete(0, tk.END)
        return None


def main():
    root = tk.Tk()
    geologydict = GeologyDict(root)
    root.mainloop()

if __name__ == '__main__': main()