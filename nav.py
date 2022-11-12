import psutil

from ocr import *
from images import *
from regions import *

ICONS = (300, 1012, 1200, 62)
TOP_LEFT = (0,0,300,100)
TOP_MIDDLE = (700,0,700,300)

locs = []
latest_path = None

def most_common(list, number):
    if len(list) == 0: return None
    number = min(number, len(list))
    data = Counter(list).most_common(number)
    number = min(number, len(data))
    return data[number - 1][0]

def hold_key(key, dur):
    pag.keyDown(key)
    time.sleep(dur)
    pag.keyUp(key)

class Loc():
    def __init__(self, name, identifier=None, optional=False, accessible=True):
        self.name = name
        self.accessible = accessible
        self.identifiers = [identifier, ]
        self.paths = []
        self.default_path = None
        self.height = 0
        self.id_absence = False
        self.optional=optional
        locs.append(self)

    class Path():
        def __init__(self, loc, destination, action, parameter, expected_loc, region=None):
            self.loc = loc
            self.destination = destination
            self.action = action
            self.parameter = parameter
            self.expected_loc = expected_loc
            self.actual_locs = []
            self.region = region
            loc.paths.append(self)
            # Load the image for clicks
            self.image = None
            # if action in ["click", "click_p", "pycharm_to_main"]:
            #     self.image = self.convert_parameter_to_image(parameter)

        # def format(self):
        #     return f"Path: {self.loc.name} -> {self.destination.name}"
        #
        def __str__(self):
            return f"Path: {self.loc.name} -> {self.destination.name} ({self.expected_loc})"

        def add_actual_loc(self, loc):
            if loc not in self.actual_locs:
                self.actual_locs = [loc] + self.actual_locs[0:10]

        def most_common_actuals(self):
            list = self.actual_locs
            actuals = []
            for x in range(1, 3):
                result = most_common(list, x)
                if result: actuals.append(result)
            return actuals

        def convert_parameter_to_image(self, parameter):
            path = f'images/nav/{parameter}.png'
            try:
                parameter = cv2.imread(path, 0)
                return parameter
            except:
                print(f"Creating location: could not find {path}")

    def __str__(self):
        if self.name:
            return f"{self.name}"
        else:
            return "No name"

    # def add_regions(self, regions):
    #     self.regions += regions
    #
    # def show_regions(self, dur=5000):
    #     goto(self)
    #     screen = get_screenshot(colour=1)
    #     for x, y, w, h in self.regions:
    #         cv2.rectangle(screen, (x, y), (x + w, y + h), 255, 5)
    #     show(screen, scale=0.7, dur=dur)
    #
    def print_loc(self):
        print("Location:", self.name)
        for x in self.paths:
            print(" -", x)
            if x.actual_locs:
                for y in x.actual_locs:
                    print("   -", y.name)

    def add_path(self, destination, action, parameter, expected_loc, region=None):
        self.Path(loc=self, destination=destination, action=action, parameter=parameter, expected_loc=expected_loc, region=region)

    def add_default_path(self, action, parameter, expected_loc, region=None):
        new_path = self.Path(loc=self, destination=unknown, action=action, parameter=parameter,
                             expected_loc=expected_loc, region=region)
        self.default_path = new_path

    def add_identifier(self, image):
        self.identifiers.append(image)

    def add_height(self, height):
        self.height = height

    def perform_action(self, path):
        action = path.action
        parameter = path.parameter
        image = path.image
        expected_loc = path.expected_loc
        region = path.region

        global current_location
        global latest_path

        # print("Perform action:", action, parameter)
        outcome = False
        if action == "click":
            path.parameter.click()
            # print("Click:", round(val,2))
        elif action == "click_p":
            time.sleep(0.1)
            path.parameter.click()
            # print("Click p:", round(val,2))
            time.sleep(0.2)
        elif action == "pycharm_to_main":
            time.sleep(0.1)
            path.parameter.click()
            # val, outcome = click(image, region=region)
            time.sleep(0.4)
            hold_key("down", 0.3)
        elif action == "click_identifier":
            self.identifiers[0].click()
            # val, outcome = click(self.identifier_images[0])
            # print("Clicking identifier:", val)
        elif action == "reload":
            close_app()
            # click_cv2("pycharm")
            rest_time = 20
            for x in range(rest_time):
                print(f"Resting {x} of {rest_time} minutes")
                pag.moveTo(x * 10, 500)
                time.sleep(60)
            click_cv2('nav/bluestacks')
            wait_and_click('start_barb')
            wait_and_click('start_cross')
            wait_and_click('maximise')
            outcome = True
        elif action == "key":
            pag.press(parameter)
            outcome = True
        elif action == "key_p":
            time.sleep(0.1)
            pag.press(parameter)
            time.sleep(0.1)
            outcome = True
        elif action == "wait":
            time.sleep(parameter)
            outcome = True
        elif action == "goto_forge":
            hold_key("a", 0.1)
            hold_key("s", 0.1)
            val, outcome = click_cv2("nav/forge_button")
        elif action == "goto_builder":
            hold_key("a", 0.1)
            hold_key("s", 0.1)
            val, outcome = click_cv2("nav/boat_to")
        elif action == "goto_lab":
            pag.click(BOTTOM_LEFT)
            for i_lab in labs:
                val, x, rect = i_lab.find_detail(fast=False, show_image=False)
                if val > i_lab.threshold:
                    i_lab.click()
                    time.sleep(0.2)
                    i_research.click()
                    time.sleep(0.2)
                    break
        elif action == "goto_main":
            hold_key("w", 0.1)
            hold_key("d", 0.1)
            val, outcome = click_cv2("nav/boat_to")
        elif action == "start_bluestacks":
            os.startfile("C:\Program Files (x86)\BlueStacks X\BlueStacks X.exe")
            wait_and_click('heart')
            wait_and_click('start_barb')
            i_ad_cross.click()
            wait_and_click('maximise')
            outcome = True
        elif action == "start_app":
            click_cv2('nav/bluestacks')
            wait_and_click('start_barb')
            i_ad_cross.click()
            wait_and_click('maximise')
            outcome = True
        elif action == "log_in":
            self.identifiers[0].click()
            # val, outcome = click(self.identifier_images[0])
            # print("Clicking identifier:", val)
            time.sleep(0.5)
            pag.click((1184, 651))
            # current_location = change_account
            # change_accounts(1)
        else:
            print("Action not coded:", action)
            return False

        # Validate location, and store unusual outcomes
        for identifier in expected_loc.identifiers:
            identifier.wait()
        current_location = loc(expected_loc)
        # print("Current location:", current_location)
        # if current_location != expected_loc:
        #     print()

        if current_location != expected_loc and current_location != unknown and path.destination != unknown:
            path.add_actual_loc(current_location)
            print(f"Actual outcome added: {path.loc.name} -> {path.destination.name}. Actual: {current_location.name}")
            for x in path.actual_locs:
                print("   ", x.name)

        latest_path = path
        return outcome

    def goto(self, destination):
        global current_location
        # print(f"Loc goto: {current_location} -> {destination}")
        path_found = False
        path = [path for path in self.paths if path.destination == destination]
        if path:
            # print(f"Goto Loc: {self.name}. {path[0]}")
            self.perform_action(path[0])
        if not path and self.default_path:
            # for x in self.paths:
            #     print(x)
            # print("Using default path. Going to", destination)
            # print(f"Goto Loc (Default): {self.name}. {self.default_path}")
            path_found = self.perform_action(self.default_path)
        return path_found

    def has_path(self, destination):
        global current_location
        # print(f"Has path: {self} -> {destination}")
        path_found = False
        path = [path for path in self.paths if path.destination == destination]
        if path: return True
        if self.default_path: return True
        print("No path found:")
        for x in self.paths:
            print(x)
        return False


