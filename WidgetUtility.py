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
	def __init__(self,parent,sql,defaultindex=None):
		cursor.execute(sql)
		droplist = cursor.fetchall()
		ttk.Combobox.__init__(self,parent,values=droplist)
		if defaultindex is not None:
			self.current(defaultindex)

class NextKey_Label(ttk.Label):
	def __init__(self,parent,table,*args,**kwargs):
		sql_getpkcolumn = "EXEC sp_pkeys {}".format(table)
		keydata = cursor.execute(sql_getpkcolumn).fetchall()
		sql_getpklist = "SELECT {} FROM {} ORDER BY {} DESC".format(keydata[0][3],table,keydata[0][3])
		self.nextpk = cursor.execute(sql_getpklist).fetchone()[0]+1
		ttk.Label.__init__(self,parent,text = str(self.nextpk),state='disabled')
	def get(self):
		return self.nextpk

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

class DataDisplay(tkinter.Frame):
	#puts some data into a series of rows or columns using tkinter labels and a tkinter frame. First submission should be labels
	def __init__(self,parent,*datalists,orientation='vertical'):
		tkinter.Frame.__init__(self,parent)
		iterable = None
		if orientation=='vertical':
			iterable = 'row'
		else:
			iterable='column'

		for t in range(0,len(datalists)):
			data=datalists[t]
			for i in range(0,len(data)):
				datapoint = data[i]
				if (type(data[i]) is int) or (type(data[i]) is float) or (type(data[i]) is complex):
					datapoint = round(datapoint,2)

				if iterable == 'row':
					lbl=tkinter.Label(self,text=str(datapoint))
					lbl.grid(row=i,column=t)
				else:
					lbl=tkinter.Label(self,text=str(datapoint))
					lbl.grid(row=t,column=i)
	def UpdateData(self,*datalists,orientation='vertical'):
		for w in self.winfo_children():
			w.destroy()

		iterable = None
		if orientation=='vertical':
			iterable = 'row'
		else:
			iterable='column'

		for t in range(0,len(datalists)):
			data=datalists[t]
			for i in range(0,len(data)):
				datapoint = data[i]
				if (type(data[i]) is int) or (type(data[i]) is float) or (type(data[i]) is complex):
					datapoint = round(datapoint,2)

				if iterable == 'row':
					lbl=tkinter.Label(self,text=str(datapoint))
					lbl.grid(row=i,column=t)
				else:
					lbl=tkinter.Label(self,text=str(datapoint))
					lbl.grid(row=t,column=i)

class Targets():
	#get,set, and display goal cycles
	def __init__(self,userid,startdateid,days=6):
		self.startdate = startdateid
		self.days = days
		self.cycleStrings = ('avg','lowest','highest','avg','low','high','avg')
		self.cycleKeys = (1,2,3,1,4,5,1)
		sql_currentweek = "SELECT DateKey,TargetType,TotalCalories,TotalGramsProtein FROM Goals WHERE DateKey BETWEEN {} AND {} AND UserID = {}".format(str(startdateid),str(int(startdateid)+self.days),str(userid))
		self.weeksdata = cursor.execute(sql_currentweek).fetchall()
		sql_userdata = "SELECT * FROM Users WHERE UserID = {}".format(userid)
		self.userdata = cursor.execute(sql_userdata).fetchall()[0]
		self.scheduledCalories = []
		self.scheduledCycle = []
		self.scheduledProtein = []
		for i in self.weeksdata:
			self.scheduledCalories.append(i[2])
			self.scheduledCycle.append(i[1])
			self.scheduledProtein.append(i[3])
	def changeCalorieTargets(self,newaverage,resetcycle = False,updatelabels = False,root=None):
		updatevalues = []#new values to be inserted into Goals table
		date = self.startdate#dateid
		updatecycle = []
		if not resetcycle:
			for day in self.scheduledCycle:
				if day == 1:
					updatevalues.append(newaverage)
				elif day ==2:
					updatevalues.append(newaverage-400)
				elif day ==3:
					updatevalues.append(newaverage+400)
				elif day ==4:
					updatevalues.append(newaverage-200)
				elif day ==5:
					updatevalues.append(newaverage+200)
			updatecycle = self.scheduledCycle
		else:
			updatevalues=[newaverage,newaverage-400,newaverage+400,newaverage,newaverage-200,newaverage+200,newaverage]
			updatecycle = [1,2,3,1,4,5,1]

		self.scheduledCalories = updatevalues

		if updatelabels:
			self.displayTargets(root)
		if resetcycle:
			self.scheduledCycle = updatecycle
	def submitChanges(self):
		date = self.startdate
		for i in self.scheduledCalories:
			sql = "UPDATE Goals SET TotalCalories={} WHERE DateKey = {} AND UserID = {}".format(str(i),str(date),str(self.userdata[0]))
			#print(sql)
			cursor.execute(sql)
			conx.commit()
			date = date + 1
	def displayTargets(self,root):
		targetsql = ("SELECT Dates.WeekDayName,Dates.DOWInMonth,Dates.MonthName,Dates.Year FROM Dates WHERE DateKey BETWEEN {} AND {}".format(self.startdate,str(self.startdate+self.days)))
		dateData = cursor.execute(targetsql).fetchall()
		days = []
		calories = []
		cnter = 0

		for i in dateData:
			days.append(str(i[0]) + ' ' + str(i[1]) + ' ' + str(i[2]) + ' ' + str(i[3]))
			calories.append(str(self.scheduledCalories[cnter]))
			cnter = cnter + 1

		display = DataDisplay(root,days,calories)
		display.grid(column=0)

