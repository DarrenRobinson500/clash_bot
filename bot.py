# import pyautogui as pag
# import cv2
# import time
import datetime
import os
import psutil
from PIL import Image
from collections import Counter
import sqlite3
from attacks import *
from clicks_old import wait_and_click
from ocr import *
from nav import *


method = cv2.TM_CCOEFF_NORMED

# === RESET ===
def reset():
    if "BlueStacksWeb.exe" in (p.name() for p in psutil.process_iter()):
        print("Bluestacks Running")
        click_cv2('bluestacks_icon')
        goto("main")
    else:
        os.startfile("C:\Program Files (x86)\BlueStacks X\BlueStacks X.exe")
        wait_cv2('start_d')
        pag.click((338,603)) # this is the love heart
        wait_and_click('start_eyes')
        wait_and_click('maximise')
        wait_cv2("attack")



# === 2. REQUEST ===
def request(account):
    # if account == 1: return
    print("Request")
    goto("army_tab")
    val, loc, rect = find_cv2('request')
    print("Request: 'request' val", val)
    if val > 0.7:
        if check_colour('request'):
            click_cv2('request')
            time.sleep(1)
            val, loc, rect = find_cv2('request_send')
            if val > 0.7:
                click_cv2('request_send')
            else:
                print("Request - couldn't find request button")
        else:
            print("Request - Check colour failed")
    else:
        print("Request - couldnt find request", val)

    job_time = datetime.now()
    if account == 2 or account == 3:
        db_update(1, "donate", job_time)
    if account == 1:
        db_update(2, "donate", job_time)

# === 3. ATTACK ===
def attack_b(account):
    troops = TROOPS_B[account]
    goto("builder")
    click_cv2("attack_b")
    if find_cv2("builder_attack_wins")[0] < 0.7:
        print("Attack b - Not ready for attack")
        return
    print("Attack b - Ready for attack")
    attack_b_get_screen()
    loc_th = th_b()
    loc_th = check_loc_th(loc_th)
    if loc_th is None:
        time.sleep(60)
        goto("main")
        return
    a, b = objects_b(loc_th)
    for troop, n, loop in troops:
        result = place_b(troop, a, b, n, loop)
        if result == "No spots":
            print("Attack b - no spots")
            break
    troops_left = True
    count = 0
    while troops_left and count <= 5 and result != "No spots":
        troops_left = check_all_troops_used(a, b)
        count += 1
        print(count)
    wait_cv2("attack_b/okay")
    goto("builder")
    return

def check_all_troops_used(a, b):
    print("Check all troops used")
    troops_left = False
    for x in ATTACK_B_TROOPS:
        rects = find_many("attack_b/" + x, confidence=0.7)
        print(rects)
        for rect in rects:
            small_rect = [rect[0] + 10, rect[1] + 10, rect[2] - 20, rect[3] - 20]
            result = check_colour_rect(small_rect)
            print(x, result)
            if result:
                troops_left = True
                place_b(x, a, b, 5, 1)
    return troops_left

def place_b(troop, a, b, n, loops=1):
    print("Place B")
    click_cv2("attack_b/" + troop)
    spots = get_spots(a,b,n)
    if spots is None:
        return "No spots"
    print(troop, a, b)
    print(spots)
    for _ in range(loops):
        for spot in spots:
            print("Place b:", spot)
            pag.click(spot)
        time.sleep(0.5)

def attack(account, data=GIANT200):
    print("Attack Start")
    goto("main")
    db_update(account, "attack", datetime.now() + timedelta(minutes=5))

    # Attack Prep
    result = attack_prep(account, data)
    if not result:
        print("attack: Troops not ready")
        db_update(account, "attack", get_time_attack())
        return

    # Find a match
    print("Attack")
    goto("find_a_match")
    match_found = False
    while not match_found:
        assessment = assess_village(account, data)
        print(assessment)
        if assessment == "Good to go":
            match_found = True
        elif assessment == "Not on attack screen":
            return
        else:
            result = next_village()
            if result == "Not on attack screen":
                return
            current = data['resource_objective']
            data['resource_objective'] = [int(current[0] * 0.98), int(current[1] * 0.98),int(current[2] * 0.98),]
            print("New gold objective:", data['resource_objective'])

    # Launch attack
    if data['drop_points']:
        launch_attack_dps(account, data)
    else:
        launch_attack(account, data)

    # Finish attack
    finish_attack(account, data)
    attack_prep(account, data)
    request(account)

    time.sleep(.2)
    return

