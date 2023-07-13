import tkinter.messagebox

import customtkinter as ctk
import sqlite3
from CTkListbox import *

conn = sqlite3.connect('info.db')
cursor = conn.cursor()
'''cursor.execute("CREATE TABLE IF NOT EXISTS contacts (name TEXT, surname TEXT, phone INT, email TEXT)")
conn.commit()'''
root = ctk.CTk()
root.geometry('300x500')
contacts_list = CTkListbox(root, 300, 300, fg_color='black', label_fg_color='white')
contacts_list.place(x=0, y=40)


# Функция для отображения контактов


def updating_all_contacts_FUNC():
    for i in range(contacts_list.size()):
        try:
            contacts_list.delete(i)
        except:
            pass
    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    for i in range(len(data)):
        contacts_list.insert(i, data[i][0] + " " + data[i][1])
    root.update()

def updating_special_contact_FUNC(list_with_tuple):
    for i in range(contacts_list.size()):
        try:
            contacts_list.delete(i)
        except:
            pass
    i = 0
    for tuple in list_with_tuple:
        cursor.execute("SELECT * FROM contacts WHERE name=? and surname=?", (tuple[0], tuple[1]))
        data = cursor.fetchone()
        contacts_list.insert(i, data[0] + " " + data[1])
        root.update()
        i += 1

# Функции добавления контакта
def adding_FUNC(e1, e2, e3, e4, o):
    cursor.execute("SELECT * FROM contacts WHERE name=? and surname=?", (e1.get(), e2.get()))
    data = cursor.fetchall()
    if len(data) > 0:
        tkinter.messagebox.showerror("Error!", "In your contacts there is contact with same name and surname.")
        return
    if not e3.get().isdigit():
        tkinter.messagebox.showerror("Error!", "You wrote letters in box for phone number (box №3), number should look like that: 89173544578")
        return
    cursor.execute("INSERT INTO contacts (name, surname, phone, email) VALUES (?, ?, ?, ?)",
                   (e1.get(), e2.get(), int(e3.get()), e4.get()))
    conn.commit()
    o.destroy()
    updating_all_contacts_FUNC()


def add_new_contact_FUNC():
    o = ctk.CTkToplevel(root)
    o.geometry('300x300')
    names = ctk.CTkEntry(o)
    names.pack()
    sirname = ctk.CTkEntry(o)
    sirname.pack()
    number = ctk.CTkEntry(o)
    number.pack()
    nail = ctk.CTkEntry(o)
    nail.pack()
    but_add = ctk.CTkButton(o, command=lambda: adding_FUNC(names, sirname, number, nail, o), text='Добвавить')
    but_add.pack()


# Функция удаления контакта
def delete_contact_FUNC():
    try:
        list = contacts_list.get().split(" ")
        cursor.execute("DELETE FROM contacts WHERE name=? and surname=?", (list[0], list[1]))
        conn.commit()
        updating_all_contacts_FUNC()
    except:
        tkinter.messagebox.showerror("Error!", "No contact selected. Please select a contact to delete.")
        return


# Функция просмотра инфрмации контакта
def show_info_FUNC():
    try:
        list = contacts_list.get().split()
        o = ctk.CTkToplevel(root)
        o.geometry('300x300')
        cursor.execute("SELECT * FROM contacts WHERE name=? and surname=?", (list[0], list[1]))
        data = cursor.fetchone()
        names = ctk.CTkLabel(o, text=data[0])
        names.pack()
        sirname = ctk.CTkLabel(o, text=data[1])
        sirname.pack()
        number = ctk.CTkLabel(o, text=str(data[2]))
        number.pack()
        nail = ctk.CTkLabel(o, text=data[3])
        nail.pack()
    except:
        tkinter.messagebox.showerror("Error!", "No contact selected. Please select a contact to see an info.")
        return


# Функции редактирования инфрмации контакта
def edit(names, sirname, number, nail, o, names1, sirname1, number1, nail1):
    if not number.isdigit():
        tkinter.messagebox.showerror("Error!", "You wrote letters in box for phone number (box №3), number should look like that: 89173544578")
        return
    cursor.execute("SELECT * FROM contacts WHERE name=? and surname=?", (names, sirname))
    data = cursor.fetchall()
    if len(data) > 0:
        if names != names1:
            tkinter.messagebox.showerror("Error!", "In your contacts there is contact with same name and surname.")
            return
    cursor.execute(
        "UPDATE contacts SET name=?, surname=?, phone=?, email=? WHERE name=? and surname=? and phone=? and email=?",
        (names, sirname, number, nail, names1, sirname1, number1, nail1))
    conn.commit()
    o.destroy()
    updating_all_contacts_FUNC()


