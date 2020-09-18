import tkinter
from tkinter import ttk as ttk
import pyodbc
import pandastable
import pandas

#tool to view, add, and edit meals

#main form
root = tkinter.Tk()
frame = tkinter.Frame(root)
frame.pack()
root.title("Meals")

#database connections
conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
cursor = conx.cursor()

#drop down lists for inserting data
foodNames = "SELECT CONCAT( Foodkey,' ',Brands.Brand,' ',Name) FROM Food INNER JOIN Brands ON Food.Brand=Brands.BrandKey UNION SELECT CONCAT(Foodkey,' ',' ',' ',Name) FROM Food WHERE Food.Brand IS NULL"
cursor.execute(foodNames)
foodStrings = cursor.fetchall()

#combobox
foodlist = ttk.Combobox(root, value = foodStrings)
foodlist.pack()

root.mainloop()
