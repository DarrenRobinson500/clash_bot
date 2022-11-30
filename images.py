from object_recognition import *
from regions import *

images = []

class Image():
    def __init__(self, name, file, threshold=0.8, always_slow=False, no_of_regions=5, region_limit=None, type=None, screen=None):
        self.name = name
        self.image = cv2.imread(file, 0)
        self.regions = []
        self.region_limit = region_limit
        self.threshold = threshold
        self.always_slow = always_slow
        self.no_of_regions = no_of_regions
        self.loc = None
        if type: self.type = type
        else: self.type = "Not specified"
        self.load_regions()
        images.append(self)

    def __str__(self):
        return self.name

    def add_loc(self, loc):
        self.loc = loc

    def show_regions_on_screen(self):
        screen = get_screenshot(colour=1)
        for rectangle in self.regions:
            print("Show regions:", rectangle)
            cv2.rectangle(screen, rectangle, (255, 0, 0), 3)
        show(screen, scale=0.6)


    def click(self):
        val, loc, rect = self.find_detail(fast=True)
        # print("Image click:", self, rect)
        if val < self.threshold:
            val, loc, rect = self.find_detail(fast=False)
        if val > self.threshold:
            pag.click(loc)
            # print("Clicked", self.name, round(val,2), self.threshold, loc)
            return True
        else:
            # print("Click Failure:", self.name, round(val,2), self.threshold)
            return False

    def click_region(self, region):
        screen = get_screenshot(region)
        print("Click region:", self.image.shape, screen.shape)
        result = cv2.matchTemplate(screen, self.image, method)
        min_val, val, min_loc, loc = cv2.minMaxLoc(result)
        rect = (loc[0] + region[0], loc[1] + region[1], self.image.shape[1], self.image.shape[0])
        loc = (int(rect[0] + rect[2] / 2), int(rect[1] + rect[3] / 2))
        print("Find (region)", self.name, round(val,2))
        if val > self.threshold:
            pag.click(loc)
            return True
        return False

    def wait(self, dur=1):
        increment = 0.2
        for x in range(int(dur / increment)):
            val, loc, rect = self.find_detail(fast=True)
            if val > self.threshold: return True
            time.sleep(increment)
        return False

    def find(self, show_image=False, fast=False):
        val, loc, rect = self.find_detail(show_image=show_image, fast=fast)
        # print("Image find:", self.name, val)
        return val > self.threshold

    def check_colour(self, fast=False):
        val, loc, rect = self.find_detail(fast=fast)
        image = get_screenshot(rect, colour=1)
        if image is None: return False
        y, x, channels = image.shape
        # show(image)
        spots = [(1 / 4, 1 / 4), (1 / 4, 3 / 4), (3 / 4, 1 / 4), (3 / 4, 3 / 4), (7 / 8, 1 / 8), (0.95, 0.05)]
        count = 0
        for s_x, s_y in spots:
            pixel = image[int(y * s_y)][int(x * s_x)]
            blue, green, red = int(pixel[0]), int(pixel[1]), int(pixel[2])
            if self.name == "i_war_left":
                print("Check colour:", self.name, s_x, s_y, blue, green, red)
            if abs(blue - green) > 5 or abs(blue - red) > 5: count += 1
        colour = False
        if count > 1: colour = True
        print("Check colour", self.name, colour)
        return colour

    def colour(self):
        val, loc, rect = self.find_detail(fast=False)
        image = get_screenshot(rect, colour=1)
        if image is None: return False
        y, x, channels = image.shape
        # show(image)
        spots = [(1 / 4, 1 / 4), (1 / 4, 3 / 4), (3 / 4, 1 / 4), (3 / 4, 3 / 4), (7 / 8, 1 / 8), (0.95, 0.05)]
        colour = 0
        image_name = "i_war_right"
        for s_x, s_y in spots:
            pixel = image[int(y * s_y)][int(x * s_x)]
            blue, green, red = int(pixel[0]), int(pixel[1]), int(pixel[2])
            if self.name == image_name:
                print("Colour:", self.name, s_x, s_y, blue, green, red)
            colour += abs(blue - green) + abs(blue - green) + abs(red - green)
        if self.name == image_name:
            print("Colour:", self.name, colour)
        return colour

    def find_detail(self, show_image=False, fast=False):
        if self.image is None:
            print("Find - No image provided:", self.name)
            return 0, 0, 0
        if self.always_slow: fast = False
        # Regions
        for region in self.regions:
            screen = get_screenshot(region)
            if show_image:
                show(self.image)
                show(screen)
            try:
                result = cv2.matchTemplate(screen, self.image, method)
            except:
                if screen is None:
                    print("Find detail - No screen:")
                    return 0, 0, 0
                print("Image didn't fit in region:", self.name)
                print(screen.shape, self.image.shape)
                self.increase_regions()
                return 0, 0, 0

            min_val, val, min_loc, loc = cv2.minMaxLoc(result)
            rect = (loc[0] + region[0], loc[1] + region[1], self.image.shape[1], self.image.shape[0])
            loc = (int(rect[0] + rect[2] / 2), int(rect[1] + rect[3] / 2))
            # print("Find (region)", self.name, round(val,2))
            if val > self.threshold:
                return round(val,2), loc, rect
        if fast: return 0,0,0
        # Whole screen
        # print("Fast:", fast)
        # print("Find detail - checking whole screen", self)
        if self.region_limit:
            screen = get_screenshot(self.region_limit)
        else:
            screen = get_screenshot()
        if show_image:
            show(self.image)
            show(screen)
        # print("Find detail:", self.name)
        try:
            result = cv2.matchTemplate(screen, self.image, method)
        except:
            return 0, 0, 0
        min_val, val, min_loc, loc = cv2.minMaxLoc(result)
        rect = (loc[0], loc[1], self.image.shape[1], self.image.shape[0])
        loc = (int(rect[0] + rect[2] / 2), int(rect[1] + rect[3] / 2))
        region = [max(rect[0] - 1, 0), max(rect[1] - 1, 0), rect[2] + 2, rect[3] + 2]
        if val > self.threshold:
            if self.region_limit is None or self.check_region_limit(region):
                self.save_region(region)
        return round(val,2), loc, rect

    def find_screen(self, screen, show_image=False, return_location=False, return_result=False):
        if self.image is None:
            print("Find - No image provided:", self.name)
            return False, (0, 0)
        if show_image:
            show(self.image)
            show(screen)
        result = cv2.matchTemplate(screen, self.image, method)
        min_val, val, min_loc, loc = cv2.minMaxLoc(result)
        # print("Find screen:", self.name, round(val, 2), self.threshold)
        if return_result: return val > self.threshold, round(val,2)
        if return_location: return val > self.threshold, loc
        return val > self.threshold

    def find_many(self, show_image=False):
        h, w = self.image.shape
        screen = get_screenshot()
        if show_image:
            show(self.image)
            show(screen)
        result = cv2.matchTemplate(screen, self.image, method)
        yloc, xloc = np.where(result >= self.threshold)
        z = zip(xloc, yloc)

        rectangles = []
        for (x, y) in z:
            rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

        return rectangles

    def check_region_limit(self, region):
        if self.region_limit is None: return True
        within_region = True
        print(region, self.region_limit)
        if region[0] < self.region_limit[0]: within_region = False
        if region[1] < self.region_limit[1]: within_region = False
        if region[0] + region[2] > self.region_limit[0] + self.region_limit[2]: within_region = False
        if region[1] + region[3] > self.region_limit[1] + self.region_limit[3]: within_region = False
        return within_region

    def increase_regions(self):
        for region in self.regions:
            print("Increase regions - image shape:", self.image.shape, self.image.shape[1], self.image.shape[0])
            print("Increase regions - Pre:", region)
            print(region[2], self.image.shape[1])
            if region[2] < self.image.shape[1]:
                print("Increasing X")
                region[2] = self.image.shape[1]
            print(region[3], self.image.shape[0])
            if region[3] < self.image.shape[0]:
                print("Increasing Y")
                region[3] = self.image.shape[0]
            print("Increase regions - Post:", region)
            self.save_region(region)

    def load_regions(self):
        self.regions = []
        if self.image is None: return
        regions = db_regions_get(self, type=self.type)
        min_y, min_x = self.image.shape
        for r in regions:
            region = [r[1], r[2], max(r[3], min_x), max(r[4], min_y)]
            r2 = [r[1], r[2], r[3], r[4]]
            check_region = self.check_region_limit(region)
            if self.region_limit is None or check_region:
                if region and region in self.regions:
                    # print("Deleting regions:", self, region, self.regions)
                    # print("Pre")
                    db_regions_delete(self, r2)
                if region and region not in self.regions:
                    self.regions.append(region)
            if not check_region:
                print("Deleting regions:", self, region, self)
                db_regions_delete(self, r2)

    def save_region(self, region):
        if region not in self.regions:
            print("Saving region", self.name, region)
            db_regions_add(self, region, type=self.type)
            self.load_regions()

    def show(self):
        show(self.image)

    def show_regions(self):
        total_area = 0
        print()
        print("Regions for", self)
        for region in self.regions:
            print(region)
            total_area += region[2] * region[3]
        print(f"Total area: {total_area}. Regions:{len(self.regions)}")

    def merge_regions(self):
        # print("Merge regions")
        self.load_regions()
        if len(self.regions) == 0: return
        min_increase = None
        min_region_a = None
        min_region_b = None
        min_region_c = None
        total_area = 0
        for region_a in self.regions:
            total_area += region_a[2] * region_a[3]
        print(f"{self} Total area: {total_area}. Regions: {len(self.regions)}")

        for region_a in self.regions:
            for region_b in self.regions:
                if region_a == region_b: continue
                if region_a[0] == region_b[0] and region_a[1] == region_b[1] and region_a[2] == region_b[2] and region_a[3] == region_b[3]:
                    print("Found Duplicate")
                    db_regions_delete(self, min_region_b)
                    self.load_regions()
                    continue
                size_a = region_a[2] * region_a[3]
                size_b = region_b[2] * region_b[3]
                combined_x1 = min(region_a[0], region_b[0])
                combined_x2 = max(region_a[0] + region_a[2], region_b[0] + region_b[2])
                combined_w = combined_x2 - combined_x1
                combined_y1 = min(region_a[1], region_b[1])
                combined_y2 = max(region_a[1] + region_a[3], region_b[1] + region_b[3])
                combined_h = combined_y2 - combined_y1
                size_c = combined_w * combined_h
                increase = size_c - size_a - size_b
                if min_increase is None or increase < min_increase:
                    min_increase = increase
                    min_region_a = region_a
                    min_region_b = region_b
                    min_region_c = [combined_x1, combined_y1, combined_w, combined_h]
        # print(min_increase, min_region_a, min_region_b, min_region_c)
        if len(self.regions) <= self.no_of_regions and min_increase and min_increase > 0:
            # print("Merge regions", len(self.regions), self.no_of_regions, min_increase)
            return False
        if min_region_a is None or min_region_b is None:
            # print("Merge regions - found None region")
            return False
        # print("Merge regions - got here")
        print("Merging regions. Net increase:", min_increase)
        db_regions_delete(self, min_region_a, type=self.type)
        db_regions_delete(self, min_region_b, type=self.type)
        self.save_region(min_region_c)
        return True


