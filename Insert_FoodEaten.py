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
root.geometry('400x600')
frame = tkinter.Frame(root)
frame.pack()
root.title("Food Eaten")

util.CreateFoodWidgets(root)



#Entry for date / data view
cal = tkcalendar.Calendar(root,font="Arial 14", selectmode='day')
cal.pack(fill="both", expand=False)

#create widgets for data view/entry
cbconsumedlist = []
lblconsumedlist = []
entrylist = []

lEaten = ttk.Label()
lPlanned = ttk.Label()
lCaloriesEaten = ttk.Label()
lCaloriesPlanned = ttk.Label()
lCaloriesTotal = ttk.Label()

#sql statements to view food consumed that day

#sql statements to view food scheduled for that day

root.mainloop()