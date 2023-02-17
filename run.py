from bot import *
# from war import *
from research import *
from games import *

sweep_period = timedelta(minutes=120)

def run():
    global current_account
    next_sweep = datetime.now() + (datetime.min - datetime.now()) % sweep_period
    db_update(account_0, "sweep", next_sweep)
    games = False
    if not games:
        war_status()
        for account in accounts:
            if account.mode in ["Attacking"]:
                db_update(account, "attack", datetime.now() + timedelta(minutes=-20))
            if account.mode in ["Donating"]:
                db_update(account, "donate", datetime.now() + timedelta(minutes=-20))

    while True:
        run_job(db_next_job(), sweep_period, games=games)

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
    # print(screens)

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
            donate(account, account_0.mode)
            capital_coin()
        account.update_resources(current_resources())
        account.next_update()
        clock()
        get_resources()


# goto(attacking_b)

# goto(builder)
# i_attack_b.click()
# i_find_now.click()


# attack_b(account_3, True)

# for troop in troops:
#     print(troop.name)
#     print(troop.i_donate1)
#     try:
#         cv2.imshow("label", troop.i_donate1)
#     except:
#         print(f"No image for {troop}")


# goto(main)

def just_donate():
    change_accounts_fast(account_1)
    account_1.attacking = False
    print("Account 1 donating: ", account_1.donating())
    count = 0
    while count < 60 * 2:
        donate(account_1)
        goto(main)
        time.sleep(60)
        count += 1

def just_attack_b_all():
    for account in accounts:
        change_accounts_fast(account)
        just_attack_b(account)

# account = account_3
# build_new(account, "main")
# account.update_build_time()
# just_attack_b_all()
# sweep()
run()


# donate(account_3)
# build_new(account_3, "main")

goto(pycharm)