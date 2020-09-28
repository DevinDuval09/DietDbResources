#goal setting program
import tkinter
from tkinter import ttk as ttk
from WidgetUtility import SQL_ComboBox as SQLBox
from WidgetUtility import NextKey_Label as KeyLabel
from WidgetUtility import LabelRow as LabelRow
from WidgetUtility import RowOfWidgets as WidgetRow
import WidgetUtility as Util
import pyodbc
import tkcalendar

class SelectUser():
	def __init__(self):
		#select user
		root = tkinter.Tk()
		root.title("Select User")
		root.geometry('400x400')
		ldirections = ttk.Label(root,text='Select a user').grid(column=0)
		user = SQLBox(root,"SELECT UserID,FirstName,LastName FROM Users")
		user.grid(column=0)

		def Submit():
			userid = user.get().split(',')[0][1:]
			

		bSubmit = ttk.Button(root,text='Select',command=Submit).grid(column=0)

		root.mainloop()

class GoalsForm():
	def __init__(self,UserID):
		root = tkinter.Tk()
		root.geometry('1000x600')
		root.title("Goals")

		#Entry for date / data view
		cal = tkcalendar.Calendar(root,font="Arial 14", selectmode='day')
		cal.grid(column = 0, row = 0,columnspan = 4,rowspan=8)

getuser = SelectUser()
getuser.__init__