# -------------------
# ---- LOCATIONS ----
# -------------------

pycharm = Loc(name="pycharm", identifier=i_pycharm, accessible=True)
pycharm.height = -1
no_app = Loc(name="no_app", identifier=i_app, accessible=False)
no_app.id_absence = True
no_app.id_val_max = 0.8
no_app.height = -0.4
no_bluestacks = Loc(name="no_bluestacks", identifier=i_bluestacks, accessible=False)
no_bluestacks.id_absence = True
no_bluestacks.id_val_max = 0.75
no_bluestacks.height = -0.5
# maintenance = Loc(name="maintenance", identifier=i_maintenance, accessible=False)
maintenance2 = Loc(name="maintenance2", identifier=i_maintenance2, accessible=False)

main = Loc(name="main", identifier=i_builder, accessible=True)
unknown = Loc(name="unknown", identifier=i_x, accessible=False)
unknown.height = -0.5
chat = Loc(name="chat", identifier=i_challenge, accessible=True)
chat.height = main.height + 1
settings = Loc(name="settings", identifier=i_settings, accessible=True)
change_account = Loc(name="change_account", identifier=i_switch_account, accessible=True)
forge = Loc(name="forge", identifier=i_forge, accessible=True)
builder = Loc(name="builder", identifier=i_master_builder, accessible=True)
builder.add_identifier(i_otto)

