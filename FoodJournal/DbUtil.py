import os
import csv
from time import sleep
from tokenize import String
from decimal import Decimal
import psycopg2
from sqlalchemy import Date, Table, Column, MetaData, Integer, Identity, Text, Numeric, ForeignKey, Boolean
from sqlalchemy import create_engine, select, join
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import registry
from sqlalchemy.orm.session import sessionmaker, Session
from sqlalchemy.exc import IntegrityError, OperationalError
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_NAME = 'db.sqlite3'


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
                    Column("description", Text, nullable=False, unique=True),
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
users  =         Table("auth_user", meta,
                    Column("id", Integer, Identity(always=True, start=1, cycle=True), primary_key=True, nullable=False),
                    Column("username", Text, nullable=False, unique=True),
                    Column("first_name", Text, nullable=True),
                    Column("last_name", Text, nullable=True),
                    Column("email", Text, nullable=True, unique=True),
                    Column("password", Text, nullable=False),
                    Column("is_staff", Boolean, nullable=False),
                    Column("is_active", Boolean, nullable=True),
                    Column("is_superuser", Boolean, nullable=True),
                    Column("last_login", Date, nullable=True),
                    Column("date_joined", Date, nullable=False)
                    )
food_eaten =    Table("food_eaten", meta,
                    Column("id", Integer, Identity(always=True, start=1, cycle=True), primary_key=True, nullable=False),
                    Column("food", Integer, ForeignKey("food_info.id"), nullable=False),
                    Column("qty", Numeric, nullable=False),
                    Column("date", Date, nullable=False),
                    Column("user", Integer, ForeignKey("auth_user.id"), nullable=False)
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

def create_test_engine(db_name=DATABASE_NAME, log_to_console=True):
    return create_engine(f"sqlite:///{BASE_DIR / db_name}", echo=log_to_console, future=True)

csv_file = os.path.dirname(__file__) + '\csv\RawFoodData.csv'
engine = create_test_engine(log_to_console=False)

def create_postgresql_engine(db=database, driver=gosling, user=admin, pword=password, host=host, port=port):
    if pword is None:
        try:
            with open("passwords.txt", "r") as file:
                pword = file.readline().strip()
        except FileNotFoundError:
            print("Cannot locate passwords.txt")
            return
    return create_engine(f"postresql+{driver}://{user}:{pword}@{host}/{db}")

def get_id(table:Table, column:Column, value, engine:Engine=engine)->int:
    stmt = select(table).filter(column == value)
    session = sessionmaker(bind=engine)
    with session.begin() as s:
        results = s.execute(stmt)
        for row in results:
            #print(f"\n\nRow: {row}")
            return int(row[0])
        return 0

def load_foodinfo_csv(path:String, engine:Engine=engine)->None:
    #get pks for all the measurements in the csv file
    measurement_dict = {}
    with open(path, "r") as file:
        for row in csv.reader(file):
            measure_string = row[measurement].lower().strip()
            if measure_string == 'measurement':
                continue
            id = get_id(measurements, measurements.c.description, measure_string, engine)
            if id > 0:
                measurement_dict[measure_string] = id
            else:
                add_measurement(measure_string, engine)
                id = get_id(measurements, measurements.c.description, measure_string, engine)
                measurement_dict[measure_string] = id
    #load any missing measurements into the db and get their new pk
    '''for string, val in measurement_dict.items():
        if val is None:
            add_measurement(string, engine)
            measurement_dict[string] = get_id(measurements, measurements.c.description, string, engine)'''
    #load all data from csv file
    new_session = sessionmaker(bind=engine)
    with open(path, "r") as file:
        with new_session.begin() as s2:
            for row in csv.reader(file):
                data_dict = {}
                try:
                    # data dict keys have to be the same as the food_info table column names
                    data_dict['description'] = row[food_description].lower().strip()
                    data_dict['calories_unit'] = float(row[calories])
                    data_dict['protein_unit'] = float(row[protein])
                    data_dict['carbs_unit'] = float(row[carbs])
                    data_dict['total_fat_unit'] = float(row[total_fat])
                    data_dict['sat_fat_unit'] = float(row[sat_fat])
                    data_dict['fiber_unit'] = float(row[fiber])
                    data_dict['measurement_unit'] = measurement_dict[row[measurement].lower().strip()]
                    insert = food_info.insert().values(**data_dict)
                    s2.execute(insert)
                except (ValueError, IntegrityError) as error:
                    continue
            s2.commit()

def add_measurement(measurement_string:String, engine:Engine=engine)->None:
    session = sessionmaker(bind=engine)
    with session.begin() as s:
        #print(f"Adding {measurement_string.lower().strip()}")
        s.execute(measurements.insert().values(description=measurement_string.lower().strip()))
        s.commit()
        s.flush()

def create_database(engine:Engine):
    for tbl in meta.sorted_tables:
        try:
            tbl.create(engine)
        except OperationalError:
            try:
                tbl = Table(tbl.name, meta, autoload_with=engine)
                #print(f"{tbl} was changed to reflect existing table.")
            except OperationalError:
                continue

FOOD_CHOICES = []
try:
    session = sessionmaker(bind=engine)
    with session.begin() as s:
        stmt = select(food_info.c.id, food_info.c.description)
        results = s.execute(stmt)
        for row in results:
            FOOD_CHOICES.append((row[1], row[0]))
except (IntegrityError, OperationalError):
    print("Failed to create FOOD_CHOICES")

def clear_db(engine:Engine):
    for tbl in reversed(meta.sorted_tables):
        try:
            #print(f"Dropping table {tbl}")
            if tbl is users:
                continue
            tbl.drop(engine)
        except OperationalError:
            continue

def reset_db(engine:Engine=engine, load_csv=True):
    clear_db(engine)
    create_database(engine)
    if load_csv:
        load_foodinfo_csv(csv_file)

def clean_input(user_input:str)->str:
    return user_input.replace(";", "").replace("(", "").replace(")", "")

def get_food_dict(food:str, engine:Engine=engine)->str:
    view = food_info.join(measurements)
    query = select(food_info, measurements.c.description).where(food_info.c.description == food)
    q = query.select_from(view)
    session = sessionmaker(bind=engine)
    food_dict = {}
    with session.begin() as s:
        results = s.execute(q)
        row = results.fetchone()
        keys = row.keys()
        for key in keys:
            val = row[key]
            if type(val) == Decimal:
                val = float(val)
            food_dict[key] = val
    return food_dict




if __name__ == "__main__":
    #deletes current db, creates the database and loads the csv file
    load_foodinfo_csv(csv_file)
