# from bot import *
# from troops import *
# from account import *
from attacks_logic import *
# from account import *



troops1 = ["edrag"] * 8 + ["dragon"] * 2 + ["lightening"] * 11
troops2 = ["dragon"] * 12 + ["balloon"] + ["lightening"] * 11
data = [(1, troops1), (2, troops2)]

def wait(minutes):
    for x in range(minutes):
        print(f"Waiting: {x} of {minutes} minutes")
        time.sleep(60)


def war_prep():
    goto(main)
    for account in [account_1, account_2,]:
        print(objects_to_str(account.war_troops))
        change_accounts(account.number, "main")
        army_prep(account, account.war_troops)
        castle_troops_change(account.clan_troops_war)

def war_donations():
    accounts = [account_1, account_2]
    rounds = []
    rounds.append(([edrag] * 12 + [dragon] * 2 + [ice_golem] * 4, 4))
    rounds.append(([super_barb] * 10 + [bloon] * 10, 1))

    for donations, loops in rounds:
        for account in accounts:
            change_accounts(account.number)
            war_donations_1(account, donations)

        for x in range(loops):
            goto(pycharm)
            wait(10)
            for account in accounts:
                change_accounts(account.number)
                war_donations_2()

def war_donations_1(account, troop_donations):
    army_prep(account, troop_donations, troops_only=True)

def war_donations_2():
    goto(main)
    i_war.click()
    time.sleep(0.1)
    if not i_war_preparation.find():
        time.sleep(1)
        if not i_war_preparation.find():
            print("Couldn't find war preparation")
            goto(pycharm)
            return
    time.sleep(2)
    if not i_war_castle.click() and not i_war_castle2.click():
        print("Couldn't find castle")
        goto(pycharm)
        return

    still_moving, count = True, 0
    while still_moving and count < 5:
        i_war_left.click()
        pag.moveTo(300,800)
        if i_war_left.colour() < 800: still_moving = False
        time.sleep(0.1)
        count += 1

    still_moving, count, fail = True, 0, 0
    while still_moving and count < 35 and fail < 15:
        print(i_donate.colour())
        if i_war_donate.colour() > 800:
            donate_screen_showing, count = False, 0
            while not donate_screen_showing and count < 3:
                time.sleep(0.1)
                if i_war_donate_reinforcements.find(fast=False):
                    donate_screen_showing = True
                if not donate_screen_showing:
                    i_war_donate.click()
                count += 1

            success = False
            for troop in [edrag, ice_golem, dragon, super_barb, bloon]:
                has_troop = troop.i_donate2.find()
                has_room = troop.i_donate2.check_colour()
                if has_troop and has_room:
                    troop.i_donate2.click_region(WAR_DONATION_AREA)
                    success = True
            if not success: fail += 1
        i_war_right.click()
        pag.moveTo(1300,800)
        if i_war_right.colour() < 800: still_moving = False
        time.sleep(0.1)
        count += 1

def war_status():
    print("War status")
    status = None
    war_banner = cv2.imread(f'temp/tracker/war_banner.png', 0)
    if i_war_preparation.find_screen(war_banner, show_image=False): status = "Preparation"
    if i_war_battle_day.find_screen(war_banner, show_image=False): status = "Battle Day"
    if status == "Preparation":
        for account in [1, 2]:
            change_accounts(account)
            war_donations_ad_hoc()
        dragon.donation_count = 1
        edrag.donation_count = 8
        freeze.donation_count = 1
        ice_golem.donation_count = 3
        ice_golem.donations = 1
    elif status == "Battle Day":
        dragon.donation_count = 15
        freeze.donation_count = 7
        lightening.donation_count = 7
        edrag.donation_count = 1
        ice_golem.donation_count = 1
        ice_golem.donations = 0
    else:
        dragon.donation_count = 1
        freeze.donation_count = 1
        edrag.donation_count = 5
        ice_golem.donation_count = 1
        ice_golem.donations = 0


def war_donations_donate_troop(troop):
    if not i_war_donate_reinforcements.find(fast=False):
        i_war_donate.click()
        time.sleep(0.1)
    troop.i_donate2.click_region(WAR_DONATION_AREA)

def war_donations_ad_hoc():
    goto(main)
    i_war.click()
    time.sleep(0.1)
    if not i_war_preparation.find():
        time.sleep(1)
        if not i_war_preparation.find():
            print("Couldn't find war preparation")
            goto(pycharm)
            return
    time.sleep(2)
    if not i_war_castle.click() and not i_war_castle2.click():
        print("Couldn't find castle")
        goto(pycharm)
        return
    still_moving, count = True, 0
    while still_moving and count < 5:
        i_war_left.click()
        pag.moveTo(300,800)
        if i_war_left.colour() < 800: still_moving = False
        time.sleep(0.1)
        count += 1

    still_moving, count = True, 0
    while still_moving and count < 35:
        remaining = remaining_donations()
        if remaining > 0:
            # donations = [(edrag, 30, 50), (dragon, 20, 29), (ice_golem, 15, 19), (bloon, 10,14), (super_barb, 5, 9), (wizard, 4, 4), (archer, 1, 4)]
            # for troop, min, max in donations:
            #     if rem
            if remaining >= 30:
                war_donations_donate_troop(edrag)
                remaining = remaining_donations()
            elif remaining >= 20:
                war_donations_donate_troop(dragon)
                remaining = remaining_donations()
            elif remaining >= 15:
                war_donations_donate_troop(ice_golem)
                remaining = remaining_donations()
            elif remaining >= 10:
                war_donations_donate_troop(bloon)
                remaining = remaining_donations()
            elif remaining >= 5:
                war_donations_donate_troop(super_barb)
                remaining = remaining_donations()
            elif remaining >= 4:
                war_donations_donate_troop(wizard)
                remaining = remaining_donations()
            elif remaining >= 1:
                war_donations_donate_troop(archer)
                war_donations_donate_troop(archer)
                war_donations_donate_troop(archer)
                war_donations_donate_troop(archer)

        i_war_right.click()
        pag.moveTo(1300,800)
        if i_war_right.colour() < 800: still_moving = False
        time.sleep(0.1)
        count += 1


def remaining_donations():
    result = war_donation_count.read(WAR_DONATION_COUNT, show_image=False)
    x_pos = result.find("x")
    try:
        received = int(result[0:x_pos])
        total = int(result[x_pos+1:])
    except:
        return 0
    return total - received





        # get_screenshot(TRADER_TIME, filename=f"tracker/trader_time")
        # time.sleep(0.1)
        # i_trader_close.click()

    # time.sleep(2)
    # get_screenshot(WAR_BANNER, filename=f"tracker/war_banner")
    # print("Saved war banner")
    #
    # i_return_home_2.click()



# war_donations()
# war_prep()