def attack_prep(account, data):
    print("Attack prep")
    # Checking if training
    goto("army_tab")
    result, loc, rect = find_cv2("army_clock", ARMY_CLOCK_SPOT)
    if result > 0.6:
        print("Army prep - still training")
        return False

    # Get required troops
    sufficient_troops = True
    troops_required = []
    troops_to_build = []
    for x in data['initial_troops']:
        troops_required.append(x)
    for x, no in data['troop_group']:
        for y in range(data['troop_groups'] * no):
            troops_required.append(x)
    for x in data['final_troops']:
        troops_required.append(x)
    requ = Counter(troops_required)
    time.sleep(0.2)
    print("A", datetime.now())
    goto("army_tab")

    # Lightening spells
    print("Lightening spells")
    print("B", datetime.now())
    actual = troop_count("lightening")
    required = data['lightening']
    print("C", datetime.now())
    print("Attack prep - create required", "lightening", required, actual)
    if actual < required:
        text = f"Need more of these - make {required - actual} more"
        print("lightening", required, actual, text)
        troops_to_build += ["lightening"] * (required - actual)
        # troop_create("lightening", required - actual)
        # time.sleep(0.2)
        print("D", datetime.now())

    backlog_deleted = False
    # Delete unneeded troops
    print("Delete unneeded troops")
    print("E", datetime.now())

    for x in TROOPS:
        print("F", x, datetime.now())
        actual = troop_count(x)
        required = requ[x]
        print("Attack prep - delete unneeded", x, required, actual)
        if actual > required:
            text = f"Too many of these - get rid of {actual - required}"
            print(x, required, actual, text)
            if not backlog_deleted:
                troop_delete_backlog()
                backlog_deleted = True
            troop_delete(x, actual - required)

    # Create needed troops
    goto("army_tab")
    print("Create required troops")
    for x in requ:
        if x not in HEROES_AND_RAMS:
            print("Troop:", x)
            actual = troop_count(x)
            required = requ[x]
            if actual == required:
                text = "Perfect"
                print(x, required, actual, text)
            if actual < required:
                sufficient_troops = False
                text = f"Need more of these - make {required - actual} more"
                print(x, required, actual, text)
                if not backlog_deleted:
                    troop_delete_backlog()
                    backlog_deleted = True
                # troop_create(x, required - actual)
                troops_to_build += [x] * (required - actual)
    if account == 1:
        troops_to_build += ["ram", "ram"]
    restock(troops_to_build)
    return sufficient_troops

def troop_delete_backlog():
    print("Troop delete backlog")
    goto("troops_tab")
    remaining_troops = True
    while remaining_troops:
        val, loc, rect = find_cv2("remove_troops", DELETE_REGION)
        center = pag.center(rect)
        if val > 0.65:
            for x in range(5): pag.click(center)
        else:
            print("Troop delete backlog:", val)
            remaining_troops = False

def troop_delete(troop, count):
    print("Troop delete")
    goto("army_tab")
    click_cv2("edit_army")
    val, loc, rect = find_cv2(troop, ARMY_EXISTING)
    spot = pag.center(rect)
    for x in range(count):
        pag.click(spot)
    click_cv2("edit_army_okay")
    click_cv2("surrender_okay")

def restock(required_troops):
    print("Restock")
    print(required_troops)
    count = Counter(required_troops)
    extra = count.most_common()
    print("Extra:", extra)

    for x in count:
        if x in TROOPS:
            goto("troops_tab")
            add_troops(x, count[x])

    for x in count:
        if x in SPELLS:
            goto("spells_tab")
            add_troops(x, count[x])

    for x in count:
        if x in SIEGE:
            goto("siege_tab")
            add_troops(x, count[x])

    if len(extra) > 0 and extra[0][0] in TROOPS:
        troop = extra[0][0]
        number = extra[0][1]
        goto("troops_tab")
        add_troops(troop, number)

def add_troops(name, count):
    if name in TROOP_TRAIN_EXT: name += "_train"
    if name in SIEGE: name += "_big"
    val, loc, rect = find_cv2(name, ARMY_CREATE)
    print("Add troops", val)
    print(name, val)
    if name == "super_barb_train" and val < 0.6:
        get_super_barbs()
    center = pag.center(rect)
    for x in range(count):
        pag.click(center)
        time.sleep(0.05)

def get_super_barbs():
    goto("main")
    hold_key("a", 0.5)
    hold_key("w", 0.5)
    sequence = ["super_boost", "super_boost_barb", "super_boost_potion", "super_boost_dark", "super_boost_potion_small", "super_boost_dark2", ]
    for image in sequence:
        time.sleep(0.5)
        val, loc, rect = find_cv2(image)
        print(image, val)
        if val > 0.6:
            print("Click")
            click_rect(rect)
    pag.press("esc")

def troop_create(troop, count):
    print("Troop create: ", troop)
    if troop in SPELLS:
        goto("spells_tab")
    else:
        goto("troops_tab")

    name = troop
    if name in TROOP_TRAIN_EXT: name += "_train"
    val, loc, rect = find_cv2(name, ARMY_CREATE)
    center = pag.center(rect)
    for x in range(count):
        pag.click(center)
        time.sleep(0.05)

def troop_count(troop):
    # goto("army_tab")
    time.sleep(.2)
    if troop in TROOPS:
        region = ARMY_EXISTING
    else:
        region = SPELLS_EXISTING

    val, loc, rect = find_cv2(troop, region)
    print("Troop count - identifying troop", troop, val)
    if val < 0.60: return 0
    region = (loc[0] - 30, loc[1] - 70, 130, 80)
    result = read_troop_count(region)
    try:
        result = int(result)
        if result > 150: result = int(result / 10)
        return result
    except:
        return 0