def red_info_FUNC():
    try:
        list = contacts_list.get().split()
        o = ctk.CTkToplevel(root)
        o.geometry('300x300')
        cursor.execute("SELECT * FROM contacts WHERE name=? and surname=?", (list[0], list[1]))
        data = cursor.fetchone()
        names = ctk.CTkEntry(o)
        names.pack()
        names.insert(0, data[0])
        sirname = ctk.CTkEntry(o)
        sirname.pack()
        sirname.insert(0, data[1])
        number = ctk.CTkEntry(o)
        number.pack()
        number.insert(0, data[2])
        nail = ctk.CTkEntry(o)
        nail.pack()
        nail.insert(0, data[3])
        o.update()
        but_add = ctk.CTkButton(o, text='Сохранить',
                                command=lambda: edit(names.get(), sirname.get(), number.get(), nail.get(), o, data[0],
                                                     data[1], data[2], data[3]))
        but_add.pack()
    except:
        tkinter.messagebox.showerror("Error!", "No contact selected. Please select a contact to edit an information.")
        return

# Search func

def search_FUNC():
    text=search_ENTRY.get().split(' ')
    if len(text) == 0:
        return
    if len(text) == 2:
        # Searching by name and surname
        cursor.execute("SELECT * FROM contacts WHERE name=? surname=?", (text[0], text[1]))
        data = cursor.fetchall()
        if len(data) == 0:
            return
        # Showing contact
        return
    # elif len(text) == 1:
    #     # Searching by name or surname
    #     cursor.execute("SELECT * FROM contacts WHERE name=? OR surname=?", (text[0], text[0]))
    #     data = cursor.fetchall()
    #     if len(data) > 0:
    #         # Showing contact/contacts
    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    data_names_surnames = [(i[0], i[1]) for i in data]
    cort = []
    for o in data_names_surnames:
        if text[0].lower() in o[0].lower() or text[0].lower() in o[1].lower():
            cort.append(o)
    print(cort)
    updating_special_contact_FUNC(cort)

# Sort Func
def sorting_FUCN():
    if sort_comb.get() == '':
        return
    cursor.execute("SELECT * FROM contacts")
    data = cursor.fetchall()
    data_names_surnames = [(i[0], i[1]) for i in data]
    if sort_comb.get() == 'Имя':
        data_names_surnames.sort(key=lambda b: b[0])
        updating_special_contact_FUNC(data_names_surnames)
    elif sort_comb.get() == 'Фамилия':
        data_names_surnames.sort(key=lambda b: b[1])
        updating_special_contact_FUNC(data_names_surnames)

# Кнопки для взаимодействия с контактами

delete_BUTTON = ctk.CTkButton(root, text='Удалить', width=50, command=delete_contact_FUNC)
delete_BUTTON.place(x=10, y=360)
add_BUTTON = ctk.CTkButton(root, text='Добавить', width=50, command=add_new_contact_FUNC)
add_BUTTON.place(x=70, y=360)
show_info_BUTTON = ctk.CTkButton(root, text='Посмотреть', width=50, command=show_info_FUNC)
show_info_BUTTON.place(x=130, y=360)
red_info_BUTTON = ctk.CTkButton(root, text='Изменить', width=50, command=red_info_FUNC)
red_info_BUTTON.place(x=190, y=360)

# Search stuff

search_ENTRY = ctk.CTkEntry(root, width=200)
search_ENTRY.place(x=0, y=0)
search_BUTTON = ctk.CTkButton(root, text='', width=20, command=search_FUNC)
search_BUTTON.place(x=210, y=0)

# Sort stuff
sort_comb = ctk.CTkComboBox(root, values=['Имя', 'Фамилия'], state="readonly")
sort_comb.place(x=10, y=400)
search_BUTTON = ctk.CTkButton(root, text='Сортировать', width=20, command=sorting_FUCN)
search_BUTTON.place(x=150, y=400)

updating_all_contacts_FUNC()
root.mainloop()
