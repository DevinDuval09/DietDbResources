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

testRow = Util.LabelRow(root,root.grid_size()[0],2,['Food Type','Food Name'])

WidRow = Util.RowOfWidgets(root,root.grid_size()[0])
NameEntry = ttk.Entry(WidRow)
foodtypelist = Util.SQL_ComboBox(WidRow,"SELECT FoodTypesKey, FoodType FROM FoodTypes ORDER BY FoodTypes.FoodType")

WidRow.placeWidget(foodtypelist,0)
WidRow.placeWidget(NameEntry,1)






root.mainloop()