import os
import csv
from tokenize import String
import psycopg2
from sqlalchemy import Date, Table, Column, MetaData, Integer, Identity, Text, Numeric, ForeignKey
from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine, Connection


database = "CalorieTracker"
admin = 'postgres'
password = None
host='127.0.0.1'
port=6000
gosling = 'psycopg2'

file_path = './csv/RawFoodData.csv'
food_description = 0
calories = 1
protein = 2
carbs = 3
total_fat = 4
sat_fat = 5
fiber = 6
measurement = 7

meta = MetaData()
food_info =     Table("food_info", meta,
                    Column("id", Integer, Identity(always=True, start=1, cycle=True), primary_key=True, nullable=False),
                    Column("description", Text, nullable=False),
                    Column("calories_unit", Numeric, nullable=False),
                    Column("protein_unit", Numeric, nullable=False),
                    Column("carbs_unit", Numeric, nullable=False),
                    Column("total_fat_unit", Numeric, nullable=False),
                    Column("sat_fat_unit", Numeric, nullable=False),
                    Column("fiber_unit", Numeric, nullable=False),
                    Column("measurement_unit", Integer, ForeignKey("measurements.id"), nullable=False)
                    )
measurements =  Table("measurements", meta,
                    Column("id", Integer, Identity(always=True, start=1, cycle=True), primary_key=True, nullable=False),
                    Column("description", Text, nullable=False, unique=True),
                    )
users =         Table("users", meta,
                    Column("id", Integer, Identity(always=True, start=1, cycle=True), primary_key=True, nullable=False),
                    Column("username", Text, nullable=False, unique=True),
                    Column("email", Text, nullable=True, unique=True)
                    )
food_eaten =    Table("food_eaten", meta,
                    Column("id", Integer, Identity(always=True, start=1, cycle=True), primary_key=True, nullable=False),
                    Column("qty", Numeric, nullable=False),
                    Column("date", Date, nullable=False)
                    )

def get_connection():
    if password is None:
        try:
            with open("passwords.txt", "r") as file:
                password = file.readline().strip()
        except FileNotFoundError:
            print("Cannot locate passwords.txt")
            return
    try:
        connection = psycopg2.connect(user=admin,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
        connection.set_session(readonly=True)
        return connection
    except psycopg2.OperationalError as e:
        print("Failed to connect to database:")
        print(e)
        connection.close()

def list_tables():
    conn = None
    try:
        conn = get_connection()
    except psycopg2.OperationalError as e:
        pass
    finally:
        if conn == None:
            return
    
    sql = "select * from information_schema.tables;"
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            for table in cursor:
                print(table)

def create_test_engine(log_to_console=True):
    return create_engine("sqlite://", echo=log_to_console, future=True)

def create_postgresql_engine(db=database, driver=gosling, user=admin, pword=password, host=host, port=port):
    if pword is None:
        try:
            with open("passwords.txt", "r") as file:
                pword = file.readline().strip()
        except FileNotFoundError:
            print("Cannot locate passwords.txt")
            return
    return create_engine(f"postresql+{driver}://{user}:{pword}@{host}/{db}")

def create_CalorieTracker_Db(engine):
    meta.create_all(engine)

def get_id(engine:Engine, table:Table, column:Column, value):
    s = select(table).where(column == value)
    with engine.connect() as conn:
        for row in conn.execute(s):
            return int(row[0])
        return 0

def load_foodinfo_csv(path:String, engine:Engine):
    with open(path, "r") as file:
        with engine.connect() as conn:
            for row in csv.reader(file):
                data_dict = {}
                try:
                    data_dict['description'] = row[food_description]
                    data_dict['calories_unit'] = float(row[calories])
                    data_dict['protein_unit'] = float(row[protein])
                    data_dict['carbs_unit'] = float(row[carbs])
                    data_dict['total_fat_unit'] = float(row[total_fat])
                    data_dict['sat_fat_unit'] = float(row[sat_fat])
                    data_dict['fiber_unit'] = float(row[fiber])
                    id = get_id(engine, measurements, measurements.c.description, row[measurement])
                    if id == 0:
                        add_measurement(row[measurement], conn)
                        id = get_id(engine, measurements, measurements.c.description, row[measurement])
                    data_dict['measurement_unit'] = id
                    insert = food_info.insert().values(**data_dict)
                    conn.execute(insert)
                    conn.commit()
                except ValueError as error:
                    continue

def add_measurement(measurement:String, conn:Connection):
    conn.execute(measurements.insert().values(description=measurement))
    conn.commit()

def create_database(engine:Engine):
    meta.create_all(engine)




if __name__ == "__main__":

    with open(file_path, "r") as file:
        for row in csv.reader(file):
           print(row)
