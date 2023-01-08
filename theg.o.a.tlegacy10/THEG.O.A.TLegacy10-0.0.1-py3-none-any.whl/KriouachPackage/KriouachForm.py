import tkinter as tk
import os
from tkinter import Entry, StringVar, messagebox
import csv


def clear_form():
    id_entry.delete(0, 'end')
    nom_entry.delete(0, 'end')
    prenom_entry.delete(0, 'end')
    group_entry.delete(0, 'end')
    note_entry.delete(0, 'end')

def send_to_csv():
    id = id_entry.get()
    nom = nom_entry.get()
    prenom = prenom_entry.get()
    group = group_entry.get()
    note = note_entry.get()

    with open('user_info.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == id:
                messagebox.showerror("Error", "ID already exists")
                return

    if id.isdigit() and nom.isalpha() and prenom.isalpha() and group.isalpha() and (note.isdigit() or note.replace('.', '', 1).isdigit()):
        with open('user_info.csv', 'a') as file:
            file.write(f"{id},{nom},{prenom},{group},{note}\n")
        messagebox.showinfo("Success", "Information saved successfully")
    else:
        messagebox.showerror("Error", "Invalid input")
    
    id_entry.delete(0, 'end')
    nom_entry.delete(0, 'end')
    prenom_entry.delete(0, 'end')
    group_entry.delete(0, 'end')
    note_entry.delete(0, 'end')


def search_and_delete():
    user_id = search_entry.get()
    if not user_id.isdigit():
        messagebox.showerror("Error", "Invalid ID")
        return

    # read the data from the CSV file
    with open('user_info.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # search for the user with the specified ID
    for i, row in enumerate(data):
        if row[0] == user_id:
            # user found
            if messagebox.askyesno("Confirm", "Do you want to delete this user?"):
                # delete user by excluding the user's row from the data
                data = [row for row in data if row[0] != user_id]
                # save the updated data to the CSV file
                with open('user_info.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
                messagebox.showinfo("Success", "User deleted successfully")
            return
    # user not found
    messagebox.showinfo("Not found", "No user with the specified ID was found")

def close_window():
    root.destroy()
    window = tk.Tk()
    window.geometry("600x400")
    window.title("USERS Data updater")
    
    def show_data():
        with open('user_info.csv', 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
            for i, row in enumerate(data[1:]):
                id, nom, prenom, group, note = row
                note_var = StringVar(value=note)
                tk.Label(window, text=id).grid(row=i+1, column=0)
                tk.Label(window, text=nom).grid(row=i+1, column=6)
                tk.Label(window, text=prenom).grid(row=i+1, column=12)
                tk.Label(window, text=group).grid(row=i+1, column=18)
                tk.Entry(window, textvariable=note_var, width=5).grid(row=i+1, column=24)
                tk.Button(window, text="Update", command=lambda r=i+1, n=note_var: update_note(r, n.get())).grid(row=i+1, column=30)
    def update_note(row, new_note):
        with open('user_info.csv', 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
            data[row][4] = new_note
            with open('user_info.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
    tk.Label(window, text="Search by ID:").grid(row=0, column=0)
    global search_entry
    search_entry = tk.Entry(window)
    search_entry.grid(row=0, column=1)
    tk.Button(window, text="Search and delete", command=search_and_delete).grid(row=0, column=2)
    
    show_data()
    window.mainloop()


root = tk.Tk()
root.geometry("150x300")
root.title("User Form")


id_label = tk.Label(root, text="ID")
id_label.pack()
id_entry = Entry(root)
id_entry.pack()


nom_label = tk.Label(root, text="Nom")
nom_label.pack()
nom_entry = Entry(root)
nom_entry.pack()


prenom_label = tk.Label(root, text="Prenom")
prenom_label.pack()
prenom_entry = Entry(root)
prenom_entry.pack()


group_label = tk.Label(root, text="Group")
group_label.pack()
group_entry = Entry(root)
group_entry.pack()


note_label = tk.Label(root, text="Note")
note_label.pack()
note_entry = Entry(root)
note_entry.pack()


clear_button = tk.Button(root, text="Clear Form", command=clear_form)
clear_button.pack()


send_button = tk.Button(root, text="Send form", command=send_to_csv)
send_button.pack()


close_button = tk.Button(root, text="See the users", command=close_window)
close_button.pack()


if not os.path.exists('user_info.csv'):
    with open('user_info.csv', 'w') as file:
        file.write("ID,NOM,PRENOM,GROUP,NOTE\n")


root.mainloop()