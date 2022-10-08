from bot import *

sweep_period = timedelta(minutes=20)

def run():
    global current_account
    current_account = account_0
    next_sweep = datetime.now() + (datetime.min - datetime.now()) % sweep_period
    db_update(account_0, "sweep", next_sweep)
    # sweep()
    for account in accounts:
        if account.attacking:
            db_update(account, "attack", datetime.now() + timedelta(minutes=-20))

    db_update(account_0, "sweep", datetime.now() + timedelta(minutes=-10))

    global current_location
    current_location = "main"
    print_info()
    # time.sleep(7)

    while True:
        run_job(db_next_job(), sweep_period)

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

# def actual_troop_count():
#     troop_count_dict = {}
#     for x in TROOPS:
#         count = troop_count(x)
#         troop_count_dict[x] = count
#     return troop_count_dict

def war_prep():
    goto(main)
    for account in accounts:
        print(objects_to_str(account.war_troops))
        change_accounts(account.number, "main")
        army_prep(account, account.war_troops)


def test(account, village):
    # change_accounts(2)
    goto(main)
    upgrade()
    # build("main")

# wait(30)

# rapid_trophy_loss(1)
# rapid_attack(1)
# war_prep()

# print(objects_to_str(troops))


# village = "main"
# get_available_upgrades_levels(village)

# build("main")

# goto(main)
# upgrade()

# troops_count(account_2)
# attack(account_2, account_2.army_troops)
# sweep()
run()


# result = get_available_upgrades_levels("main")
# for tower, cost, count in result:
#     print(tower, cost, count)



# goto_list_top("main")

# print(i_lab8.regions)
goto(pycharm)

