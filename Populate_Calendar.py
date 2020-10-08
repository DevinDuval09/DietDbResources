import pyodbc
import datetime
import math
import pandas

#adds 31 days to date table

#db connection
conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
cursor = conx.cursor()

#Create date range to insert
sqlStatements = []
dateseed = datetime.date.today()
nextkey = cursor.execute("SELECT DateKey FROM Dates ORDER BY DateKey DESC").fetchone()[0]+1

for d in range(0,31):
	nextkey = nextkey + d
	dt = dateseed + datetime.timedelta(days=d)
	date = dt.strftime("%x")
	daysuffix = dt.strftime("%a")[0:2]
	weekdaynum = dt.strftime("%w")
	weekdayname = dt.strftime("%A")
	weekdayshort = dt.strftime("%a")
	weekdayfirst = dt.strftime("%A")[0]
	DOWinMonth = dt.strftime("%d")
	DOY = dt.strftime("%j")
	WeekOfMonth = str((math.ceil((dt.day + dt.replace(day=1).weekday())/7.0)))
	WeekOfYear = dt.strftime("%U")
	MonthNum = str(dt.month)
	MonthName = dt.strftime("%B")
	MonthNameShort = dt.strftime("%b")
	MonthNameLetter = dt.strftime("%B")[0]
	Quarter = str(pandas.Timestamp(dt).quarter)
	QuarterName = 'Q' + str(Quarter) + str(dt.year)
	Year = str(dt.year)
	MMYYYY = str(dt.month)+str(dt.year)
	if(len(MMYYYY))<6:MMYYYY = '0'+MMYYYY
	MonthYear = MonthNameShort + str(dt.year)
	IsWeekend = 0
	if(weekdayshort == "Sun" or weekdayshort == "Sat"): IsWeekend = 1

	sqlStatements.append("INSERT INTO Dates VALUES(" + str(nextkey) + ", CONVERT(DATE,'" + str(date) + "',1),'" + daysuffix + 
		"'," + weekdaynum + ",'" + weekdayname + "','" + weekdayshort + "','" + weekdayfirst + "'," + DOWinMonth + ","
		+ DOY + "," + WeekOfMonth + "," + WeekOfYear + "," + MonthNum + ",'" + MonthName + "','" + MonthNameShort + "','" 
		+ MonthNameLetter + "'," + Quarter + ",'" + QuarterName + "'," + Year + ",'" + MMYYYY + "','" + MonthYear +"',"+
		str(IsWeekend) + ")")

for s in sqlStatements:
	cursor.execute(s)
	conx.commit()
	#print(s)