def check_towers(towers, img):
    found = False
    for tower in towers:
        val, loc, rect = find_cv2_image(tower, img)
        print("Check towers - val", val)
        if val > 0.65:
            found = True
            cv2.rectangle(img, rect, (0,255,255), 2)
    return found
    return found, img

def assess_village(account, data):
    start_time = datetime.now()
    global DP
    print("Assess village")
    time.sleep(0.5)
    # zoom_out()

    # Check if its returned to main (due to a reload)
    print("A", datetime.now() - start_time)
    if not wait_cv2("end_battle", END_ATTACK_SPOT):
        print("Not on attack screen")
        return "Not on attack screen"

    # Screenshot
    print("B", datetime.now() - start_time)
    # post = datetime.now().strftime('%I%M%p')
    # x = f'attacks{account}/attack {post}.png'
    # pag.screenshot(x)
    # pag.screenshot("attacks/attack.png")

    # Resource Check
    print("C", datetime.now() - start_time)
    # if not wait_cv2("coin"): return "Not on attack screen"
    # gold_adj = 0
    # if data['th_gold_adj']:
    #     gold_adj = max((data['max_th'] - th) * 100000,0)
    resources = available_resources()
    required = data['resource_objective']
    print("Assess village: A")
    print(resources, required)
    if resources[0] < required[0] or resources[1] < required[1] or resources[2] < required[2]:
        print("Assess village:", resources, required)
        print("C2", datetime.now() - start_time)
        return "Insufficient gold"

    # Advanced Town Hall
    print("D", datetime.now() - start_time)
    print("Assess village: B")
    img = create_double_screen(account)

    # pag.screenshot("attacks/attack.png")
    th, loc = town_hall(img)
    if th > data['max_th']:
        return "Town hall too high"

    # Aggressive defences
    print("E", datetime.now() - start_time)
    print("Assess village: C")
    if not wait_cv2("coin"): return "Not on attack screen"
    if check_towers(data['towers_to_avoid'], img): return  "Aggressive defence"

    # Barb drop spot
    print("F", datetime.now() - start_time)
    print("Assess village: D")
    if data['name'] == "barbs":
        DP = ram_drop_point(account, img)
        if DP is None:
            DP = STANDARD_DP2
            # print("Assess village - couldn't identify drop spot")
            # return "Couldn't identify drop spot"

    # Goblin mines
    print("G", datetime.now() - start_time)
    if data['name'] == "goblins":
        mines = find_many_array(MINES)
        if len(mines) == 0:
            return "No identified mines"

    print("H", datetime.now() - start_time)
    return "Good to go"

def next_village():
    print("Next attack")
    time.sleep(0.25)
    if find_cv2("next_attack")[0] > 0.7:
        wait_and_click('next_attack')
        time.sleep(0.1)
        wait_and_click('next_attack')
    else:
        goto("find_a_match")
    if not wait_cv2("end_battle"): return "Not on attack screen"

def launch_attack_dps(account, data):
    print("Launch attack dps")
    pag.click(1000, 1000)
    pag.drag(0, -400, 0.25, button='left')

    mines = find_many_array(MINES)
    town = cv2.imread('temp.png', 0)
    print(data)
    for m in mines:
        dp = drop_point(m, town)
        for troop in data["drop_point_troops"]:
            place(troop, 1, dp)
    time.sleep(10)
    click_cv2("surrender")
    click_cv2("surrender_okay")

def drop_point(r, image):
    range_y = 70
    range_x = int(range_y * 4/3)
    x, y, w, h = r
    center_x = x + w//2
    center_y = y + w//2
    town_center_h, town_center_w = image.shape
    town_center_x = town_center_w // 2
    town_center_y = town_center_h // 2
    if center_x > town_center_x:
        dp_x = center_x + range_x
    else:
        dp_x = center_x - range_x
    if center_y > town_center_y:
        dp_y = center_y + range_y
    else:
        dp_y = center_y - range_y
    dp = (dp_x, dp_y)
    image = cv2.circle(image, dp, 3, (255,255,255), 3)
    # show(image)
    return dp

def launch_attack(account, data):
    standard_pace = True

    if data['name'] == 'barbs':
        if DP is None: return
        dp = DP
        if DP[1] > 700:
            print(DP)
            for _ in range(2): pag.scroll(-300)
            print("Drop point A", dp)
            # if scroll_adj:
            #     dp[1] += -scroll_adj - 100
            # else:
            dp[1] -= 350
            print("Drop point B", dp)
    else:
        dp = STANDARD_DP

    print("Launch attack: bombing")
    if data['bomb']: bomb(data['bomb_target'])
    if data['bomb_target2'] is not None: bomb(data['bomb_target2'])
    troop_pause = data['troop_pause']

    print("Launch attack: initial troops")
    for x in data['initial_troops']:
        place(x, 1, dp)

    print("Launch attack: main troops")
    for x in range(data['troop_groups']):
        for troop, n in data['troop_group']:
            place(troop, n, dp, troop_pause=troop_pause)
        damage = read_text(DAMAGE, WHITE,True)
        try:
            if int(damage) > 60:
                standard_pace = False
        except:
            pass
        print("launch_attack Damage:", damage)
        if standard_pace: time.sleep(3)
    if standard_pace: time.sleep(10)

    print("Launch attack: final troops")
    for x in data['final_troops']:
        place(x, 1, dp)
    wait_cv2("return_home")