overlays = []
for overlay in [i_another_device, i_ad_cross, i_ad_back, i_reload, i_reload_game, i_ad_cross, i_try_again, i_return_home, i_pre_app, i_okay, i_okay2, i_okay3, i_okay4, i_okay5,
                i_next2, i_bluestacks_message_cross, i_return_home_2, i_return_home_3, i_red_cross, i_red_cross2, i_bluestacks_app]:
    new_overlay = Loc(name=overlay.name[2:], identifier=overlay, accessible=False)
    if overlay == i_another_device:
        new_overlay.add_default_path(action="reload", parameter=None, expected_loc=main)
        another_device = new_overlay
    else:
        new_overlay.add_default_path(action="click_identifier", parameter=None,expected_loc=main)
    new_overlay.id_val_min = 0.8
    new_overlay.add_height(4)
    overlays.append(new_overlay)

log_in = Loc(name="log_in", identifier=i_log_in)
log_in.add_default_path(action="log_in", parameter=None, expected_loc=main)

army_tab = Loc(name="army_tab", identifier=i_army_tab, accessible=True)
troops_tab = Loc(name="troops_tab", identifier=i_troops_tab, accessible=True)
spells_tab = Loc(name="spells_tab", identifier=i_spells_tab, accessible=True)
siege_tab = Loc(name="siege_tab", identifier=i_siege_tab, accessible=True)

lab = Loc(name="lab", identifier=i_research_upgrading, accessible=True)

n_attack = Loc(name="attack", identifier=i_multiplayer, accessible=True)
find_a_match = Loc(name="find_a_match", identifier=i_next, accessible=True)
attacking = Loc(name="attacking", identifier=i_surrender, accessible=False)
attacking_end_1 = Loc(name="attacking_end_1", identifier=i_surrender_okay, accessible=False)
attack_end = Loc(name="attack_end", identifier=i_return_home, accessible=False)

attack_b2 = Loc(name="attack_b2", identifier=i_versus_battle, accessible=True)
attack_b2.height = 3
attacking_b = Loc(name="attacking_b", identifier=i_defender, accessible=True)
attacking_b_end_1 = Loc(name="attacking_b_end_1", identifier=i_surrender_okay, accessible=False)

# ---------------
# ---- PATHS ----
# ---------------

# Start-up
pycharm.add_default_path(action="pycharm_to_main", parameter=i_app, expected_loc=main, region=ICONS)
unknown.add_default_path(action="wait", parameter=0.2, expected_loc=main)
no_bluestacks.add_default_path(action="start_bluestacks", parameter=None, expected_loc=main)
no_app.add_default_path(action="start_app", parameter=None, expected_loc=main)
# maintenance.add_default_path(action="reload", parameter=None, expected_loc=main)
maintenance2.add_default_path(action="reload", parameter=None, expected_loc=main)

# Main
main.add_path(destination=pycharm, action="click", parameter=i_pycharm_icon, expected_loc=pycharm)
main.add_path(destination=chat, action="key_p", parameter="c", expected_loc=chat)
main.add_path(destination=army_tab, action="click", parameter=i_army, expected_loc=army_tab)
main.add_path(destination=troops_tab, action="click", parameter=i_army, expected_loc=army_tab)
main.add_path(destination=spells_tab, action="click", parameter=i_army, expected_loc=army_tab)
main.add_path(destination=siege_tab, action="click", parameter=i_army, expected_loc=army_tab)
main.add_path(destination=settings, action='click', parameter=i_settings_on_main, expected_loc=settings)
main.add_path(destination=change_account, action='click', parameter=i_settings_on_main, expected_loc=settings)
main.add_path(destination=forge, action='goto_forge', parameter='', expected_loc=forge)
main.add_path(destination=builder, action="goto_builder", parameter='', expected_loc=builder)
main.add_path(destination=find_a_match, action="click", parameter=i_attack, expected_loc=n_attack)
main.add_path(destination=n_attack, action="click_p", parameter=i_attack, expected_loc=n_attack)
main.add_path(destination=attack_b2, action="goto_builder", parameter="", expected_loc=builder)
main.add_path(destination=attacking_b, action="goto_builder", parameter="", expected_loc=builder)
main.add_path(destination=lab, action="goto_lab", parameter="", expected_loc=lab)

