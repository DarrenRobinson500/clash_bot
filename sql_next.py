import sqlite3
from bot import *

def db(db_str):
    con = sqlite3.connect('data.db')
    c = con.cursor()
    print(db_str)
    c.execute(db_str)
    output = c.fetchall()
    con.commit()
    con.close()
    return output

def db_create_table():
    db_str = "CREATE TABLE next(account INTEGER, village TEXT, currency TEXT, building TEXT, cost INTEGER, comment TEXT)"
    db(db_str)

# account, village, currency, building, cost, comment

def db_delete_table(table):
    db_str = f"DROP TABLE {table}"
    db(db_str)

def db_delete(rowid):
    if rowid == "all":
        db_str = f"DELETE from next"
    else:
        db_str = f"DELETE from next WHERE rowid = {rowid}"
    db(db_str)


def initial_entries():
    db_delete('all')
    building, cost, comment = 'none', 0, ''
    for account in range(1,4):
        for village in ['main', 'builder']:
            for currency in ['elixir1', 'dark', 'gold', 'elixir']:
                condition = f" WHERE account='{account}' and village='{village}' and currency='{currency}'"
                db_str = f"SELECT * FROM next" + condition
                existing = len(db(db_str))
                if existing == 0:
                    db_str = f"INSERT INTO next VALUES ({account}, '{village}', '{currency}', '{building}', '{cost}', '{comment}')"
                    db(db_str)
        else:
            print("Record already exists", account, village, currency)

# account, village, currency, building, cost, comment

def db_clear(accounts=[1,2,3], villages=["main", "village"]):
    for account in accounts:
        for village in villages:
            db_update(account, village, "")


# db_delete_table('next')

# db_update(1, "main", "archer_tower")
# db_update(1, "builder", "lava")
# db_update(2, "main", "cannon")
# db_clear()


# db_update_next(1, "main", "none", 0)

# db_update_next(1,"main","elixir", "none")
# db_update_next(2,"main","elixir", "none")
# db_update_next(3,"main","elixir", "none")
# db_update_next(1,"builder","gold", "none")
# db_update_next(2,"builder","dark", "none")
# db_update_next(1,"main","elixir1", "none")
# db_update_next(3,"main","gold", "none")
db_update_next(1,"main","dark", "none")

# db_create_table()
# initial_entries()
# next_build()
db_view_next()
