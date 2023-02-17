from operator import attrgetter

from nav import *
from towers_load import *
from tracker import *
from utilities import *

buildings_to_upgrade = [
    "air_bomb", "air_defence", "air_mine", "air_sweeper", "archer_tower", "barracks", "bomb", "bomb_tower", "camp",
    "cannon", "champ", "dark_barracks", "dark_drill", "dark_spell", "spell", "eagle", "elixir_storage",
    "giant_bomb", "giga_tesla", "gold_storage", "inferno", "king", "lab", "mortar", "queen","skeleton",
    "spell", "spring_trap", "sweeper", "tesla", "tornado", "warden", "war_machine", "wizard_tower", "x-bow",
                        ]

def build_new(account, village):
    builders = spare_builders(account, village)
    print("Build - spare builders", builders)
    if builders == 0: return
    # remove_trees(village)

    desirable = buildings_to_upgrade
    if account.needs_walls and account.build_cycle < 6:
        desirable = ["wall", ]

    print("Desirable:", desirable)

    goto_list_top("main")
    region = [BUILDER_FIRST_ROW[0], BUILDER_FIRST_ROW[1], BUILDER_FIRST_ROW[2], BUILDER_FIRST_ROW[3], ]
    count, found = 0, False
    time.sleep(0.5)
    while count < 50:
        next_row = get_screenshot(region)
        # show(next_row, label=str(region[1]))
        result = build_towers.read_screen(next_row, return_y=True)
        if result[0] in desirable:
            print("Found in desirable:", result[0])
            print(result[0], region[1], count)
            pag.click(region[0] + 30, region[1] + 50)
            found = True
            break
        if result[1]:
            print(result[0], region[1], count)
            region[1] = result[1] + region[1]
            count += 1
            region[1] = region[1] + 35
        else:
            region[1] += 5
        if region[1] > 660:
            # print("Moving list")
            gap, dur = 250, 1
            pag.moveTo(855, 240 + gap)
            pag.dragTo(855, 240, dur)
            region[1] -= gap
            time.sleep(0.5)

    print("Summary", found, result[0])
    if found:
        if result[0] == "wall":
            upgrade_wall("elixir", select_tower_bool=False)
            account.build_cycle += 1
            if account.build_cycle > 5: account.build_cycle = 0
        else:
            upgrade()

        builders = spare_builders(account, village)
        if builders > 0:
            db_update(account, "build", datetime.now())

        account.attacking = True
        db_update(account, "attack", datetime.now() + timedelta(minutes=2))
        # get_castle_resources()
    return




def build(account, village="main"):
    return
    builders = spare_builders(account, village)
    print("Build - spare builders", builders)
    if builders == 0: return
    remove_trees(village)
    if account.use_suggestion_b and village == "builder":
        # print("Using suggestion")
        goto_list_top(village)
        val, loc, rect = i_suggested_upgrades.find_detail()
        pag.click(loc[0], loc[1] + 50)
        gold, elixir, dark = current_resources()
        # print("Build", gold, elixir)
        upgrade_currency = "gold"
        if elixir > gold: upgrade_currency = "elixir"
        print(upgrade_currency)
        upgrade_wall(upgrade_currency, select_tower_bool=False)

        return

    available_options, all_options = get_available_upgrades(village)
    if wall in available_options:
        need_walls = True
    else:
        need_walls = False
    preferences = get_preferences(available_options)

    print("Needs walls", need_walls)
    if need_walls:
        print("Build", account, "Building walls")
        count = 1
        if account.th <= 12: count = 2
        if account.th <= 11: count = 5
        if account.th <= 8: count = 5
        upgrade_currency = "gold"
        if preferences[0].resource == "gold": upgrade_currency = "elixir"
        print(upgrade_currency)
        for x in range(count):
            upgrade_wall(upgrade_currency)

    for preference in preferences:
        select_tower(village, preference)
        time.sleep(0.2)
        upgrade()
        if spare_builders(account, village) == 0:
            account.attacking = True
            db_update(account, "attack", datetime.now() + timedelta(minutes=2))
            get_castle_resources()
            return

def get_available_upgrades(village):
    print("Get available upgrades")
    goto_list_top(village)
    bottom_image_previous = None
    available_upgrades, all_upgrades = [], []

    at_bottom, count = False, 0
    while not at_bottom and count < 5:
        all_upgrades, available_upgrades = identify_towers(village, all_upgrades, available_upgrades)
        bottom_image_current = get_screenshot(BUILDER_BOTTOM)
        at_bottom = image_similar(bottom_image_previous, bottom_image_current)
        bottom_image_previous = bottom_image_current
        move_list("up", dur=1)
        time.sleep(.2)
        count += 1
    all_upgrades, available_upgrades = identify_towers(village, all_upgrades, available_upgrades)
    move_list("down", dur=1)
    all_upgrades, available_upgrades = identify_towers(village, all_upgrades, available_upgrades)

    available_upgrades.sort(key=lambda x: x.priority, reverse=False)
    all_upgrades.sort(key=lambda x: x.priority, reverse=False)
    print("Available upgrades:", objects_to_str(available_upgrades))

    return all_upgrades, available_upgrades

