from bot import *
from war import *
from research import *

sweep_period = timedelta(minutes=120)

def run():
    global current_account
    next_sweep = datetime.now() + (datetime.min - datetime.now()) % sweep_period
    db_update(account_0, "sweep", next_sweep)
    # sweep()
    for account in accounts:
        print("Run:", account, account.attacking)
        if account.attacking:
            db_update(account, "attack", datetime.now() + timedelta(minutes=-20))
        if account.donating():
            db_update(account, "donate", datetime.now() + timedelta(minutes=-20))

    # db_update(account_0, "sweep", datetime.now() + timedelta(minutes=-10))

    change_current_location(pycharm)
    print_info()

    while True:
        run_job(db_next_job(), sweep_period)

def wait(minutes):
    for x in range(minutes):
        print(f"Waiting: {x} of {minutes} minutes")
        time.sleep(60)

def rapid_attack(account):
    start()
    change_accounts(1, "main")
    count = 0
    while count < 20:
        attack(account, account.army_troops)
        time.sleep(60)
        count += 1
    end()

def rapid_trophy_loss(account):
    start()
    change_accounts(1, "main")
    count = 0
    while count < 50:
        lose_trophies(1, troops=["super_barb", ])
        time.sleep(1)
        count += 1
    end()


def test2(account):
    screens = dir_to_list('attacks2')
    print(screens)

    count = 0
    max_count = 50
    for screen in screens:
        if count < max_count:
            count += 1
            image = cv2.imread("images/" + screen + ".png", 1)
            image_bw = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            target_locs = find_many_img(MINES, image_bw, confidence=0.7)
            center = (image.shape[1] // 2, image.shape[0] // 2)
            result = get_drop_points(account, image, center, target_locs)
            print(result)
            # show(result, 10000, screen, 0.7)



def info_grab():
    for account in accounts:
        change_accounts_fast(account)
        if account == account_1:
            war_get_status_image()
        get_resources()
        if account.th > 5:
            donate(account)
            capital_coin()
        account.update_resources(current_resources())
        account.next_update()
        clock()
        get_resources()


# info_grab()

# sweep(fast=True)

# get_trader_info(account_2)
# create_combined_builders_image(accounts)

# initial_entries(accounts, account_0)
# war_prep()
# wait(30)
# war_donations()
# sweep()
# print(clone)
# print(golem)
run()
# war_prep()

# next_research(account_4)

# get_time_coin()

# goto(main)
# goto(lab)

goto(pycharm)

