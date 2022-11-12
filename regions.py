# To do
#  - set up database
#  - save to database (manual)
#  - print out database
#  - save to database (program)
#  - read from database and add to nav objects

import sqlite3
from sql_metadata import *
# from nav import *

def db(db_str):
    con = sqlite3.connect('data.db')
    c = con.cursor()
    # print(db_str)
    c.execute(db_str)
    output = c.fetchall()
    # names = list(map(lambda x: x[0], c.description))
    # print(names)
    con.commit()
    con.close()
    return output

def db_create_table():
    db_str = "CREATE TABLE regions(object_name TEXT, x INTEGER, y INTEGER, w INTEGER, h INTEGER)"
    db(db_str)

def db_entry():
    db_str = "INSERT INTO regions VALUES ('1')"
    db(db_str)

# def db_add(object, region):
#     x, y, w, h = region
#
#     print("Inserting region record")
#     db_str = f"INSERT INTO regions VALUES ('{object.name}', '{x}', '{y}', '{w}', '{h}')"
#     db(db_str)


def db_regions_get(object, type=None):
    if type == None or type == "Not specified": db_name = object.name
    else: db_name = type
    return db(f"SELECT * FROM regions WHERE object_name='{db_name}'")


def db_regions_add(object, region, type=None):
    if type == None or type == "Not specified": db_name = object.name
    else: db_name = type

    x, y, w, h = region

    existing = db(f"SELECT * FROM regions WHERE object_name='{db_name}' and x = '{x}' and y = '{y}' and w = '{w}' and h = '{h}'")
    # print(len(existing))

    if len(existing) == 0:
        # print("Inserting region record:", object.name)
        db_str = f"INSERT INTO regions VALUES ('{db_name}', '{x}', '{y}', '{w}', '{h}')"
        db(db_str)
    else:
        print("Region record already exists:", db_name)

def db_delete():
    db("DELETE from regions")

def db_delete_table(table):
    db_str = f"DROP TABLE {table}"
    db(db_str)

def db_regions_view():
    output = db("SELECT * FROM regions")
    for region in output:
        print(region)

def db_regions_delete(object, region, type=None):
    if type == None or type == "Not specified": db_name = object.name
    else: db_name = type

    x, y, w, h = region
    selected_for_deletion = db(f"SELECT * FROM regions WHERE object_name='{db_name}' and x = {x} and y = {y} and w = {w} and h = {h}")
    print(db_name, " Region:", region, "Selected for deletion", selected_for_deletion)
    db(f"DELETE FROM regions WHERE object_name='{db_name}' and x = '{x}' and y = '{y}' and w = '{w}' and h = '{h}'")

def db_regions_delete_object(object, type=None):
    if object is None: db_name = type
    elif type == None or type == "Not specified": db_name = object.name
    else: db_name = type
    where_string = f"WHERE object_name='{db_name}'"

    selected_for_deletion = db(f"SELECT * FROM regions " + where_string)
    print(db_name, "Selected for deletion", selected_for_deletion)
    db(f"DELETE FROM regions " + where_string)

# db_regions_delete_object(None, type='Not specified')
# db_delete_table('regions')
# db_create_table()
# # db_add("main", [10,10,10,11])
# # db_entry()
db_regions_view()

# db_delete()

# columns = sql_metadata.get_query_columns("SELECT regions")
# print(columns)



