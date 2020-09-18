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
#



#lists for food that is added to meal
comboboxlist = []
entrylist = []

def CreateWidgets():
	#create a new line of widgets to enter food into meal
	#sql query to get food list
	foodNames = "SELECT CONCAT( Foodkey,' ',Brands.Brand,' ',Name) FROM Food INNER JOIN Brands ON Food.Brand=Brands.BrandKey UNION SELECT CONCAT(Foodkey,' ',' ',' ',Name) FROM Food WHERE Food.Brand IS NULL"
	cursor.execute(foodNames)
	foodStrings = cursor.fetchall()

	#combobox list of food
	foodlist = ttk.Combobox(root, value = foodStrings)
	foodlist.pack()
	comboboxlist.append(foodlist)

	#entry box for quantity
	qtyEntry = ttk.Entry()
	qtyEntry.pack()
	entrylist.append(qtyEntry)

bAddWidgets = ttk.Button(root,text='Add Food to Meal',command=CreateWidgets)
bAddWidgets.pack()

lTotalCalories = ttk.Label(root)

def CalcCalories():
	calCount = float(0)
	for ind in range(0,len(comboboxlist)):
		# get food index out of combo box
		foodindex = comboboxlist[ind].get().split()[0][2:]
		sqlCalories = "SELECT Calories FROM FOOD WHERE Foodkey = " + str(foodindex) + ";"
		cursor.execute(sqlCalories)
		caloriesList = cursor.fetchall()
		caloriesPer = float(caloriesList[0][0])
		# get qty
		qty = float(entrylist[ind].get())
		calCount = calCount + (caloriesPer * qty)

	lTotalCalories.config(text='Total Calories: ' + str(calCount))
	lTotalCalories.pack()
	lTotalCalories.update()

bCalculate = ttk.Button(root,text='Calculate Calories',command=CalcCalories)
bCalculate.pack()


#need to devise a way to track widgets to create insert statement

root.mainloop()
