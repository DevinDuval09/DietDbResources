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
#Create labels
lTotalCalories = ttk.Label(root)
lTotalCalories.pack()
entryMealName = ttk.Entry()
entryMealName.pack()

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

#insert current meal into database
def InsertMeal():
	#get next pk
	cursor.execute('SELECT TOP 1 MealsKey FROM Meals ORDER BY MealsKey Desc;')
	lpk = int(cursor.fetchone()[0])
	pk = str(lpk + 1)

	#get inputs
	name = entryMealName.get()

	#write sql statments
	insertStatements = []
	insertStatements.append("INSERT INTO Meals(MealsKey,Name) VALUES(" + pk + ",'" + name + "');")
	for ind in range(0,len(comboboxlist)):
		insertStatements.append("INSERT INTO MealsFood(MealsKey,FoodKey,Quantity) VALUES(" + pk + "," + str(comboboxlist[ind].get().split()[0][2:]) + "," + str(entrylist[ind].get())+");")
		
	#insert statements into tables
	for statement in insertStatements:
		#print(statement) #(uncomment to debug SQL statements)
		cursor.execute(statement)
		conx.commit()

#display meal calorie total on label
def CalcCalories():
	calCount = float(0)
	for ind in range(0,len(comboboxlist)):
		# get food index out of combo box
		foodindex = comboboxlist[ind].get().split()[0][2:] #throwing error
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

#create buttons
bAddWidgets = ttk.Button(root,text='Add Food to Meal',command=CreateWidgets)
bAddWidgets.pack()

bCalculate = ttk.Button(root,text='Calculate Calories',command=CalcCalories)
bCalculate.pack()

bSubmit = ttk.Button(root,text='Submit Meal',command =InsertMeal)
bSubmit.pack()


#need to devise a way to track widgets to create insert statement

root.mainloop()
