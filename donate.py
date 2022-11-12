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
    requests = find_many("donate", DONATE_BUTTONS, 0.8)
    for rect in requests:
        # requestor = get_requestor_name(rect[1])
        # print("REQUESTOR:", requestor.name)
        region = (160, rect[1] - 150, 560, 120)
        screen = get_screenshot(region)
        for x in troops:
            if x.type == "siege" and not account.has_siege: continue
            if x.i_donate1 is None or x.i_donate1.image is None: continue
            if x.currently_training: continue
            show_image = False
            if x == edrag: show_image = False
            val, loc, rect = find(x.i_donate1.image, screen, text=x.name, show_image=show_image)
            if val > 0.65:
                required_troops.append(x)
                if x.donation_count == 0: x.donation_count = 1
    print("Donate (get troops):", troop_str(required_troops))
    return required_troops

def donate_train_required_troops(account, required_troops):
    time.sleep(0.2)
    time_required = 20 * 60
    # print("Donate - train required troops")
    for troop in required_troops:
        print("Donate - train required troops:", troop.name.capitalize())
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
        print("Donate - give", troop_str(required_troops))
        for x in requests:
            click_rect(x)
            time.sleep(0.4)
            print("Required troops", troop_str(required_troops))
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
    print(val)
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

def donate(account):
    donate_go_up()
    donate_basic()
    if not account.donating():
        db_update(account, "donate", datetime.now() + timedelta(days=1))
        return
    print("Donate get required troops")
    required_troops = donate_get_required_troops(account)
    queue_up_donations(account, extra_troops=required_troops)
    db_update(account, "donate", datetime.now() + timedelta(minutes=20))

def queue_up_donations(account, extra_troops=None):
    troops_to_queue = []
    for troop in extra_troops:
        troops_to_queue.append(troop)
    for troop in troops:
        if troop.name in ["super_minion", ""]: continue
        if troop.donations > 0:
            for x in range(troop.donation_count):
                troops_to_queue.append(troop)
    if account.has_siege:
        siege_queue = [x for x in troops_to_queue if x.type == 'siege']
        if len(siege_queue) < 6:
            for _ in range(6 - len(siege_queue)):
                troops_to_queue.append(log_thrower)

    print("Queue up donations:", troop_str(troops_to_queue))
    army_prep(account, troops_to_queue, army_or_total="total")

def get_time_attack():
    # print("Get time until attack is ready")
    goto(army_tab)
    result = time_to_army_ready()

    if result:
        result = datetime.now() + max(timedelta(minutes=result), timedelta(minutes=2))
    else:
        result = datetime.now() + timedelta(minutes=20)
    return result

def print_total_donations():
    print("\nTOTAL DONATIONS")
    for troop in troops:
        if troop.donations > 0:
            print(f" - {troop.name}s: {troop.donations}")

def donate_basic():
    print("Donate")
    goto(chat)
    requests = find_many("donate", DONATE_BUTTONS, 0.8)
    print("Donate request buttoms:", requests)
    start_time = datetime.now()
    for x in requests:
        click_rect(x)
        time.sleep(0.1)
        for x in troops:
            if x.donate_bool:
                screen = get_screenshot(DONATE_AREA, colour=0)
                show_image = False
                if x == super_barb: show_image = False
                print(x)
                val, loc, rect = find(x.i_donate2.image, screen, x.name, show_image=show_image)
                print("Donate:", x.name, round(val,2), datetime.now() - start_time)
                if val > 0.65:
                    count = 0
                    screen = get_screenshot(DONATE_AREA, colour=1)
                    image_colour = screen[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
                    colour = check_colour_screen(image_colour)
                    print(x.name, val, colour)
                    while colour and count < 10:
                        print("Donate - clicking:", x.name)
                        click(x.i_donate2.image, DONATE_AREA)
                        x.donations += 1
                        time.sleep(0.1)
                        count += 1
                        if x.type == "siege": count += 10
                        image_colour = get_screenshot(DONATE_AREA, colour=1)[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]]
                        colour = check_colour_screen(image_colour)
        i_donate_cross.click()
        print("Donate:", datetime.now() - start_time)
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
    print("Check colour", colour)
    return colour


