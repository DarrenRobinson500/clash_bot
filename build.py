from operator import attrgetter

from nav import *
from towers_load import *
from sql import *
from tracker import *

def build(account, village):
    builders = spare_builders(account, village)
    print("Build - spare builders", builders)
    if builders == 0: return
    if village == "main": goto(main)
    else: goto(builder)
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
        # print(upgrade_currency)
        upgrade_wall(upgrade_currency, select_tower_bool=False)

        return

    available_options, all_options = get_available_upgrades(village)
    if wall in available_options:
        need_walls = True
    else:
        need_walls = False
    preferences = get_preferences(available_options)

    if need_walls:
        print("Build", account, "Building walls")
        count = 1
        if account.th <= 8: count = 20
        upgrade_currency = "gold"
        if preferences[0].resource == "gold": upgrade_currency = "elixir"
        for x in range(count):
            upgrade_wall(upgrade_currency)



    for preference in preferences:
        select_tower(village, preference)
        time.sleep(0.2)
        upgrade()
        if spare_builders(account, village) == 0:
            db_update(account, "attack", datetime.now() + timedelta(minutes=2))
            return



# def get_available_upgrades(village):
#     print("Get available upgrades")
#     if village == "main": goto(main)
#     else: goto(builder)
#     goto_list_top(village)
#     available_upgrades = []
#     if village == "main": region = BUILDER_LIST_REGION
#     else: region = BUILDER_B_LIST_REGION
#     # for scroll_direction in ["up", "final"]:
#     for scroll_direction in ["up", "up", "down", "final"]:
#         screen = get_screenshot(region)
#         for tower in towers:
#             if tower.village == village:
#                 if tower not in available_upgrades:
#                     show_image = False
#                     if tower.name == "lab": show_image = False
#                     val, loc, rect = find(tower.i_text, screen, text=tower.name, show_image=show_image)
#                     print("Available upgrades", tower.name, round(val,2))
#
#                     # check tower isn't above suggested upgrades
#                     if val > 0.85:
#                         val2, loc2, rect2 = i_suggested_upgrades.find_detail()
#                         if val2 > i_suggested_upgrades.threshold:
#                             print(loc[1] + region[1], loc2[1])
#                             if loc[1] + region[1] < loc2[1]: val = 0
#
#                     # if tower.name == "wizard_tower": print("Val:", val)
#                     if val > 0.80:
#                         print("Appending")
#                         available_upgrades.append(tower)
#                         tower_region = [region[0] + rect[0], region[1] + rect[1], 480, 30]
#                         get_screenshot(tower_region, filename=f"{tower.name}")
#         if scroll_direction != "final":
#             move_list(scroll_direction, dur=2)
#             time.sleep(3)
#     available_upgrades.sort(key=lambda x: x.priority, reverse=False)
#     print("Available upgrades:", objects_to_str(available_upgrades))
#     return available_upgrades

def get_available_upgrades(village):
    print("Get available upgrades")
    if village == "main": goto(main)
    else: goto(builder)

    goto_list_top(village)
    available_upgrades = []
    all_upgrades = []
    if village == "main": region = BUILDER_LIST_REGION
    else: region = BUILDER_B_LIST_REGION
    for scroll_direction in ["up", "up", "down", "final"]:
        screen = get_screenshot(region)
        for tower in towers:
            if tower.village == village:
                if tower not in all_upgrades:
                    show_image = False
                    if tower.name == "lab": show_image = False
                    val, loc, rect = find(tower.i_text, screen, text=tower.name, show_image=show_image)
                    if val > 0.75:
                        val2, loc2, rect2 = i_suggested_upgrades.find_detail()
                        if val2 > i_suggested_upgrades.threshold:
                            # print(loc[1] + region[1], loc2[1])
                            if loc[1] + region[1] < loc2[1]: val = 0

                    if val > 0.77:
                        tower_region = [region[0] + rect[0], region[1] + rect[1], 480, 30]
                        get_screenshot(tower_region, filename="temp_tower")
                        i = cv2.imread("temp/temp_tower.png", 1)
                        all_upgrades.append(tower)
                        if has_cash_2(i):
                            available_upgrades.append(tower)
        if scroll_direction != "final":
            move_list(scroll_direction, dur=2)
            time.sleep(3)
    # print("Available upgrades (unsorted):", objects_to_str(available_upgrades))
    available_upgrades.sort(key=lambda x: x.priority, reverse=False)
    all_upgrades.sort(key=lambda x: x.priority, reverse=False)
    print("Available upgrades:", objects_to_str(available_upgrades))
    return available_upgrades, all_upgrades

