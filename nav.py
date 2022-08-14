from object_recognition import *
from ocr import read_text

current_location = None

# === 1. ACCOUNTS AND NAVIGATION ===
def current_resources():
    time.sleep(1)
    result_array = []
    for x in [RESOURCES_G, RESOURCES_E, RESOURCES_D]:
        result_array.append(read_text(x, WHITE, True))
    if result_array[0] > 20000000: result_array[0] = result_array[0]/10
    # print("Current Resources:", result_array)
    return result_array



def change_accounts(account, target_base="main"):
    global current_account
    print("Change accounts")
    if account != current_account:
        if account == 1: loc = (1184, 651)
        elif account == 3: loc = (1184, 792)
        elif account == 2: loc = (1184, 524)
        else: return
        goto("switch_account")
        pag.click(loc)
        time.sleep(0.2)

        wait_many_result = wait_many([("main", BUILDER_REGION), ("master", BUILDER_B_REGION), ("otto", BUILDER_B_REGION), ("okay", OKAY_SPOT)])
        if wait_many_result == False:
            goto("main")
            return
        if find_cv2("okay")[0] > 0.5:
            click_cv2("okay")
            time.sleep(2)
    goto(target_base)
    zoom_out()
    current_account = account
    if info['gold'][account-1] is None:
        resources = current_resources()
        info['gold'][account-1] = resources
    return


def start():
    click_cv2('bluestacks_icon')
    time.sleep(.2)
    pag.moveTo(1000,500)
    pag.keyDown('ctrl')
    for x in range(5):
        pag.scroll(-100)
    pag.keyUp('ctrl')

def end():
    click_cv2("pycharm")

NON_DESTINATIONS = [
    # location and image, region
    ("okay", OKAY_SPOT),
    ("war_okay", ALL),
    ("donate", ALL),
    ("attacking", ATTACKING_SPOT),
    ("log_in_with_supercell", SUPERCELL_LOGIN_SPOT),
    # ("splash", ALL),
    ("return_home", ALL),
    ("return_home_2", RETURN_HOME_2_SPOT),
    ("reload_game", RELOAD_SPOT),
    ("reload", RELOAD_SPOT),
    ("try_again", RELOAD_SPOT),
    ("red_cross", ALL),
    ("bluestacks_message", ALL),
    ("bluestacks_app", BLUESTACKS_APP_SPOT),
    ("maintenance", MAINTENANCE_SPOT),
    ("pycharm_running", PYCHARM_RUNNING_SPOT),
    ("raid_weekend", RAID_WEEKEND_NEXT_SPOT),
    ("raid_weekend2", RAID_WEEKEND_NEXT_SPOT),
]

DESTINATIONS = [
    # location and image, region
    ("chat", CHAT_SPOT),
    ("main", BUILDER_REGION),
    ("builder", BUILDER_B_REGION),
    ("otto", BUILDER_B_REGION),
    ("army_tab", ARMY_TABS),
    ("troops_tab", ARMY_TABS),
    ("spells_tab", ARMY_TABS),
    ("siege_tab", ARMY_TABS),
    ("attack", ATTACK_SPOT),
    ("find_a_match", FIND_A_MATCH_SPOT),
    ("switch_account", SWITCH_ACCOUNT_SPOT),
    ("settings", ALL),
    ("forge", FORGE_SPOT),
    ("attack_b", ATTACK_B_SPOT),
]

LOCATION_OVERLAYS = [
    ("reload_game", RELOAD_SPOT),
    ("reload", RELOAD_SPOT),
    ("bluestacks_message", BLUESTACKS_MESSAGE_SPOT),
    ("chat", CHAT_SPOT),
    ("forge", FORGE_SPOT),
    ("try_again", RELOAD_SPOT),
    ("red_cross", ALL),
    ("bluestacks_app", BLUESTACKS_APP_SPOT),
    ("log_in_with_supercell", SUPERCELL_LOGIN_SPOT),
    ("find_a_match", FIND_A_MATCH_SPOT),
    ("battle_end_b1", ALL),
    # ("battle_end_b2", ALL),
]

