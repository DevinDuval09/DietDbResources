import tkinter
from tkinter import ttk as ttk
import pyodbc
import pandastable
import pandas
import tkcalendar

#Utility for creating widgets when necessary
#DB connection
conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
cursor = conx.cursor()

#create Widgets
def FoodWidgets(root,firstcolumn,includecheckbox=False,checkvariable=None):
	#create a new line of widgets to enter food into a table
	#if include checkbox = true, main code must pass in tkinter variable for checkvariable to use on checkbutton
	#pass in root tkinter form
	#sql query to get food list
	foodNames = "SELECT CONCAT( Foodkey,' ',Brands.Brand,' ',Name) FROM Food INNER JOIN Brands ON Food.Brand=Brands.BrandKey UNION SELECT CONCAT(Foodkey,' ',' ',' ',Name) FROM Food WHERE Food.Brand IS NULL"
	cursor.execute(foodNames)
	foodStrings = cursor.fetchall()

	#combobox list of food
	foodlist = ttk.Combobox(root, value = foodStrings)
	foodlist.grid(column=firstcolumn)
	r = foodlist.grid_info()['row']
	#foodlist.pack()

	#entry box for quantity
	qtyEntry = ttk.Entry()
	qtyEntry.grid(row=r,column = firstcolumn + 1)
	#qtyEntry.pack()

	#label for calorie data
	lblCalories = tkinter.Label(root)
	lblCalories.grid(row=r,column = firstcolumn + 2)
	#lblCalories.pack()

	#button to calculate and display info for line:
	bCalories = ttk.Button(root, text = "Calculate Calories")

	def CalcCalories():
		calCount = float(0)
		# get food index out of combo box
		foodindex = foodlist.get().split()[0][2:]
		sqlCalories = "SELECT Calories FROM FOOD WHERE Foodkey = " + str(foodindex) + ";"
		cursor.execute(sqlCalories)
		caloriesList = cursor.fetchall()
		caloriesPer = float(caloriesList[0][0])
		# get qty
		qty = float(qtyEntry.get())
		calCount = calCount + (caloriesPer * qty)
		lblCalories.config(text = str(calCount))

	bCalories.config(command=CalcCalories)
	bCalories.grid(row=r,column = firstcolumn + 3)

	if includecheckbox == True:
		check = ttk.Checkbutton(root,text = 'Consumed',onvalue=1,offvalue=0,variable=checkvariable).grid(row=r,column=firstcolumn + 4)

def CreateTable(frame,sql):
	#create a table to display a given query
	query = pandas.read_sql(sql,conx)
	display = pandastable.Table(frame,dataframe=query,showbartool=True,showstatusbar=True)
	display.show()

def UpdateTable(table,new_sql):
	#Update an existing table with new sql query
	new_query = pandas.read_sql(new_sql,conx)
	table.model.df = new_query
	table.redraw()