def image_similar(bottom_image_previous, bottom_image_current, confidence=0.8):
    if bottom_image_current is None or bottom_image_previous is None: return False
    result = cv2.matchTemplate(bottom_image_previous, bottom_image_current, method)
    min_val, val, min_loc, loc = cv2.minMaxLoc(result)
    print("Image similar:", val)
    return val > confidence

def identify_towers(village, all_upgrades, available_upgrades):
    if village == "main": region = BUILDER_LIST_REGION
    else: region = BUILDER_B_LIST_REGION
    screen = get_screenshot(region)
    for tower in towers:
        if tower.village == village:
            if tower not in all_upgrades:
                show_image = False
                if tower.name == "lab": show_image = False
                val, loc, rect = find(tower.i_text, screen, text=tower.name, show_image=show_image)
                print("Get available upgrades:", tower, val)
                if val > 0.75:
                    val2, loc2, rect2 = i_suggested_upgrades.find_detail()
                    if val2 > i_suggested_upgrades.threshold:
                        # print(loc[1] + region[1], loc2[1])
                        if loc[1] + region[1] < loc2[1]: val = 0

                if val > 0.80:
                    # print("Val > 0.8")
                    tower_region = [region[0] + rect[0], region[1] + rect[1], 480, 30]
                    get_screenshot(tower_region, filename="temp_tower")
                    i = cv2.imread("temp/temp_tower.png", 1)
                    all_upgrades.append(tower)
                    if tower == wall: show(i)
                    cash = has_cash_2(i)
                    print("Cash:", cash)
                    if cash:
                        available_upgrades.append(tower)
    return all_upgrades, available_upgrades

def get_all_upgrades(account, village):
    print("Get available upgrades")
    goto_list_very_top(village)
    bottom_image_previous = None
    upgrades = []

    at_bottom, count = False, 0
    while not at_bottom and count < 5:
        upgrades = identify_towers_with_levels(upgrades)
        bottom_image_current = get_screenshot(BUILDER_BOTTOM)
        at_bottom = image_similar(bottom_image_previous, bottom_image_current)
        bottom_image_previous = bottom_image_current
        move_list("up", dur=1)
        time.sleep(.2)
        count += 1
    upgrades = identify_towers_with_levels(upgrades)
    move_list("down", dur=1)
    upgrades = identify_towers_with_levels(upgrades)

    upgrades.sort(key=lambda x: x[0].priority, reverse=False)
    print("Available upgrades:")
    total_time = timedelta(days=0)
    for tower, level, count in upgrades:
        if level is None:
            print(" -", tower, count, "No level")
        else:
            remaining_time = tower.remaining_time(level.number, account.th) * count
            total_time += remaining_time
            print(" -", tower, level.number, count, "Remaining Time:", remaining_time)
    print("Total time:", total_time)
    return total_time

def identify_towers_with_levels(upgrades):
    gap = int((661 - 196) / 9)
    points = []
    for x in range(9):
        point = (600, 196 + x * gap)
        points.append(point)
    print("Points", points)

    for point in points:
        result = get_tower(point)
        if result:
            tower_region = [point[0], point[1] - gap / 2, 200, gap]
            screen = get_screenshot(tower_region, filename="temp_tower")
            # show(screen)
            count = tower_count.read_screen(screen, show_image=False, return_number=True)
            if count == 0 or count == "": count = 1

            # print(result)
            existing = next((x for x in upgrades if x[0] == result[0] and x[1] == result[1]), None)
            if not existing:
                upgrades.append((result[0], result[1], count))
    return upgrades

def get_tower(loc):
    # Level
    pag.click(loc)
    time.sleep(0.35)
    filename = f'temp/temp_read_tower.png'
    pag.screenshot(filename, region=SELECTED_TOWER)
    screen = cv2.imread(filename, 0)
    tower_name = selected_tower.read_screen(screen)
    tower = return_tower(tower_name)
    if tower is None: return
    level_int = selected_level.read_screen(screen, show_image=False, return_number=True)
    level = tower.return_level(level_int)
    print("Get Tower", tower, level, level_int)

    return tower, level, 1



def get_count(screen, tower, screen_loc):
    # Count
    screen_count = screen[:, 0:200]
    count = tower_count.read_screen(screen_count, show_image=False, return_number=True)
    if count == 0 or count == "": count = 1
    return count



