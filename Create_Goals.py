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

root = tkinter.Tk()
root.geometry('800x600')
frame=tkinter.Frame(root)
frame.grid(column=0)

ldirections = ttk.Label(frame,text='Select a user').grid(column=0)
user = SQLBox(frame,"SELECT UserID,FirstName,LastName FROM Users")
user.grid(column=0)

UserID = None

def Submit():
	UserID = user.get().split(',')[0][1:]
	for w in frame.winfo_children():
		w.destroy()
	goals = GoalsForm(UserID,frame)
			

bSubmit = ttk.Button(frame,text='Select',command=Submit).grid(column=0)


class GoalsForm():
	def __init__(self,UserID,frame):
		user = UserID

		#Entry for date / data view
		cal = tkcalendar.Calendar(frame,font="Arial 14", selectmode='day')
		cal.grid(column = 0, row = 0,columnspan = 4,rowspan=8)


root.mainloop()