def get_available_upgrades_levels(account, village):
    print("Get available upgrades with levels")
    if village == "main": goto(main)
    else: goto(builder)
    goto_list_top(village)
    available_upgrades = []
    if village == "main": region = BUILDER_LIST_REGION
    else: region = BUILDER_B_LIST_REGION
    for scroll_direction in ["up", "up", "down", "final"]:
        screen = get_screenshot(region)
        # show(screen)
        for tower in towers:
            if tower.village == village:
                show_image = False
                # if tower.name == "wizard_tower": show_image = True
                val, loc, rect = find(tower.i_text, screen, text=tower.name, show_image=show_image)
                # if tower.name == "wizard_tower": print("Val:", val)
                # print("Get available upgrades with levels", tower, val)
                if val > 0.85:
                    tower_region = [region[0] + rect[0], region[1] + rect[1] - 3, 480, 40]
                    screen_2 = get_screenshot(tower_region, filename=f"{tower.name}")
                    level, count = get_level(screen_2, tower)
                    print(tower, level, count)
                    available_upgrades.append((tower, level, count))
                    account.add_available_upgrades((tower, level, count))
                    # if account.available_upgrades
        if scroll_direction != "final":
            move_list(scroll_direction, dur=2)
            time.sleep(3)
    # available_upgrades.sort(key=lambda x: x.priority, reverse=False)
    # print("Available upgrades:", objects_to_str(available_upgrades))
    return available_upgrades

def clean_cost(string):
    string = string.replace("g", "")
    string = string.replace("h", "")
    try:
        cost = int(string)
    except:
        cost = 0
    return cost

def get_level(screen, tower):
    screen_cost = screen[:, 200:]
    screen_count = screen[:, 0:200]
    result_cost = cost_numbers.read_screen(screen_cost)
    result_count = clean_cost(cost_numbers.read_screen(screen_count))
    if result_count == 0: result_count = 1
    result_cost = clean_cost(result_cost) * 2
    result_level = None
    for level in tower.levels:
        # print(level.tower, level.level, level.gold)
        if level.gold == result_cost:
            result_level = level

    if result_level == None:
        print("Get level failure")
        # print("Printing all towers")
        # for tower_x in towers:
        #     for level_x in tower_x.levels:
        #         print(level_x.tower, level_x.level, level_x.gold)
        # print()
        # print("Problem tower details")
        print("Tower:", tower, tower.levels)
        print("Cost read from builder list:", result_cost)
        print("Available levels")
        for level in tower.levels:
            print(level.tower, level.level, level.gold)

    # print("Get level:", tower, result_cost, result_count)
    # print(result_level)
    return result_level, result_count

# print()
# screen = cv2.imread(f'temp/mortar.png',0)
# level, count = get_level(screen, mortar)
# print(mortar.name, level.days * count)



def total_build_time(village):
    available_upgrades = get_available_upgrades(village)
    print("Total build time:", objects_to_str(available_upgrades))
    # for tower in available_upgrades[0]:
    select_tower(village, available_upgrades[0])

