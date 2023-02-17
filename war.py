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
        # print("Couldn't find castle")
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
    status = None
    war_banner = cv2.imread(f'temp/tracker/war_banner.png', 0)
    war_info = cv2.imread(f'temp/tracker/war_info.png', 0)
    if i_war_preparation.find_screen(war_banner, show_image=False): status = "preparation"
    if i_war_battle_day.find_screen(war_banner, show_image=False): status = "battle_day"
    if i_season_info.find_screen(war_info, show_image=False): status = "cwl"
    account_0.mode = status
    print("War status:", status)

    if status == "cwl":
        for account in war_participants:
            change_accounts_fast(account)
            if i_attacks_available.find():
                account.cwl_attacks_left = True
            else:
                account.cwl_attacks_left = False
            print(account, "cwl_attacks_left", account.cwl_attacks_left)
            change_accounts_fast(account)
            remaining = cwl_donations_ad_hoc(cwl=True)
            print("REMAINING DONATIONS:", remaining)
            if remaining == 0:
                for a in accounts: a.cwl_donations_left = False
            else:
                for a in accounts: a.cwl_donations_left = True
    elif status == "preparation":
        for account in [account_1, ]:
            change_accounts(account.number)
            remaining = cwl_donations_ad_hoc(cwl=False)
            print("REMAINING DONATIONS:", remaining)
            if remaining == 0:
                for a in accounts: a.cwl_donations_left = False
            else:
                for a in accounts: a.cwl_donations_left = True
    else:
        for a in accounts: a.cwl_donations_left = False

    for account in accounts:
        change_accounts_fast(account)
        account.update_resources(current_resources())
        account.set_mode()
        queue_up_troops(account)

def war_donations_ad_hoc():
    print("War donations ad hoc")
    goto(main)
    i_war.click()
    time.sleep(0.1)
    if not i_war_preparation.find():
        time.sleep(1)
        if not i_war_preparation.find():
            print("Couldn't find war preparation")
            goto(main)
            return 0
    time.sleep(2)

    for x in range(5):
        found = click_war_castle()
        if found: break
        time.sleep(1)

    if not found:
        print("Couldn't find castle - war donation ad hoc")
        goto(main)
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
    pag.press("esc")
    return remaining
