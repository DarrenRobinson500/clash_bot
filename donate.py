from account import *
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
            if x.currently_training: continue
            show_image = False
            if x == edrag: show_image = False
            val, loc, rect = find(x.donate1, screen, text=x.name, show_image=show_image)
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
        val, loc, rect = find(troop.training, get_screenshot(BACKLOG))
        if val > 0.7:
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
                screen = get_screenshot(DONATE_AREA)
                val, loc, rect = find(x.donate2, screen, x.name)
                print(x.name, round(val, 2))
                if val > 0.65 and check_troop_colour_donate(x):
                    click(x.donate2, DONATE_AREA)
                    pag.move(755,322)
                    time.sleep(0.1)
                    x.donations += 1
                    x.currently_training = False
                    required_troops.remove(x)
            click(donate_cross)
            time.sleep(10)

def check_troop_colour_donate(troop):
    val, loc, rect = find(troop.donate2, get_screenshot(DONATE_AREA), troop.name)
    rect_adj = [rect[0] + DONATE_AREA[0], rect[1] + DONATE_AREA[1], rect[2], rect[3], ]
    colour = check_colour_rect(rect_adj, show_image=False, text=troop.name)
    return colour

def donate_go_up():
    goto(chat)
    val, loc, rect = find(more_donates, get_screenshot(DONATE_BUTTONS), show_image=False)
    print(val)
    if val > 0.65:
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
    print("Donate get required troops")
    required_troops = donate_get_required_troops(account)
    if len(required_troops) > 0:
        print("Donate - required troops:", troop_str(required_troops))
        time_required = donate_train_required_troops(account, required_troops)

        next_donation = datetime.now() + timedelta(seconds=time_required + 1)
        next_attack = next_donation + timedelta(seconds=20)
        db_update(account, "donate", next_donation)
        db_update(account, "attack", next_attack)

    if account.donating():
        queue_up_donations(account)
        db_update(account, "donate", datetime.now() + timedelta(minutes=3))

    print_total_donations()
    print_training()

def queue_up_donations(account):
    troops_to_queue = []
    for troop in troops:
        if account == account_3 and troop == edrag: continue
        if troop.donations > 0:
            for x in range(troop.donation_count):
                troops_to_queue.append(troop)
    print("Queue up donations:", troop_str(troops_to_queue))
    troops_to_queue.append(ram)
    result = army_prep(account, troops_to_queue)
    if not result:
        db_update(account, "donate", get_time_attack())

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
    for x in requests:
        click_rect(x)
        time.sleep(0.1)
        for x in troops:
            if x.donate_bool:
                screen = get_screenshot(DONATE_AREA)
                show_image = False
                if x == dragon: show_image = False
                val, loc, rect = find(x.donate2, screen, x.name, show_image=show_image)
                print("Donate:", x.name, round(val,2))
                if val > 0.65:
                    count = 0
                    colour = check_troop_colour_donate(x)
                    print(x.name, val, colour)
                    while colour and count < 10:
                        print("Donate - clicking:", x.name)
                        click(x.donate2, DONATE_AREA)
                        x.donations += 1
                        time.sleep(0.1)
                        count += 1
                        if x.type == "siege": count += 10
                        colour = check_troop_colour_donate(x)
        click(donate_cross)
        time.sleep(0.2)

def army_prep(account, troops_required):
    print("Army prep")
    # Checking if training
    goto(army_tab)
    result, loc, rect = find_cv2("army_clock", ARMY_CLOCK_SPOT)
    if result > 0.6:
        print("Army prep - still training")
        return False

    troops_to_build = []

    # Get required troops
    required_counter = Counter(troops_required)
    time.sleep(0.2)

    # Get actual troops
    actual_troops = troops_count(account)

    # Delete unneeded troops
    print("Delete unneeded troops")
    backlog_deleted = False
    for x in troops:
        try: actual = actual_troops[x]
        except: actual = 0
        required = required_counter[x]
        if actual > required:
            print("Attack prep - delete unneeded", x.name, required, actual)
            if not backlog_deleted: troop_delete_backlog()
            backlog_deleted = True
            x.delete(actual - required)

    # Create needed troops
    print("Create required troops:", required_counter)
    for x in required_counter:
        print(x)
        if x and x.type != "hero" and x.type != "siege":
            print("Troop:", x.name)
            actual = actual_troops[x]
            required = required_counter[x]
            if actual < required:
                text = f"Need more of these - make {required - actual} more"
                print("Army prep", x, required, actual, text)
                troops_to_build += [x] * (required - actual)
    print("Army prep:", troop_str(troops_to_build))
    restock(troops_to_build, extra=False)

    return

def troops_count(account, confidence=0.8):
    goto(army_tab)
    screen = get_screenshot(ARMY_EXISTING)
    troop_count_dict = {}
    for troop in troops:
        troop_count_dict[troop] = 0
        if troop.army is None:
            print("Find many img: couldn't find file:", troop.name)
            continue

        result = cv2.matchTemplate(screen, troop.army, method)
        min_val, val, min_loc, loc = cv2.minMaxLoc(result)
        if val > confidence:
            x = max(loc[0] - 30, 0)
            if troop.type == "troop":
                numbers_image = screen[0: 50, x: x + 130]
            else:
                numbers_image = screen[270: 320, x: x + 130]
            result = read_troop_count_image(numbers_image)
            try:
                result = int(result)
                if result > 150: result = int(result / 10)
            except:
                result = 0
            troop_count_dict[troop] = result
    troop_count_dict[ram] = 0
    troop_count_dict[log_thrower] = 0
    troop_count_dict[siege_in_castle(account)] = 1
    for key in troop_count_dict:
        try:
            print(key.name, '->', troop_count_dict[key])
        except:
            print(key, '->', troop_count_dict[key])

    return troop_count_dict

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

def restock(required_troops, extra=True):
    print("Restock")
    print(troop_str(required_troops))
    count = Counter(required_troops)
    extra_troops = []
    if extra:
        extra_troops = count.most_common()
    print("Extra:", extra)

    for x in count:
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
    if account == account_1:
        db_update(account_2, "donate", job_time)
    else:
        db_update(account_1, "donate", job_time)