def place(troop, count_total, dp=[400,400], troop_pause=0):
    if troop in TROOP_ATTACK_EXT: troop = troop + "_attack"
    dp1 = (dp[0],min(dp[1],815))
    val, loc, rect = find_cv2(troop, TROOP_ZONE)
    print("Place troops:", troop, val, loc)
    if val > 0.63:
        click_cv2(troop, TROOP_ZONE)
        time.sleep(.2)
        count = 0
        pause_dur = 0.2
        while count < count_total:
            pag.click(dp1)
            time.sleep(troop_pause)
            time.sleep(pause_dur)
            prop_troops = int(count / count_total * 100)
            damage = read_text(DAMAGE, WHITE, True)
            if damage > 100: damage = 0
            # print("Place:", prop_troops, damage)
            if damage + 30 > prop_troops and damage > 30:
                pause_dur += 0.1
                pause_dur = min (1.5, pause_dur)
            if damage + 20 > prop_troops and damage > 50:
                reduction = int((1 - prop_troops/damage) * count_total)
                count += reduction
                count += reduction
                print("Reduction:", reduction)
            count += 1

def has_spells():
    print("Has spells")
    lightening_buttons = find_many("lightening", TROOP_ZONE, 0.5)
    for x in lightening_buttons:
        if check_colour_rect(x):
            print("Has spells - True")
            return True, x
    print("Has spells - False")
    return False, None

def bomb_mult(coords, count):

    for x in range(count):
        pag.click(pag.center(coords))

def bomb(targets):
    spells, loc = has_spells()
    click_cv2("lightening", TROOP_ZONE, 0.50)
    print("Bomb (initial):", spells)
    count = 0
    for x in targets:
        if count < 4:
            val, loc, rect = find_cv2(x)
            if val > 0.65 and loc[1] < 728 and  300 < loc[1] < 1500:
                print("Bomb - Found target")
                hits = 3
                if targets == EAGLE:    hits = 6
                if targets == INFERNOS: hits = 5
                enlarged_rect = [rect[0] - 2, rect[1] - 2, rect[2] + 4, rect[3] + 4]
                bomb_mult(rect, hits)
                time.sleep(1.5)
                for _ in range(2):
                    time.sleep(0.5)
                    val, loc, rect  = find_cv2(x, enlarged_rect)
                    if val > 0.7:
                        print("Bomb - One more")
                        bomb_mult(rect, 1)
                count += 1
            else:
                print(f"Did not find {x}. Val:", val)
        spells, loc = has_spells()
        print("Bomb (loop):", x, spells)
    return

def finish_attack(account, data):
    global current_location
    wait_cv2("return_home",max_time=80)
    current_location = "return_home"
    goto("main")
    resources = current_resources()
    info['gold'][account-1] = resources
    log("gold", account, resources[0])

