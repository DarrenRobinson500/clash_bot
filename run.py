from bot import *

def run(attacking, building):
    next_sweep = datetime.now() + (datetime.min - datetime.now()) % sweep_period
    db_update(0, "sweep", next_sweep)
    for x in attacking:
        db_update(x, "attack", datetime.now() + timedelta(minutes=-20))

    global current_location
    current_location = "main"
    print_info()
    time.sleep(7)

    start()
    # reset()
    while True:
        run_job(db_next_job(), attacking, building)

def wait(minutes):
    for x in range(minutes):
        print(f"Waiting: {x} of {minutes} minutes")
        time.sleep(60)



def walls():
    walls = 150
    x = 0
    while walls >= 0:
        date_to_print = datetime.now() + timedelta(days=x)
        print(date_to_print.strftime('%d %b'), walls)
        walls -= 5
        x += 1

def rapid_attack(account):
    start()
    change_accounts(1, "main")
    count = 0
    while count < 20:
        troops = FAV_ATTACK[account]
        attack(account, troops)
        time.sleep(60)
        count += 1
    end()

def test(account, village):
    start()
    # change_accounts(account, village)
    # remove_trees("builder")
    # sweep()
    # clock()
    # attack(2, BARBS_11)
    # attack(3, GIANT220)
    # attack_b(account)
    # build(account, village)
    # goto("troops_tab")
    # add_troops("super_barb",1)
    end()


wait(0)
attacking = [1,2]
building = [1,2,3]
# rapid_attack(1)
# db_update_next(2,"builder","gold", "none")
account, village = 1, "main"
# test(account, village)
# run(attacking, building)
db_view_next()
# walls()