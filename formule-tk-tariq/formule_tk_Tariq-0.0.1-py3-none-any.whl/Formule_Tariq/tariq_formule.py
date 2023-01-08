from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from csv import writer
from csv import *
import os
import asyncio
import re


my_w=Tk()

my_w.geometry("1000x1000")
my_w.title("inscreprion formule")
filepath = os.path.join(os.getcwd(),'myfile.csv')
regex = '[0-9]+\.?[0-9]+'
if not os.path.exists(filepath):
    with open("myfile.csv","w",newline="") as fobj:
        wt=writer(fobj,delimiter=',')
        wt.writerow(["ID","NOM","PRENOM","GROUPE","NOTE"])
fichier=open(os.path.join(os.getcwd(),'myfile.csv'))
fileObject=reader(fichier)

rows_number=sum(1 for row in fileObject)

#Send_function
def envoyer():
    global rows_number
    nom_info=nom_entry.get()
    prenonom_info=prenom_entry.get()
    groupe_info=groupe_entry.get()
    note_info=note_entry.get()   
    if len(nom_info)==0 or len(prenonom_info)==0 or len(groupe_info)==0 or len(note_info)==0:
        messagebox.showerror("error de valodation", "l'un des champs est vide")    
    else:
        try :
            if any (ch.isdigit() for ch in nom_info) :
                messagebox.showerror("error de valodation", "Le nom ne doit pas contenir des caractère numérique")    
            elif any (i.isdigit() for i in prenonom_info) :
                messagebox.showerror("error de valodation", "Le prenom ne doit pas contenir des caractère numérique")    
            elif not (re.search(regex, note_info)):
                messagebox.showerror("error de valodation", "La note doit etre decimal")    
                    

            else:
                with open("myfile.csv","a",newline="") as fobj:        
                    wt=writer(fobj)        
                    wt.writerow([rows_number,nom_info,prenonom_info,groupe_info,note_info])
                fobj.close()
                
                remplir_tree()

                rows_number=rows_number+1
        except:
            messagebox.showerror("error de valodation", "un erreur est servenu")
        
def clear_text():
   nom_entry.delete(0, END)
   prenom_entry.delete(0, END)
   groupe_entry.delete(0, END)
   note_entry.delete(0, END)
clear_button=Button(my_w,text="Vider",command=clear_text,height=2,width=10)
clear_button.grid(row=5,column=3,padx=50,pady=25)
#LABELS
nom_label=Label(my_w,text="Nom",font=("Helvetica", 15))
nom_label.grid(row=0,column=0,sticky=W)
prenom_label=Label(my_w,text="Prenom",font=("Helvetica", 15))
prenom_label.grid(row=1,column=0,sticky=W)
groupe_label=Label(my_w,text="Groupe",font=("Helvetica", 15))
groupe_label.grid(row=2,column=0,sticky=W)
note_label=Label(my_w,text="Note",font=("Helvetica", 15))
note_label.grid(row=3,column=0,sticky=W)


#Entrys
nom_entry=Entry(my_w)
nom_entry.grid(row=0,column=1,sticky=W,padx=15)
prenom_entry=Entry(my_w)
prenom_entry.grid(row=1,column=1,sticky=W,padx=15)
groupe_entry=Entry(my_w)
groupe_entry.grid(row=2,column=1,sticky=W,padx=15)
note_entry=Entry(my_w)
note_entry.grid(row=3,column=1,sticky=W,padx=15)
    #Buttons
registre_button=Button(my_w,text="Envoyer",command=envoyer,height=2,width=10)
registre_button.grid(row=5,column=1)
    #Treeview
def remplir_tree():
    file=open(os.path.join(os.getcwd(),'myfile.csv'))
    csvreader = reader(file)
    l1=[]
    l1=next(csvreader)
    r_set = [row for row in csvreader]
    global table
    table = ttk.Treeview(my_w,selectmode="browse")
    table.place(x = 50,y = 200, width = 1200, height = 450)
    table["height"]=5
    table["show"]="headings"
    table["columns"]=l1
    for i in l1:
        table.column(i, width = 100, anchor ='c')
        table.heading(i,text=i)
    for dt in r_set:
        table.insert("",'end',values=dt)
 

remplir_tree()

def edit():
    selected_row=table.focus()
    row_deatils=table.item(selected_row)
    row_spesific=row_deatils.get("values")
    id_info=row_spesific[0]
    
    edit_window=Tk()
    edit_window.geometry("500x500")
    edit_window.title("inscreprion formule")
    id_label=Label(edit_window,text="ID :         ",font=("Helvetica", 15))
    id_label.grid(row=0,column=0,sticky=W)
    id_label_inc=Label(edit_window,text=id_info,font=("Helvetica", 15))
    id_label_inc.grid(row=0,column=1,sticky=W)
    edit_note_label=Label(edit_window,text="Votre nouvelle note",font=("Helvetica", 15))
    edit_note_label.grid(row=2,column=0,sticky=W)
    
    edit_note_entry=Entry(edit_window)
    edit_note_entry.grid(row=2,column=1,sticky=W,padx=15)
    edit_button=Button(edit_window,text="Modifier",command=lambda:role(id_info,edit_note_entry),height=2,width=10)
    edit_button.grid(row=3,column=1,sticky=W,pady=5)



    mainloop()
def role(id_info,edit_note_entry):
    asyncio.run(submiter_point(id_info,edit_note_entry)) 

async def submiter_point(id_info,edit_note_entry):
    await edit_file(id_info, edit_note_entry)
    
    remplir_tree()

async def edit_file(id_info, edit_note_entry):
    scv_file=open(os.path.join(os.getcwd(),'myfile.csv'))
    fileObject_csv=reader(scv_file)
    lines = list(fileObject_csv)
    lines[id_info][4] = edit_note_entry.get()
    writer_new_file = writer(open('myfile.csv', 'w',newline=""))
    writer_new_file.writerows(lines)
    scv_file.close()


    

get=Button(my_w,text="Modifier",command=edit,height=2,width=10)
get.grid(row=5,column=2)

mainloop()