LOCATIONS = [
    # location and image, region
    ("main", BUILDER_REGION),
    ("builder", BUILDER_B_REGION),
    ("otto", BUILDER_B_REGION),
    ("army_tab", ARMY_TABS),
    ("troops_tab", ARMY_TABS),
    ("spells_tab", ARMY_TABS),
    ("siege_tab", ARMY_TABS),
    ("attack", ATTACK_SPOT),
    ("switch_account", SWITCH_ACCOUNT_SPOT),
    ("settings", ALL),
    ("attack_b", ATTACK_B_SPOT),
    ("attacking_b", ATTACKING_B_SPOT),
    ("battle_end_b1", ALL),
    # ("battle_end_b2", ALL),
    ("okay", OKAY_SPOT),
    ("war_okay", ALL),
    ("donate", ALL),
    ("return_home", ALL),
    ("return_home_2", RETURN_HOME_2_SPOT),
    ("maintenance", MAINTENANCE_SPOT),
    ("attacking", ATTACKING_SPOT),
    ("pycharm_running", PYCHARM_RUNNING_SPOT),
    ("raid_weekend", RAID_WEEKEND_NEXT_SPOT),
    ("raid_weekend2", RAID_WEEKEND_NEXT_SPOT),
]

PATHS = {
    # current|destination: next action
    "main|chat": "c",
    'main|donate': 'c',
    "main|army_tab": "army",
    "main|troops_tab": "army",
    "main|spells_tab": "army",
    "main|siege_tab": "army",
    "main|settings": "settings",
    "main|switch_account": "settings",
    'main|attack': 'attack',
    'main|find_a_match': 'attack',
    'main|attacking': 'attack',
    'main|forge': 'forge_path',
    'main|builder': 'boat_to_builder',
    'main|attack_b': 'boat_to_builder',
    'main|attacking_b': 'boat_to_builder',

    'chat|donate': 'donate',
    'chat|other': 'esc',

    'army_tab|troops_tab': 'troops_tab_dark',
    'army_tab|spells_tab': 'spells_tab_dark',
    'army_tab|siege_tab': 'siege_tab_dark',
    'army_tab|other': 'esc',

    'troops_tab|army_tab': 'army_tab_dark',
    'troops_tab|spells_tab': 'spells_tab_dark',
    'troops_tab|siege_tab': 'siege_tab_dark',
    'troops_tab|other': 'esc',

    'spells_tab|army_tab': 'army_tab_dark',
    'spells_tab|troops_tab': 'troops_tab_dark',
    'spells_tab|siege_tab': 'siege_tab_dark',
    'spells_tab|other': 'esc',

    'siege_tab|army_tab': 'army_tab_dark',
    'siege_tab|troops_tab': 'troops_tab_dark',
    'siege_tab|spells_tab': 'spells_tab_dark',
    'siege_tab|other': 'esc',

    'attack|find_a_match': 'find_a_match',
    'attack|attacking': 'find_a_match',
    'attack|other': 'esc',

    'find_a_match|attacking': 'find_a_match',
    'find_a_match|other': 'end_battle',

    'attacking|other': 'end_battle',

    'settings|switch_account': 'switch',
    'settings|other': 'esc',

    'switch_account|other': 'esc',

    'forge|other': 'esc',

    'builder|attack_b': 'attack_b',
    'builder|chat': 'c',
    'builder|settings': 'settings',
    'builder|switch_account': 'settings',
    'builder|attacking_b': 'attack_b',
    'builder|other': 'boat_to_main',

    'otto|attack_b': 'attack_b',
    'otto|chat': 'c',
    'otto|settings': 'settings',
    'otto|switch_account': 'settings',
    'otto|other': 'boat_to_main',

    'attack_b|attacking_b': 'find_now_b',
    'attack_b|other': 'esc',
    'battle_end_b1|other': 'esc',
    'battle_end_b2|other': 'esc',

    'unknown|other': 'wait',

    'reload_game|other': 'reload_game',
    'reload|other': 'reload',
    'red_cross|other': 'red_cross',
    'okay|other': 'okay',
    'war_okay|other': 'war_okay',
    'try_again|other': 'try_again',
    'return_home|other': 'return_home',
    'return_home_2|other': 'return_home_2',
    'bluestacks_message|other': 'bluestacks_message',
    'log_in_with_supercell|other': 'log_in_with_supercell',
    'maintenance|other': 'reload_maintenance',
    'bluestacks_app|other': 'bluestacks_app',
    'pycharm_running|other': 'bluestacks_icon',

    'raid_weekend|other': 'next',
    'raid_weekend2|other': 'raid_weekend_okay',

}