# Navigation images
i_ad_cross = Image(name="i_ad_cross", file='images/nav/ad_cross.png')
i_ad_back = Image(name="i_ad_cross", file='images/nav/ad_back.png')
i_app = Image(name="i_app", file='images/nav/app.png')
i_another_device = Image(name="i_another_device", file='images/nav/another_device.png')
i_army = Image(name="i_army", file='images/nav/army.png')
i_army_tab = Image(name="i_army_tab", file='images/nav/army_tab.png')
i_army_tab_dark = Image(name="i_army_tab_dark", file='images/nav/army_tab_dark.png')
i_attack = Image(name="i_attack", file='images/nav/attack.png')
i_attack_b = Image(name="i_attack_b", file='images/nav/attack_b.png')
i_attacking = Image(name="i_attacking", file='images/nav/attacking.png')
i_battle_end_b1 = Image(name="i_battle_end_b1", file='images/nav/battle_end_b1.png')
i_battle_end_b2 = Image(name="i_battle_end_b2", file='images/nav/battle_end_b2.png')
i_bluestacks = Image(name="i_bluestacks", file='images/nav/bluestacks.png', always_slow=True)
i_bluestacks_app = Image(name="i_bluestacks_app", file='images/nav/bluestacks_app.png')
i_bluestacks_message = Image(name="i_bluestacks_message", file='images/nav/bluestacks_message.png')
i_bluestacks_message_cross = Image(name="i_bluestacks_message_cross", file='images/nav/bluestacks_message_cross.png')
i_boat_to = Image(name="i_boat_to", file='images/nav/boat_to.png')
i_builder = Image(name="i_builder", file='images/nav/builder.png')
i_challenge = Image(name="i_challenge", file='images/nav/challenge.png')
i_change_accounts_button = Image(name="i_change_accounts_button", file='images/nav/change_accounts_button.png')
i_chat = Image(name="i_chat", file='images/nav/chat.png')
i_close_close = Image(name="i_close_close", file='images/nav/close_close.png')
i_close_cross = Image(name="i_close_cross", file='images/nav/close_cross.png')
i_coin = Image(name="i_coin", file='images/nav/coin.png')
i_defender = Image(name="i_defender", file='images/nav/defender.png')
i_donate = Image(name="i_donate", file='images/nav/donate.png')
i_end_battle = Image(name="i_end_battle", file='images/nav/end_battle.png')
i_find_a_match = Image(name="i_find_a_match", file='images/nav/find_a_match.png')
i_find_now = Image(name="i_find_now", file='images/nav/find_now.png')
i_forge = Image(name="i_forge", file='images/nav/forge.png')
i_forge_button = Image(name="i_forge_button", file='images/nav/forge_button.png')
i_forge_path = Image(name="i_forge_path", file='images/nav/forge_path.png')
i_heart = Image(name="i_heart", file='images/nav/heart.png')
i_log_in = Image(name="i_log_in", file='images/nav/log_in.png')
i_log_in_with_supercell = Image(name="i_log_in_with_supercell", file='images/nav/log_in_with_supercell.png')
i_main = Image(name="i_main", file='images/nav/main.png')
i_maintenance = Image(name="i_maintenance", file='images/nav/maintenance.png', threshold=0.9)
i_maintenance2 = Image(name="i_maintenance", file='images/nav/maintenance2.png')
i_master = Image(name="i_master", file='images/master.png')
i_master_builder = Image(name="i_master_builder", file='images/nav/master_builder.png')
i_maximise = Image(name="i_maximise", file='images/nav/maximise.png')
i_multiplayer = Image(name="i_multiplayer", file='images/nav/multiplayer.png')
i_next = Image(name="i_next", file='images/nav/next.png')
i_next2 = Image(name="i_next2", file='images/nav/next2.png')
i_okay = Image(name="i_okay", file='images/nav/okay.png')
i_okay2 = Image(name="i_okay2", file='images/nav/okay2.png')
i_okay3 = Image(name="i_okay3", file='images/nav/okay3.png')
i_okay4 = Image(name="i_okay4", file='images/nav/okay4.png')
i_okay5 = Image(name="i_okay5", file='images/nav/okay5.png')
i_otto = Image(name="i_otto", file='images/nav/otto.png')
i_pre_app = Image(name="i_pre_app", file='images/nav/pre_app.png')
i_pycharm = Image(name="i_pycharm", file='images/nav/pycharm.png')
i_pycharm_icon = Image(name="i_pycharm_icon", file='images/nav/pycharm_icon.png')
i_pycharm_running = Image(name="i_pycharm_running", file='images/nav/pycharm_running.png')
i_raid_weekend = Image(name="i_raid_weekend", file='images/nav/raid_weekend.png')
i_red_cross = Image(name="i_red_cross", file='images/nav/red_cross.png')
i_red_cross2 = Image(name="i_red_cross2", file='images/nav/red_cross2.png')
i_reload = Image(name="i_reload", file='images/nav/reload.png')
i_reload_game = Image(name="i_reload_game", file='images/nav/reload_game.png')
i_return_home = Image(name="i_return_home", file='images/nav/return_home.png')
i_return_home_2 = Image(name="i_return_home_2", file='images/nav/return_home_2.png', threshold=0.7)
i_return_home_3 = Image(name="i_return_home_3", file='images/nav/return_home_3.png')
i_settings = Image(name="i_settings", file='images/nav/settings.png')
i_settings_on_main = Image(name="i_settings_on_main", file='images/nav/settings_on_main.png')
i_siege_tab = Image(name="i_siege_tab", file='images/nav/siege_tab.png')
i_siege_tab_dark = Image(name="i_siege_tab_dark", file='images/nav/siege_tab_dark.png')
i_spells_tab = Image(name="i_spells_tab", file='images/nav/spells_tab.png')
i_spells_tab_dark = Image(name="i_spells_tab_dark", file='images/nav/spells_tab_dark.png')
i_splash = Image(name="i_splash", file='images/nav/splash.png')
i_start_eyes = Image(name="i_start_eyes", file='images/nav/start_eyes.png')
i_start_eyes_2 = Image(name="i_start_eyes_2", file='images/nav/start_eyes_2.png')
i_surrender = Image(name="i_surrender", file='images/nav/surrender.png')
i_surrender_okay = Image(name="i_surrender_okay", file='images/nav/surrender_okay.png')
i_switch_account = Image(name="i_switch_account", file='images/nav/switch_account.png')
i_troops_tab = Image(name="i_troops_tab", file='images/nav/troops_tab.png')
i_troops_tab_dark = Image(name="i_troops_tab_dark", file='images/nav/troops_tab_dark.png')
i_try_again = Image(name="i_try_again", file='images/nav/try_again.png')
i_versus_battle = Image(name="i_versus_battle", file='images/nav/versus_battle.png')
i_war_okay = Image(name="i_war_okay", file='images/war/okay.png')
i_wins = Image(name="i_wins", file='images/nav/wins.png')
i_x = Image(name="i_unknown", file='images/nav/x.png')

