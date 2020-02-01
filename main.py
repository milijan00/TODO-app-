import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb
from database_manager import DBManager
APP_NAME = 'To do v0.1'
class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(APP_NAME)
        self.resizable(width=False, height=False)
        self.selected_note = ''
        self.frames = {}
        self.master_frame = tk.Frame(self)
        self.master_frame.pack(fill='both', expand=True)
        for frame in (Home, Add, Show):
            self.frames[frame] = frame(self, self.master_frame)
            self.frames[frame].grid(row=0, column=0, sticky='nsew')
        self.frames[Home].tkraise()

class Home(tk.Frame):
    def __init__(self, base, master):
        tk.Frame.__init__(self, master)
        self.master = tk.Frame(self)
        self.master.pack(fill='both', expand=True)
        self.users_notes = tk.Listbox(self.master, width='50', height='20')
        self.users_notes.pack(fill='x', side='top')
        self.frame_bottom = tk.Frame(self.master)
        self.frame_bottom.pack(fill='x', padx=2, pady=2)
        tk.Button(self.frame_bottom, text='Add', command=lambda:base.frames[Add].tkraise()).pack(side='right')
        tk.Button(self.frame_bottom, text='Show note', command=lambda b=base: self.show_note(base)).pack(side='right')
        tk.Button(self.frame_bottom, text='Delete', command=self.delete_note).pack(side='right')
        tk.Button(self.frame_bottom, text='Refresh', command=self.load_notes).pack(side='right')
        self.load_notes()
    def show_note(self, base)->None:
        #before Show frame is revealed we have to check weather our user has selected a note or not
        if self.users_notes.curselection():
            base.selected_note = self.users_notes.get(tk.ACTIVE)
            base.frames[Show].tkraise()
    def load_notes(self)->None:
        '''loading notes from database and adding them to listbox'''
        try:
            self.users_notes.delete(0, 'end')
            db_manager = DBManager()
            db_manager.make_connection('./data.db')
            db_manager.cursor.execute('''select * from notes;''')
            database_selection = db_manager.get_selection()
            notes = [database_selection[i][0] for i in range(len(database_selection))]
            for note in notes:
                self.users_notes.insert('end', note)
            db_manager.disconnect()
        except Exception as e:
            mb.showinfo('ERROR3', 'UNABLE TO LOAD DATABASE')
    def delete_note(self)->None:
        if self.users_notes.curselection() and mb.askyesno(APP_NAME, 'Are you sure you want to delete ' + self.users_notes.get(tk.ACTIVE) + '?'):
            index = self.users_notes.curselection()
            selected_item =  self.users_notes.get(tk.ACTIVE)
            try:
                db_manager = DBManager()
                db_manager.make_connection('./data.db')
                db_manager.cursor.execute('''delete from notes where name = ?;''', (selected_item,))
                db_manager.disconnect()
                self.users_notes.delete(index)
            except Exception as e:
                mb.showinfo('ERROR2', 'DELETING NOTE IS IMPOSSIBLE')
            # print(selected_item, self.users_notes.index(selected_item))
class Add(tk.Frame):
    def __init__(self, base, master):
        tk.Frame.__init__(self, master)
        self.master = tk.Frame(self)
        self.master.pack()
        self.frame_top = tk.Frame(self.master)
        self.frame_top.pack(pady=5)
        tk.Label(self.frame_top, text='Name:').pack(side='left')
        self.note_name = tk.Entry(self.frame_top)
        self.note_name.pack(side='left')
        self.note_content = tk.Text(self.master, width='50', height='17')
        self.note_content.pack(fill='x')
        self.frame_bottom = tk.Frame(self.master)
        self.frame_bottom.pack(fill='x', padx=2, pady=2)
        tk.Button(self.frame_bottom, text='Add', command=self.add).pack(side='right')
        tk.Button(self.frame_bottom, text='Back', command=lambda: base.frames[Home].tkraise()).pack(side='right')
    def add(self)->None:
        '''add entered input into database'''
        #check input, both notename and content
        if self.note_name.get() and self.note_content.get('1.0', 'end-1c'):
            #insert data into database with specific order
            # note_name, note_content
            #firstly make sure that this note doesn't exist
            try:
                db_manager = DBManager()
                db_manager.make_connection('./data.db')
                values = (self.note_name.get(), self.note_content.get('1.0', 'end-1c'))
                db_manager.cursor.execute('''INSERT INTO notes VALUES(?, ?)''', values)
                db_manager.disconnect()
                mb.showinfo('Information', values[0] + ' has been successfuly added!')
            except:
                mb.showinfo('ERROR1', "THIS OPERATION ISN'T POSSIBLE")
    def clear_input(self)->None:
        '''clears entered input after inserting them into database'''
class Show(tk.Frame):
    NORMAL_FONT = ('Arial', 14)
    def __init__(self, base, master):
        tk.Frame.__init__(self, master)
        self.master = tk.Frame(self)
        self.master.pack()
        self.note_name = tk.Label(self.master, text='Note name', font=self.NORMAL_FONT)
        self.note_name.pack()
        self.note_content = tk.Text(self.master, font=self.NORMAL_FONT, width='50', height='15')
        self.note_content.pack()
        self.frame_bottom = tk.Frame(self.master)
        self.frame_bottom.pack(side='bottom')
        tk.Button(self.frame_bottom, text='Go to Home', command=lambda:base.frames[Home].tkraise()).pack(side='right')
        tk.Button(self.frame_bottom, text='Display note', command=lambda b=base: self.display_note(b)).pack(side='right')
    def display_note(self, base)->None:
        '''displays selected note's name and content'''
        try:
            db_manager = DBManager()
            db_manager.make_connection('./data.db')
            db_manager.cursor.execute('''select * from notes where name = ?''', (base.selected_note,))
            database_selection = db_manager.get_selection()
            name = database_selection[0][0]
            content = database_selection[0][1]
            self.note_name['text'] = name
            self.note_content.delete('1.0', 'end')
            self.note_content.insert('end', content)
        except Exception as e:
            raise
if __name__ == '__main__':
    app = App()
    app.mainloop()
