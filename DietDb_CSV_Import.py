import csv
import pyodbc


#create connection to database
conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
#create cursor object
cursor = conx.cursor()


#popup box for file path


#create csv file
path = 'C:\\Users\\Devin\\Desktop\\FoodTable.csv'

addData = open(path)
reader = csv.reader(addData,delimiter=",")
data = [r for r in reader]

#new csv file to bounce any data that throws an error
failData = open('C:\\Users\\Devin\\Desktop\\FailedImports.csv','w+')
writer = csv.writer(failData)

sqlLog = open('C:\\Users\\Devin\\Desktop\\SqlStatements.csv','w+')
sqlwriter = csv.writer(sqlLog)

for x in range(1,len(data)):
	if len(data[x][3]) == 0:
		data[x][3] = 'NULL'

	sqlInput = 'INSERT INTO FOOD(' + ",".join(data[0]) + ') VALUES(' + data[x][0] + ',' + data[x][1] + ",'" + data[x][2] + "'," + data[x][3] + ",'" + data[x][4] + "'," + ",".join(data[x][5:]) + ")"
	#print(sqlInput)
	try:
		sqlwriter.writerow('worked ' + sqlInput)
		cursor.execute(sqlInput)
		conx.commit()
	except:
		sqlwriter.writerow('failed' + sqlInput)
		writer.writerow(data[x])
		continue
	finally:
		sqlwriter.writerow('failed' + sqlInput)
		writer.writerow(data[x])
		
conx.close()