NEEDS_DELAY = ["reload_game", "reload", "red_cross", "okay", "war_okay", "try_again", "return_home","return_home_2", "bluestacks_message",]

def loc(guess="main"):
    global current_location
    # print(f"Loc - current location: '{current_location}'")
    for location, region in LOCATION_OVERLAYS:
        val, loc, rect = find_cv2("nav/" + location, region)
        if val > 0.65:
            current_location = location
            # print("Loc (overlay):", location, "- found:", val, region)
            return location
        else:
            # print("Loc (overlay):", location, "- not found:", val, region)
            pass

    if guess in ["Unknown", "", "wait",]:
        guess = None
    if guess in ["army_tab", "troops_tab", "spells_tab", "siege_tab"]:
        region = ARMY_TABS
    elif guess in ["main", ]:
        region = BUILDER_REGION
    elif guess in ["otto", "builder"]:
        region = BUILDER_B_REGION
    else:
        region = ALL
    if guess:
        val, loc, rect = find_cv2("nav/" + guess, region)
        if val > 0.69:
            # print("Loc:", guess, val)
            if guess == "otto": guess = "builder"
            return guess
        # else:
        #     print(f"Loc: guess failure '{guess}':", find_cv2("nav/" + guess, region)[0])

    start_time = datetime.now()
    prev_time = datetime.now()
    for location, region in LOCATIONS + LOCATION_OVERLAYS:
        val, loc, rect = find_cv2("nav/" + location, region)
        if val > 0.65:
            if location == "otto": location = "builder"
            if location == "attacking":
                val, loc, rect = find_cv2("nav/" + "find_a_match", FIND_A_MATCH_SPOT)
                if val > 0.65: location = "find_a_match"
            current_location = location
            # print("Loc:", location, "- found")
            return location
        # else:
            # print("Loc:", location, "- not found:", val, region)
        current_time = datetime.now()
        # print("Loc", location, current_time-prev_time, current_time-start_time)
        prev_time = datetime.now()
    # print("Loc: Unknown")
    return "Unknown"

def next_step(location, destination):
    if location == destination:
        return "None"
    map_question = f"{location}|{destination}"
    try:
        result = PATHS[map_question]
    except:
        map_question = f"{location}|other"
        try:
            result = PATHS[map_question]
        except:
            result ="Unknown path"
            result = "No path"
    # print(f"Next step: {location} => {destination}: {result}" )
    return result

def track_loc():
    while True:
        print(loc(current_location))
        time.sleep(1)

def goto(destination):
    global current_location
    print(f"Goto: {destination} (Guess: {current_location})")
    current_location = loc(current_location)
    if current_location == destination: return True
    not_there = True
    while not_there:
        next = next_step(current_location, destination)
        move(next)
        time.sleep(0.1)
        current_location = loc(current_location)
        if current_location == destination: not_there = False