i_okay_buttons = [i_okay, i_okay2, i_okay3, i_okay4, i_okay5]

# Main screen
i_trader = Image(name="i_trader", file='images/nav/trader.png')
i_trader_close = Image(name="i_trader_close", file='images/nav/trader_close.png')
i_raid_medals = Image(name="i_raid_medals", file='images/nav/raid_medals.png', threshold=0.95)
i_raid_medals_selected = Image(name="i_raid_medals_selected", file='images/nav/raid_medals_selected.png', threshold=0.95)
i_collect_capital_coin = Image(name="i_collect_capital_coin", file='images/collect_capital_coin.png')

# Castle
i_treasury = Image(name="i_treasury", file='images/treasury.png')
i_collect_castle = Image(name="i_collect_castle", file='images/collect_castle.png')

# Games
i_caravan = Image(name="i_caravan", file='images/nav/caravan.png')
i_games = Image(name="i_games", file='images/nav/games.png')

# Research
i_research = Image(name="i_research", file='images/research/research.png')
i_research_upgrading = Image(name="i_research", file='images/research/research_upgrading.png')
i_research_elixir = Image(name="i_research_elixir", file='images/research/research_elixir.png')
i_lab_girl = Image(name="lab_girl", file="images/nav/lab_girl.png")
# i_research_dark = Image(name="i_research_dark", file='images/research/research_dark.png')

