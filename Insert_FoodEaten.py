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
root.geometry('1000x600')
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
foodeatenkeys = []
eatenLabels = []#order:calories,protein,carbs,totalfat,satfat
plannedLabels=[]#calories,protein,carbs,totalfat,satfat
totalLabels=[]

#labels for nutrion columns
lCalCol = ttk.Label(root,text='Calories').grid(row=7,column=5)
lProtCol = ttk.Label(root,text='Protein').grid(row=7,column=6)
lCarbsCol=ttk.Label(root,text='Carbs').grid(row=7,column=7)
lTotFatCol=ttk.Label(root,text='Total Fat').grid(row=7,column=8)
lSatFatcol=ttk.Label(root,text='Saturated Fat').grid(row=7,column=9)
lFibercol = ttk.Label(root,text='Fiber').grid(row=7,column=10)
#labels for totals summary
lblTotals = tkinter.Label(root,text="Totals",).grid(row=0,column=6,columnspan=4,padx=20)
lblPlanned = tkinter.Label(root,text='Planned').grid(row=1,column=7)
lblEaten=tkinter.Label(root,text='Eaten').grid(row=1,column=8)
lblTotalTotal=tkinter.Label(root,text='Total').grid(row=1,column=9)
lblCalTot=tkinter.Label(root,text='Calories').grid(row=2,column=6)
lblProtTot=tkinter.Label(root,text='Protein').grid(row=3,column=6)
lblCarbsTot=tkinter.Label(root,text='Carbs').grid(row=4,column=6)
lblTotFatTot=tkinter.Label(root,text='TotalFat').grid(row=5,column=6)
lblSatFatTot=tkinter.Label(root,text='SatFat').grid(row=6,column=6)
#labels for data
lPlannedCal=tkinter.Label(root)
lPlannedCal.grid(row=2,column=7)
plannedLabels.append(lPlannedCal)
lEatenCal = tkinter.Label(root)
lEatenCal.grid(row=2,column=8)
eatenLabels.append(lEatenCal)
lTotalCal = tkinter.Label(root)
lTotalCal.grid(row=2,column=9)
lPlannedProt=tkinter.Label(root)
lPlannedProt.grid(row=3,column=7)
plannedLabels.append(lPlannedProt)
lEatenProt=tkinter.Label(root)
lEatenProt.grid(row=3,column=8)
eatenLabels.append(lEatenProt)
lTotalProt=tkinter.Label(root)
lTotalProt.grid(row=3,column=9)
lPlannedCarbs=tkinter.Label(root)
lPlannedCarbs.grid(row=4,column=7)
plannedLabels.append(lPlannedCarbs)
lEatenCarbs=tkinter.Label(root)
lEatenCarbs.grid(row=4,column=8)
eatenLabels.append(lEatenCarbs)
lTotalCarbs=tkinter.Label(root)
lTotalCarbs.grid(row=4,column=9)
lPlannedTF=tkinter.Label(root)
lPlannedTF.grid(row=5,column=7)
plannedLabels.append(lPlannedTF)
lEatenTF=tkinter.Label(root)
lEatenTF.grid(row=5,column=8)
eatenLabels.append(lEatenTF)
lTotalTF=tkinter.Label(root)
lTotalTF.grid(row=5,column=9)
lPlannedSF=tkinter.Label(root)
lPlannedSF.grid(row=6,column=7)
plannedLabels.append(lPlannedSF)
lEatenSF=tkinter.Label(root)
lEatenSF.grid(row=6,column=8)
eatenLabels.append(lEatenSF)
lTotalSF=tkinter.Label(root)
lTotalSF.grid(row=6,column=9)
totalLabels.append(lTotalCal)
totalLabels.append(lTotalProt)
totalLabels.append(lTotalCarbs)
totalLabels.append(lTotalTF)
totalLabels.append(lTotalSF)

