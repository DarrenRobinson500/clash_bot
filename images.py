from object_recognition import *
from regions import *

images = []

class Image():
    def __init__(self, name, file, threshold=0.8, always_slow=False):
        self.name = name
        self.image = cv2.imread(file, 0)
        self.regions = []
        self.load_regions()
        self.threshold = threshold
        self.always_slow = always_slow
        images.append(self)

    def __str__(self):
        return self.name

    def click(self):
        val, loc, rect = self.find_detail(fast=True)
        if val < self.threshold:
            val, loc, rect = self.find_detail(fast=False)
        if val > self.threshold:
            pag.click(loc)
            # print("Clicked", self.name, round(val,2), self.threshold, loc)
            return True
        else:
            print("Click Failure:", self.name, round(val,2), self.threshold)
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
        # print(self.name, val)
        return val > self.threshold

    def find_detail(self, show_image=False, fast=False):
        if self.always_slow: fast = False
        # Regions
        for region in self.regions:
            screen = get_screenshot(region)
            if self.image is None:
                print("Find - No image provided:", self.name)
                return 0, 0, 0
            if show_image:
                show(self.image)
                show(screen)
            try:
                result = cv2.matchTemplate(screen, self.image, method)
            except:
                print("Image didn't fit in region:", self.name)
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
        print("Find detail - checking whole screen", self)
        screen = get_screenshot()
        if show_image:
            show(self.image)
            show(screen)
        # print("Find detail:", self.name)
        result = cv2.matchTemplate(screen, self.image, method)
        min_val, val, min_loc, loc = cv2.minMaxLoc(result)
        rect = (loc[0], loc[1], self.image.shape[1], self.image.shape[0])
        loc = (int(rect[0] + rect[2] / 2), int(rect[1] + rect[3] / 2))
        region = [max(rect[0] - 1, 0), max(rect[1] - 1, 0), rect[2] + 2, rect[3] + 2]
        if val > self.threshold:
            self.save_region(region)
        return round(val,2), loc, rect

    def load_regions(self):
        regions = db_regions_get(self)
        for r in regions:
            region = [r[1], r[2], r[3], r[4]]
            self.regions.append(region)

    def save_region(self, region):
        if region not in self.regions:
            self.regions.append(region)
            db_regions_add(self, region)

    def show(self):
        show(self.image)

    def merge_regions(self):
        min_increase = None
        min_region_a = None
        min_region_b = None
        min_region_c = None
        total_area = 0
        for region_a in self.regions:
            total_area += region_a[2] * region_a[3]
        # print(f"Total area: {total_area}. Regions: {len(self.regions)}")

        for region_a in self.regions:
            for region_b in self.regions:
                if region_a == region_b: continue
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
        if len(self.regions) <= 5 and min_increase and min_increase > 0: return False
        if min_region_a is None or min_region_b is None: return False
        db_regions_delete(self, min_region_a)
        db_regions_delete(self, min_region_b)
        self.save_region(min_region_c)
        return True

# Tower images
i_lab8 = Image(name="i_lab8", file="images/towers/lab8.png")
i_lab9 = Image(name="i_lab9", file="images/towers/lab9.png")
i_lab11 = Image(name="i_lab11", file="images/towers/lab11.png")
labs = [i_lab8, i_lab9, i_lab11]

# Navigation images
i_ad_cross = Image(name="i_ad_cross", file='images/nav/ad_cross.png')
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
i_maintenance = Image(name="i_maintenance", file='images/nav/maintenance.png')
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
i_research = Image(name="i_research", file='images/nav/research.png')
i_return_home = Image(name="i_return_home", file='images/nav/return_home.png')
i_return_home_2 = Image(name="i_return_home_2", file='images/nav/return_home_2.png')
i_return_home_3 = Image(name="i_return_home_3", file='images/nav/return_home_3.png')
i_settings = Image(name="i_settings", file='images/nav/settings.png')
i_settings_on_main = Image(name="i_settings_on_main", file='images/nav/settings_on_main.png')
i_siege_tab = Image(name="i_siege_tab", file='images/nav/siege_tab.png')
i_siege_tab_dark = Image(name="i_siege_tab_dark", file='images/nav/siege_tab_dark.png')
i_spells_tab = Image(name="i_spells_tab", file='images/nav/spells_tab.png')
i_spells_tab_dark = Image(name="i_spells_tab_dark", file='images/nav/spells_tab_dark.png')
i_splash = Image(name="i_splash", file='images/nav/splash.png')
i_start_eyes = Image(name="i_start_eyes", file='images/nav/start_eyes.png')
i_surrender = Image(name="i_surrender", file='images/nav/surrender.png')
i_surrender_okay = Image(name="i_surrender_okay", file='images/nav/surrender_okay.png')
i_switch_account = Image(name="i_switch_account", file='images/nav/switch_account.png')
i_troops_tab = Image(name="i_troops_tab", file='images/nav/troops_tab.png')
i_troops_tab_dark = Image(name="i_troops_tab_dark", file='images/nav/troops_tab_dark.png')
i_try_again = Image(name="i_try_again", file='images/nav/try_again.png')
i_versus_battle = Image(name="i_versus_battle", file='images/nav/versus_battle.png')
i_war_okay = Image(name="i_war_okay", file='images/nav/war_okay.png')
i_wins = Image(name="i_wins", file='images/nav/wins.png')
i_x = Image(name="i_unknown", file='images/nav/x.png')

i_suggested_upgrades = Image(name="i_suggested_upgrades", file='images/towers/suggested_upgrades.png')
i_upgrades_in_progress = Image(name="i_upgrades_in_progess", file='images/towers/upgrades_in_progess.png')

more_donates = cv2.imread('images/more_donates.png', 0)
img_message = cv2.imread('images/message.png', 0)
donate_cross = cv2.imread('images/donate_cross.png', 0)
# i_builder = cv2.imread('images/nav/builder.png', 0)
i_builder_zero = cv2.imread('images/builder_zero.png', 0)
i_builder_one = cv2.imread('images/builder_one.png', 0)
i_upgrade_button = cv2.imread('images/upgrade.png', 0)
i_attack_b_0 = cv2.imread('images/attack_b/attack_0.png', 0)
i_attack_b_1 = cv2.imread('images/attack_b/attack_1.png', 0)
i_attack_b_2 = cv2.imread('images/attack_b/attack_2.png', 0)
i_attack_b_3 = cv2.imread('images/attack_b/attack_3.png', 0)


count = 0
for image in images:
    print(image.name, len(image.regions))
    merge_success = image.merge_regions()
    if merge_success: count += 1

print("Merged Regions:", count)