def select_tower(village, tower):
    print("Select tower:", tower)
    goto(main)
    if village == "main": region = BUILDER_LIST_REGION
    else: region = BUILDER_B_LIST_REGION
    if check_if_tower_visible(tower, region): return
    goto_list_top(village)
    for scroll_direction in ["up", "up", "down", "final"]:
        screen = get_screenshot(region)
        val, loc, rect = find(tower.i_text, screen, show_image=False)
        print("Select tower", tower, val)
        if val > 0.8:
            click(tower.i_text, region=region)
            return True
        if scroll_direction != "final":
            move_list(scroll_direction, dur=2)
            time.sleep(3)
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
    preferences = []
    try:
        available_towers.remove(wall)
    except:
        pass
    available_towers.sort(key=lambda x: x.priority, reverse=False)
    print("Get preferences - sorted initial list:", objects_to_str(available_towers))
    if len(available_towers) == 0: return preferences
    count = 0
    while count < 5:
        preference = available_towers[0]
        preferences.append(preference)
        print("Round", count, "Available towers:", objects_to_str(available_towers))
        print("Round", count, "Preferences:", objects_to_str(preferences))
        available_towers = [x for x in available_towers if x.resource != preference.resource]
        if len(available_towers) == 0:
            for pref in preferences:
                print(pref, preference.priority)
            return preferences
        count += 1
        print("Get preferences:", preferences, count)
        print(objects_to_str(available_towers))
        print(objects_to_str(preferences))
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
    # val, loc, rect = find(i_upgrade_button, get_screenshot(SELECTED_TOWER_BUTTONS, filename="upgrade"), show_image=False)
    # print("Upgrade:", val)
    rects = find_many("upgrade", confidence=0.75)
    print("Upgrade - upgrade buttons found:", len(rects))
    if len(rects) == 0:
        rects = find_many("upgrade_2", confidence=0.75)
        print("Upgrade - upgrade2 (second attempt) buttons found:", len(rects))
    sufficient_funds = False
    print(rects)
    for rect in rects:
        region = (rect[0] - 20, rect[1] - 110, 130, 40)
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
    pag.screenshot('temp/upgrade_colour.png', region=region)
    image = cv2.imread('temp/upgrade_colour.png', 1)
    # show(image)
    new, counter = simplify(image, gradients=2)
    if counter[(128,128,0)] > 4000: return False  # This is the wall rings
    if counter[(0, 128, 128)] < 400: return True
    if counter[(0, 128, 0)] > 100 and counter[(0, 128, 128)] < 1000: return True # This is the warden
    return False

def has_cash_2(image):
    image = image[:, 0:400]
    new, counter = simplify(image, gradients=2)
    return counter[(0, 128, 128)] < 400

def combine_image_horizontal(images):
    max_height = 0
    for image in images:
        if image is None: continue
        height, width, channels = image.shape
        max_height = max(max_height, height)

    line = np.zeros((max_height, 3, 3), np.uint8)
    line.fill(255)
    combined = np.zeros((max_height, 1, 3), np.uint8)

    for image in images:
        if image is None: continue
        height, width, channels = image.shape
        if height < max_height:
            buffer = np.zeros((max_height - height, width, 3), np.uint8)
            image = np.concatenate((image, buffer), axis=0)
        combined = np.concatenate((combined, line, image), axis=1)
    combined = np.concatenate((combined, line), axis=1)

    # show(combined)
    return combined[:, 1:]

def combine_image_vertical(images):
    max_width = 0
    for image in images:
        height, width, channels = image.shape
        max_width = max(max_width, width)

    line = np.zeros((3, max_width, 3), np.uint8)
    line.fill(255)
    combined = np.zeros((1, max_width, 3), np.uint8)

    for image in images:
        height, width, channels = image.shape
        if width < max_width:
            buffer = np.zeros((height, max_width - width, 3), np.uint8)
            image = np.concatenate((image, buffer), axis=1)
        combined = np.concatenate((combined, line, image), axis=0)
    combined = np.concatenate((combined, line), axis=0)

    # show(combined)
    return combined[1:, :]

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
    header = combine_image_horizontal([header, war_banner])

    images = [header] + account_images
    result = combine_image_vertical(images)
    # show(result)
    cv2.imwrite("C:/Users/darre/OneDrive/Darren/clash_bot/tracker/builders_combined.png", result)

def get_next_completion(account, village):
    print("Get next completion")
    if village == "main": goto(main)
    else: goto(builder)
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
        excel_write(account.number, "completion", previous_completion)
        progress(account, previous_completion)
    print("Check completion", previous_completion, next_completion, result)



