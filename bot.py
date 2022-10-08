import datetime

from attacks import *
from donate import *
from build import *

method = cv2.TM_CCOEFF_NORMED

# === 3. ATTACK ===
def attack_b(account):
    start_time = datetime.now()
    goto(builder)
    # print("A0", datetime.now() - start_time)
    screen = get_screenshot(ATTACK_BUTTON)
    # print("A1", datetime.now() - start_time)
    val, loc, rect = find(i_attack_b_0, screen)
    if val > 0.85:
        print("Attack b - Not ready for attack")
        return
    print("Going to attacking b")
    print("B", datetime.now() - start_time)
    result = goto(attacking_b)
    if result != attacking_b:
        print("Couldn't get to attack screen")
        return

    print("Attack b - Ready for attack")
    print("C", datetime.now() - start_time)
    time.sleep(0.5)
    attack_b_get_screen()
    loc_th = th_b()
    loc_th = check_loc_th(loc_th)
    if loc_th is None:
        time.sleep(60)
        goto(main)
        return
    a, b = objects_b(loc_th)
    print("D", datetime.now() - start_time)
    for troop, n, loop in account.army_troops_b:
        result = place_b(troop, a, b, n, loop)
        if result == "No spots":
            print("Attack b - no spots")
            break
    troops_left = True
    count = 0
    print("E", datetime.now() - start_time)

    while troops_left and count <= 5 and result != "No spots":
        troops_left = check_all_troops_used(a, b)
        count += 1
        print(count)
    wait_cv2("attack_b/okay")
    goto(builder)
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
    # print("Place B")
    click_cv2("attack_b/" + troop)
    spots = get_spots(a,b,n)
    if spots is None:
        return "No spots"
    # print(troop, a, b)
    # print(spots)
    for _ in range(loops):
        for spot in spots:
            # print("Place b:", spot)
            pag.click(spot)
        time.sleep(0.5)

def attack(account, data):
    account.update_resources(current_resources())
    if not account.attacking:
        # print(f"{account} not attacking")
        db_update(account, "attack", datetime.now() + timedelta(hours=5))
        return
    print("Attack Start")
    goto(main)
    db_update(account, "attack", datetime.now() + timedelta(minutes=5))

    # Attack Prep
    result = attack_prep(account)
    if not result:
        print("attack: Troops not ready")
        db_update(account, "attack", get_time_attack())
        return

    # Find a match
    print("Attack")
    goto(find_a_match)
    match_found = False
    war_goals = account.war_goals()
    while not match_found:
        assessment = assess_village(account, data, war_goals)
        if assessment[0] == "Good to go":
            match_found = True
            print(assessment[0])

        elif assessment == "Not on attack screen":
            return
        else:
            print(assessment)
            result = next_village()
            if result == "Not on attack screen":
                return
            war_goals = [int(war_goals[0] * 0.98), int(war_goals[1] * 0.98),int(war_goals[2] * 0.98),]
            print("New gold objective:", war_goals)

    # Launch attack
    image = assessment[1]
    if data['name'] == "goblins":
        drop_points = assessment[2]
        launch_attack_dps(account, data, image, drop_points)
    else:
        launch_attack(account, data, image)

    # Finish attack
    finish_attack(account, data)
    attack_prep(account)
    if data['name'] != "goblins": # Ask for donations (if not goblins)
        request(account)
    if data['name'] != "goblins": # Short check time (if goblins)
        db_update(account, "attack", datetime.now() + timedelta(minutes=0))

    time.sleep(.2)
    return

def attack_prep(account, war=False):
    if war:
        data = account.war_troops
    else:
        data = account.army_troops
    print("Attack prep")
    # Checking if training
    goto(army_tab)
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
    for x, no in data['spells']:
        for y in range(no):
            troops_required.append(x)

    required_lightening = data['lightening']
    troops_required += [lightening] * required_lightening
    print(troop_str(troops_required))
    requ = Counter(troops_required)
    time.sleep(0.2)

    # Get actual troops
    actual_troops = troops_count(account)

    # Delete unneeded troops
    print("Delete unneeded troops")
    backlog_deleted = False
    for x in troops:
        try: actual = actual_troops[x]
        except: actual = 0
        required = requ[x]
        if actual > required:
            print("Attack prep - delete unneeded", x.name, required, actual)
            if not backlog_deleted: troop_delete_backlog()
            backlog_deleted = True
            x.delete(actual - required)

    # Create needed troops
    print("Create required troops")
    for x in requ:
        if x.type != "hero" and x.type != "siege":
            print("Troop:", x.name)
            actual = actual_troops[x]
            required = requ[x]
            if actual < required:
                if x.type != "spell": sufficient_troops = False
                text = f"Need more of these - make {required - actual} more"
                print(x, required, actual, text)
                troops_to_build += [x] * (required - actual)
    if account.has_siege: troops_to_build.append(log_thrower)
    print("Attack prep:", troop_str(troops_to_build))
    if war: extra = False
    else: extra = True
    restock(troops_to_build, extra=extra)
    if not account.has_siege and actual_troops[log_thrower] != 1:
        sufficient_troops = False
        request(account)
        db_update(account_1, "donate", datetime.now())

    return sufficient_troops