#load any data entered for date
def Load_data(date):
	#clear any existing data in lists
	cmblist.clear()
	qtylist.clear()
	checklist.clear()
	checkvariables.clear()
	foodeatenkeys.clear()
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
	sql_DateFood = ("SELECT Dates.Date,Food.Foodkey,Brands.Brand,Food.Name,Food.Calories,FoodEaten.Quantity, FoodEaten.Consumed, FoodEaten.FoodEatenKey "
					"FROM FoodEaten INNER JOIN Food ON Food.FoodKey = FoodEaten.FoodKey INNER JOIN Dates ON Dates.Datekey = FoodEaten.DateKey INNER JOIN "
					"Brands ON Food.Brand = Brands.BrandKey WHERE FoodEaten.DateKey = {} "
					"UNION SELECT Dates.Date,Food.FoodKey, ' ', Food.Name,Food.Calories,FoodEaten.Quantity,FoodEaten.Consumed,FoodEaten.FoodEatenKey "
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
		foodeatenkeys.append(int(strdata[r][7]))
		text = ("('{} {} {}',)".format(str(strdata[r][1]),str(strdata[r][2]),str(strdata[r][3])))
		cmblist[r].set(text)
		qtylist[r].insert(0,str(strdata[r][5]))
		if strdata[r][6]==True:
			cmblist[r].config(state='disabled')
			qtylist[r].config(state='disabled')
			#checklist[r].config(state='disabled')
	CalcCalories()

def AddWidgets():
	#add a row of widgets
	x = tkinter.IntVar()
	x.set(0)
	util.FoodWidgets(root,firstcolumn=0,includecheckbox=True,checkvariable = x)
	checkvariables.append(x)
	checklist.append(root.grid_slaves(root.grid_size()[1]-1,4)[0])
	cmblist.append(root.grid_slaves(root.grid_size()[1]-1,0)[0])
	qtylist.append(root.grid_slaves(root.grid_size()[1]-1,1)[0])
	foodeatenkeys.append(None)

def CalcCalories():
	#column order:foodlist, qtyEntry,bCalc,checkbox,calories,prot,carbs,totfat,satfat,fiber
	planned_totals=[0,0,0,0,0]#calories,protein,carbs,totalfat,satfat
	eaten_totals=[0,0,0,0,0]#calories,protein,carbs,totalfat,satfat
	for i in range(0,len(cmblist)):
		foodkey = cmblist[i].get().split()[0][2:]
		sql_data="SELECT Calories,Protein,Carbs,TotalFat,SatFat FROM Food WHERE FoodKey = {}".format(foodkey)
		rowdata = cursor.execute(sql_data).fetchall()
		for x in range(0,len(eaten_totals)):
			y = float(rowdata[0][x])
			if int(checkvariables[i].get()) == 1:
				eaten_totals[x] = round(eaten_totals[x] + (y*float(qtylist[i].get())),2)
			else:
				planned_totals[x] = round(planned_totals[x] + (y*float(qtylist[i].get())),2)

	for i in range(0,len(eatenLabels)):
		eatenLabels[i].config(text=str(eaten_totals[i]))
		plannedLabels[i].config(text=str(planned_totals[i]))
		totalLabels[i].config(text=str(round(planned_totals[i]+eaten_totals[i],2)))



def Submit(date):
	#submit all foods listed to database
	#get next key
	sql_FoodEatenKey = "SELECT TOP 1 FoodEatenKey FROM FoodEaten ORDER BY FoodEatenKey DESC"
	nextkey = cursor.execute(sql_FoodEatenKey).fetchall()[0][0] + 1
	#get date key
	sql_DateKey = "SELECT DateKey FROM Dates WHERE Date = CONVERT(Date,'{}',1)".format(date)
	cursor.execute(sql_DateKey)
	datekey = cursor.fetchall()[0][0]
	#sort cmblist indexes by changes and new items
	insertIndexes = []
	updateIndexes = []
	for ind in range(0,len(cmblist)):
		if foodeatenkeys[ind] == None:
			insertIndexes.append(ind)
		else:
			updateIndexes.append(ind)

	#create insert statements
	for i in insertIndexes:
		insertStatement =("INSERT INTO FoodEaten(DateKey,FoodKey,Quantity,"
								"Consumed,Accuracey,Location,Note,FoodEatenKey) "
								"VALUES ({},{},{},{},{},{},{},"#will need to add "' '" around Accuracey when accuracey is implemented
								"{})").format(datekey,cmblist[i].get().split()[0][2:],qtylist[i].get(),checkvariables[i].get(),'Null','Null','Null',nextkey)
		cursor.execute(insertStatement)
		conx.commit()
		nextkey = nextkey + 1

	#create update statements
	for i in updateIndexes:
		updateStatement =("UPDATE FoodEaten SET "
							"DateKey = {},FoodKey = {},Quantity = {},Consumed = {},"
							"Accuracey = {},Location = {},Note = {} "
							"WHERE FoodEaten.FoodEatenKey = {}" #will need to add "' '" around Accuracey when accuracey is implemented
							).format(datekey,cmblist[i].get().split()[0][2:],qtylist[i].get(),checkvariables[i].get(),'Null','Null','Null',foodeatenkeys[i])
		cursor.execute(updateStatement)
		conx.commit()
	Load_data(date)

bAddFoodWidgets = ttk.Button(root,text="Add Entry Row",command=AddWidgets)
bAddFoodWidgets.grid(row=0,column=5)
bCalculate = ttk.Button(root,text="Total Entries",command=CalcCalories)
bCalculate.grid(row=1,column=5)
bGetFood = ttk.Button(root,text="Get Food",command=lambda:Load_data(cal.get_date()))
bGetFood.grid(row=2,column=5)
bSubmit = ttk.Button(root,text="Submit Changes",command=lambda:Submit(cal.get_date())).grid(row=3,column=5)



root.mainloop()