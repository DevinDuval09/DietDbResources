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
from datetime import date

root = tkinter.Tk()
root.geometry('800x600')
frame=tkinter.Frame(root)
frame.grid(column=0)

conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
cursor = conx.cursor()

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
		#use Mifflin St.Jeor calculation
		#Base Metobalic Rate(men) = (10 x weight(kg)) + (6.25 x height(cm)) - (5 x age) + 5
		#BMR(women) = (10 x weight(kg)) + (6.25 x heigh(cm)) - (5 x age) - 161
		#Calories Needed = BMR x activity multiplier
		#Activity multiplier is estimate and will be different for different people
		#ACTM general numbers: 1.2 for sedentary, 1.375 for light exercise 3x week, 1.55 for moderate exercise 
		#3-5x weeik, 1.725 for hard exercise 6-7x week, 1.9 for hard exercise + physical job 7x week)
		inchCmConversion = 2.54
		lbsKGConversion = (1/2.205)

		user = UserID

		sql_data = "SELECT * FROM Users WHERE UserID = {}".format(UserID)
		userdata = cursor.execute(sql_data).fetchall()[0]
		sql_weight = "SELECT * FROM UsersWeight WHERE UserID = {} ORDER BY Date DESC".format(UserID)
		weightinfo = cursor.execute(sql_weight).fetchall()[0]

		#Entry for date / data view
		cal = tkcalendar.Calendar(frame,font="Arial 14", selectmode='day')
		cal.grid(column = 0, row = 0,columnspan = 4,rowspan=8)
		#Display user data on top of form
		lFirstName = ttk.Label(frame,text= 'First Name: \n{}'.format(userdata[1])).grid(column=4,row=0,rowspan = 2)
		lLastName = ttk.Label(frame,text = 'Last Name: \n{}'.format(userdata[2])).grid(column=5,row=0,rowspan=2)

		lMultiplier = ttk.Label(frame,text = 'Activity Multiplier').grid(column=6,row=0)
		eMultiplier = tkinter.Entry(frame)
		eMultiplier.grid(column = 6,row = 1)
		eMultiplier.insert(0,str(weightinfo[3]))

		lWeight = ttk.Label(frame,text = "Current Weight").grid(column = 7, row = 0)
		eWeight = tkinter.Entry(frame)
		eWeight.grid(column = 7,row = 1)
		eWeight.insert(0,str(weightinfo[2]))

		lHeight = ttk.Label(frame,text = "Height: \n {}'".format(str(int(userdata[5]/12)))+'{}"'.format(str(userdata[5]%12))).grid(column = 8, row = 0, rowspan=2)
		
		dt = cal.get_date().split('/')
		year = int('20'+dt[2])
		month = int(dt[0])
		day = int(dt[1])
		age=date(year,month,day).year-userdata[3].year

		lAge = ttk.Label(frame,text = 'Age: \n' + str(age)).grid(column=9,row=0,rowspan=2)
		def CalcBMR():
			if userdata[4] == 'm':
				return (10*float(weightinfo[2])*lbsKGConversion)+(6.25*float(userdata[5])*inchCmConversion)-(5*age)+5
			else:
				return (10*float(weightinfo[2])*lbsKGConversion)+(6.25*float(userdata[5])*inchCmConversion)-(5*age)-161

		cmbGoal = SQLBox(frame,"SELECT * FROM Goaltypes")
		cmbGoal.grid(column = 0)
		def CalcCalories(Goal,multiply):
			#weight changes assume safe gain/loss based on 1 lbs week, = 3500 calorie surplus/deficit per week
			base = CalcBMR() * multiply
			if int(Goal) == 1:
				return base + 500
			elif int(Goal) == 2:
				return base - 500
			elif int(Goal) ==3:
				return base
			else:
				print(Goal)

		lCalReq = tkinter.Label(frame,text= 'Average Daily Requirements: {}'.format(''))
		lCalReq.grid(column=0)
		def UpdateReq(Goal,multiply,lbl):
			daily = round(CalcCalories(Goal,multiply),0)
			lbl.config(text = 'Average Daily Requirements: {}'.format(str(daily)))

		def SetWeek():
			array = []
			daily = CalcBMR() * float(eMultiplier.get())
			array.append(daily)
			array.append(daily-400)
			array.append(daily+400)
			array.append(daily)
			array.append(daily + 200)
			array.append(daily - 200)
			array.append(daily)
			return array

		dailygoals = SetWeek()

		display = Util.DataDisplay(frame,('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'),dailygoals)
		display.grid(column=0)


		bCalc = ttk.Button(frame,text="Calculate Calorie Requirements",command=lambda:UpdateReq(cmbGoal.get().split(",")[0][1:],float(eMultiplier.get()),lCalReq))
		bCalc.grid(column=0)

		#Calculate the 7 day calorie cycle
		#display the cycle using the DataDisplay class from Utils

		#lAge = ttk.Label(frame,text = "Age: \n {}".format(date(cal.get()).year - date(userdata)[3].year))
		#display selected date
		#input user weight, height, calc age and goals (maintenance, weight gain, weight loss)



root.mainloop()