def troop_create(troop, count):
    print("Troop create: ", troop)
    troop.start_train(count)

# def troop_count(troop):
#     # goto(army_tab)
#     time.sleep(.2)
#     if troop.type == "troop":
#         region = ARMY_EXISTING
#     else:
#         region = SPELLS_EXISTING
#
#     val, loc, rect = find(troop.army, get_screenshot(region))
#
#     print("Troop count - identifying troop", troop.name, val)
#     if val < 0.60: return 0
#     region = (loc[0] - 30, loc[1] - 70, 130, 80)
#     result = read_troop_count(region)
#     try:
#         result = int(result)
#         if result > 150: result = int(result / 10)
#         return result
#     except:
#         return 0

# def troop_count_old(troop):
#     # goto(army_tab)
#     time.sleep(.2)
#     if troop in TROOPS:
#         region = ARMY_EXISTING
#     else:
#         region = SPELLS_EXISTING
#     troop = "troops/" + troop
#
#     val, loc, rect = find_cv2(troop, region)
#
#     print("Troop count - identifying troop", troop, val)
#     if val < 0.60: return 0
#     region = (loc[0] - 30, loc[1] - 70, 130, 80)
#     result = read_troop_count(region)
#     try:
#         result = int(result)
#         if result > 150: result = int(result / 10)
#         return result
#     except:
#         return 0
#

def check_towers(towers, img, return_image=False):
    found = False
    for tower in towers:
        val, loc, rect = find_cv2_image(tower, img)
        if val > 0.65:
            found = True
            cv2.rectangle(img, rect, (0,255,255), 2)
    if return_image:
        return found, img
    else:
        return found