def army_prep(account, required_army, army_or_total="army", troops_only=False):
    print("Army prep")

    troops_to_build = []

    # Get required troops
    required_counter = Counter(required_army)

    # Get actual troops
    actual_army_counter, actual_total_counter = full_count(account)
    if actual_army_counter == "Still training": return False
    if army_or_total == "army": actual_troops = actual_army_counter
    else: actual_troops = actual_total_counter

    # Delete unneeded troops
    print("Delete unneeded troops")
    backlog_deleted = False
    for x in troops:
        if troops_only and x.type == "spell": continue
        if troops_only and x.type == "siege": continue
        try: actual = actual_troops[x]
        except: actual = 0
        required = required_counter[x]
        if actual > required:
            print("Attack prep - delete unneeded", x.name, required, actual)
            if not backlog_deleted: troop_delete_backlog()
            backlog_deleted = True
            x.delete(actual - required)

    # Create needed troops
    print("Required troops:")
    print_count(required_counter)
    for x in required_counter:
        if x and x.type != "hero":
            try: actual = actual_troops[x]
            except: actual = 0
            required = required_counter[x]
            text = ""
            if actual < required: text = f"Need more of these - make {required - actual} more"
            # print("Army prep:", x, required, actual, text)
            troops_to_build += [x] * (required - actual)
    print("Army prep - troops to build:", troop_str(troops_to_build))
    restock(troops_to_build, account, extra=False)
    return

def add_to_dict(dict, key, amount):
    if key in dict:
        dict[key] += amount
    else:
        dict[key] = amount
    return dict

def troops_count_flex(tab, region, troops, count_dict={}):
    goto(tab)
    screen = get_screenshot(region)
    for troop in troops:
        if troop.i_army is None:
            print("Troops count flex: couldn't find file:", troop.name)
            continue
        if tab == army_tab:
            result, loc = troop.i_army.find_screen(screen, return_location=True, show_image=False)
        else:
            result, loc = troop.i_training.find_screen(screen, return_location=True, show_image=False)

        if result:
            x = max(loc[0] - 30, 0)
            numbers_image = screen[0: 50, x: x + 130]
            result = troop_numbers.read_screen(numbers_image, return_number=True)
            if result > 200: result = int(result / 10)
            add_to_dict(count_dict, troop, result)

    return count_dict

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

def full_count(account):
    print("Full count - start")
    count = empty_count()
    if still_training(account, just_troops=True): return "Still training", "Still training"
    count = troops_count_flex(army_tab, ARMY_EXISTING, just_troops, count)
    count = troops_count_flex(army_tab, SPELLS_EXISTING, spells, count)
    count = troops_count_flex(army_tab, ARMY_EXISTING, siege_troops, count)
    army_count = count
    count = troops_count_flex(troops_tab, TRAINING_RANGE, just_troops, count)
    count = troops_count_flex(spells_tab, TRAINING_RANGE, spells, count)
    if account.has_siege:
        count = troops_count_flex(siege_tab, TRAINING_RANGE, siege_troops, count)

    print()
    print("Full Count:")
    print_count(count)
    return army_count, count

def troop_delete_backlog():
    goto(troops_tab)
    remaining_troops = True
    while remaining_troops:
        val, loc, rect = find_cv2("remove_troops", DELETE_REGION)
        center = pag.center(rect)
        if val > 0.65:
            for x in range(5): pag.click(center)
        else:
            remaining_troops = False

def siege_in_castle(account):
    for siege in [ram, log_thrower]:
        if siege.in_castle(): return siege

def restock(required_troops, account, extra=True):
    print("Restock")
    print(troop_str(required_troops))
    count = Counter(required_troops)
    extra_troops = []
    if extra:
        extra_troops = count.most_common()
    print("Extra:", extra)

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
    # show(screen)
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

        # print(troop.i_army.find_detail())
        # print(troop.i_train.find_detail())
        # print(troop.i_attack.find_detail())

    time.sleep(0.1)
    i_army_donate_confirm.click()
    time.sleep(0.1)
    i_army_request.click()
    time.sleep(0.1)
    i_army_request_send.click()


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

