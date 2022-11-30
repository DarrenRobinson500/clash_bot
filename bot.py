import datetime

# from donate import *
from build import *
# from account import *
from war import *
from research import *
# from lose_trophies import *
# from attacks_logic import *
from games import *

method = cv2.TM_CCOEFF_NORMED



# ============
# === COIN ===
# ============

def capital_coin():
    goto(main)
    hold_key('s', 0.5)
    hold_key('a', 0.5)
    time.sleep(1)
    val, loc, rect = find_cv2("capital_coin", FORGE_PATH_SPOT)
    print("Coin available:", val)
    if val > 0.7:
        goto(forge)
        return i_collect_capital_coin.click()
    return False

# =============
# === CLOCK ===
# =============

def clock():
    goto(builder)
    val, loc, rect = find_cv2('clock')
    print(val)
    if val > 0.65:
        print("Clock found")
        click_cv2('clock')
        click_cv2('free_boost')
        click_cv2('boost')
        return True
    return False

# ====================
# === 6. RESOURCES ===
# ====================

def get_resources():
    for x in resource_templates:
        x.click()

def war_get_status_image():
    goto(main)
    time.sleep(0.1)
    if i_war.find(fast=False):
        i_war.click()
    elif i_war_cwl.find(fast=False):
        i_war_cwl.click()
    else:
        print("War - get status image failure")
        return
    time.sleep(2)
    get_screenshot(WAR_BANNER, filename=f"tracker/war_banner")
    print("Saved war banner")

    i_return_home_2.click()

def get_trader_info(account):
    goto(main)
    time.sleep(0.1)
    hold_key("a", 0.5)
    hold_key("w", 0.5)
    if i_trader.click():
        i_raid_medals.click()
        pag.moveTo(1000,900)
        pag.dragTo(1000,280, .2)
        time.sleep(0.3)
        get_screenshot(CLOCK_POTION, filename=f"tracker/trader_clock_potion{account.number}")
        get_screenshot(RESEARCH_POTION, filename=f"tracker/trader_research_potion{account.number}")
        pag.press("space")

def sweep(fast=False):
    start_time = datetime.now()
    for account in accounts:
        if fast:
            change_accounts_fast(account)
        else:
            change_accounts(account.number)
        if account.number == 1:
            war_get_status_image()
            i_return_home_3.click()
        get_resources()
        get_trader_info(account)
        if account.th > 5:
            if not fast: donate(account)
        if not fast:
            account.update_resources(current_resources())
            check_completion(account)
        if account.building and not fast:
            build(account, "main")
        # check_trophies(account)
        account.next_update()
        clock()
        get_resources()
        if account.building_b and not fast:
            build(account, "builder")
        if account.th > 5 and not fast:
            attack_b(account)
            goto(builder)
            time.sleep(0.1)
        get_screenshot(REMAINING_ATTACKS, filename=f"tracker/remaining_attacks{account.number}")
        goto(main)
        if account.th > 5:
            capital_coin()
        print("Timer:", account, datetime.now() - start_time)
    create_combined_builders_image(accounts)
    war_status()

# === DATABASE ===
def db(db_str):
    con = sqlite3.connect('data.db')
    c = con.cursor()
    # print(db_str)
    c.execute(db_str)
    output = c.fetchall()
    con.commit()
    con.close()
    return output

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

def db_next_job_old():
    db_str = "SELECT * FROM jobs ORDER BY time"
    return db(db_str)[0]

# ============
# === JOBS ===
# ============