def log(var, account, no):
    time = datetime.now().strftime('%d %b %I:%M%p')
    no = f"{no:,}"
    line = f"{time}: Account: {account}. {var.title()}: {no}"
    with open(f"log{account}.txt", 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def max2(list):
    try:
        return max(list)
    except:
        return 0

def calc_score_sub(defences):
    wizard = [item[1] for item in defences if item[0] == "Wizard"]
    inferno = [item[1] for item in defences if item[0] == "Inferno"]
    cross = [item[1] for item in defences if item[0] == "Cross"]
    eagle = [item[1] for item in defences if item[0] == "Eagle"]
    th = [item[1] for item in defences if item[0] == "TH"]
    result = max2(wizard) + max2(inferno) + max2(cross) + max2(eagle) + max2(th)
    print("TH:", max2(th), "Result", result)
    return result

def calc_score(img):
    img_orig = img.copy()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    defences = []
    for name, templates, score, type in TOWERS:
        rects = find_many_img(templates, img, 0.63)
        for x in rects: cv2.rectangle(img_orig, x, (255,255,255), 1)
        if len(rects) > 0:
            defences.append((type, score))
    result = calc_score_sub(defences)
    print("Calc score:", result)
    return result

# =================
# === 4. DONATE ===
# =================

def donate():
    print("Donate")
    goto("chat")
    requests = find_many("donate", confidence=0.8)
    print("Donate - donation:", requests)
    donations = []
    for x in requests:
        click_rect(x)
        for x in ALL_TROOPS:
            print("Donate:", x)
            if x not in DONT_DONATE:
                name = x
                if name in TROOP_DONATE_EXT: name += "_donate"
                val, loc, rect = find_cv2(name, DONATE_AREA)
                while val > 0.65 and check_colour_rect(rect):
                    click_cv2(name, DONATE_AREA)
                    donations.append(x)
                    time.sleep(0.1)
                    val, loc, rect = find_cv2(name, DONATE_AREA)
        if find_cv2("donate_cross")[0] > 0.5:
            click_cv2("donate_cross")
    time.sleep(0.1)
    if len(donations) > 0:
        restock(donations)

# =============
# === Build ===
# =============
def spare_builders(village):
    region = BUILDER_ZERO_REGION
    if village == "builder": region = BUILDER_B_ZERO_REGION
    val, loc, rect = find_cv2("builder_zero", region)
    if val > 0.8: return 0
    val, loc, rect = find_cv2("builder_one", region)
    if val > 0.8: return 1
    return 2


def build(account, village):
    goto(village)
    builders = spare_builders(village)
    if builders == 0: return
    remove_trees(village)
    if builders == 1 and village == "main" and account in ACCOUNT_NEEDS_WALLS:
        result = get_time_build(account, "main")
        if result is None: return
        time_remaining = result - datetime.now()
        print("Build - time remaining until 2 builders:", time_remaining)
        start_saving = time_remaining < timedelta(hours=48)
        print("Build - start saving", start_saving)
        if not start_saving:
            print("Building walls")
            build_sub("main", "wall")
            return

    for currency in CURRENCIES:
        if spare_builders(village) == 0: return
        result = db(f"SELECT * FROM next WHERE account='{account}' and village='{village}' and currency = '{currency}'")[0]
        account, village, currency, building, cost, comment = result
        preference = building
        print("Build - preference:", preference)
        if preference != "none" and preference != "complete":
            result = build_sub(village, preference)
            print("Build", result)
            if result:
            # if preference != "wall" and result:
                print("Build - updating db_next")
                db_update_next(account, village, currency, "none", 0)
                next_build(account, village)
                update_time_build(account, village)

def next_build(account, village):
    condition = f" WHERE account='{account}' and village='{village}'"
    result = db(f"SELECT * FROM next" + condition)
    need_update = False
    for current_account, current_village, current_currency, current_building, current_cost, comment in result:
        if current_building == "none": need_update = True

    if need_update:
        preferences = get_build_preference(village)
        # cost = build_cost(village, building)[1]
        db_update_next(account, village, "elixir1", preferences[0])
        db_update_next(account, village, "dark", preferences[1])
        db_update_next(account, village, "gold", preferences[2])
        db_update_next(account, village, "elixir", preferences[3])
        # account, village, currency, building, cost, comment

def db_update_next(account, village, currency, building, cost=0, comment=""):
    # account, village, currency, building, cost, comment

    condition = f" WHERE account='{account}' and village='{village}' and currency='{currency}'"
    db_str = f"SELECT * FROM next" + condition
    existing = len(db(db_str))
    if existing == 1:
        db(f"UPDATE next SET building='{building}'" + condition)
        db(f"UPDATE next SET cost='{cost}'" + condition)
        db(f"UPDATE next SET comment='{comment}'" + condition)
    else:
        print("Records not updated - didn't find exactly 1 record to update")

def db_update_comment(account, village, currency, comment):
    # account, village, currency, building, cost, comment

    condition = f" WHERE account='{account}' and village='{village}' and currency='{currency}'"
    db_str = f"SELECT * FROM next" + condition
    existing = len(db(db_str))
    if existing == 1:
        db(f"UPDATE next SET comment='{comment}'" + condition)
    else:
        print("Records not updated - didn't find exactly 1 record to update")


def move_list(direction):
    dur = 0.5
    if direction == "up":
        pag.moveTo(855,666, dur)
        pag.dragTo(855,210, dur)
    if direction == "down":
        pag.moveTo(855,210, dur)
        pag.dragTo(855,666, dur)

def has_cash(region):
    pag.screenshot('temp/upgrade_colour.png', region=region)
    image = cv2.imread('temp/upgrade_colour.png', 1)
    new, counter = simplify(image, gradients=2)
    print(region)
    print(counter)
    print(counter[(0, 128, 128)])
    if counter[(128,128,0)] > 4000: return False  # This is the wall rings
    return counter[(0, 128, 128)] < 700

def upgrade():
    if wait_cv2("upgrade") == False:
        print("Upgrade: couldn't find upgrade button")
        return False
    rects = find_many("upgrade", confidence=0.8)
    sufficient_funds = False
    print("Upgrade - upgrade buttons found:", len(rects))
    for rect in rects:
        region = (rect[0] - 20, rect[1] - 120, 180, 50)
        result = has_cash(region)
        print("Upgrade:", result)
        if result:
            sufficient_funds = True
            click_rect(rect)
    if not sufficient_funds:
        print("Upgrade - inadequate funds")
        return False

    val, loc, rect = find_cv2("upgrade_hero")
    val2, loc2, rect2 = find_cv2("upgrade_hero2")
    print("Upgrade - hero upgrade val", val, val2)
    if val > 0.8:
        print("Upgrade: hero")
        click_cv2("upgrade_hero")
    if val2 > 0.8:
        print("Upgrade: hero2")
        click_cv2("upgrade_hero2")
    else:
        print("Upgrade: non-hero")
    pag.click((933, 877))

    click_cv2("red_cross")
    return True

def goto_list_top(village):
    pag.click(BOTTOM_LEFT)
    click_builder(village)
    if village == "main": region = BUILDER_LIST_REGION
    else: region = BUILDER_B_LIST_REGION
    at_top = False
    count = 0
    while not at_top and count < 6:
        val, loc, rect = find_cv2("suggested_upgrades", region)
        # print("Suggested upgrade:", val)
        if val > 0.8:
            at_top = True
        else:
            move_list("down")
        count += 1

def get_available_upgrades(village):
    print("Get available upgrades")
    # goto("builder")
    goto_list_top(village)
    count = 0
    available_upgrades = []
    if village == "main":
        preferences = build_preferences_e1 + build_preferences_d + build_preferences_g + build_preferences_e
        region = BUILDER_LIST_REGION
        directory = "builder/"
        max_count = 4
    elif village == "builder":
        preferences = build_b_preferences_e + build_b_preferences_g
        region = BUILDER_B_LIST_REGION
        directory = "builder_b/"
        max_count = 3
    else:
        print("Get available upgrades - incorrect village specification")
        return
    while count < max_count:
        for item in preferences:
            val, loc, rect = find_cv2(directory + item, region)
            val_upgrade, loc_upgrade, rect_upgrade = find_cv2("suggested_upgrades", region)
            # print(f"Get available upgrades: ({count})", item, val)
            # print(val, val_upgrade, rect[1], rect_upgrade[1])
            # print(val > 0.75 and not (val_upgrade > 0.75 and rect[1] < rect_upgrade[1]))
            if val > 0.80 and not (val_upgrade > 0.80 and rect[1] < rect_upgrade[1]) and item not in available_upgrades:
                # print("Get available upgrades:", item, "added")
                available_upgrades.append(item)
        move_list("up")
        count += 1
    print("Available options:", available_upgrades)
    return available_upgrades

def build_available(village, build_type):
    try:
        resource_type, cost = build_cost(village, build_type)
    except:
        return False
    if village == "main":
        resources = current_resources()
    elif village == "builder":
        goto("builder")
        resources = current_resources_b()
    else:
        return

    resource = 0
    if resource_type == "Gold": resource = resources[0]
    if resource_type == "Elixir": resource = resources[1]
    if resource_type == "Dark" and village == "main": resource = resources[2]
    print("Build available: cost, resource", cost, resource)
    return cost < resource

def get_build_preference(village):
    options = get_available_upgrades(village)
    preferences = ["complete","complete","complete","complete"]
    if village == "main":
        loops = [(0, build_preferences_e1), (1, build_preferences_d), (2, build_preferences_g), (3, build_preferences_e)]
    else:
        loops = [(0, build_b_preferences_e1), (2, build_b_preferences_g), (3, build_b_preferences_e)]

    print(loops)
    for loop_index, loop_list in loops:
        for x in loop_list:
            if x in options:
                preferences[loop_index] = x
                break

    print(f"Get build preferences: Options {options}, Preferences {preferences}")
    return preferences

def build_sub(village, item):
    if village == "main":
        region = BUILDER_LIST_REGION
        directory = "builder/"
        max_count = 4
    elif village == "builder":
        region = BUILDER_B_LIST_REGION
        directory = "builder_b/"
        max_count = 3
    else:
        print("Build sub - incorrect village specification")
        return

    goto_list_top(village)
    count = 0
    while count < max_count:
        val, loc, rect = find_cv2(directory + item, region)
        val_upgrade, loc_upgrade, rect_upgrade = find_cv2("suggested_upgrades", region)
        print("Build sub:", item, val)
        # print(val, val_upgrade, rect[0], rect_upgrade[0])
        # print(val > 0.75 and not(val_upgrade > 0.75 and rect[1] < rect_upgrade[1]))
        if val > 0.79 and not(val_upgrade > 0.8 and rect[1] < rect_upgrade[1]):
            print("trying to click and then upgrade")
            click_cv2(directory + item, region)
            result = upgrade()
            if result and item == "wall":
                build_sub(village, item)
            return result
        else:
            move_list("up")
            time.sleep(1)
        count += 1

def build_cost(village, item):
    if item is None: return "", 0
    if village == "main":
        region = BUILDER_LIST_REGION
        directory = "builder/"
        max_count = 5
    elif village == "builder":
        region = BUILDER_B_LIST_REGION
        directory = "builder_b/"
        max_count = 3
    else:
        print("Build sub - incorrect village specification")
        return "", 0

    goto_list_top(village)
    count = 0
    while count < max_count:
        val, loc, rect = find_cv2(directory + item, region)
        val_upgrade, loc_upgrade, rect_upgrade = find_cv2("suggested_upgrades", region)
        print("Build cost:", item, val)
        # print(val > 0.75 and not(val_upgrade > 0.75 and rect[1] < rect_upgrade[1]))
        if val > 0.80 and not(val_upgrade > 0.75 and rect[1] < rect_upgrade[1]):
            print("Found item")
            region = (loc[0] + 200, loc[1] - 30, 390, 55)
            print("Build cost - taking screenshot", region)
            pag.screenshot('temp/temp_build_cost.png', region=region)
            screen = cv2.imread('temp/temp_build_cost.png', 0)
            cost = read_cost(screen)
            if len(cost) == 0:
                return ("Read Failure", 0)
            # if item == "wall": show(screen)
            type = "Dark"
            if cost[0] == 'g' or cost[0] == 'h': type = "Gold"
            elif cost[0] == 'e' or cost[0] == 'f': type = "Elixir"
            try:
                if cost[0].isnumeric():
                    cost = int(cost)
                elif cost[1].isnumeric():
                    cost = int(cost[1:])
                else:
                    cost = int(cost[2:])
            except:
                cost = 0
            return (type, cost)
        else:
            move_list("up")
            time.sleep(1)
        count += 1
    return "", 0

def remove_tree(r, village):
    click_rect(r)
    time.sleep(0.1)
    click_cv2("trees/remove_tree")
    time.sleep(2)
    pag.click(BOTTOM_LEFT)
    builders = False
    count = 0
    region = BUILDER_ZERO_REGION
    if village == "builder": region = BUILDER_B_ZERO_REGION
    while not builders and count < 80:
        time.sleep(1)
        val, loc, rect = find_cv2("builder_zero", region)
        print("Remove tree - Builder Available Val", val)
        if val < 0.8: builders = True
        count += 1

def remove_trees(village):
    zoom_out()
    # for letter in ['w', 's']:
    #     hold_key(letter, 0.5)
    rects = find_many_array(BUSHES, confidence=0.80)
    for r in rects:
        remove_tree(r, village)

# ============
# === COIN ===
# ============

def capital_coin():
    goto("forge")
    if find_cv2("collect_capital_coin")[0] > 0.7:
        click_cv2("collect_capital_coin")
        return True
    return False

# =============
# === CLOCK ===
# =============

def clock():
    goto("builder")
    val, loc, rect = find_cv2('clock')
    if val > 0.6:
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
    # rects = find_many_array(RESOURCE_TEMPLATES, confidence=0.8)
    # print("Get resources - count of resources:", len(rects))
    # for rect in rects:
    #     x, y = pag.center(rect)
    #     if not (400 < x < 490 and 260 < y < 370):  # seller on the side of the village
    #         click_rect(rect)

    for x in RESOURCE_TEMPLATES:
        val, loc, rect = find_cv2(x)
        if val > 0.8:
            click_cv2(x)

# ========================
# === 7. LOSE TROPHIES ===
# ========================

def calc_trophies():
    goto("main")
    time.sleep(1)
    result = read_num(TROPHIES, WHITE, 1.00)
    try:
        result = int(result)
    except:
        result = 0
    if result < 20: result = result * 100
    if result < 200: result = result * 10
    return result

def lose_trophies(account):
    max_trophies = MAX_TROPHIES[account]
    current_trophies = calc_trophies()
    info["trophies"][account - 1] = f"{current_trophies}/{max_trophies}"
    print("Lose trophies", account, max_trophies, current_trophies)
    if current_trophies > max_trophies:
        goto("find_a_match")
        hold_key("a", 0.5)
        # zoom_out()
        dp = STANDARD_DP
        place("king", 1, dp)
        place("queen", 1, dp)
        place("warden", 1, dp)
        goto("main")
        return True
    return False

def sweep():
    build_bool = True
    for account in [1,2,3]:
        change_accounts(account)
        get_resources()
        next_build(account, "main")
        if build_bool:
            build(account, "main")
        update_time_build(account, "main")

        donate()
        capital_coin()
        clock()
        get_resources()
        next_build(account, "builder")
        if build_bool:
            build(account, "builder")
        update_time_build(account, "builder")
        if account in [1, 2, 3,]:
            attack_b(account)

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

def db_update(account, job, time):
    db_str = f"SELECT * FROM jobs WHERE account='{account}' and job = '{job}'"
    existing = len(db(db_str))
    print("Current Records: ", existing)
    if existing == 1:
        db_str = f"UPDATE jobs SET time='{time}' WHERE account = {account} AND job = '{job}'"
        db(db_str)
    else:
        print("Records not updated")

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

def db_get(job='all', no=5):
    if job == 'all':
        db_str = "SELECT * FROM jobs ORDER BY time"
    else:
        db_str = f"SELECT * FROM jobs WHERE job='{job}' ORDER BY time"
    output = db(db_str)
    return output

def db_read(account, job):
    db_str = f"SELECT * FROM jobs WHERE account='{account}' AND job = '{job}' ORDER BY time"
    x = db(db_str)
    if len(x) == 1 and x[0][2] is not None and x[0][2] != "None":
        time = datetime.fromisoformat(x[0][2])
    else:
        time = None
    # print(time)
    # print(time.astimezone().isoformat())
    return time


# ============
# === JOBS ===
# ============

def run_job(job, attacking, building):
    print("Job:", job)
    account, job, job_time = job
    job_time = string_to_time(job_time)
    if time_to_string(job_time) == "Now":
        if job == "sweep":
            next_sweep = datetime.now() + (datetime.min - datetime.now()) % sweep_period
            db_update(0, "sweep", next_sweep)
            sweep()
        elif job == "attack":
            if account in attacking:
                change_accounts(account)
                troops = FAV_ATTACK[account]
                attack(account, troops)
            else:
                db_update(account, job, datetime.now() + timedelta(hours=2))
        elif job == "donate":
            change_accounts(account)
            donate()
            db_update(account, job, datetime.now() + timedelta(days=1))
        elif job == "build":
            if account in building:
                change_accounts(account, "main")
                build(account, "main")
                db_update(account, job, datetime.now() + timedelta(minutes=20))
            else:
                db_update(account, job, datetime.now() + timedelta(hours=2))
        elif job == "build_b":
            change_accounts(account, "builder")
            build(account, "builder")
            db_update(account, job, datetime.now() + timedelta(minutes=20))
        elif job == "attack_b":
            change_accounts(account, "builder")
            job_time = get_time_attack_b()
            default = datetime.now() + timedelta(hours=1)
            if not job_time:
                job_time = default
            else:
                job_time = max(default, job_time)
            db_update(account, job, job_time)
            print(f"Updated time for next builder attack for account {account}")
        elif job == "coin":
            change_accounts(account, "main")
            if capital_coin():
                db_update(account, job, datetime.now() + timedelta(hours=23, minutes=30))
            else:
                db_update(account, job, datetime.now() + timedelta(minutes=30))
        elif job == "clock":
            change_accounts(account, "builder")
            if clock():
                job_time = datetime.now() + timedelta(hours=23)
                print(f"Clicked the clock")
            else:
                print("Clock not found")
                job_time = datetime.now() + timedelta(hours=3)
            db_update(account, job, job_time)
            print(f"Updated time for next clock click for account {account}")
        elif job == "lose_trophies":
            change_accounts(account, "main")
            if lose_trophies(account):  minutes = 10
            else:                       minutes = 120
            job_time = datetime.now() + timedelta(minutes=minutes)
            db_update(account, job, job_time)
        else:
            job_time = datetime.now() + timedelta(hours=24)
            db_update(account, job, job_time)
            print(f"Job type '{job}' not coded yet.")
    else:
        rest_time = job_time - datetime.now()
        print("Rest time:", rest_time)
        print_info()
        click_cv2("pycharm")
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
        change_accounts(account)
        db_update(account, "build", get_time_build(account, "main"))
        db_update(account, "attack", get_time_attack())
        db_update(account, "build_b", get_time_build(account, "village"))
        db_update(account, "attack_b", get_time_attack_b())
        db_update(account, "coin", get_time_coin())

def get_time_attack():
    print("Get time until attack is ready")
    goto("army_tab")
    result = time_to_army_ready()

    if result:
        result = datetime.now() + max(timedelta(minutes=result), timedelta(minutes=2))
    else:
        result = datetime.now() + timedelta(minutes=20)
    return result

def get_time_attack_b():
    print("Get time attack - builder")
    goto("builder")
    click_cv2("attack_b")
    if find_cv2("builder_attack_wins")[0] > 0.7:
        print("Ready for attack")
        result = datetime.now()
        pag.click(BOTTOM_LEFT)
        return result
    result = read_text(ARMY_TIME_B, WHITE)
    result = alpha_to_numbers(result)
    result = text_to_time(result)
    pag.click(BOTTOM_LEFT)
    return result

def update_time_build(account, village):
    db_str = f"SELECT * FROM next WHERE account = '{account}' and village = '{village}' and currency = 'elixir1'"
    account_r, village_r, currency_r, building_r, cost, comment = db(db_str)[0]
    print("Get time build: ", account_r, village_r, currency_r, building_r, cost, comment)
    time_temp = string_to_time(comment)
    if time_temp > datetime.now(): return time_temp
    result = get_time_build(account, village)
    db_update_comment(account, village, 'elixir1', result)

def get_time_build(account, village):
    goto(village)
    click_builder(village)
    goto_list_top(village)
    time.sleep(0.2)
    if village == "main": region = BUILDER_LIST_TIMES
    else: region = BUILDER_LIST_TIMES_B
    pag.screenshot('temp/build_time.png', region=region)
    i = cv2.imread(f"temp/build_time.png", 0)
    result = read_build_time(i)
    result = text_to_time_2(result)
    print(result)
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

def click_builder(village="builder"):
    if village == "main":
        click_cv2("builder", BUILDER_REGION, 0.5)
        return
    val, loc, rect = find_cv2("master", BUILDER_B_REGION)
    # print(val)
    if val > 0.5:
        click_cv2("master")
    elif find_cv2("otto", BUILDER_B_REGION)[0] > 0.5:
        click_cv2("otto")

def get_time_build_b():
    print("Get build time - Builder Base")
    goto("builder")
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
    goto("forge")
    time.sleep(0.2)
    result = read_text(CAPITAL_COIN_TIME, WHITE)
    print("Raw:", result)
    try:
        result = alpha_to_numbers(result)
        result = text_to_time(result)
        print("after text_to_time:", result)
    except:
        print("Failed to read screenshot")
        print(result)
        time.sleep(0.2)
    print("Coin time:", result)
    return result