# Builder
builder.add_path(destination=pycharm, action="click", parameter=i_pycharm_icon, expected_loc=pycharm)
builder.add_path(destination=chat, action="key", parameter="c", expected_loc=chat)
builder.add_path(destination=settings, action='click', parameter=i_settings_on_main, expected_loc=settings)
builder.add_path(destination=change_account, action='click', parameter=i_settings_on_main, expected_loc=settings)
builder.add_path(destination=main, action="goto_main", parameter='', expected_loc=main)
builder.add_path(destination=attack_b2, action="click", parameter=i_attack_b, expected_loc=attack_b2)
builder.add_path(destination=attacking_b, action="click", parameter=i_attack_b, expected_loc=attack_b2)
builder.add_default_path(action="goto_main", parameter='', expected_loc=main)

# Research
lab.add_default_path(action="key", parameter="esc", expected_loc=main)

# Chat
chat.add_height(1)
chat.add_default_path(action="key", parameter="esc", expected_loc=main)

# Settings
settings.add_path(destination=change_account, action="click_p", parameter=i_change_accounts_button, expected_loc=change_account)
settings.add_default_path(action="key", parameter="esc", expected_loc=main)
change_account.add_default_path(action="key_p", parameter="esc", expected_loc=settings)
change_account.height = settings.height + 1

# Forge
forge.add_default_path(action="key", parameter="esc", expected_loc=main)
forge.add_height(main.height + 1)

# Army tabs
army_tab.add_default_path(action="key", parameter="esc", expected_loc=main)
troops_tab.add_default_path(action="key", parameter="esc", expected_loc=main)
spells_tab.add_default_path(action="key", parameter="esc", expected_loc=main)
siege_tab.add_default_path(action="key", parameter="esc", expected_loc=main)

army_tab.add_path(destination=troops_tab, action="click", parameter=i_troops_tab_dark, expected_loc=troops_tab)
army_tab.add_path(destination=spells_tab, action="click", parameter=i_spells_tab_dark, expected_loc=spells_tab)
army_tab.add_path(destination=siege_tab, action="click", parameter=i_siege_tab_dark, expected_loc=siege_tab)
troops_tab.add_path(destination=spells_tab, action="click", parameter=i_spells_tab_dark, expected_loc=spells_tab)
troops_tab.add_path(destination=siege_tab, action="click", parameter=i_siege_tab_dark, expected_loc=siege_tab)
troops_tab.add_path(destination=army_tab, action="click", parameter=i_army_tab_dark, expected_loc=army_tab)
spells_tab.add_path(destination=troops_tab, action="click", parameter=i_troops_tab_dark, expected_loc=troops_tab)
spells_tab.add_path(destination=siege_tab, action="click", parameter=i_siege_tab_dark, expected_loc=siege_tab)
spells_tab.add_path(destination=army_tab, action="click", parameter=i_army_tab_dark, expected_loc=army_tab)
siege_tab.add_path(destination=troops_tab, action="click", parameter=i_troops_tab_dark, expected_loc=troops_tab)
siege_tab.add_path(destination=spells_tab, action="click", parameter=i_spells_tab_dark, expected_loc=spells_tab)
siege_tab.add_path(destination=army_tab, action="click", parameter=i_army_tab_dark, expected_loc=army_tab)

# Attacking
n_attack.add_path(destination=find_a_match, action="click", parameter=i_find_a_match, expected_loc=find_a_match)
find_a_match.add_default_path(action="click", parameter=i_end_battle, expected_loc=main)
attacking.add_default_path(action="click", parameter=i_surrender, expected_loc=main)
n_attack.add_default_path(action="key", parameter="esc", expected_loc=main)

attack_b2.add_default_path(action="key", parameter="esc", expected_loc=builder)
attack_b2.add_path(destination=attacking_b, action='click', parameter=i_find_now, expected_loc=attacking_b)
attacking_b.add_default_path(action='click', parameter=i_surrender, expected_loc=attack_b2)
attacking_b_end_1.add_default_path(action="click_identifier", parameter=None,expected_loc=attack_b2)