# Games
i_start_game = Image(name="i_start_game", file='images/games/start_game.png')
i_complete = Image(name="i_complete", file="images/games/complete.png", threshold=0.93)

# War
i_war = Image(name="i_war", file='images/nav/war.png')
i_war_cwl = Image(name="i_war_cwl", file='images/nav/war_cwl.png')
i_war_preparation = Image(name="i_war_preparation", file='images/war/preparation.png')
i_war_battle_day = Image(name="i_battle_day", file='images/war/battle_day.png')
i_war_castle = Image(name="i_war_castle", file='images/war/castle.png', threshold=0.7)
i_war_castle2 = Image(name="i_war_castle2", file='images/war/castle2.png', threshold=0.7)
i_war_left = Image(name="i_war_left", file='images/war/left.png', threshold=0.7, region_limit=[470, 750, 100, 140])
i_war_right = Image(name="i_war_right", file='images/war/right.png')
i_war_donate = Image(name="i_war_donate", file='images/war/donate.png')
i_war_donate_reinforcements = Image(name="i_war_donate_reinforcements", file='images/war/donate_reinforcements.png', threshold=0.7)
i_clan_army = Image(name="i_clan_army", file="images/troops_new/clan_army.png")

# Donate images
i_more_donates = Image(name="i_more_donates", file="images/more_donates.png")
i_donate_cross = Image(name="i_donate_cross", file='images/donate_cross.png')

