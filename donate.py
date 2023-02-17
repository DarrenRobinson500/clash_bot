# from account import *
from attacks import *
from sql import *

def get_requestor_name(y):
    name_region = (100, y - 200, 200, 150)
    screen = get_screenshot(name_region)
    max_val = 0.5
    max_member = None
    for x in members:
        val, loc, rect = find(x.i_chat, screen)
        if val > max_val:
            max_val = val
            max_member = x
    return max_member

def donate_get_required_troops(account):
    goto(chat)
    required_troops = []
    donate_buttons = i_donate.find_many()
    for x, y, w, h in donate_buttons:
        region = (350, y - 150, 560, 120)
        screen = get_screenshot(region)
        for troop in troops:
            if troop.type == "siege" and not account.has_siege: continue
            if troop.i_donate1 is None or troop.i_donate1.image is None: continue
            if troop.currently_training: continue
            show_image = False
            if troop == edrag: show_image = False
            val, loc, rect = find(troop.i_donate1.image, screen, text=troop.name, show_image=show_image)
            if val > 0.65:
                # print("Required troop:", troop)
                if troop not in required_troops:
                    required_troops.append(troop)
                if troop.donation_count == 0: troop.donation_count = 1
    # print("Donate (get troops):", troop_str(required_troops))
    return required_troops

def donate_train_required_troops(account, required_troops):
    time.sleep(0.2)
    time_required = 20 * 60
    # print("Donate - train required troops")
    for troop in required_troops:
        # print("Donate - train required troops:", troop.name.capitalize())
        if troop.type == "siege":
            if not account.has_siege: continue
        if troop.i_training.find(fast=True):
            print("Already training:", troop.name)
            troop.currently_training = True
        else:
            troop.start_train(count=1)
            if troop == required_troops[0]:
                move_to_queue_start(troop)
                time_required = troop.training_time
    return time_required

def donate_give_required_troops(required_troops):
    goto(chat)
    end_time = datetime.now() + timedelta(minutes=3)
    requests = find_many("donate", DONATE_BUTTONS, 0.8)
    while datetime.now() < end_time and len(required_troops) > 0:
        # print("Donate - give", troop_str(required_troops))
        for x in requests:
            click_rect(x)
            time.sleep(0.4)
            # print("Required troops", troop_str(required_troops))
            for x in required_troops:
                if x.i_donate2.find() and x.i_donate2.check_colour():
                    x.i_donate2.image.click()
                    pag.move(755,322)
                    time.sleep(0.1)
                    x.donations += 1
                    x.currently_training = False
                    required_troops.remove(x)
            i_donate_cross.click()
            time.sleep(10)

def check_troop_colour_donate(troop):
    val, loc, rect = troop.i_donate2.find_detail(fast=True)
    rect_adj = [rect[0] + DONATE_AREA[0], rect[1] + DONATE_AREA[1], rect[2], rect[3], ]
    colour = check_colour_rect(rect_adj, show_image=False, text=troop.name)
    return colour

def donate_go_up():
    goto(chat)
    val, loc, rect = i_more_donates.find_detail()
    if val > i_more_donates.threshold:
        rect_adj = [rect[0] + DONATE_BUTTONS[0], rect[1] + DONATE_BUTTONS[1], rect[2], rect[3], ]
        click_rect(rect_adj)
        time.sleep(0.5)

def send_message(text):
    goto(chat)
    click(img_message)
    time.sleep(0.1)
    pag.write(text)
    pag.press('enter')
    time.sleep(2)

def print_training():
    for troop in troops:
        if troop.currently_training: print("Currently training:", troop.name)

def donate(account, mode=""):
    if account.cwl_donations_left and account.number != 3:
        if mode == "cwl": result = cwl_donations_ad_hoc(cwl=True)
        else: result = cwl_donations_ad_hoc(cwl=False)
        if result == 0:
            account.cwl_donations_left = False
            account.set_mode()
            queue_up_troops(account)
        # print("Donate (mode):", account.mode, account.cwl_donations_left, account.troops_to_build)

        return
    donate_go_up()
    donate_basic()
    if not account.donating:
        db_update(account, "donate", datetime.now() + timedelta(days=1))
        return
    required_troops = donate_get_required_troops(account)
    queue_up_troops(account, extra_troops=required_troops)

    db_update(account, "donate", datetime.now() + timedelta(minutes=20))