def goto(destination):
    global current_location
    print(f"Goto: {current_location} -> {destination}")
    if current_location == destination: return
    loop_count = 0
    path_found = True
    while current_location != destination and path_found and loop_count < 5 and current_location:
        # print("Goto (loc):", current_location)
        path_found = current_location.has_path(destination)
        result = current_location.goto(destination)
        loop_count += 1
        current_location = loc(current_location) # This validates that expectations match reality wrt location
    if not path_found:
        # for path in current_location.paths:
        #     print(path)
        # print(current_location, destination, path_found, loop_count)
        print(f"Path not found (loc): {current_location} -> {destination}")
    # print("Goto complete:", current_location)
    return current_location

def loc(guess=None):
    start_time = datetime.now()
    global current_location
    time.sleep(0.2)

    # for identifier in another_device.identifiers:
    #     if identifier.find(fast=True):
    #         print("Found reload")
    #         return another_device
    #

    # print("A", datetime.now() - start_time)
    if guess and guess != unknown:
        guesses = [guess]
        if latest_path:
            guesses += latest_path.most_common_actuals()
        for guess in guesses:
            for identifier in guess.identifiers:
                val, loc, rect = identifier.find_detail(fast=False)
                result = val > identifier.threshold
                if result != guess.id_absence:
                    # print(identifier.name, val, result, val)
                    # print("Loc guess", guess)
                    current_location = guess
                    return current_location
                print("Loc guess (fail)", guess, identifier.name, val, identifier.threshold)

    for location in locs:
        if location.height >= 4:
            for identifier in location.identifiers:
                val, loc, rect = identifier.find_detail(fast=True)
                result = val > identifier.threshold
                if result != location.id_absence:
                    current_location = location
                    # print("Loc success (overlays)", location, "FAST", identifier.name, round(val,2), identifier.threshold, result)
                    return current_location
                # print("Loc fail (overlays)", location, "FAST", identifier.name, round(val,2), identifier.threshold, identifier.regions)

    current_location = unknown
    # Search all locations quickly then thoroughly
    # print("B", datetime.now() - start_time)
    for location in locs:
        # print("C", datetime.now() - start_time)
        for identifier in location.identifiers:
            val, loc, rect = identifier.find_detail(fast=True)
            result = val > identifier.threshold
            if result != location.id_absence:
                current_location = location
                # print("Loc success (all locations)", location, "FAST", identifier.name, round(val,2), identifier.threshold, result)
                return current_location
            # print("Loc fail (all locations)", location, "FAST", identifier.name, round(val,2), identifier.threshold, identifier.regions)
    time.sleep(0.5)
    for location in locs:
        # print("C", datetime.now() - start_time)
        for identifier in location.identifiers:
            val, loc, rect = identifier.find_detail(fast=False)
            result = val > identifier.threshold
            if result != location.id_absence:
                current_location = location
                # print("Loc success (all locations)", location, "SLOW", identifier.name, round(val,2), identifier.threshold, result)
                return current_location
            # print("Loc fail (all locations)", location, "SLOW", identifier.name, round(val,2), identifier.threshold, identifier.regions)
    time.sleep(0.5)

    # print("D", datetime.now() - start_time)
    print(f"Loc: (guess unsuccessful). Guess:{guess}. Actual:{current_location}")

    return current_location

def click_builder():
    # print("Click builder")
    pag.click(BOTTOM_LEFT)
    for image in [i_builder, i_master, i_otto]:
        if image.find():
            image.click()
            return True

    return False

def move_list(direction, dur=0.5):
    if direction == "up":
        pag.moveTo(855,666)
        pag.dragTo(855,210, dur)
    if direction == "down":
        # pag.press("s")
        pag.moveTo(855,210)
        pag.dragTo(855,666, dur)

def goto_list_top(village):
    if village == "main": goto(main)
    else: goto(builder)
    time.sleep(.2)
    pag.click(BOTTOM_LEFT)
    time.sleep(.2)
    click_builder()
    at_top = False
    count = 0
    time.sleep(0.2)
    while not at_top and count < 3:
        if i_suggested_upgrades.find():
            at_top = True
        if not at_top:
            move_list("down", 1)
            time.sleep(0.2)
        count += 1
    time.sleep(2)
    val, loc, rect = i_suggested_upgrades.find_detail()
    print("Goto list top", val)
    pag.moveTo(855, loc[1])
    pag.dragTo(855,210, 1)
    time.sleep(2)