def select_tower(village, tower):
    print("Select tower:", tower)
    goto(main)
    if village == "main": region = BUILDER_LIST_REGION
    else: region = BUILDER_B_LIST_REGION
    if check_if_tower_visible(tower, region): return
    goto_list_top(village)
    bottom_image_previous, at_bottom, count = None, False, 0
    while not at_bottom and count < 5:
        screen = get_screenshot(region)
        val, loc, rect = find(tower.i_text, screen, show_image=False)
        print("Select tower", tower, val)
        if val > 0.8:
            click(tower.i_text, region=region)
            return True
        bottom_image_current = get_screenshot(BUILDER_BOTTOM)
        at_bottom = image_similar(bottom_image_previous, bottom_image_current)
        bottom_image_previous = bottom_image_current
        move_list("up", dur=1)
        time.sleep(.2)
        count += 1
    return False

def check_if_tower_visible(tower, region):
    click_builder()
    screen = get_screenshot(region)
    val, loc, rect = find(tower.i_text, screen, show_image=False)
    val1, loc2 = i_suggested_upgrades.find_screen(screen, return_location=True)
    print(loc, loc2)
    if loc2[1] > loc[1]: return False
    if val > 0.85:
        click(tower.i_text, region=region)
        return True


def get_preference(available_towers):
    available_towers.sort(key=lambda x: x.priority, reverse=False)
    print("Available towers")
    for tower in available_towers:
        print(tower.name, tower.priority)
    if len(available_towers) == 0: return None
    chosen_upgrade = min(available_towers, key=attrgetter('priority'))
    print("Chosen upgrade:", chosen_upgrade)
    return chosen_upgrade

def get_preferences(available_towers):
    available_towers.sort(key=lambda x: x.priority, reverse=False)
    if wall in available_towers: available_towers.remove(wall)
    print("Get preferences (initial list):", objects_to_str(available_towers))

    preferences = []
    if len(available_towers) == 0: return preferences
    count = 0
    while count < 5:
        preference = available_towers[0]
        preferences.append(preference)
        # print("Round", count, "Available towers:", objects_to_str(available_towers))
        # print("Round", count, "Preferences:", objects_to_str(preferences))
        available_towers = [x for x in available_towers if x.resource != preference.resource]
        if len(available_towers) == 0:
            print("Get preferences (preferences):", objects_to_str(preferences))
            return preferences
        count += 1
    return preferences

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
    while not builders and count < 65:
        time.sleep(1)
        val, loc, rect = find_cv2("builder_zero", region)
        # print("Remove tree - Zero Builder Val:", val)
        if val < 0.8:
            builders = True
        else:
            builders = False
        count += 1

def remove_trees(village):
    zoom_out()
    for letter in ['w', 's']:
        hold_key(letter, 0.5)
        rects = find_many_array(BUSHES, confidence=0.82)
        # print(len(rects))
        for r in rects:
            remove_tree(r, village)

def upgrade():
    rects = i_upgrade_button.find_many()
    print("Upgrade - upgrade buttons found:", len(rects))
    if len(rects) == 0:
        rects = find_many("upgrade_2", confidence=0.75)
        print("Upgrade - upgrade2 (second attempt) buttons found:", len(rects))
    if len(rects) == 0:
        rects = find_many("upgrade_3", confidence=0.75)
        print("Upgrade - upgrade3 (third attempt) buttons found:", len(rects))

    sufficient_funds = False
    print(rects)
    for rect in rects:
        region = (rect[0] - 20, rect[1] - 50, 130, 40)
        image = get_screenshot(region)
        show(image)
        result = has_cash(region)
        if result:
            sufficient_funds = True
            print("Clicking")
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

def upgrade_wall(currency, select_tower_bool=True):
    if select_tower_bool:
        select_tower("main", wall)
    result = i_upgrade_button.find_many(show_image=False)
    result = sorted(result, key=lambda x: x[0])
    print("Upgrade wall result:", result)
    if len(result) == 0:
        print(result)
        return False
    elif len(result) == 1:
        currency = "gold"
    if currency == "gold": rectangle = result[0]
    else: rectangle = result[1]
    spot = int(rectangle[0] + rectangle[2] / 2), int(rectangle[1] + rectangle[3] / 2)
    print(spot)
    pag.click(spot)
    time.sleep(0.1)
    pag.click((933, 877))
    return True