def assess_village(account, data, war_goals):
    start_time = datetime.now()
    global DP
    print("Assess village")
    time.sleep(0.5)
    # zoom_out()

    # Check if its returned to main (due to a reload)
    if not wait_cv2("end_battle", END_ATTACK_SPOT):
        print("Not on attack screen")
        return "Not on attack screen"

    # Resource Check
    resources = available_resources()
    required = war_goals
    if resources[0] < required[0] or resources[1] < required[1] or resources[2] < required[2]:
        print("Assess village:", resources, required)
        return "Insufficient resources"

    # Advanced Town Hall
    img = create_double_screen(account)
    # show(img, scale=0.5)

    # pag.screenshot("attacks/attack.png")
    th, loc = town_hall(img)
    if th > data['max_th']:
        return "Town hall too high"

    # Aggressive defences
    if not wait_cv2("coin"): return "Not on attack screen"
    if check_towers(data['towers_to_avoid'], img): return  "Aggressive defence"

    # Barb drop spot
    if data['name'] == "barbs":
        DP = ram_drop_point(account, img)
        if DP is None:
            DP = STANDARD_DP2

    # Goblin mines
    if data['name'] == "goblins":
        image_bw = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        target_locs = find_many_img(MINES, image_bw, confidence=0.7)
        center = (img.shape[1] // 2, img.shape[0] // 2)
        drop_points = get_drop_points(account, img, center, target_locs)
        print("Assessment drop points:", drop_points)
        if len(drop_points) == 0:
            return "No identified mines"
        else:
            return "Good to go", img, drop_points

    # show(img, scale=0.5)
    return "Good to go", img

def next_village():
    print()
    print("Next village")
    time.sleep(0.5)
    if find_cv2("next_attack")[0] > 0.7:
        wait_and_click('next_attack')
        time.sleep(0.1)
        # wait_and_click('next_attack')
    else:
        goto(find_a_match)
    if not wait_cv2("end_battle"): return "Not on attack screen"

def launch_attack_dps(account, data, image, drop_points):
    print("Launch attack dps - drop points:", drop_points)
    for drop_point in drop_points:
        print("Drop point:", drop_point)
        if drop_point[1] > 700:
            print("Down")
            pag.scroll(-300)
            pag.scroll(-300)
            drop_point[1] -= 350
        else:
            print("Up")
            pag.scroll(300)
            pag.scroll(300)

        for troop in data["drop_point_troops"]:
            place(troop, 1, drop_point)

    time.sleep(10)
    click_cv2("surrender")
    click_cv2("surrender_okay")
    wait_cv2("return_home")

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

def launch_attack(account, data, image):
    standard_pace = True

    if data['name'] == 'barbs':
        if DP is None: return
        dp = DP
        if DP[1] > 700:
            pag.scroll(-300)
            pag.scroll(-300)
            dp[1] -= 350
    else:
        dp = STANDARD_DP

    if data['name'] == "golems":
        dp = top
        dp2 = left
    else:
        dp2 = None

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
            if not dp2:
                place(troop, n, dp, troop_pause=troop_pause)
            else:
                place_line(troop, n, dp, dp2)
        try:
            damage = read_text(DAMAGE, WHITE,True)
        except:
            damage = 0
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
    dp1 = (dp[0],min(dp[1],815))
    val, loc, rect = find(troop.attack, get_screenshot(TROOP_ZONE))
    print("Place troops:", troop, val, loc)
    if val > 0.63:
        click(troop.attack, TROOP_ZONE)
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
                count += reduction * 2
            count += 1

def place_old(troop, count_total, dp=[400,400], troop_pause=0):
    if troop in TROOP_ATTACK_EXT: troop = troop + "_attack"
    troop = f"troops/{troop}"
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
                count += reduction * 2
            count += 1

def place_line(troop, count_total, dp1, dp2, troop_pause=0):
    if troop in TROOP_ATTACK_EXT: troop = troop + "_attack"
    troop = "troops/" + troop
    val, loc, rect = find_cv2(troop, TROOP_ZONE)
    print("Place troops:", troop, val, loc)
    if val > 0.63:
        click_cv2(troop, TROOP_ZONE)
        time.sleep(.1)
        print("Place line", top, left)
        for count in range(count_total):
            prop = round((count + 1) / (count_total + 1),2)
            prop2 = (1 - prop)
            x = int(dp1[0] * prop + dp2[0] * prop2)
            y = int(dp1[1] * prop + dp2[1] * prop2)
            print(troop, dp1, dp2, count, prop, prop2, x, y)
            pag.click(x,y)
            time.sleep(troop_pause)

def has_spells():
    print("Has spells")
    lightening_buttons = find_many("troops/lightening", TROOP_ZONE, 0.5)
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
    click_cv2("troops/lightening", TROOP_ZONE, 0.50)
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
    goto(main)
    account.update_resources(current_resources())

def log(var, account, no):
    time = datetime.now().strftime('%d %b %I:%M%p')
    no = f"{no:,}"
    line = f"{time}: Account: {account.number}. {var.title()}: {no}"
    with open(f"log{account.number}.txt", 'r+') as f:
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

# =============
# === Build ===
# =============


def build(account, village):
    builders = spare_builders(village)
    print("Build - spare builders", builders)
    if spare_builders(village) == 0: return
    if village == "main": goto(main)
    else: goto(builder)
    remove_trees(village)
    available_options = get_available_upgrades(village)
    preference = get_preference(available_options)
    if preference:
        select_tower(village, preference)
        upgrade()
        attack(account, account.army_troops)

# def build_old(account, village):
#     if village == "main": goto(main)
#     else: goto(builder)
#     for currency in CURRENCIES:
#         account_no, village, currency, preference, cost, comment = db(f"SELECT * FROM next WHERE account='{account.number}' and village='{village}' and currency = '{currency}'")[0]
#         print("Build - preference:", preference)
#         if preference == "none": next_build(account, village)
#
#     builders = spare_builders(village)
#     if builders == 0: return
#     remove_trees(village)
#     if builders == 1 and village == "main" and account.needs_walls:
#         result = get_time_build(account, "main")
#         if result is None: return
#         time_remaining = result - datetime.now()
#         print("Build - time remaining until 2 builders:", time_remaining)
#         start_saving = time_remaining < timedelta(hours=24)
#         print("Build - start saving", start_saving)
#         if not start_saving:
#             print("Building walls")
#             build_sub("main", "wall")
#             return
#
#     for currency in CURRENCIES:
#         if spare_builders(village) == 0: return
#         result = db(f"SELECT * FROM next WHERE account='{account.number}' and village='{village}' and currency = '{currency}'")[0]
#         account_no, village, currency, building, cost, comment = result
#         preference = building
#         print("Build - preference:", preference)
#         if preference != "none" and preference != "complete":
#             result = build_sub(village, preference)
#             print("Build", result)
#             if result:
#             # if preference != "wall" and result:
#                 print("Build - updating db_next")
#                 db_update_next(account.number, village, currency, "none", 0)
#                 next_build(account, village)
#                 update_time_build(account, village)
#                 account.attacking = True
#
# def next_build(account, village):
#     condition = f" WHERE account='{account.number}' and village='{village}'"
#     result = db(f"SELECT * FROM next" + condition)
#     need_update = False
#     for current_account_no, current_village, current_currency, current_building, current_cost, comment in result:
#         if current_building == "none": need_update = True
#
#     if need_update:
#         preferences = get_build_preference(village)
#         # cost = build_cost(village, building)[1]
#         db_update_next(account.number, village, "elixir1", preferences[0])
#         db_update_next(account.number, village, "dark", preferences[1])
#         db_update_next(account.number, village, "gold", preferences[2])
#         db_update_next(account.number, village, "elixir", preferences[3])
#         # account, village, currency, building, cost, comment

# def db_update_next(account, village, currency, building, cost=0, comment=""):
#     # account, village, currency, building, cost, comment
#
#     condition = f" WHERE account='{account.number}' and village='{village}' and currency='{currency}'"
#     db_str = f"SELECT * FROM next" + condition
#     existing = len(db(db_str))
#     if existing == 1:
#         db(f"UPDATE next SET building='{building}'" + condition)
#         db(f"UPDATE next SET cost='{cost}'" + condition)
#         db(f"UPDATE next SET comment='{comment}'" + condition)
#     else:
#         print("Records not updated - didn't find exactly 1 record to update")
#
# def db_update_comment(account, village, currency, comment):
#     # account, village, currency, building, cost, comment
#
#     condition = f" WHERE account='{account.number}' and village='{village}' and currency='{currency}'"
#     db_str = f"SELECT * FROM next" + condition
#     existing = len(db(db_str))
#     if existing == 1:
#         db(f"UPDATE next SET comment='{comment}'" + condition)
#     else:
#         print("Records not updated - didn't find exactly 1 record to update")


def move_list(direction):
    dur = 0.5
    if direction == "up":
        pag.moveTo(855,666, dur)
        pag.dragTo(855,210, dur)
    if direction == "down":
        pag.moveTo(855,210, dur)
        pag.dragTo(855,666, dur)



# def build_available(village, build_type):
#     try:
#         resource_type, cost = build_cost(village, build_type)
#     except:
#         return False
#     if village == "main":
#         resources = current_resources()
#     elif village == "builder":
#         goto(builder)
#         resources = current_resources_b()
#     else:
#         return
#
#     resource = 0
#     if resource_type == "Gold": resource = resources[0]
#     if resource_type == "Elixir": resource = resources[1]
#     if resource_type == "Dark" and village == "main": resource = resources[2]
#     print("Build available: cost, resource", cost, resource)
#     return cost < resource
#
# def get_build_preference(village):
#     options = get_available_upgrades(village)
#     preferences = ["complete","complete","complete","complete"]
#     if village == "main":
#         loops = [(0, build_preferences_e1), (1, build_preferences_d), (2, build_preferences_g), (3, build_preferences_e)]
#     else:
#         loops = [(0, build_b_preferences_e1), (2, build_b_preferences_g), (3, build_b_preferences_e)]
#
#     print(loops)
#     for loop_index, loop_list in loops:
#         for x in loop_list:
#             if x in options:
#                 preferences[loop_index] = x
#                 break
#
#     print(f"Get build preferences: Options {options}, Preferences {preferences}")
#     return preferences

# def build_sub(village, item):
#     if village == "main":
#         region = BUILDER_LIST_REGION
#         directory = "builder/"
#         max_count = 4
#     elif village == "builder":
#         region = BUILDER_B_LIST_REGION
#         directory = "builder_b/"
#         max_count = 3
#     else:
#         print("Build sub - incorrect village specification")
#         return
#
#     goto_list_top(village)
#     count = 0
#     while count < max_count:
#         val, loc, rect = find_cv2(directory + item, region)
#         val_upgrade, loc_upgrade, rect_upgrade = find_cv2("suggested_upgrades", region)
#         print("Build sub:", item, val)
#         # print(val, val_upgrade, rect[0], rect_upgrade[0])
#         # print(val > 0.75 and not(val_upgrade > 0.75 and rect[1] < rect_upgrade[1]))
#         if val > 0.82 and not(val_upgrade > 0.8 and rect[1] < rect_upgrade[1]):
#             print("trying to click and then upgrade")
#             click_cv2(directory + item, region)
#             result = upgrade()
#             if result and item == "wall":
#                 build_sub(village, item)
#             return result
#         else:
#             move_list("up")
#             time.sleep(1)
#         count += 1

# def build_cost(village, item):
#     if item is None: return "", 0
#     if village == "main":
#         region = BUILDER_LIST_REGION
#         directory = "builder/"
#         max_count = 5
#     elif village == "builder":
#         region = BUILDER_B_LIST_REGION
#         directory = "builder_b/"
#         max_count = 3
#     else:
#         print("Build sub - incorrect village specification")
#         return "", 0
#
#     goto_list_top(village)
#     count = 0
#     while count < max_count:
#         val, loc, rect = find_cv2(directory + item, region)
#         val_upgrade, loc_upgrade, rect_upgrade = find_cv2("suggested_upgrades", region)
#         print("Build cost:", item, val)
#         # print(val > 0.75 and not(val_upgrade > 0.75 and rect[1] < rect_upgrade[1]))
#         if val > 0.80 and not(val_upgrade > 0.75 and rect[1] < rect_upgrade[1]):
#             print("Found item")
#             region = (loc[0] + 200, loc[1] - 30, 390, 55)
#             print("Build cost - taking screenshot", region)
#             pag.screenshot('temp/temp_build_cost.png', region=region)
#             screen = cv2.imread('temp/temp_build_cost.png', 0)
#             cost = read_cost(screen)
#             if len(cost) == 0:
#                 return ("Read Failure", 0)
#             # if item == "wall": show(screen)
#             type = "Dark"
#             if cost[0] == 'g' or cost[0] == 'h': type = "Gold"
#             elif cost[0] == 'e' or cost[0] == 'f': type = "Elixir"
#             try:
#                 if cost[0].isnumeric():
#                     cost = int(cost)
#                 elif cost[1].isnumeric():
#                     cost = int(cost[1:])
#                 else:
#                     cost = int(cost[2:])
#             except:
#                 cost = 0
#             return (type, cost)
#         else:
#             move_list("up")
#             time.sleep(1)
#         count += 1
#     return "", 0


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
        if find_cv2("collect_capital_coin")[0] > 0.7:
            click_cv2("collect_capital_coin")
            return True
    return False

# =============
# === CLOCK ===
# =============

def clock():
    goto(builder)
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
    for x in RESOURCE_TEMPLATES:
        val, loc, rect = find_cv2(x)
        if val > 0.8:
            click_cv2(x)

# ========================
# === 7. LOSE TROPHIES ===
# ========================

def calc_trophies():
    goto(main)
    time.sleep(1)
    result = read_num(TROPHIES, WHITE, 1.00)
    try:
        result = int(result)
    except:
        result = 0
    if result < 20: result = result * 100
    if result < 500: result = result * 10
    return result

def lose_trophies(account):
    global current_location
    current_trophies = calc_trophies()
    print("Lose trophies", account.number, account.max_trophies, current_trophies)
    if current_trophies > account.max_trophies:
        goto(find_a_match)
        hold_key("a", 0.5)
        # zoom_out()
        dp = STANDARD_DP
        for troop in [king, queen, warden, champ, barb, giant, bomber, ]:
            val, loc, rect = find(troop.attack, get_screenshot(TROOP_ZONE))
            print("Lose trophies:", troop.name, val)
            if val > 0.65:
                place(troop, 1, dp)
                print("Unleashed", troop)
                break
        click_cv2("surrender")
        click_cv2("surrender_okay")
        current_location = "return_home"
        goto(main)

        if troop in [barb, giant, bomb, ]:
            troop_delete_backlog()
            restock([troop], extra=False)
            attack(account, account.army_troops)

        return True
    return False

def check_trophies(account):
    current_trophies = calc_trophies()
    if account.number == 1 and current_trophies > 1600:
        account_1.troops = GOBLIN_13
    if account.number == 1 and current_trophies < 1000:
        account_1.troops = BARBS_13
    if account.number == 2 and current_trophies > 1400:
        account_2.troops = GOBLIN
    if account.number == 2 and current_trophies < 1000:
        account_2.troops = BARBS_11

def sweep():
    for account in accounts:
        change_accounts(account.number)
        get_resources()
        account.update_resources(current_resources())
        if account.building:
            build(account, "main")
        # check_trophies(account)
        donate(account)
        capital_coin()
        account.next_update()
        clock()
        get_resources()
        if account.building_b:
            build(account, "builder")
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

def run_job(job, sweep_period):
    print("Job:", job)
    account, job, job_time = job
    account = accounts[account]
    job_time = string_to_time(job_time)
    if time_to_string(job_time) == "Now":
        if job == "sweep":
            next_sweep = datetime.now() + (datetime.min - datetime.now()) % sweep_period
            db_update(account_0, "sweep", next_sweep)
            sweep()
        elif job == "attack":
            if account.attacking:
                change_accounts(account.number)
                attack(account, account.army_troops)
            else:
                db_update(account, job, datetime.now() + timedelta(hours=2))
        elif job == "donate":
            change_accounts(account.number)
            donate(account)
            if account.attacking:
                db_update(account, job, datetime.now() + timedelta(days=1))
            else:
                db_update(account, job, datetime.now() + timedelta(minutes=5))
        elif job == "build":
            if account.building:
                change_accounts(account.number, "main")
                build(account, "main")
                db_update(account, job, datetime.now() + timedelta(minutes=20))
            else:
                db_update(account, job, datetime.now() + timedelta(hours=2))
        elif job == "build_b":
            change_accounts(account.number, "builder")
            build(account, "builder")
            db_update(account, job, datetime.now() + timedelta(minutes=20))
        elif job == "attack_b":
            change_accounts(account.number, "builder")
            job_time = get_time_attack_b()
            default = datetime.now() + timedelta(hours=1)
            if not job_time:
                job_time = default
            else:
                job_time = max(default, job_time)
            db_update(account, job, job_time)
            print(f"Updated time for next builder attack for account {account.number}")
        elif job == "coin":
            change_accounts(account.number, "main")
            if capital_coin():
                db_update(account, job, datetime.now() + timedelta(hours=23, minutes=30))
            else:
                db_update(account, job, datetime.now() + timedelta(minutes=30))
        elif job == "clock":
            change_accounts(account.number, "builder")
            if clock():
                job_time = datetime.now() + timedelta(hours=23)
                print(f"Clicked the clock")
            else:
                print("Clock not found")
                job_time = datetime.now() + timedelta(hours=3)
            db_update(account, job, job_time)
            print(f"Updated time for next clock click for account {account.number}")
        elif job == "lose_trophies":
            change_accounts(account.number, "main")
            if lose_trophies(account):  minutes = 2
            else:                       minutes = 120
            job_time = datetime.now() + timedelta(minutes=minutes)
            db_update(account, job, job_time)
        else:
            job_time = datetime.now() + timedelta(hours=24)
            db_update(account, job, job_time)
            print(f"Job type '{job}' not coded yet.")
    else:
        rest_time = job_time - datetime.now()
        print_info()
        print("Rest time:", rest_time)
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
    # print_locs()
    print_total_donations()
    print()
    for account in accounts:
        account.print_info()
    print()
    db_view()
    print()

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
        db_update(account, "attack_b", get_time_attack_b())
        db_update(account, "coin", get_time_coin())

def get_time_attack_b():
    print("Get time attack - builder")
    goto(builder)
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


def current_resources():
    time.sleep(.1)
    result = []

    for region in [RESOURCES_G, RESOURCES_E, RESOURCES_D]:
        result_ind = resource_numbers.read(region)
        try:
            result.append(int(result_ind))
        except:
            result.append(0)

    # for name, region in [(gold, RESOURCES_G), (elixir, RESOURCES_E), (dark, RESOURCES_D)]:
    #     pag.screenshot(f'temp/current_{name}.png', region=region)
    #     i = cv2.imread(f"temp/current_{name}.png", 0)
    #     result_ind = read_resources(i)
    #     try:
    #         result_ind = int(result_ind)
    #     except:
    #         result_ind = 0

    print("Available Resources:", result)

    return result


def current_resources_old():
    time.sleep(.1)
    result = []

    for name, region in [(gold, RESOURCES_G), (elixir, RESOURCES_E), (dark, RESOURCES_D)]:
        pag.screenshot(f'temp/current_{name}.png', region=region)
        i = cv2.imread(f"temp/current_{name}.png", 0)
        result_ind = read_resources(i)
        try:
            result_ind = int(result_ind)
        except:
            result_ind = 0
        result.append(result_ind)

    print("Available Resources:", result)


    return result