def goto_list_very_top(village):
    if village == "main": goto(main)
    else: goto(builder)
    time.sleep(0.5)
    pag.click(BOTTOM_LEFT)
    click_builder()
    at_top = False
    count = 0
    while not at_top and count < 5:
        if i_upgrades_in_progress.find(show_image=False):
            at_top = True
        else:
            move_list("down", 1)
            time.sleep(0.2)
        count += 1

def format_list_of_locs(locs):
    output = ""
    for x in locs:
        output += x.name + ", "
    return output

def print_locs():
    print()
    print("ALL LOCATIONS")
    for x in locs:
        print()
        print(x.name)
        for path in x.paths:
            print(" -", path)
            for added in path.actual_locs:
                print("   -", added.name)





# OLD NAV

def attack_b_get_screen():
    time.sleep(1)
    hold_key('s', 0.5)
    hold_key('down', 0.5)
    time.sleep(1)
    hold_key('down', 0.5)
    pag.screenshot('temp/attacking_b.png')

def zoom_out():
    time.sleep(0.1)
    hold_key("down", 0.2)

    # time.sleep(1)
    # for x in range(1):
    #     pag.keyDown('ctrl')
    #     time.sleep(0.1)
    #     pag.scroll(-300)
    #     time.sleep(0.1)
    #     pag.keyUp('ctrl')
    #     time.sleep(0.1)


def start():
    click_cv2('bluestacks_icon')
    time.sleep(.2)
    # pag.moveTo(1000,500)
    pag.keyDown('ctrl')
    for x in range(5):
        pag.scroll(-100)
    pag.keyUp('ctrl')

def end():
    click_cv2("pycharm")


def current_resources():
    time.sleep(.1)
    result_array = []
    for region in [RESOURCES_G, RESOURCES_E, RESOURCES_D]:
        result_array.append(resource_numbers.read(region, show_image=False, return_number=True))
    if result_array[0] > 30000000: result_array[0] = result_array[0]/10
    # print("Current Resources:", result_array)
    return result_array

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

def open_app():
    global current_location
    success = False
    while not success:
        current_location = loc(current_location)
        if current_location == "pycharm_running":
            click_cv2("nav/bluestacks")
        else:
            click_cv2("nav/" + current_location.name)
            if current_location == "heart": current_location = "start_eyes"
            elif current_location == "start_eyes": current_location = "maximise"
            elif current_location == "maximise": current_location = "main"
        if current_location not in ["pycharm_running", "start_eyes", "heart", "maximise", ]: # loc doesn't return maximise if it finds it at the top of the screen (above y = 100)
            success = True
        if current_location == "pycharm_running": current_location = None
        time.sleep(1)

def close_app():
    val, loc, rect = find_cv2("nav/close_cross")
    if val < 0.5:
        click_cv2('bluestacks_icon')
        time.sleep(0.2)
    val, loc, rect = find_cv2("nav/close_cross")
    print(val)
    if val > 0.6:
        click_rect(rect)
        time.sleep(0.2)
        click_cv2("nav/close_close")



def tour():
    goto(main)
    goto(chat)
    goto(settings)
    goto(change_account)
    goto(forge)
    goto(army_tab)
    goto(troops_tab)
    goto(spells_tab)
    goto(siege_tab)
    goto(n_attack)
    goto(find_a_match)
    goto(builder)
    goto(attacking_b)

def spare_builders(account, village):
    if village == "main":
        goto(main)
        region = BUILDER_ZERO_REGION
    else:
        goto(builder)
        region = BUILDER_B_ZERO_REGION
    screen = get_screenshot(region, filename=f"tracker/builders{account.number}{village}")
    if i_builder_zero.find_screen(screen, show_image=False): return 0
    if i_builder_one.find_screen(screen): return 1
    return 2

def change_current_location(loc):
    global current_location
    current_location = loc


# Set-up
locs.sort(key=lambda x: x.height, reverse=True)
current_location = pycharm
# tour()
# goto(pycharm)

# goto(main)
# print(loc())

# goto(attacking_b)
# goto(pycharm)

# goto(builder)

# goto(main)
# click_builder()
# move_list("down")
# goto_list_top("main")
# goto(python)


# for i in labs:
#     if i.name == "towers/labs//lab11":
#         goto(main)
#         i.add_loc(main)
#         goto(i.loc)
#         i.show_regions_on_screen()
#         i.show_regions()
#         current_location = pycharm

# goto(main)
# lab11 = next((x for x in images if "lab11" in x.name), None)
# lab11.click()
# lab11.show_regions()
# lab11.show_regions_on_screen()