import tkinter
from tkinter import ttk as ttk
import pyodbc
import pandastable
import pandas

#The purpose of the dashboard is to display a given table when the appropriate

#tkinter main form

root = tkinter.Tk()
frame = tkinter.Frame(root)
frame.pack()
root.title("DietDb")

#DB connection stuff

conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
cursor = conx.cursor()


#function to set Sql Queries to display table
query = pandas.read_sql('SELECT * FROM Food;',conx)
display = pandastable.Table(frame,dataframe=query,showbartool=True,showstatusbar=True)
display.show()

def DisplayTable(data):
	#update table with new query
	new_query = pandas.read_sql('SELECT * FROM ' + data +';',conx)
	display.model.df = new_query
	display.redraw()

#buttons for table display
#some tables have disabled simply because of a lack of value in viewing them. Simply uncomment to reinstate.
# bAccuracey = ttk.Button(root,text = 'Accuracey Table',command=lambda: DisplayTable("Accuracey"))
# bAccuracey.pack()
bBrands = ttk.Button(root,text = 'Brands', command=lambda: DisplayTable("Brands"))
bBrands.pack()
# bDates = ttk.Button(root,text = 'Dates', command=lambda: DisplayTable("Dates"))
# bDates.pack()
bFood = ttk.Button(root,text = 'Food', command=lambda: DisplayTable("Food"))
bFood.pack()
bFoodEaten = ttk.Button(root,text = 'Food Eaten', command=lambda: DisplayTable("FoodEaten"))
bFoodEaten.pack()
bFoodTypes = ttk.Button(root,text = 'Food Types', command=lambda: DisplayTable("FoodTypes"))
bFoodTypes.pack()
bGoals = ttk.Button(root,text = 'Goals', command = lambda: DisplayTable('Goals'))
bGoals.pack()
bMealsFood = ttk.Button(root, text = 'Meals Food', command = lambda:DisplayTable('MealsFood'))
bMealsFood.pack()
bMeals = ttk.Button(root,text = "Meals Food with meal and food names", command=lambda:DisplayQuery("SELECT Meals.Name,Food.Name,MealsFood.Quantity FROM MealsFood INNER JOIN Food ON MealsFood.FoodKey = Food.FoodKey INNER JOIN Meals ON Meals.Mealskey = MealsFood.MealsKey;"))
bMeals.pack()



root.mainloop()