class DateInfo():
	#cal.get_date formats to mm/dd/yy
	def __init__(self,sqllist):
		self.data = []
		for s in sqllist:
			self.data.append(cursor.execute(s).fetchall()[0])

	@classmethod
	def initFromDateID(cls,*ID) -> 'DateInfo':
		sqlStatements = []
		for i in ID:
			sqlStatements.append("SELECT * FROM Dates WHERE DateKey = {}".format(str(i)))
		return cls(sqlStatements)

	@classmethod
	def initFromString(cls,*datestring) -> 'DateInfo':
		from datetime import date
		sqlStatements = []
		for d in datestring:
			dt = d.split('/')
			year = int('20'+str(dt[2]))
			month = int(dt[0])
			day = int(dt[1])
			sqlStatements.append("SELECT * FROM Dates WHERE Date = CONVERT(Date,'{}',111)".format(date(year,month,day)))
		return cls(sqlStatements)
	@classmethod
	def initFromDate(cls,*dates)->'DateInfo':
		import datetime
		sqlStatements = []
		for d in dates:
			sqlStatements.append("SELECT * FROM Dates WHERE Date = CONVERT(Date,'{}',111)".format(d.strftime('%Y/%m/%d')))
		return cls(sqlStatements)

class User():
	import datetime
	def __init__(self,ID):
		data = cursor.execute("SELECT * FROM Users WHERE UserID = {}".format(ID)).fetchall()[0]
		self._ID = ID
		self._FirstName = data[1]
		self._LastName = data[2]
		self._Birthday = data[3]
		self._Gender = data[4]
		self._Height = data[5]
		newdata = cursor.execute("SELECT * FROM UsersWeight WHERE UserID = {} ORDER BY Date Desc".format(self.ID)).fetchall()[0]
		self._MostRecentDate = cursor.execute("SELECT * FROM Dates WHERE DateKey = {}".format(newdata[1])).fetchall()[0]
		self._Weight = newdata[2]
		self._Activity = newdata[3]
		self._Goal = newdata[4]

	def Age(self,date=datetime.date.today()):
		#function to calcuate age
		from datetime import date as dt
		from datetime import datetime
		
		if date.month >= self._Birthday.month and date.day >= self._Birthday.day:
			return (int(date.year - self._Birthday.year)+1)
		else:
			return (int(date.year - self._Birthday.year))

	def CalcBMR(self,date=datetime.date.today()):
		inchCmConversion = 2.54
		lbsKGConversion = (1/2.205)
		if self._Gender == 'm':
			return (10*float(self._Weight)*lbsKGConversion)+(6.25*float(self._Height)*inchCmConversion)-(5*self.Age(date))+5
		else:
			return (10*float(self._Weight)*lbsKGConversion)+(6.25*float(self._Height)*inchCmConversion)-(5*self.Age(date))-161

	def CalcCalories(self):
			#weight changes assume safe gain/loss based on 1 lbs week, = 3500 calorie surplus/deficit per week
		base = float(self.CalcBMR()) * float(self._Activity)
		if int(self._Goal) == 1:
			return base + 500
		elif int(self._Goal) == 2:
			return base - 500
		elif int(self._Goal) ==3:
			return base
		else:
			print(self._Goal)

	def calcTargets(self,startdate=datetime.date.today(),days=6,reset=False):
		#add: check for targets. If don't exist, make, if exist, get
		dateinfo = DateInfo.initFromDate(startdate)
		sqlCheckDates = "SELECT * FROM Goals WHERE UserID = {}".format(self._ID)
		goals = [r for r in cursor.execute(sqlCheckDates).fetchall()]
		keys = [r[0] for r in goals]

		self._updatekeys = []
		self._insertkeys = []
		self._datekeys = []

		for k in keys:
			for x in range(dateinfo.data[0][0],int(dateinfo.data[0][0])+days):
				if x not in self._datekeys:
					self._datekeys.append(x)
				if x == k:
					self._updatekeys.append(k)
				elif (x > max(keys)) and (x not in self._insertkeys):
					self._insertkeys.append(x)

		avg = round(self.CalcCalories(),2)

		sqlCycle = "SELECT TargetType FROM Goals WHERE DateKey Between {} AND {} AND UserID = {} ORDER BY DateKey ASC".format(dateinfo.data[0][0]-1,dateinfo.data[0][0],self._ID)
		cycle = [r[0] for r in cursor.execute(sqlCycle).fetchall()]
		
		cycleKeys = [1,2,3,1,4,5,1]
		self._goalcycle = []
		self._scheduledCalories = []

		#print(goals)
		#print(cycle)

		#set the upcoming cycle is not reset #not working
		if reset == False:
			if cycle == [5,1]:
				self._goalcycle = cycleKeys[6:]
			elif cycle == [1,1]:
				self._goalcycle = cycleKeys[0:]
			elif cycle == [1,2]:
				self._goalcycle = cycleKeys[1:]
			elif cycle == [2,3]:
				self._goalcycle = cycleKeys[2:]
			elif cycle == [3,1]:
				self._goalcycle = cycleKeys[3:]
			elif cycle == [1,4]:
				self._goalcycle =cycleKeys[4:]
			elif cycle == [4,5]:
				self._goalcycle = cycleKeys[5:]
			else:
				print('error in goal cycle if statement')
				print(cycle)
				print(self._goalcycle)

		while len(self._goalcycle)<days:
			self._goalcycle = self._goalcycle+cycleKeys

		#print(self._goalcycle)

		for day in self._goalcycle:
			if day == 1:
				self._scheduledCalories.append(avg)
			elif day ==2:
				self._scheduledCalories.append(avg-400)
			elif day ==3:
				self._scheduledCalories.append(avg+400)
			elif day ==4:
				self._scheduledCalories.append(avg-200)
			elif day ==5:
				self._scheduledCalories.append(avg+200)

		#print(self._goalcycle)
		#print(self._scheduledCalories)
		#print(self._updatekeys)
		#print(self._insertkeys)
		#print(self._datekeys)

	def submitTargets(self):
		#update display in DB
		import datetime
		for i in range(0,len(self._datekeys)-1):
			if self._datekeys[i] in self._updatekeys:
				cursor.execute(("UPDATE Goals SET TotalCalories = {}, TargetType = {} "
								"WHERE DateKey = {} AND UserID = {}".
								format(self._scheduledCalories[i],self._goalcycle[i],self._datekeys[i],self._ID)))
				#print("i: " + str(i))
				conx.commit()
			elif self._datekeys[i] in self._insertkeys:
				cursor.execute(("INSERT INTO Goals VALUES({},{},{},{},{})"
								.format(self._datekeys[i],self._scheduledCalories[i],200,self._goalcycle[i],self._ID)))
				conx.commit()
			else:
				print('Error')
		datekey = DateInfo.initFromDate(datetime.date.today()).data[0][0]
		cursor.execute("INSERT INTO UsersWeight(UserID, Date, Pounds, ActivityMultiplier, GoalType) VALUES({}, {}, {}, {}, {})".format(self._ID,datekey,round(self._Weight,1),round(self._Activity,2),self._Goal))
		conx.commit()

	@property
	def ID(self):
		return self._ID
	@property
	def FirstName(self):
		return self._FirstName
	@property
	def LastName(self):
		return self._LastName
	@property
	def Birthday(self):
		return self._Birthday
	@property
	def Gender(self):
		return self._Gender
	@property
	def Height(self):
		return self._Height
	@property
	def MostRecentDate(self):
		return self._MostRecentDate
	@property
	def Weight(self):
		return self._Weight
	@property
	def Activity(self):
		return self._Activity
	@property
	def Goal(self):
		return self._Goal
	@MostRecentDate.setter
	def MostRecentDate(self,date):
		self._MostRecentDate = date
	@Weight.setter
	def Weight(self,weight):
		self._Weight = weight
	@Activity.setter
	def Activity(self,activity):
		self._Activity = activity
	@Goal.setter
	def Goal(self,GoalID):
		self._Goal = GoalID
	
	
	
	
	
	
	
	
	






		














	
