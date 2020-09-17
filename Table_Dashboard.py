import tkinter
from tkinter import ttk as ttk
import pyodbc

#DB connection stuff

conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
cursor = conx.cursor()

#tkinter main form

root = tkinter.Tk()
root.title("DietDb")
display = tkinter.scrolledtext(root)

root.mainloop()