def move(code):
    global current_location
    print("Move:", code)
    if code in ["reload"]:
        click_cv2("pycharm")
        rest_time = 10 # in response to personal break - which requires a shield => hopefully enough time to be attacked
        for x in range(rest_time):
            print(f"Resting {x} of {rest_time} minutes")
            time.sleep(60)
        start()
    if code in ["bluestacks_icon"]:
        time.sleep(5)
    if code in ["army", "army_tab", "army_tab_dark", "troops_tab", "spells_tab", "siege_tab", "troops_tab_dark",
                "spells_tab_dark", "siege_tab_dark", "settings", "switch", "attack", "attack_b", "find_a_match",
                "end_battle", "reload_game", "reload", "red_cross", "okay", "war_okay", "try_again", "return_home",
                "return_home_2", "log_in_with_supercell", "bluestacks_app", "pycharm", "next", "raid_weekend_okay",
                "bluestacks_icon", "find_now_b"]:
        val, success = click_cv2(code)
        print("Move", code, val, success)
        if code == "attack" and not success:
            print("attack 2nd option")
            pag.click(100, 900)
        if code == "siege_tab_dark" and not success:
            print("Resetting account")
            change_accounts(1, "main")
    elif code in ["c", "esc"]:
        pag.press(code)
    elif code == 'forge_path':
        pag.click(BOTTOM_LEFT)
        pag.drag(250, -450, 0.5, button='left')
        val, loc, rect = find_cv2("capital_coin1")
        print("Move (forge_path) capital_coin1", val)
        if find_cv2("forge_path")[0] > 0.5:
            click_cv2("forge_path", confidence=0.5)
            current_location = "forge"
        elif find_cv2("capital_coin")[0] > 0.5:
            click_cv2("capital_coin", confidence=0.5)
            current_location = "forge"
        elif find_cv2("capital_coin1")[0] > 0.5:
            click_cv2("capital_coin1", confidence=0.5)
            current_location = "forge"
    elif code == "boat_to_builder":
        zoom_out()
        val, loc, rect = find_cv2('boat')
        if val > 0.55:
            click_rect(rect)
            return
        pag.click(BOTTOM_LEFT)
        pag.drag(250, -450, 0.5, button='left')
        click_cv2('boat', confidence=0.55)
    elif code == "boat_to_main":
        zoom_out()
        pag.click(TOP_RIGHT)
        pag.drag(-250, 400, 0.5, button='left')
        # val, loc, rect = find_cv2('boat')
        # if val > 0.6:
        #     click_rect(rect, BOAT_B_SPOT)
        # else:
        pag.click(1212,384)
        time.sleep(1.5)
        current_location = "main"
    elif code == "bluestacks_message":
        pag.click(1872,823)
    elif code in ["Unknown", "", "wait",]:
        time.sleep(1)
    elif code == "reload_maintenance":
        click_cv2("pycharm")
        count = 5
        while count >= 1:
            print(f"Maintenance. Trying again in {count} minutes")
            time.sleep(60)
            count -= 1
        start()
        click_cv2("reload_maintenance")
        time.sleep(60)
    else:
        print("Code not coded")
    if code in NEEDS_DELAY:
        time.sleep(3)
    if code == "esc":
        if current_location == "battle_end_b": current_location = "builder"
    if code in ["settings", "attack",]:
        current_location = code
    if code == "army_tab_dark": current_location = "army_tab"
    if code == "spells_tab_dark": current_location = "spells_tab"
    if code == "siege_tab_dark": current_location = "siege_tab"

    if code == "army": current_location = "army_tab"
    if code == "switch": current_location = "switch_account"
    if code == "find_a_match": current_location = "find_a_match"
    if code == "end_battle": current_location = "war_okay"
    if code == "war_okay": current_location = "return_home"
    if code == "log_in_with_supercell":
        current_location = "switch_account"
        time.sleep(2)
        pag.click(1184, 651)
        global current_account
        current_account = 1

    if code == "No path":
        time.sleep(3)

def test_goto(destination):
    # reset()

    click_cv2('bluestacks_icon')
    time.sleep(0.2)
    # pag.click(85, 1000)
    # print(find_cv2("nav/" + 'switch_account', ARMY_TABS))
    goto(destination)
    click_cv2("pycharm")

def test_next_step(current):
    for loc1, region1 in [(current, ALL),]:
        for loc2, region2 in DESTINATIONS:
            print(f"'{loc1}|{loc2}': '{next_step(loc1, loc2)}',")

def zoom_out():
    time.sleep(1)
    for x in range(1):
        pag.keyDown('ctrl')
        time.sleep(0.1)
        pag.scroll(-300)
        time.sleep(0.1)
        pag.keyUp('ctrl')
        time.sleep(0.1)

def hold_key(letter, dur):
    pag.keyDown(letter)
    time.sleep(dur)
    pag.keyUp(letter)

def attack_b_get_screen():
    goto("attacking_b")
    time.sleep(1)
    zoom_out()
    hold_key('s', 0.5)
    time.sleep(1)
    zoom_out()
    pag.screenshot('temp/attacking_b.png')


