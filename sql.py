import sqlite3
from datetime import datetime, timedelta
from ocr import string_to_time, time_to_string

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
    db_str = "CREATE TABLE jobs(account INTEGER, job TEXT, time datetime)"
    db(db_str)

def db_delete_table(table):
    db_str = f"DROP TABLE {table}"
    db(db_str)

def db_add(account, job, time):
    if not isinstance(account, int):
        account = account.number
    db_str = f"INSERT INTO jobs VALUES ({account}, '{job}', '{time}')"
    db(db_str)

def db_update(account, job, time, use_account_number=False):
    if use_account_number:
        account_number = account
    else:
        account_number = account.number
    db_str = f"SELECT * FROM jobs WHERE account='{account_number}' and job = '{job}'"
    existing = len(db(db_str))
    # print("DB Update - Current records:", existing, account.number, job)
    print(existing)
    if existing == 1:
        # print("DB Update", account, job, time)
        db_str = f"UPDATE jobs SET time='{time}' WHERE account = {account_number} AND job = '{job}'"
        # print("DB Str:", db_str)
        db(db_str)
    else:
        print("Records not updated")

def db_delete(rowid):
    if rowid == "all":
        db_str = f"DELETE from jobs"
    else:
        db_str = f"DELETE from jobs WHERE rowid = {rowid}"
    db(db_str)

def db_delete_job(job):
    db_str = f"DELETE from jobs WHERE job = {job}"
    db(db_str)

def db_view(job='all', no=5):
    output = db_get(job='all', no=no)
    count = 0
    for x in output:
        if count < no:
            time = string_to_time(x[2])
            time = time_to_string(time)
            tabs = "\t"
            if len(x[1]) <= 5: tabs += "\t"
            if len(x[1]) <= 9: tabs += "\t"
            print("Account:", x[0], " Job:", x[1], tabs + "Time:", time)
        count += 1

def db_view_builds(job='all', no=5):
    output = db_get(job='all', no=no)
    count = 0
    for account, job, time in output:
        if count < no:
            if job in ["build", "research"]:
                time = string_to_time(time)
                time = time_to_string(time)
                tabs = "\t"
                if len(job) <= 5: tabs += "\t"
                if len(job) <= 9: tabs += "\t"
                print("Account:", account, " Job:", job, tabs + "Time:", time)
                count += 1

def db_get(job='all', no=5):
    if job == 'all':
        db_str = "SELECT * FROM jobs ORDER BY time"
    else:
        db_str = f"SELECT * FROM jobs WHERE job='{job}' ORDER BY time"
    output = db(db_str)
    return output

def db_read(account, job):
    db_str = f"SELECT * FROM jobs WHERE account='{account.number}' AND job = '{job}' ORDER BY time"
    x = db(db_str)
    if len(x) == 1 and x[0][2] is not None and x[0][2] != "None":
        time = datetime.fromisoformat(x[0][2])
    else:
        time = None
    # print(time)
    # print(time.astimezone().isoformat())
    return time

def initial_entries(accounts, zero_account):
    db_delete('all')
    time = datetime.now() + timedelta(days=0)
    for x in accounts:
        for y in ["build", "research", "lose_trophies", "attack", "donate", "coin"]:
            db_add(x, y, time)
    db_add(zero_account, "sweep", time)
    db_add(zero_account, "games", time)

def add_entries():
    time = datetime.now() + timedelta(minutes=-20)
    for x in range(1,4):
        for y in ["sweep"]:
            db_add(x, y, time)

def add_entries_all():
    print("add_entries all")
    time = datetime.now() + timedelta(minutes=-20)
    db_add(0, "games", time)

# add_entries_all()

def update_entries():
    time = datetime.now() + timedelta(minutes=0)
    for x in range(1,4):
        for y in ["build", "attack", "build_b", "attack_b", "clock", "coin", "research", "research_b", "donate", "coin"]:
            db_update(x, y, time)

# db_update(2, "lose_trophies", datetime.now(), use_account_number=True)
# db_update(3, "lose_trophies", datetime.now(), use_account_number=True)
# db_update(4, "lose_trophies", datetime.now(), use_account_number=True)

def db_next_job():
    db_str = "SELECT * FROM jobs ORDER BY time"
    result = db(db_str)
    current_jobs = []
    for job_info in result:
        account, job, job_time = job_info
        job_time = string_to_time(job_time)
        if job_time <= datetime.now():
            current_jobs.append(job_info)
    current_jobs.sort(key=lambda tup: tup[0])
    if len(current_jobs) > 0:
        return current_jobs[0]
    else:
        return result[0]



# db_create_table()
# db_delete('all')
# db_delete_table('jobs')
# db_add(2, "attack", datetime.datetime.now())

# update_entries()
# db_view()
# add_entries()
# add_entries()
# for x in [account_3,]:
#     db_update(x, "attack", datetime.now() + timedelta(minutes=3))
# add_entries_all()
# db_delete_job("'attack_b'")

db_view(no=50)
#
# db_next_job()
