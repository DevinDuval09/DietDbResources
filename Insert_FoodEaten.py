import tkinter
from tkinter import ttk as ttk
import pyodbc
import pandastable
import pandas
import tkcalendar
import WidgetUtility as util

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

#create widgets for data view/entry
cmblist = []
qtylist = []
checklist = []
checkvariables = []
var = tkinter.IntVar()
var.set(0)

util.FoodWidgets(root, firstcolumn = 0,includecheckbox=True,checkvariable=var)
cmblist.append(root.grid_slaves(0,8))
qtylist.append(root.grid_slaves(1,8))
checklist.append(root.grid_slaves(4,8))
checkvariables.append(var)

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
	checklist.append(root.grid_slaves(4,root.grid_size()[1]))
	cmblist.append(root.grid_slaves(0,root.grid_size()[1]))
	qtylist.append(root.grid_slaves(1,root.grid_size()[1]))


def CalcCalories():
	#column order:foodlist, qtyEntry,lblCalories,bCalc,checkbox
	pass

def Submit():
	#submit all foods listed to database
	pass
	
bAddFoodWidgets = ttk.Button(root,text="Add Entry Row",command=AddWidgets)
bAddFoodWidgets.grid(row=0,column=5)
bCalculate = ttk.Button(root,text="Total Entries",command=CalcCalories)
bCalculate.grid(row=1,column=5)




#submit button to add everything to database

root.mainloop()