# Building images
i_builder_zero = Image(name="i_builder_zero", file='images/builder_zero.png', threshold=0.75, region_limit=[744, 79, 198, 32])
i_builder_one = Image(name="i_builder_one", file='images/builder_one.png', threshold=0.75)
i_upgrade_button = Image(name="i_upgrade_button", file='images/upgrade.png', threshold=0.7)
i_suggested_upgrades = Image(name="i_suggested_upgrades", file='images/towers/suggested_upgrades.png')
i_upgrades_in_progress = Image(name="i_upgrades_in_progess", file='images/towers/upgrades_in_progess.png')

# Builder base attacks
i_attack_b_0 = Image(name="i_attack_b_0", file='images/attack_b/attack_0.png', threshold=0.85)

# Army tab
i_army_clock = Image(name="i_army_clock", file='images/army_clock.png')
i_army_edit = Image(name="i_army_edit", file='images/nav/army_edit.png')
i_army_okay = Image(name="i_army_okay", file='images/nav/army_okay.png')
i_army_request = Image(name="i_army_request", file='images/nav/army_request.png')
i_army_donate_edit = Image(name="i_army_donate_edit", file='images/nav/army_donate_edit.png')
i_army_donate_confirm = Image(name="i_army_donate_confirm", file='images/nav/army_donate_confirm.png')
i_army_request_send = Image(name="i_army_request_send", file='images/nav/army_request_send.png')
i_remove_troops = Image(name="i_remove_troops", file='images/remove_troops.png')