def queue_up_troops(account, extra_troops=[]):
    for troop in extra_troops:
        troop.donations += 1
    account.update_troops_to_build()
    army_prep(account, account.troops_to_build, army_or_total="total")

def print_total_donations():
    print("\nTOTAL DONATIONS")
    for troop in troops:
        if troop.donations > 0:
            print(f" - {troop.name}s: {troop.donations}")

def donate_basic():
    print("Donate")
    goto(chat)
    donate_buttons = i_donate.find_many()
    # print("Donate request buttoms:", donate_buttons)
    start_time = datetime.now()
    for x, y, w, h in donate_buttons:
        pag.click(x + w/2, y + h/2)
        region = (160, y - 150, 560, 120)
        time.sleep(0.1)
        for troop in troops:
            if troop.donate_bool:
                screen = get_screenshot(DONATE_AREA, colour=0)
                show_image = False
                if troop == super_barb: show_image = False
                val, loc, rect = find(troop.i_donate2.image, screen, troop.name, show_image=show_image)
                print("Donate basic:", troop.name, round(val,2), datetime.now() - start_time)
                if val > 0.65:
                    count = 0
                    screen = get_screenshot(DONATE_AREA, colour=1)
                    image_colour = screen[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
                    colour = check_colour_screen(image_colour)
                    # print(troop.name, val, colour)
                    while colour and count < 10:
                        # print("Donate - clicking:", troop.name)
                        click(troop.i_donate2.image, DONATE_AREA)
                        troop.donations += 1
                        time.sleep(0.1)
                        count += 1
                        if troop.type == "siege": count += 10
                        image_colour = get_screenshot(DONATE_AREA, colour=1)[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
                        colour = check_colour_screen(image_colour)
        i_donate_cross.click()
        # print("Donate:", datetime.now() - start_time)
        time.sleep(0.2)

def check_colour_screen(image):
    spots = [(1 / 4, 1 / 4), (1 / 4, 3 / 4), (3 / 4, 1 / 4), (3 / 4, 3 / 4), (7 / 8, 1 / 8), (0.95, 0.05)]
    count = 0
    y, x, channels = image.shape
    for s_x, s_y in spots:
        pixel = image[int(y * s_y)][int(x * s_x)]
        blue, green, red = int(pixel[0]), int(pixel[1]), int(pixel[2])
        if abs(blue - green) > 5 or abs(blue - red) > 5: count += 1
        # print("Check colour screen", blue, green, red, count)
    colour = False
    if count > 1: colour = True
    # print("Check colour", colour)
    return colour


def army_prep(account, required_army, army_or_total="army", include_backlog=True, troops_only=False, extra=False):
    print("Army prep")

    troops_to_build = []

    # Get required troops
    required_counter = Counter(required_army)

    # Get actual troops
    actual_army_counter, actual_total_counter = full_count(account)
    if actual_army_counter == "Still training":
        print("Still training")
        return False, None
    if army_or_total == "army": actual_troops = actual_army_counter
    else: actual_troops = actual_total_counter

    # Create needed troops
    print_count(required_counter)
    sufficient_troops = True
    sufficient_spells = True
    for x in required_counter:
        if x and x.type != "hero":
            try: actual = actual_troops[x]
            except: actual = 0
            required = required_counter[x]
            text = ""
            if actual < required:
                text = f"Need more of these - make {required - actual} more"
                # print("Army prep:", x, required, actual, text)
                if x.type == "troop": sufficient_troops = False
                if x.type == "spell": sufficient_spells = False
            troops_to_build += [x] * (required - actual)
    # print("Army prep - troops to build:", troop_str(troops_to_build))

    if not sufficient_troops:
        # Delete unneeded troops
        backlog_deleted = False
        for x in troops:
            if x.type == "spell" or x.type == "siege": continue
            try: actual = actual_troops[x]
            except: actual = 0
            required = required_counter[x]
            if actual > required:
                print("Attack prep - delete unneeded troops:", x.name, required, actual)
                if not backlog_deleted: troop_delete_backlog()
                backlog_deleted = True
                x.delete(actual - required)

    if not sufficient_spells:
        # Delete unneeded spells
        for x in troops:
            if x.type == "troop" or x.type == "siege": continue
            try: actual = actual_troops[x]
            except: actual = 0
            required = required_counter[x]
            if actual > required:
                print("Attack prep - delete unneeded spells", x.name, required, actual)
                x.delete(actual - required)

    restock(troops_to_build, account, extra=extra)

    return sufficient_troops, actual_troops

def add_to_dict(dict, key, amount):
    if key in dict:
        dict[key] += amount
    else:
        dict[key] = amount
    return dict

def troops_count_flex(tab, region, troops, count_dict={}):
    goto(tab)
    screen = get_screenshot(region)
    # print("Screen size:", screen.shape)
    # show(screen, label="Troops region")
    for troop in troops:
        if troop.i_army is None:
            print("Troops count flex: couldn't find file:", troop.name)
            continue
        if tab == army_tab:
            if troop.name == "super_barbx":
                show(troop.i_army.image)
            result, loc = troop.i_army.find_screen(screen, return_location=True, show_image=False)
            if result:
                x = max(loc[0] - 30, 0)
                numbers_image = screen[0: 70, x: x + 130]
                result = troop_numbers.read_screen(numbers_image, return_number=True, show_image=False)
                if result > 200: result = int(result / 10)
                add_to_dict(count_dict, troop, result)
        else:
            rectangles = troop.i_training.find_screen_many(screen, show_image=False)
            for loc in rectangles:
                x = max(loc[0] - 30, 0)
                numbers_image = screen[0: 70, x: x + 130]
                result = troop_numbers.read_screen(numbers_image, return_number=True)
                if result > 200: result = int(result / 10)
                add_to_dict(count_dict, troop, result)

    return count_dict

def full_count(account):
    # print("Full count - start")
    count = empty_count()
    if still_training(account, just_troops=True): return "Still training", "Still training"
    count = troops_count_flex(army_tab, ARMY_EXISTING, just_troops, count)
    count = troops_count_flex(army_tab, SPELLS_EXISTING, spells, count)
    count = troops_count_flex(army_tab, ARMY_EXISTING, siege_troops, count)
    count = troops_count_flex(army_tab, CASTLE_TROOPS, siege_troops, count)
    count_no_backlog = count.copy()
    count = troops_count_flex(troops_tab, TRAINING_RANGE, just_troops, count)
    count = troops_count_flex(spells_tab, TRAINING_RANGE, spells, count)
    if account.has_siege:
        count = troops_count_flex(siege_tab, TRAINING_RANGE, siege_troops, count)
    count_with_backlog = count
    return count_no_backlog, count_with_backlog

def still_training(account, just_troops=False):
    if account.has_siege: tabs = [troops_tab, spells_tab, siege_tab]
    else: tabs = [troops_tab, spells_tab]
    if just_troops: tabs = [troops_tab]
    for tab in tabs:
        goto(tab)
        if i_army_clock.find(show_image=False): return True
    return False

def empty_count():
    count = {}
    for troop in troops:
        count[troop] = 0
    return count

def print_count(count):
    string = ""
    for key in count:
        string += f"{key}:{count[key]}. "
    print(string)

def army_count(account):
    if still_training(account, just_troops=True): return "Still training"
    count = empty_count()
    count = troops_count_flex(army_tab, ARMY_EXISTING, just_troops, count)
    count = troops_count_flex(army_tab, SPELLS_EXISTING, spells, count)
    count = troops_count_flex(army_tab, ARMY_EXISTING, siege_troops, count)
    count = troops_count_flex(army_tab, CASTLE_TROOPS, siege_troops, count)
    print()
    print("Army Count:")
    print_count(count)
    return count

def troop_delete_backlog():
    print("Delete Backlog")
    goto(troops_tab)
    remaining_troops = True
    while remaining_troops:
        val, loc, rect = i_remove_troops.find_detail()
        center = pag.center(rect)
        if val > 0.65:
            for x in range(5): pag.click(center)
        else:
            remaining_troops = False

def siege_in_castle(account):
    for siege in [ram, log_thrower]:
        if siege.in_castle(): return siege

def restock(required_troops, account, extra=True):
    count = Counter(required_troops)
    extra_troops = []
    if extra:
        extra_troops = count.most_common()
    # print("Extra:", extra)

    for x in count:
        if x.type == "siege" and not account.has_siege: continue
        x.start_train(count[x])

    if extra and len(extra_troops) > 0:
        troop = extra_troops[0][0]
        number = extra_troops[0][1]
        troop.start_train(number)

# === 2. REQUEST ===
def request(account):
    print("Request")
    goto(army_tab)
    val, loc, rect = i_army_request.find_detail()
    print("Request: 'request' val", val)
    if val > 0.7:
        if i_army_request.check_colour():
            i_army_request.click()
            time.sleep(1)
            val, loc, rect = i_army_request_send.find_detail()
            if val > 0.7:
                i_army_request_send.click()
            else:
                print("Request - couldn't find request button")
        else:
            print("Request - Check colour failed")
    else:
        print("Request - couldn't find request", val)

    job_time = datetime.now()
    account_to_donate = 1
    if account.number == 1: account_to_donate = 2
    db_update(account_to_donate, "donate", job_time, use_account_number=True)

def castle_troops_change(required_troops):
    goto(army_tab)
    troops_to_delete = []
    troops_to_add = []
    current_troops = castle_troops_current()
    for troop in troops:
        surplus = current_troops.count(troop) - required_troops.count(troop)
        if surplus != 0: print(troop, surplus)
        if surplus > 0:
            print("Surplus", troop, surplus)
            for x in range(surplus):
                troops_to_delete.append(troop)
        elif surplus < 0:
            print("Deficit", troop, surplus)
            for x in range(-surplus):
                troops_to_add.append(troop)
    print("Delete:", troop_str(troops_to_delete))
    print("Add:", troop_str(troops_to_add))
    castle_troops_delete(troops_to_delete)
    castle_troops_add(troops_to_add)

def castle_troops_current():
    screen = get_screenshot(CASTLE_TROOPS)
    current_troops = []
    for troop in [super_barb, dragon, bloon, lightening, freeze]:
        result, loc = troop.i_army.find_screen(screen, return_location=True)
        if result:
            x = max(loc[0] - 30, 0)
            numbers_image = screen[0: 50, x: x + 130]
            result = troop_numbers.read_screen(numbers_image, return_number=True)
            for x in range(result):
                current_troops.append(troop)
    return current_troops

def castle_troops_delete(troops_to_delete):
    print(len(troops_to_delete))
    if len(troops_to_delete) == 0: return
    # Delete existing
    i_army_edit.click()
    for troop in troops_to_delete:
        troop.i_army.click_region(CASTLE_TROOPS)
    i_army_okay.click()
    time.sleep(0.2)
    i_surrender_okay.click()

def castle_troops_add(troops_to_add):
    # Delete request info
    i_army_request.click()
    time.sleep(.2)
    i_army_donate_edit.click()
    time.sleep(.2)
    more_troops = True
    while more_troops:
        more_troops = i_remove_troops.click()
        time.sleep(.2)

    # goto(army_tab)
    for troop in troops_to_add:
        troop.i_army.click_region(CASTLE_REQUEST_AREA_2)
        time.sleep(.2)

    time.sleep(0.1)
    i_army_donate_confirm.click()
    time.sleep(0.1)
    i_army_request.click()
    time.sleep(0.1)
    i_army_request_send.click()


def cwl_donations_ad_hoc(cwl=False):
    print("War donations ad hoc")
    goto(main)
    for x in range(500):
        if i_war.find():
            i_war.click()
            break
        if i_war_cwl.find():
            i_war_cwl.click()
            break
        # print(i_war.find_detail(fast=False, show_image=True))
        time.sleep(0.1)
        if x % 10 == 0: print(x)
    if cwl:
        prep_found = False
        start_time = datetime.now()
        for x in range(10):
            if i_cwl_prep.find(fast=False):
                prep_found = True
                break
            time.sleep(0.1)
            print("Prep find:", datetime.now() - start_time)
        if not prep_found:
            print("Prep not found - returning 0")
            return 0
        i_cwl_prep.click()
        for x in range(500):
            if i_cwl_prep.find(fast=False): break
            time.sleep(0.1)

    for x in range(5):
        if click_war_castle(): break
        time.sleep(1)

    # if not found:
    #     print("Couldn't find castle")
    #     goto(main)
    #     return
    still_moving, count = True, 0
    while still_moving and count < 30:
        i_war_left.click()
        pag.moveTo(300,800)
        if i_war_left.colour() < 700: still_moving = False
        time.sleep(0.1)
        count += 1

    remaining_total = 0
    still_moving, count = True, 0
    while still_moving and count < 35:
        remaining = remaining_donations()
        if remaining > 0:
            remaining_total += remaining
            # print("CWL donations - remaining:", count, remaining_total)
            donation_list = []
            if remaining >= 36: donation_list = [super_minion] * 3
            elif remaining >= 24: donation_list = [super_minion] * 2
            elif remaining >= 12: donation_list = [super_minion]
            war_donations_donate_troops(donation_list)

            time.sleep(0.1)
            remaining = remaining_donations()
            if remaining == 11: donation_list = [super_barb] + [minion] * 3
            elif remaining == 10: donation_list = [minion] * 5
            elif remaining == 9: donation_list = [super_barb] + [minion] * 2
            elif remaining == 8: donation_list = [minion] * 4
            elif remaining == 7: donation_list = [super_barb] + [minion]
            elif remaining == 6: donation_list = [minion] * 3
            elif remaining == 5: donation_list = [super_barb]
            elif remaining == 4: donation_list = [minion] * 2
            elif remaining == 3: donation_list = [minion, archer]
            elif remaining == 2: donation_list = [minion]
            elif remaining == 1: donation_list = [archer]
            war_donations_donate_troops(donation_list)

        i_war_right.click()
        pag.moveTo(1300,800)
        if i_war_right.colour() < 800: still_moving = False
        time.sleep(0.1)
        count += 1


    print("REMAINING DONATIONS:", remaining_total)
    return remaining_total

def click_war_castle():
    found = False
    for castle in war_castles:
        # print(castle, castle.find_detail())
        if not found and castle.find(show_image=False):
            found = True
            castle.click()
    return found

def remaining_donations():
    result = war_donation_count.read(WAR_DONATION_COUNT, show_image=False)
    x_pos = result.find("x")
    try:
        received = int(result[0:x_pos])
        total = int(result[x_pos+1:])
    except:
        return 0
    return total - received

def war_donations_donate_troop(troop):
    if not i_war_donate_reinforcements.find(fast=False):
        i_war_donate.click()
        time.sleep(0.1)
    troop.i_donate2.click_region(WAR_DONATION_AREA)

def war_donations_donate_troops(troops):
    if not i_war_donate_reinforcements.find(fast=False):
        i_war_donate.click()
        time.sleep(0.1)
    for troop in troops:
        if troop.i_donate2.colour() > 400:
            troop.i_donate2.click_region(WAR_DONATION_AREA)



# change_castle_troops([super_barb] * 7 + [lightening])
# castle_troops_change([dragon, bloon, bloon, bloon, freeze])

# goto(army_tab)
# i_army_request.click()
# time.sleep(0.1)
# i_army_donate_edit.click()
# time.sleep(5)
# castle_troops_change([dragon, bloon, bloon, bloon])

# goto(army_tab)
# goto(pycharm)