def has_cash(region):
    # Warden: Counter({(128, 128, 128): 3475, (0, 128, 128): 949, (0, 0, 0): 814, (0, 128, 0): 159, (0, 0, 128): 3})
    # Mortar: Counter({(128, 128, 128): 4093, (0, 0, 0): 924, (0, 128, 128): 131, (0, 128, 0): 52})
    # Wall (inadequate cash): Counter({(128, 128, 128): 3818, (0, 0, 0): 668, (0, 128, 128): 416, (0, 0, 128): 298})
    # Queen (adequate cash): Counter({(128, 128, 128): 3495, (0, 0, 0): 910, (0, 128, 128): 576, (0, 0, 128): 185, (0, 128, 0): 30, (128, 0, 128): 4})
    pag.screenshot('temp/upgrade_colour.png', region=region)
    image = cv2.imread('temp/upgrade_colour.png', 1)
    # show(image)
    new, counter = simplify(image, gradients=2)
    print(counter)
    if counter[(128,128,0)] > 4000: return False  # This is the wall rings
    if counter[(0, 128, 128)] < 400: return True
    if counter[(0, 128, 0)] > 100 and counter[(0, 128, 128)] < 1000: return True # This is the warden
    if counter[(0, 0, 0)] > 800 and counter[(0, 128, 128)] < 600: return True # This is the queen
    return False

def has_cash_2(image):
    image = image[:, 0:400]
    # show(image)
    new, counter = simplify(image, gradients=2)

    print(counter)
    return counter[(0, 128, 128)] < 400

def create_combined_builders_image(accounts):
    account_images = []
    max_width = 0
    for account in accounts:
        no = account.number
        i1 = cv2.imread(f'temp/tracker/builders{no}main.png', 1)
        i2 = cv2.imread(f'temp/tracker/builder_time{no}main.png', 1)
        i3 = cv2.imread(f'temp/tracker/gold{no}.png', 1)
        i4 = cv2.imread(f'temp/tracker/research_time{no}main.png', 1)
        i5 = cv2.imread(f'temp/tracker/trader_clock_potion{no}.png', 1)
        i6 = cv2.imread(f'temp/tracker/trader_research_potion{no}.png', 1)
        i7 = cv2.imread(f'temp/tracker/builders{no}builder.png', 1)
        i8 = cv2.imread(f'temp/tracker/builder_time{no}builder.png', 1)
        i9 = cv2.imread(f'temp/tracker/remaining_attacks{no}.png', 1)

        i4 = cv2.resize(i4, (0, 0), fx=.65, fy=.65)
        i5 = cv2.resize(i5, (0, 0), fx=.25, fy=.25)
        i6 = cv2.resize(i6, (0, 0), fx=.25, fy=.25)

        combined = combine_image_horizontal([i1, i2, i3, i4, i5, i6, i7, i8, i9])
        account_images.append(combined)
        max_width = max(max_width, combined.shape[1])

    header = np.zeros((50, 200, 3), np.uint8)
    x = datetime.now().strftime("%I:%M") + datetime.now().strftime("%p").lower()
    cv2.putText(header, x, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    war_banner = cv2.imread(f'temp/tracker/war_banner.png', 1)
    war_banner = cv2.resize(war_banner, (0, 0), fx=.65, fy=.65)
    header = combine_image_horizontal([header, war_banner])

    images = [header] + account_images
    result = combine_image_vertical(images)
    # show(result)
    cv2.imwrite("C:/Users/darre/OneDrive/Darren/clash_bot/tracker/builders_combined.png", result)

def get_next_completion(account, village):
    print("Get next completion")
    if spare_builders(account, village) > 0: return
    goto_list_very_top(village)
    if i_upgrades_in_progress.find():
        pag.click(570,250)
        time.sleep(0.15)
        pag.screenshot('temp/temp_read_tower.png', region=SELECTED_TOWER)
        screen = cv2.imread('temp/temp_read_tower.png', 0)
        level = selected_level.read_screen(screen, show_image=False)
        tower = selected_tower.read_screen(screen, show_image=False)
        # print("Get next completion:", tower, level)
        if level == "": level = None
        excel_write(account.number, "next_completion", (tower, level))
        return tower, level
    else:
        return None, None

def check_completion(account):
    if spare_builders(account, "main") == 0: return
    previous_completion = excel_read(account.number, "next_completion")
    next_completion = get_next_completion(account, "main")
    print("Check completion (next completion):", next_completion)
    result = "No result"
    if previous_completion == (None, None): result = "No previous result"
    elif previous_completion == next_completion: result = "No change"
    elif previous_completion != next_completion:
        result = f"Completed: {previous_completion[0]} level: {previous_completion[1]}"
        # excel_write(account.number, "completion", previous_completion)
        # progress(account, previous_completion)
    print("Check completion", previous_completion, next_completion, result)

def get_castle_resources():
    global current_location
    goto(l_castle)
    for i in [i_treasury, i_collect_castle, i_okay3]:
        time.sleep(0.2)
        i.click()
    current_location = main
