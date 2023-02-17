import sqlite3

def db(db_str):
    con = sqlite3.connect('data.db')
    c = con.cursor()
    # print(db_str)
    c.execute(db_str)
    output = c.fetchall()
    con.commit()
    con.close()
    return output

def db_create_table(name):
    db_str = f"CREATE TABLE {name}(account INTEGER, game TEXT)"
    db(db_str)

def db_delete_table(name):
    db_str = f"DROP TABLE {name}"
    db(db_str)

def db_games_update(account, game):
    condition = f" WHERE account='{account}'"
    db_str = f"SELECT * FROM games" + condition
    existing = len(db(db_str))
    # print("Current Records: ", existing)
    if existing == 0:
        db_str = f"INSERT INTO games VALUES ({account}, '{game}')"
        db(db_str)
    else:
        db_str = f"UPDATE games SET game='{game}'" + condition
        db(db_str)

def db_games_view():
    db_str = "SELECT * FROM games ORDER BY account"
    output = db(db_str)
    for account, game in output:
        if game == "": game = None
        # print(f"Account {account}: {game}")

def db_games_read(account):
    db_str = f"SELECT * FROM games WHERE account='{account}'"
    output = db(db_str)
    if len(output) > 0: return output[0][1]
    return None

def db_games_clear():
    for x in range(1, 5):
        db_games_update(x, "")
    db_games_view()

# db_create_table("games")
# db_games_update(1, "destroy_wizard")
# db_games_view()
# print(db_games_read(2))

# db_games_clear()