def run_job(job, sweep_period, games=False):
    print()
    print("Job:", job)
    account, job, job_time = job
    account = accounts[account - 1]
    job_time = string_to_time(job_time)
    if time_to_string(job_time) == "Now":
        if job == "sweep":
            next_sweep = datetime.now() + (datetime.min - datetime.now()) % sweep_period
            db_update(account_0, "sweep", next_sweep)
            sweep()
        elif job == "games":
            if not games:
                db_update(account_0, "games", datetime.now() + timedelta(days=27))
                return
            next_games = datetime.now() + timedelta(minutes=10)
            db_update(account_0, "sweep", next_games)
            run_games()
        elif job == "attack":
            if games:
                db_update(account, job, datetime.now() + timedelta(hours=2))
                return
            if account.attacking:
                change_accounts_fast(account)
                print("Run job", account.army_troops)
                attack(account, account.army_troops)
            else:
                db_update(account, job, datetime.now() + timedelta(hours=2))
        elif job == "donate":
            if account.attacking or not account.donating():
                db_update(account, job, datetime.now() + timedelta(days=1))
                return
            change_accounts_fast(account)
            donate(account)
            db_update(account, job, datetime.now() + timedelta(minutes=20))
        elif job == "research":
            if not account.researching:
                db_update(account, job, datetime.now() + timedelta(days=2))
                return
            change_accounts_fast(account)
            goto(main)
            next_research(account)
            account.update_lab_time()
        elif job == "build":
            if account.building:
                change_accounts_fast(account)
                goto(main)
                build(account, "main")
                goto_list_very_top("main")
                time.sleep(0.2)
                result = build_time.read(BUILDER_LIST_TIMES)
                result = text_to_time_2(result)
                account.next_build = result
                db_update(account, "build", result)

        # elif job == "build_b":
        #     change_accounts(account.number, "builder")
        #     build(account, "builder")
        #     db_update(account, job, datetime.now() + timedelta(minutes=20))
        # elif job == "attack_b":
        #     change_accounts(account.number, "builder")
        #     # job_time = get_time_attack_b()
        #     # default = datetime.now() + timedelta(hours=1)
        #     if not job_time:
        #         job_time = default
        #     else:
        #         job_time = max(default, job_time)
        #     db_update(account, job, job_time)
        #     print(f"Updated time for next builder attack for account {account.number}")
        elif job == "coin":
            change_accounts_fast(account)
            pag.click(BOTTOM_LEFT)
            if capital_coin():
                db_update(account, job, datetime.now() + timedelta(hours=23, minutes=2))
            else:
                result = get_time_coin()
                db_update(account, job, result)
        # elif job == "clock":
        #     change_accounts(account.number, "builder")
        #     if clock():
        #         job_time = datetime.now() + timedelta(hours=23)
        #         print(f"Clicked the clock")
        #     else:
        #         print("Clock not found")
        #         job_time = datetime.now() + timedelta(hours=3)
        #     db_update(account, job, job_time)
        #     print(f"Updated time for next clock click for account {account.number}")
        elif job == "lose_trophies":
            change_accounts_fast(account)
            if lose_trophies(account):  minutes = 5
            else:                       minutes = 120
            print(minutes)
            job_time = datetime.now() + timedelta(minutes=minutes)
            print("Run - lose trophies", datetime.now(), timedelta(minutes=minutes), job_time)
            db_update(account, job, job_time)
        else:
            job_time = datetime.now() + timedelta(hours=24)
            db_update(account, job, job_time)
            print(f"Job type '{job}' not coded yet.")
    else:
        rest_time = job_time - datetime.now()
        print("Rest time:", rest_time)
        goto(pycharm)
        print_info()
        if rest_time > timedelta(minutes=5):
            main.perform_action(main.sleep_path)
        else:
            time.sleep(rest_time.seconds)
            reset()
            time.sleep(0.2)

def db_view_next():
    db_str = "SELECT * FROM next ORDER BY account"
    output = db(db_str)
    for account in [1,2,3]:
        for village in ["main", "builder"]:
            building = ["none", "none", "none", "none"]
            time = ""
            for account_r, village_r, currency_r, building_r, cost, comment in output:
                if account == account_r and village == village_r:
                    if currency_r == "elixir1":
                        building[0] = building_r
                        time = string_to_time(comment)
                        time = time_to_string(time)
                    if currency_r == "dark": building[1] = building_r
                    if currency_r == "gold": building[2] = building_r
                    if currency_r == "elixir": building[3] = building_r
            spacer = ""
            if village == "main": spacer = "   "
            print(f"Account {account} ({village}) {spacer} {building} {time}")

def print_info():
    # print_locs()
    # print_total_donations()
    # print()
    for account in accounts:
        account.print_info()
    print()
    db_view(no=1)
    db_view_builds(no=5)
    # print()

def print_info_old():
    db_view()
    update_info()
    for key in info:
        if key == "gold":
            text = ""
            resources_all = info[key]
            text += '['
            for resources in resources_all:
                if resources:
                    text += "["
                    text += str(round(resources[0] / 1000000, 1)) + "m, "
                    text += str(round(resources[1] / 1000000, 1)) + "m, "
                    text += str(round(resources[2] / 1000, 0)) + "k, "
                    text += "], "
                else:
                    text += "Unknown, "
            text += '], '
            print("resources:", text)
    db_view_next()

def update_info():
    for var in ["build", "build_b", "clock", "coin", "lose_trophies"]:
        results = db_get(var, 5)
        for result in results:
            if result:
                account, job, time = result
                info[var][account-1] = time_to_string(string_to_time(time))

