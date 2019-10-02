#!/usr/bin/python3
# EsperantoDict Written by: Ali M
import sqlite3 as sqlite
import tkinter as tk
from tkinter import ttk


# GUI Widgets

class EsperantoDict:
    def __init__(self, master):

        master.title("EsperantoVortaro")
        master.iconbitmap("Esperanto.ico")
        master.resizable(False, False)
        master.configure(background='#EAFFCD')

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
        ttk.Label(self.frame_header, text='EsperantoVortaro', font=('Arial', 18, 'bold')).grid(row=0, column=1)

        self.frame_content = ttk.Frame(master)
        self.frame_content.config(style="TFrame")
        self.frame_content.pack()

        self.entry_search = ttk.Entry(self.frame_content, textvariable=self.search_var, width=30)
        self.entry_search.bind('<FocusIn>', self.entry_delete)
        self.entry_search.bind('<FocusOut>', self.entry_insert)
        self.entry_search.grid(row=0, column=0, padx=5)
        self.entry_search.focus()
        self.entry_search.bind("<KeyRelease>", self.edit_input)

        self.button_search = ttk.Button(self.frame_content, text=u"Serĉu", command=self.button)
        self.photo_search = tk.PhotoImage(file=r'C:\EsperantoDict\search.png')
        self.small_photo_search = self.photo_search.subsample(3, 3)
        self.button_search.config(image=self.small_photo_search, compound=tk.LEFT, style="TButton")
        self.button_search.grid(row=0, column=2, columnspan=1, sticky='nw', padx=5)
        self.button_search.bind('<Return>', self.button)

        self.listbox = tk.Listbox(self.frame_content, height=30, width=30)
        self.listbox.grid(row=1, column=0, padx=5)
        self.scrollbar = ttk.Scrollbar(self.frame_content, orient=tk.VERTICAL, command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=1, sticky='nsw')
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.bind('<<ListboxSelect>>', self.enter_meaning)

        self.textbox = tk.Text(self.frame_content, relief=tk.GROOVE, width=60, height=30, borderwidth=2)
        self.textbox.config(wrap='word')
        self.textbox.grid(row=1, column=2, sticky='w', padx=5)
        self.textbox.tag_configure("center", justify="center")
        self.textbox.tag_add("center", 1.0, "end")

        self.menubar = tk.Menu(master)
        master.configure(menu=self.menubar)
        master.option_add('*tearOff', False)
        self.about = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.about, label='Helpo')
        self.about.add_command(label='Pri ni', command=self.menu_click)

        # SQLite
        self.db = sqlite.connect(r'C:\EsperantoDict\test.db')
        self.cur = self.db.cursor()
        self.cur.execute("SELECT Esperanto FROM Words ORDER BY Esperanto")

        for row in self.cur:
            self.listbox.insert(tk.END, row)
            self.update_list()

    def update_list(self):
        self.listbox.delete(0, tk.END)
        search_term = self.search_var.get().lower()
        if search_term == 'type to search':
            search_term = ''
        self.cur.execute("SELECT Esperanto FROM Words WHERE LOWER(Esperanto) LIKE ? ORDER BY Esperanto",
                         ('%' + search_term + '%',))
        for row in self.cur:
            self.listbox.insert(tk.END, row[0])
        for row in range(0, self.listbox.size(), 2):
            self.listbox.itemconfigure(row, background="#f0f0ff")

    def edit_input(self, tag):
        word_to_esp = {'gx': 'ĝ', 'cx': 'ĉ', 'hx': 'ĥ', 'jx': 'ĵ', 'ux': 'ŭ', 'sx': 'ŝ'}
        user_input = self.entry_search.get()
        user_input = user_input.lower()
        for i in word_to_esp:
            if i in user_input:
                user_input = user_input.replace(i, word_to_esp[i])
                return self.search_var.set(user_input)

    def enter_meaning(self, tag=None):
        index = self.listbox.curselection()
        esperanto = self.listbox.get(index)
        eng_words = self.cur.execute("SELECT English FROM Words WHERE Esperanto = ?", (esperanto,))
        for word in eng_words:
            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.END, word[0])

    def entry_delete(self, tag):
        if self.entry_search.get():
            self.entry_search.delete(0, tk.END)
            self.textbox.delete(1.0, tk.END)
        return None

    def entry_insert(self, tag):
        if self.entry_search.get() == '':
            self.entry_search.insert(0, "Type to Search")
        return None

    @staticmethod
    def menu_click():
        import doctest
        window = tk.Toplevel(doctest.master, width=300, height=200)
        window.title("Pri ni")

    def button(self):
        esperanto = self.search_var.get()
        results = self.cur.execute("SELECT English FROM Words WHERE LOWER (Esperanto) = ?", (esperanto,))
        for row2 in results:
            self.textbox.delete(1.0, tk.END)
            self.textbox.insert(tk.END, row2[0])


def main():
    root = tk.Tk()
    EsperantoDict(root)
    root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
    root.mainloop()


if __name__ == '__main__':
    main()

# db tbl name: Words
# db first field name: Esperanto
# db second field name: English
