from operator import attrgetter

from nav import *
from towers_load import *


def get_available_upgrades(village):
    print("Get available upgrades")
    if village == "main": goto(main)
    else: goto(builder)
    goto_list_top(village)
    available_upgrades = []
    if village == "main": region = BUILDER_LIST_REGION
    else: region = BUILDER_B_LIST_REGION
    for _ in range(2):
        screen = get_screenshot(region)
        for tower in towers:
            if tower.village == village:
                if tower not in available_upgrades:
                    show_image = False
                    # if tower.name == "wizard_tower": show_image = True
                    val, loc, rect = find(tower.i_text, screen, text=tower.name, show_image=show_image)
                    # if tower.name == "wizard_tower": print("Val:", val)
                    if val > 0.85:
                        available_upgrades.append(tower)
                        tower_region = [region[0] + rect[0], region[1] + rect[1], 480, 30]
                        get_screenshot(tower_region, filename=f"{tower.name}")
        move_list("up", dur=2)
        time.sleep(3)
    available_upgrades.sort(key=lambda x: x.priority, reverse=False)
    print("Available upgrades:", objects_to_str(available_upgrades))
    return available_upgrades

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
    goto_list_top(village)
    if village == "main": region = BUILDER_LIST_REGION
    else: region = BUILDER_B_LIST_REGION
    for _ in range(3):
        screen = get_screenshot(region)
        val, loc, rect = find(tower.i_text, screen, show_image=False)
        if val > 0.85:
            click(tower.i_text, region=region)
            return True
        move_list("up", dur=2)
        time.sleep(3)
    return False

def get_preference(available_towers):
    available_towers.sort(key=lambda x: x.priority, reverse=False)
    print("Available towers")
    for tower in available_towers:
        print(tower.name, tower.priority)
    if len(available_towers) == 0: return None
    chosen_upgrade = min(available_towers, key=attrgetter('priority'))
    print("Chosen upgrade:", chosen_upgrade)
    return chosen_upgrade

def objects_to_str(objects):
    string = ""
    for x in objects:
        try:
            string += x.name + ", "
        except:
            pass
    return string[0:-1]

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
    while not builders and count < 10:
        time.sleep(1)
        val, loc, rect = find_cv2("builder_zero", region)
        print("Remove tree - Builder Available Val", val)
        if val < 0.8:
            builders = True
        else:
            builders = False
        count += 1

def remove_trees(village):
    zoom_out()
    # for letter in ['w', 's']:
    #     hold_key(letter, 0.5)
    rects = find_many_array(BUSHES, confidence=0.80)
    for r in rects:
        remove_tree(r, village)

def upgrade():
    val, loc, rect = find(i_upgrade_button, get_screenshot(SELECTED_TOWER_BUTTONS, filename="upgrade"), show_image=False)
    print("Upgrade:", val)
    rects = find_many("upgrade", confidence=0.75)
    print("Upgrade:", type(rects))
    print("Upgrade - upgrade buttons found:", len(rects))
    if len(rects) == 0:
        rects = find_many("upgrade_2", confidence=0.75)
        print("Upgrade - upgrade 2 buttons found:", len(rects))
    sufficient_funds = False
    print(rects)
    for rect in rects:
        region = (rect[0] - 20, rect[1] - 110, 130, 40)
        result = has_cash(region)
        print("Upgrade:", result)
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

def has_cash(region):
    # Warden: Counter({(128, 128, 128): 3475, (0, 128, 128): 949, (0, 0, 0): 814, (0, 128, 0): 159, (0, 0, 128): 3})
    # Mortar: Counter({(128, 128, 128): 4093, (0, 0, 0): 924, (0, 128, 128): 131, (0, 128, 0): 52})

    pag.screenshot('temp/upgrade_colour.png', region=region)
    image = cv2.imread('temp/upgrade_colour.png', 1)
    # show(image)
    new, counter = simplify(image, gradients=2)
    print(region)
    print(counter)
    print(counter[(0, 128, 128)])
    if counter[(128,128,0)] > 4000: return False  # This is the wall rings
    if counter[(0, 128, 128)] < 800: return True
    if counter[(0, 128, 0)] > 100 and counter[(0, 128, 128)] < 1000: return True # This is the warden
    return False


# current_account = 1
#
# available_towers = get_available_upgrades("main")
# goto(pycharm)
#
# print("Available upgrades:")
# for tower in available_towers:
#     print(" -", tower.name)
#

# goto(main)
# time.sleep(1)
# click_builder()
# time.sleep(1)
# pag.click(691,108)
# time.sleep(1)
# goto(pycharm)