import tkinter
from tkinter import ttk as ttk
import pyodbc
import pandastable
import pandas
import tkcalendar
import math

#Utility for creating widgets when necessary
#DB connection
conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
cursor = conx.cursor()

#create Widgets
def FoodWidgets(root,firstcolumn,includecheckbox=False,checkvariable=None):
	#create a new line of widgets to enter food data into a table
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

	#label for nutrional info
	lblCalories = tkinter.Label(root)
	lblCalories.grid(row=r,column = firstcolumn + 5)
	lblProtein=tkinter.Label(root)
	lblProtein.grid(row=r,column=firstcolumn+6)
	lblCarbs=tkinter.Label(root)
	lblCarbs.grid(row=r,column=firstcolumn+7)
	lblTotalFat=tkinter.Label(root)
	lblTotalFat.grid(row=r,column=firstcolumn+8)
	lblSatFat=tkinter.Label(root)
	lblSatFat.grid(row=r,column=firstcolumn+9)
	lblFiber=tkinter.Label(root)
	lblFiber.grid(row=r,column=firstcolumn+10)
	#lblCalories.pack()

	#button to calculate and display info for line:
	bCalories = ttk.Button(root, text = "Calculate Calories")

	def CalcCalories():
		calCount = float(0)
		# get food index out of combo box
		foodindex = foodlist.get().split()[0][2:]
		sqlCalories = "SELECT Calories,Protein,Carbs,TotalFat,SatFat,Fiber FROM FOOD WHERE Foodkey = " + str(foodindex) + ";"
		cursor.execute(sqlCalories)
		caloriesList = cursor.fetchall()
		caloriesPer = float(caloriesList[0][0])
		proteinPer = float(caloriesList[0][1])
		carbsPer = float(caloriesList[0][2])
		totalFatPer=float(caloriesList[0][3])
		satFatPer=float(caloriesList[0][4])
		fiberPer = float(caloriesList[0][5])
		# get qty
		qty = float(qtyEntry.get())
		calCount = calCount + (caloriesPer * qty)
		lblCalories.config(text = str(round(calCount,2)))
		lblProtein.config(text=str(round(proteinPer*qty,2)))
		lblCarbs.config(text=str(round(carbsPer*qty,2)))
		lblTotalFat.config(text=str(round(totalFatPer*qty,2)))
		lblSatFat.config(text=str(round(satFatPer*qty,2)))
		lblFiber.config(text=str(round(fiberPer*qty,2)))

	bCalories.config(command=CalcCalories)
	bCalories.grid(row=r,column = firstcolumn + 2)

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

def InsertStatement(table,columns,values,datatypes):
	#update db with given query
	numberOfColumns = len(columns)
	numberOfValues = len(values)
	sqlStatement = "INSERT INTO {}(".format(table)

	#iterate over column names and add columns to statement
	for i in range(0,numberOfColumns-1):
		sqlStatement = sqlStatement +"{},".format(columns[i])
	sqlStatement = sqlStatement + "{}) VALUES(".format(columns[numberOfColumns-1])

	#insert values into sql statement
	for i in range(0,numberOfValues-1):
		if datatypes[i] == 'string':
			sqlStatement = sqlStatement + "'{}',".format(values[i])
		elif datatypes[i] == 'date':
			print('Now you need to implement a way to handle dates')
		else:
			sqlStatement = sqlStatement + "{},".format(values[i])
	if datatypes[numberOfValues-1] == 'string':
		sqlStatement = sqlStatement + "'{}');".format(values[numberOfValues-1])
	elif datatypes[numberOfValues-1] == 'date':
		print('implement date handler')
	else:
		sqlStatement = sqlStatement + "{});".format(values[numberOfValues-1])

	cursor.execute(sqlStatement)
	conx.commit()

class SQL_ComboBox(ttk.Combobox):
	def __init__(self,parent,sql,*args,**kwargs):
		cursor.execute(sql)
		droplist = cursor.fetchall()
		ttk.Combobox.__init__(self,parent,values=droplist)

class NextKey_Label(ttk.Label):
	def __init__(self,parent,table,*args,**kwargs):
		sql_getpkcolumn = "EXEC sp_pkeys {}".format(table)
		keydata = cursor.execute(sql_getpkcolumn).fetchall()
		sql_getpklist = "SELECT {} FROM {} ORDER BY {} DESC".format(keydata[0][3],table,keydata[0][3])
		nextpk = cursor.execute(sql_getpklist).fetchone()[0]+1
		ttk.Label.__init__(self,parent,text = str(nextpk),state='disabled')

class RowOfWidgets(tkinter.Frame):
	def __init__(self,parent,row,*args,**kwargs):
		tkinter.Frame.__init__(self,parent)
		self.grid(row=row)
		self.widgets = []
		self.config(height=parent.winfo_height(),width=parent.winfo_width())
	def placeWidget(self,widget,columnnumber):
		self.widgets.append(widget)
		widget.grid(row=0,column=columnnumber)
	def centerWidgets(self,numberofcolumns):
		for w in self.widgets:
			w.config(width=(math.floor(self.winfo_width()/numberofcolumns)))


class LabelRow(tkinter.Frame):
	def __init__(self,parent,row,numberofcolumns,columnnames,*args,**kwargs):
		WidRow = RowOfWidgets(parent,row)
		for i in range(0,numberofcolumns):
			lbl = tkinter.Label(WidRow,text=columnnames[i])
			lbl.grid(row=row,column=i)
			WidRow.widgets.append(lbl)






	
