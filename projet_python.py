import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ================= DATABASE =================
conn = sqlite3.connect("employes.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS employes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    adresse TEXT,
    matricule TEXT,
    echelle INTEGER,
    anciennete INTEGER,
    salaire INTEGER
)
""")
conn.commit()

# ================= WINDOW =================
fenetre = tk.Tk()
fenetre.title("Gestion des Employés")
fenetre.geometry("1400x600")
fenetre.resizable(False, False)

# ================= LEFT FRAME =================
frame_info = tk.LabelFrame(fenetre, text="Informations Employé", padx=10, pady=10)
frame_info.place(x=20, y=20, width=450, height=380)

labels = ["Nom", "Adresse", "Matricule", "Échelle ", "Ancienneté", "Salaire"]
entries = []

for i, l in enumerate(labels):
    tk.Label(frame_info, text=l).grid(row=i, column=0, pady=6, sticky="w")
    e = tk.Entry(frame_info, width=30)
    e.grid(row=i, column=1)
    entries.append(e)

nom, adresse, matricule, echelle, anciennete, salaire = entries

# ================= FUNCTIONS =================
def clear_fields():
    for e in entries:
        e.delete(0, tk.END)

def charger():
    table.delete(*table.get_children())
    cur.execute("SELECT * FROM employes")
    for row in cur.fetchall():
        table.insert("", tk.END, values=(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            f"{row[5]} ans",
            f"{row[6]} DH"
        ))

def validation():
    if not anciennete.get().isdigit():
        messagebox.showerror("Erreur", "Ancienneté il doit etre des chiffres")
        return False

    if not salaire.get().isdigit():
        messagebox.showerror("Erreur", "Salaire  il doit etre des chiffres")
        return False

    if not echelle.get().isdigit():
        messagebox.showerror("Erreur", "Échelle   il doit entre 6 et 11")
        return False

    ech = int(echelle.get())
    if ech < 6 or ech > 11:
        messagebox.showerror("Erreur", "Échelle  6 et 11 invalide")
        return False

    return True

def ajouter():
    if nom.get() == "" or matricule.get() == "":
        messagebox.showwarning("Attention", "Nom و Matricule ")
        return

    if not validation():
        return

    cur.execute(
        "INSERT INTO employes (nom, adresse, matricule, echelle, anciennete, salaire) VALUES (?,?,?,?,?,?)",
        (
            nom.get(),
            adresse.get(),
            matricule.get(),
            int(echelle.get()),
            int(anciennete.get()),
            int(salaire.get())
        )
    )
    conn.commit()
    charger()
    clear_fields()

def supprimer():
    selected = table.selection()
    if not selected:
        return
    emp_id = table.item(selected)["values"][0]
    cur.execute("DELETE FROM employes WHERE id=?", (emp_id,))
    conn.commit()
    charger()
    clear_fields()

def modifier():
    selected = table.selection()
    if not selected:
        return

    if not validation():
        return

    emp_id = table.item(selected)["values"][0]
    cur.execute("""
        UPDATE employes
        SET nom=?, adresse=?, matricule=?, echelle=?, anciennete=?, salaire=?
        WHERE id=?
    """, (
        nom.get(),
        adresse.get(),
        matricule.get(),
        int(echelle.get()),
        int(anciennete.get()),
        int(salaire.get()),
        emp_id
    ))
    conn.commit()
    charger()
    clear_fields()

def remplir(event):
    selected = table.selection()
    if not selected:
        return
    values = table.item(selected)["values"]
    clear_fields()
    nom.insert(0, values[1])
    adresse.insert(0, values[2])
    matricule.insert(0, values[3])
    echelle.insert(0, values[4])
    anciennete.insert(0, values[5].replace(" ans", ""))
    salaire.insert(0, values[6].replace(" DH", ""))

# ================= BUTTONS =================
tk.Button(frame_info, text="Ajouter", bg="green", fg="white", width=15, command=ajouter)\
    .grid(row=6, column=0, pady=15)

tk.Button(frame_info, text="Modifier", bg="blue", fg="white", width=15, command=modifier)\
    .grid(row=6, column=1, pady=15)

tk.Button(frame_info, text="Supprimer", bg="red", fg="white", width=15, command=supprimer)\
    .grid(row=6, column=2, pady=15)

# ================= TABLE =================
frame_table = tk.Frame(fenetre, bg="#e8a3d1")
frame_table.place(x=520, y=20, width=850, height=420)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#5dc0e7",
                foreground="black",
                rowheight=25,
                fieldbackground="#a18b9a")
style.map("Treeview", background=[("selected", "#5a9abe71")])

columns = ("ID", "Nom", "Adresse", "Matricule", "Échelle", "Ancienneté", "Salaire")
table = ttk.Treeview(frame_table, columns=columns, show="headings")

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120)

table.pack(fill="both", expand=True)
table.bind("<<TreeviewSelect>>", remplir)

charger()
fenetre.mainloop()
