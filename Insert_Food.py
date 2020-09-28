import WidgetUtility as Util
import tkinter
from tkinter import ttk as ttk
import pandas as pd
import pandastable as table
import pyodbc

conx = pyodbc.connect("DRIVER={SQL SERVER NATIVE CLIENT 11.0};SERVER=(local);DATABASE=DietDb;Trusted_Connection=yes")
cursor = conx.cursor()

root = tkinter.Tk()
root.geometry('800x600')
frame=tkinter.Frame()
frame.grid(row=0,column=0,rowspan=12,columnspan=12)


sql = ("SELECT Food.FoodKey,FoodTypes.FoodType,Food.Measurement,Brands.Brand,Food.Name,Food.Calories,Food.Protein,Food.Carbs,Food.TotalFat,Food.SatFat,Food.Fiber "
		"FROM Food INNER JOIN FoodTypes ON FoodTypes.FoodTypesKey = Food.FoodType INNER JOIN Brands ON Brands.BrandKey=Food.Brand UNION SELECT "
		"Food.FoodKey,FoodTypes.FoodType,Food.Measurement,' ',Food.Name,Food.Calories,Food.Protein,Food.Carbs,Food.TotalFat,Food.SatFat,Food.Fiber "
		"FROM Food INNER JOIN FoodTypes ON FoodTypes.FoodTypesKey = Food.FoodType WHERE Food.Brand IS NULL ORDER BY FoodTypes.FoodType ASC")

query = pd.read_sql(sql,conx)

display = table.Table(frame,dataframe=query)
display.show()

labels = Util.LabelRow(root,root.grid_size()[0],11,['FoodKey','Food Type','Measurement','Brand','Food Name','Calories Per','Protein Per','Carbs Per','Total Fat Per','Sat Fat Per','Fiber Per'])


WidRow = Util.RowOfWidgets(root,root.grid_size()[0]+1)

PKLabel = Util.NextKey_Label(WidRow,'Food',width=5)
eMeasurement = ttk.Entry(WidRow,width=10)
NameEntry = ttk.Entry(WidRow,width=10)
foodtypelist = Util.SQL_ComboBox(WidRow,"SELECT FoodTypesKey, FoodType FROM FoodTypes ORDER BY FoodTypes.FoodType",width=10)
brandlist = Util.SQL_ComboBox(WidRow,"SELECT BrandKey, Brand FROM Brands ORDER BY Brand",width=10)
eCalories = ttk.Entry(WidRow,width=7)
eProtein = ttk.Entry(WidRow,width=7)
eCarbs = ttk.Entry(WidRow,width=7)
eTotalFat = ttk.Entry(WidRow,width=7)
eSatFat = ttk.Entry(WidRow,width=7)
eFiber = ttk.Entry(WidRow,width=7)

WidRow.placeWidget(PKLabel,0)
WidRow.placeWidget(foodtypelist,1)
WidRow.placeWidget(eMeasurement,2)
WidRow.placeWidget(brandlist,3)
WidRow.placeWidget(NameEntry,4)
WidRow.placeWidget(eCalories,5)
WidRow.placeWidget(eProtein,6)
WidRow.placeWidget(eCarbs,7)
WidRow.placeWidget(eTotalFat,8)
WidRow.placeWidget(eSatFat,9)
WidRow.placeWidget(eFiber,10)

values = []

def SubmitData():
	for w in range(0,len(WidRow.widgets)):
		if len(str(WidRow.widgets[w].get()))==0:
			values.append('NULL')
		elif WidRow.widgets[w].winfo_class()=='TCombobox':
			values.append(WidRow.widgets[w].get().split(',')[0][1:])
		elif WidRow.widgets[w].winfo_class()=='TLabel':
			values.append(WidRow.widgets[w].get())
		else:
			values.append(WidRow.widgets[w].get())
	sql_insert = ("INSERT INTO Food(FoodKey,FoodType,Measurement,Brand,Name,Calories,Protein,Carbs,TotalFat,SatFat,Fiber) "
					"VALUES({},{},'{}',{},'{}',{},{},{},{},{},{})".format(values[0],values[1],values[2],values[3],values[4],values[5],values[6],values[7],values[8],values[9],values[10]))
	cursor.execute(sql_insert)
	conx.commit()
	#print(sql_insert)
	conx.close()


bSubmit = ttk.Button(root,text='Submit',command=SubmitData)
bSubmit.grid(column=0)


root.mainloop()