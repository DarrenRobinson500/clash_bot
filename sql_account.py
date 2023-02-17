import sqlite3
from bot import *

def db(db_str):
    con = sqlite3.connect('data.db')
    c = con.cursor()
    # print(db_str)
    c.execute(db_str)
    output = c.fetchall()
    con.commit()
    con.close()
    return output

def db_create_table():
    db_str = "CREATE TABLE buildings(account INTEGER, building TEXT, complete bool, level INTEGER, loc_x INTEGER, loc_y INTEGER)"
    db(db_str)

def db_delete_table(table):
    db_str = f"DROP TABLE {table}"
    db(db_str)

def db_add(account, building, loc_x, loc_y, level, complete):
    condition = f" WHERE account='{account}' and building = '{building}' and loc_x = '{loc_x}' and loc_y = '{loc_y}'"
    db_str = f"SELECT * FROM buildings" + condition
    existing = len(db(db_str))
    # print("Current Records: ", existing)
    if existing == 0:
        db_str = f"INSERT INTO buildings VALUES ({account}, '{building}', '{loc_x}', '{loc_y}', '{complete}', '{level}')"
        db(db_str)
    else:
        print("Records not updated")

def db_update(account, building, loc_x, loc_y, level, complete):
    condition = f" WHERE account='{account}' and building = '{building}' and loc_x = '{loc_x}' and loc_y = '{loc_y}'"
    db_str = f"SELECT * FROM buildings" + condition
    existing = len(db(db_str))
    print("Current Records: ", existing)
    if existing == 0:
        db_str = f"INSERT INTO buildings VALUES ({account}, '{building}', '{loc_x}', '{loc_y}', '{complete}', '{level}')"
        db(db_str)
    elif existing == 1:
        db_str = f"UPDATE buildings SET level='{level}', complete='{complete}'" + condition
        db(db_str)
    else:
        print("Records not updated")

def db_delete(rowid):
    if rowid == "all":
        db_str = f"DELETE from buildings"
    else:
        db_str = f"DELETE from buildings WHERE rowid = {rowid}"
    db(db_str)

def db_view():
    db_str = "SELECT * FROM buildings ORDER BY account"
    output = db(db_str)
    count = 0
    for account, building, loc_x, loc_y, level, complete in output:
        if count < 50:
            complete_text = ""
            if complete: complete_text = "[Complete]"
            print(f"Account {account}: {building} ({loc_x},{loc_y}). Level {level} {complete_text}")
        count += 1

def initial_entries():
    db_delete('all')
    loc_x, loc_y, level, complete = 0, 0, 0, False
    for account in range(1,4):
        for building in ["Lab", ]:
            db_add(account, building, loc_x, loc_y, level, complete)

def read_tower(x, y):
    pag.screenshot('temp/temp.png')
    i = cv2.imread('temp/temp.png', 0)

    th = town_hall()
    if th is None: return
    th_loc = th[1]

    x += th_loc[0]
    y += th_loc[1]
    print(x,y)
    pag.click(x,y)
    time.sleep(0.5)
    pag.screenshot('temp/temp_read_tower.png', region=SELECTED_TOWER)
    screen = cv2.imread('temp/temp_read_tower.png', 0)
    level = find_best(LEVELS, screen)
    tower = find_best(TOWERS, screen)
    if level[1] > 0.7 and tower[1] > 0.7:
        print(tower, level)
        return tower[0], level[0]
    if tower[0] in OBSTACLES:
        print(tower, level)
        return tower[0], 0
    return

# db_update(account=3, building="Lab", loc_x=0, loc_y=0, level=0, complete=False)
# def main():
#     start()
#     pag.screenshot(f'attacks/attack.png')
#     i = cv2.imread(f'attacks/attack.png', 0)
#     lab = find_many_img(LABS, i)
#     th = town_hall()
#     if len(lab) == 0 or th is None: return
#     th_loc = th[1]
#
#     print("Lab", lab)
#     lab_rect = lab[0]
#     lab_loc = pag.center(lab_rect)
#
#     print("TH:", th_loc)
#     print("Lab:", lab_loc)
#     loc_x = lab_loc[0] - th_loc[0]
#     loc_y = lab_loc[1] - th_loc[1]
#     print("Relative loc:", loc_x, loc_y)
#
#     tower_stats = read_tower(loc_x, loc_y)
#     if tower_stats:
#         building, level = tower_stats
#         db_update(account=3, building=building, loc_x=loc_x, loc_y=loc_y, level=level, complete=False)
#         db_view()
#     else:
#         print("Couldn't read label")
#     end()

# main()

# start()
# pag.screenshot(f'attacks/attack.png')
# th = town_hall()
# print(th)
# pag.moveTo(th[1])
#

# pag.screenshot('temp/temp.png')
# i = cv2.imread('temp/temp.png', 0)
# th = find_many_img(TH, i)
# th_rect = th[0]
# th_loc = pag.center(th_rect)
# print(th_loc)

# end()