def get_times(accounts):
    print("Get times")
    for account in accounts:
        change_accounts(account.number)
        db_update(account, "build", get_time_build(account, "main"))
        db_update(account, "attack", get_time_attack())
        db_update(account, "build_b", get_time_build(account, "village"))
        # db_update(account, "attack_b", get_time_attack_b())
        db_update(account, "coin", get_time_coin())

# def get_time_attack_b():
#     print("Get time attack - builder")
#     goto(builder)
#     click_cv2("attack_b")
#     if find_cv2("builder_attack_wins")[0] > 0.7:
#         print("Ready for attack")
#         result = datetime.now()
#         pag.click(BOTTOM_LEFT)
#         return result
#     result = read_text(ARMY_TIME_B, WHITE)
#     result = alpha_to_numbers(result)
#     result = text_to_time(result)
#     pag.click(BOTTOM_LEFT)
#     return result

def update_time_build(account, village):
    db_str = f"SELECT * FROM next WHERE account = '{account.number}' and village = '{village}' and currency = 'elixir1'"
    account_r, village_r, currency_r, building_r, cost, comment = db(db_str)[0]
    print("Get time build: ", account_r, village_r, currency_r, building_r, cost, comment)
    time_temp = string_to_time(comment)
    if time_temp > datetime.now(): return time_temp
    result = get_time_build(village)
    # db_update_comment(account, village, 'elixir1', result)

def get_time_build(village):
    if village == "main": goto(main)
    else: goto(builder)
    goto_list_very_top(village)
    time.sleep(0.2)
    if village == "main": region = BUILDER_LIST_TIMES
    else: region = BUILDER_LIST_TIMES_B
    # pag.screenshot('temp/build_time.png', region=region)
    # i = cv2.imread(f"temp/build_time.png", 0)
    result = build_time.read(region)
    # result = read_build_time(i)
    result = text_to_time_2(result)
    # print(result)
    return result

    # result = read_text(BUILDER_LIST_TIMES, WHITE)
    # try:
    #     result = alpha_to_numbers(result)
    #     result = text_to_time(result)
    # except:
    #     print("Failed to read screenshot")
    #     print(result)
    #     result = datetime.now() + timedelta(minutes=5)
    # db_update(current_account, "build", result)
    # time.sleep(0.2)
    #
    # click_cv2("builder", BUILDER_REGION, 0.5)
    # print("Final:", result)
    # return result

def get_time_build_b():
    print("Get build time - Builder Base")
    goto(builder)
    click_builder()
    time.sleep(0.2)
    result = read_text(BUILDER_LIST_TIMES_B, WHITE)
    print("Raw:", result)
    try:
        result = alpha_to_numbers(result)
        result = text_to_time(result)
        print("after text_to_time:", result)
    except:
        print("Failed to read screenshot")
        print(result)
        time.sleep(0.2)
    click_builder()
    print("Builder build time:", result)
    return result

def get_time_coin():
    print("Get time to next coin")
    goto(forge)
    time.sleep(0.2)
    result = coin_time.read(CAPITAL_COIN_TIME, show_image=False)
    result = text_to_time_2(result) + timedelta(minutes=2)
    print("Coin time:", result)
    return result


# def current_resources():
#     time.sleep(.1)
#     result = []
#
#     for region in [RESOURCES_G, RESOURCES_E, RESOURCES_D]:
#         result_ind = resource_numbers.read(region)
#         try:
#             result.append(int(result_ind))
#         except:
#             result.append(0)

    # for name, region in [(gold, RESOURCES_G), (elixir, RESOURCES_E), (dark, RESOURCES_D)]:
    #     pag.screenshot(f'temp/current_{name}.png', region=region)
    #     i = cv2.imread(f"temp/current_{name}.png", 0)
    #     result_ind = read_resources(i)
    #     try:
    #         result_ind = int(result_ind)
    #     except:
    #         result_ind = 0

    # print("Available Resources:", result)
    #
    # return result


# def current_resources_old():
#     time.sleep(.1)
#     result = []
#
#     for name, region in [(gold, RESOURCES_G), (elixir, RESOURCES_E), (dark, RESOURCES_D)]:
#         pag.screenshot(f'temp/current_{name}.png', region=region)
#         i = cv2.imread(f"temp/current_{name}.png", 0)
#         result_ind = read_resources(i)
#         try:
#             result_ind = int(result_ind)
#         except:
#             result_ind = 0
#         result.append(result_ind)
#
#     print("Available Resources:", result)
#
#
#     return result

# clock()