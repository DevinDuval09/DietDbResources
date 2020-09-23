import tkinter
from tkinter import ttk as ttk
import pyodbc
import pandastable
import pandas
import tkcalendar
import WidgetUtility as util
import datetime as dt

#tool to view, add, and edit food eaten

#main form
root = tkinter.Tk()
root.geometry('800x600')
frame = tkinter.Frame(root)
frame.grid(column = 0,row=0)
root.title("Food Eaten")

#Entry for date / data view
cal = tkcalendar.Calendar(root,font="Arial 14", selectmode='day')
cal.grid(column = 0, row = 0,columnspan = 4,rowspan=8)

#DB connection
conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
cursor = conx.cursor()

#widget lists
cmblist = []
qtylist = []
checklist = []
checkvariables = []

#load any data entered for date
def Load_data(date):
	#clear any existing data in lists
	cmblist.clear()
	qtylist.clear()
	checklist.clear()
	checkvariables.clear()#check variable not reiniating correctly
	#remove anything currently on grid
	for widget in root.grid_slaves():
		if int(widget.grid_info()["row"]) > 7:
			widget.grid_forget()
	#sql statement to pull data
	#get date key for date
	sql_DateKey = "SELECT DateKey FROM Dates WHERE Date = CONVERT(Date,'{}',1)".format(date)
	cursor.execute(sql_DateKey)
	dateKey = cursor.fetchall()[0][0]
	
	#get all food loaded to day
	sql_DateFood = ("SELECT Dates.Date,Food.Foodkey,Brands.Brand,Food.Name,Food.Calories,FoodEaten.Quantity, FoodEaten.Consumed "
					"FROM FoodEaten INNER JOIN Food ON Food.FoodKey = FoodEaten.FoodKey INNER JOIN Dates ON Dates.Datekey = FoodEaten.DateKey INNER JOIN "
					"Brands ON Food.Brand = Brands.BrandKey WHERE FoodEaten.DateKey = {} "
					"UNION SELECT Dates.Date,Food.FoodKey, ' ', Food.Name,Food.Calories,FoodEaten.Quantity,FoodEaten.Consumed "
					"FROM FoodEaten INNER JOIN Food ON Food.Foodkey = FoodEaten.Foodkey INNER JOIN Dates ON Dates.Datekey = FoodEaten.Datekey WHERE Food.Brand Is Null "
					"AND FoodEaten.DateKey = {}".format(dateKey,dateKey))
	data = cursor.execute(sql_DateFood).fetchall()
	strdata = [r for r in data]
	for r in range(0,len(strdata)):
		x=tkinter.IntVar()
		if strdata[r][6] == True:
			x.set(1)
		else:
			x.set(0)
		util.FoodWidgets(root, firstcolumn = 0,includecheckbox=True,checkvariable=x)
		cmblist.append(root.grid_slaves(r+8,0)[0])
		qtylist.append(root.grid_slaves(r+8,1)[0])
		checklist.append(root.grid_slaves(r+8,4)[0])
		checkvariables.append(x)
		text = ("('{} {} {}',)".format(str(strdata[r][1]),str(strdata[r][2]),str(strdata[r][3])))
		cmblist[r].set(text)
		qtylist[r].insert(0,str(strdata[r][5]))
		if strdata[r][6]==True:
			cmblist[r].config(state='disabled')
			qtylist[r].config(state='disabled')
			#checklist[r].config(state='disabled')

	#load data into widgets
#create widgets for data view/entry

# var = tkinter.IntVar()
# var.set(0)

# util.FoodWidgets(root, firstcolumn = 0,includecheckbox=True,checkvariable=var)
# cmblist.append(root.grid_slaves(8,0)[0])
# qtylist.append(root.grid_slaves(8,1)[0])
# checklist.append(root.grid_slaves(8,4)[0])
# checkvariables.append(var)

lEaten = ttk.Label()
lPlanned = ttk.Label()
lCaloriesEaten = ttk.Label()
lCaloriesPlanned = ttk.Label()
lCaloriesTotal = ttk.Label()

def AddWidgets():
	x = tkinter.IntVar()
	x.set(0)
	util.FoodWidgets(root,firstcolumn=0,includecheckbox=True,checkvariable = x)
	checkvariables.append(x)
	checklist.append(root.grid_slaves(root.grid_size()[1],4)[0])
	cmblist.append(root.grid_slaves(root.grid_size()[1],0)[0])
	qtylist.append(root.grid_slaves(root.grid_size()[1],1)[0])

def CalcCalories():
	#column order:foodlist, qtyEntry,lblCalories,bCalc,checkbox
	#Load_data(dt.date.today())
	print(cal.get_date())

def Submit():
	#submit all foods listed to database
	pass

bAddFoodWidgets = ttk.Button(root,text="Add Entry Row",command=AddWidgets)
bAddFoodWidgets.grid(row=0,column=5)
bCalculate = ttk.Button(root,text="Total Entries",command=CalcCalories)
bCalculate.grid(row=1,column=5)
bGetFood = ttk.Button(root,text="Get Food",command=lambda:Load_data(cal.get_date()))
bGetFood.grid(row=2,column=5)




#submit button to add everything to database

root.mainloop()