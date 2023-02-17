from account import *
from lose_trophies import *
from donate import *
from people import *

def return_account(number):
    return next((x for x in accounts if x.number == number), None)

# === 3. ATTACK ===

def just_attack_b(account):
    still_attacking = True
    while still_attacking:
        result = attack_b(account)
        if result:
            still_attacking = False

def attack_b(account, attack_regardless=False):
    goto(builder)
    if not attack_regardless:
        if i_attack_b_0.find():
            # print("Attack b - Not ready for attack")
            return "No attacks left"
    result = goto(attacking_b)
    if i_watch.find():
        time.sleep(5)
        return
    if result != attacking_b:
        print("Couldn't get to attack screen")
        return

    time.sleep(0.5)
    attack_b_get_screen()
    loc_th = th_b()
    loc_th = check_loc_th(loc_th)
    # if loc_th is None:
    #     time.sleep(60)
    #     goto(main)
    #     return
    a, b = objects_b(loc_th)
    for troop, n, loop in account.army_troops_b:
        result = place_b(troop, a, b, n, loop)
        if result == "No spots":
            print("Attack b - no spots")
            break

    check_all_troops_used(a, b)
    still_going = True
    while still_going:
        if i_okay4.find(): still_going = False
        time.sleep(1)

    i_okay4.click()
    goto(builder)
    return

def check_all_troops_used(a, b):
    print("Check all troops used")
    for x in [i_barb, i_bomber, i_giant, i_pekka, i_cannon, i_machine]:
        place_b(x, a, b, 5, 1)
    return

def place_b(troop, a, b, n, loops=1):
    print("Place B", a, b, n, troop)
    troop.click()
    # click_cv2("attack_b/" + troop)
    spots = get_spots(a,b,n)
    if spots is None:
        return "No spots"
    # print(troop, a, b)
    # print(spots)
    for _ in range(loops):
        for spot in spots:
            # print("Place b:", spot)
            spot = (max(spot[0],275), spot[1])
            pag.click(spot)
        time.sleep(0.5)

def get_time_attack():
    # print("Get time until attack is ready")
    goto(army_tab)
    result = time_to_army_ready()

    if result:
        result = datetime.now() + max(timedelta(minutes=result), timedelta(minutes=2))
    else:
        result = datetime.now() + timedelta(minutes=20)
    return result

def attack(account, data, siege_required=True, attack_regardless=False):
    db_update(account, "attack", datetime.now() + timedelta(minutes=5))
    account.update_resources(current_resources())
    if not attack_regardless:
        if not account.attacking:
            # print(f"{account} not attacking")
            db_update(account, "attack", datetime.now() + timedelta(hours=5))
            return
    goto(main)
    db_update(account, "attack", datetime.now() + timedelta(minutes=5))

    # Attack Prep
    result = attack_prep(account, siege_required=account.requires_siege)
    if not result:
        print("attack: Troops not ready")
        db_update(account, "attack", text_to_time_2(army_time.read(region=ARMY_TIME, show_image=False)))
        return

    goto(find_a_match)
    match_found = False
    war_goals = account.war_goals()
    while not match_found:
        assessment = assess_village(account, data, war_goals)
        if assessment[0] == "Good to go":
            match_found = True
        elif assessment == "Not on attack screen":
            return
        else:
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
        # print("Attack - initial troops 4:", objects_to_str(data['initial_troops']))
        launch_attack(account, data, image)

    # Finish attack
    finish_attack(account, data)
    invite_latest_attackee()
    account.update_resources(current_resources())
    army_prep(account, account.troops_to_build, army_or_total="total", extra=True)

    # attack_prep(account, data)
    if data['name'] != "goblins": # Ask for donations (if not goblins)
        request(account)
    if data['name'] != "goblins": # Short check time (if goblins)
        db_update(account, "attack", datetime.now() + timedelta(minutes=0))

    time.sleep(.2)
    return


def convert_attack_to_troops(data):
    troops_required = data['initial_troops'] + data['final_troops']
    for x, no in data['troop_group']:
        troops_required += [x] * no * data['troop_groups']
    troops_required += [lightening] * data['lightening']

    return troops_required


def attack_prep(account, siege_required=True):
    goto(army_tab)

    army_prep(account, account.troops_to_build, army_or_total="total")
    sufficient_troops, actual_troops = army_prep(account, account.troops_to_build, army_or_total="army")
    if not sufficient_troops: return sufficient_troops

    if siege_required and not account.has_siege and actual_troops and actual_troops[log_thrower] != 1 and account.th > 8:
        sufficient_troops = False
        request(account)
        db_update(return_account(1), "donate", datetime.now())

    print("Attack prep - sufficient troops", sufficient_troops)
    return sufficient_troops

def troop_create(troop, count):
    print("Troop create: ", troop)
    troop.start_train(count)

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
    # print("Assess village")
    time.sleep(0.5)
    # zoom_out()

    # Check if its returned to main (due to a reload)
    if not wait_cv2("end_battle", END_ATTACK_SPOT):
        print("Not on attack screen")
        return "Not on attack screen"

    # Resource Check
    resources = available_resources()
    required = war_goals
    print("Assess village (resources vs required):", resources, required)
    if resources[0] < required[0] or resources[1] < required[1] or resources[2] < required[2]:
        return "Insufficient resources"

    # Advanced Town Hall
    img = create_double_screen(account)
    # show(img, scale=0.5)

    # pag.screenshot("attacks/attack.png")
    th, loc = town_hall(img)
    if th > data['max_th'] and account.th > 5:
        return "Town hall too high"

    # Aggressive defences
    if not wait_cv2("coin"): return "Not on attack screen"
    if check_towers(data['towers_to_avoid'], img): return "Aggressive defence"

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
    print("Attack - initial troops 4:", objects_to_str(data['initial_troops']))

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

    if account.th < 9:
        place_clan()
    print("Launch attack: initial troops")
    print("Attack - initial troops 6:", objects_to_str(data['initial_troops']))

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
    dp1 = (max(dp[0], 275), min(dp[1],815))
    val, loc, rect = find(troop.i_attack.image, get_screenshot(TROOP_ZONE))
    print("Place troops:", troop, val, loc, ". Drop point:", dp1)
    if val > 0.63:
        click(troop.i_attack.image, TROOP_ZONE)
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

def place_clan():
    i_clan_army.click()
    pag.click(STANDARD_DP)

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
            # print(troop, dp1, dp2, count, prop, prop2, x, y)
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

def bomb(tower_to_bomb):
    targets = tower_to_bomb.images
    spells, loc = has_spells()
    lightening.i_army.click()
    print("Bomb (initiwsal):", spells)
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
                    time.sleep(2)
                    val, loc, rect = find_cv2(x, enlarged_rect)
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
    time = text_to_time_2(army_time.read(region=ARMY_TIME, show_image=False))
    db_update(account, "attack", time)


# def log(var, account, no):
#     time = datetime.now().strftime('%d %b %I:%M%p')
#     no = f"{no:,}"
#     line = f"{time}: Account: {account.number}. {var.title()}: {no}"
#     with open(f"log{account.number}.txt", 'r+') as f:
#         content = f.read()
#         f.seek(0, 0)
#         f.write(line.rstrip('\r\n') + '\n' + content)
#
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
