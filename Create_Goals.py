#goal setting program
import tkinter
from tkinter import ttk as ttk
from WidgetUtility import SQL_ComboBox as SQLBox
from WidgetUtility import NextKey_Label as KeyLabel
from WidgetUtility import LabelRow as LabelRow
from WidgetUtility import RowOfWidgets as WidgetRow
from WidgetUtility import *
import WidgetUtility as Util
import pyodbc
import tkcalendar
from datetime import date

root = tkinter.Tk()
root.geometry('800x600')
frame=tkinter.Frame(root)
frame.grid(column=0)

conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
cursor = conx.cursor()

ldirections = ttk.Label(frame,text='Select a user').grid(column=0)
cmbuser = SQLBox(frame,"SELECT UserID,FirstName,LastName FROM Users")
cmbuser.grid(column=0)

UserID = None

def Submit():
	UserID = cmbuser.get().split(',')[0][1:]
	user = User(UserID)
	for w in frame.winfo_children():
		w.destroy()
	goals = GoalsForm(user,frame)
			

bSubmit = ttk.Button(frame,text='Select',command=Submit).grid(column=0)


class GoalsForm():
	def __init__(self,user,frame):
		#use Mifflin St.Jeor calculation
		#Base Metobalic Rate(men) = (10 x weight(kg)) + (6.25 x height(cm)) - (5 x age) + 5
		#BMR(women) = (10 x weight(kg)) + (6.25 x heigh(cm)) - (5 x age) - 161
		#Calories Needed = BMR x activity multiplier
		#Activity multiplier is estimate and will be different for different people
		#ACTM general numbers: 1.2 for sedentary, 1.375 for light exercise 3x week, 1.55 for moderate exercise 
		#3-5x weeik, 1.725 for hard exercise 6-7x week, 1.9 for hard exercise + physical job 7x week)

		#on start, calculate and populate goals

		#Entry for date / data view
		cal = tkcalendar.Calendar(frame,font="Arial 14", selectmode='day')
		cal.grid(column = 0, row = 0,columnspan = 4,rowspan=8)
		#Display user data on top of form
		lFirstName = ttk.Label(frame,text= 'First Name: \n{}'.format(user.FirstName)).grid(column=4,row=0,rowspan = 2)
		lLastName = ttk.Label(frame,text = 'Last Name: \n{}'.format(user.LastName)).grid(column=5,row=0,rowspan=2)

		lMultiplier = ttk.Label(frame,text = 'Activity Multiplier').grid(column=6,row=0)
		eMultiplier = tkinter.Entry(frame)
		eMultiplier.grid(column = 6,row = 1)
		eMultiplier.insert(0,user.Activity)

		lWeight = ttk.Label(frame,text = "Current Weight").grid(column = 7, row = 0)
		eWeight = tkinter.Entry(frame)
		eWeight.grid(column = 7,row = 1)
		eWeight.insert(0,user.Weight)

		lHeight = ttk.Label(frame,text = "Height: \n {}'".format(str(int(user.Height/12)))+'{}"'.format(str(user.Height%12))).grid(column = 8, row = 0, rowspan=2)

		targets = Util.Targets(int(user.ID),10,6)
		targets.displayTargets(frame)

		#lAge = ttk.Label(frame,text = 'Age: \n' + str(user.Age(cal.get_date()))).grid(column=9,row=0,rowspan=2)
		user.Age(cal.get_date())

		datestuff = Util.DateInfo.initFromDate(cal.get_date())

		targets = Util.Targets(user.ID,datestuff.data[0][0])

		cmbGoal = SQLBox(frame,"SELECT * FROM Goaltypes")
		cmbGoal.grid(column = 0)


		lCalReq = tkinter.Label(frame,text= 'Average Daily Requirements: {}'.format(''))
		lCalReq.grid(column=0)

		def UpdateReq(Goal,multiply,lbl):
			daily = round(CalcCalories(Goal,multiply),0)
			lbl.config(text = 'Average Daily Requirements: {}'.format(str(daily)))

		bCalc = ttk.Button(frame,text="Calculate Calorie Requirements",command=lambda:UpdateReq(cmbGoal.get().split(",")[0][1:],float(eMultiplier.get()),lCalReq))
		bCalc.grid(column=0)

		#Calculate the 7 day calorie cycle
		#display the cycle using the DataDisplay class from Utils

		#lAge = ttk.Label(frame,text = "Age: \n {}".format(date(cal.get()).year - date(userdata)[3].year))
		#display selected date
		#input user weight, height, calc age and goals (maintenance, weight gain, weight loss)



root.mainloop()