# Resources
RESOURCE_TEMPLATES = ["gold", "gold_b", "elixir", "elixir_b", "dark", "gem", ]
resource_templates = []
for x in RESOURCE_TEMPLATES:
    new = Image(name=x, file= "images/resources/" + x + ".png")
    resource_templates.append(new)

# Labs
dir = "towers/labs/"
files = dir_to_list(dir)
labs = []
for file in files:
    new = Image(name=file, file='images/' + file + ".png", threshold=0.7)
    labs.append(new)

# Castles
dir = "towers/castles/"
files = dir_to_list(dir)
castles = []
for file in files:
    new = Image(name=file, file='images/' + file + ".png", threshold=0.7)
    castles.append(new)

# Building
i_wall_text = Image(name="i_wall_text", file="images/towers/wall.png")

# Attacking
# i_next_attack = Image(name="i_next_attack", file=)


img_message = cv2.imread('images/message.png', 0)

# print("Zero regions:", i_builder_zero.regions)

def merge_regions():
    for image in images:
        count = 0
        merge_success = True
        while merge_success and count < 3:
            merge_success = image.merge_regions()
            count +=1

    print("Merged Regions:", count)
    return count

# i_log_thrower_donate2 = next((x for x in images if x.name == 'log_thrower'), None)
# i_log_thrower_donate2 = Image(name="i_log_thrower_donate2", file="images/troops_new/log_thrower_donate2.png")
# i_log_thrower_donate2.show_regions()

# print(i_log_thrower_donate2.regions, len(i_log_thrower_donate2.regions))
# i_log_thrower_donate2.merge_regions()

merge_regions()


def merge_regions_sql(image):
    # print("Merge regions")
    self.load_regions()
    if len(self.regions) == 0: return
    min_increase = None
    min_region_a = None
    min_region_b = None
    min_region_c = None
    total_area = 0
    for region_a in self.regions:
        total_area += region_a[2] * region_a[3]
    print(f"{self} Total area: {total_area}. Regions: {len(self.regions)}")

    for region_a in self.regions:
        for region_b in self.regions:
            if region_a == region_b: continue
            if region_a[0] == region_b[0] and region_a[1] == region_b[1] and region_a[2] == region_b[2] and region_a[
                3] == region_b[3]:
                print("Found Duplicate")
                db_regions_delete(self, min_region_b)
                self.load_regions()
                continue
            size_a = region_a[2] * region_a[3]
            size_b = region_b[2] * region_b[3]
            combined_x1 = min(region_a[0], region_b[0])
            combined_x2 = max(region_a[0] + region_a[2], region_b[0] + region_b[2])
            combined_w = combined_x2 - combined_x1
            combined_y1 = min(region_a[1], region_b[1])
            combined_y2 = max(region_a[1] + region_a[3], region_b[1] + region_b[3])
            combined_h = combined_y2 - combined_y1
            size_c = combined_w * combined_h
            increase = size_c - size_a - size_b
            if min_increase is None or increase < min_increase:
                min_increase = increase
                min_region_a = region_a
                min_region_b = region_b
                min_region_c = [combined_x1, combined_y1, combined_w, combined_h]
    # print(min_increase, min_region_a, min_region_b, min_region_c)
    if len(self.regions) <= self.no_of_regions and min_increase and min_increase > 0:
        # print("Merge regions", len(self.regions), self.no_of_regions, min_increase)
        return False
    if min_region_a is None or min_region_b is None:
        # print("Merge regions - found None region")
        return False
    # print("Merge regions - got here")
    print("Merging regions. Net increase:", min_increase)
    db_regions_delete(self, min_region_a, type=self.type)
    db_regions_delete(self, min_region_b, type=self.type)
    self.save_region(min_region_c)
    return True
