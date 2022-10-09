from attacks import *
from sql import *

accounts = []

def save_tower_details(tower, region):
    get_screenshot(region, filename=tower.name)

def spare_builders(village):
    if village == "main":
        goto(main)
        region = BUILDER_ZERO_REGION
    else:
        goto(builder)
        region = BUILDER_B_ZERO_REGION
    screen = get_screenshot(region)
    val, loc, rect = find(i_builder_zero, screen, show_image=False)
    if val > 0.7: return 0
    val, loc, rect = find(i_builder_one, screen, show_image=False)
    if val > 0.7: return 1
    return 2

def extend_string(string, length):
    extra_spaces = max(length - len(string), 0)
    if extra_spaces > 0:
        string = string + " " * extra_spaces
    return string

class Account():
    def __init__(self, number, th, has_siege, building, building_b, needs_walls, barracks, total_gold, total_elixir,
                 total_dark, army_troops, war_troops, army_troops_b, max_trophies, required_currency):
        self.number = number
        self.th = th
        self.has_siege = has_siege
        self.building = building
        self.building_b = building_b
        self.needs_walls = needs_walls
        self.barracks = barracks
        self.max_trophies = max_trophies
        self.gold = None
        self.elixir = None
        self.dark = None
        self.total_gold = total_gold
        self.total_elixir = total_elixir
        self.total_dark = total_dark
        self.required_currency = required_currency
        self.army_troops = army_troops
        self.war_troops = war_troops
        self.army_troops_b = army_troops_b
        self.attacking = True
        self.next_build = None
        self.next_build_b = None
        self.next_research = None
        self.next_research_b = None
        self.available_upgrades = []
        accounts.append(self)

    def __str__(self):
        return f"Account: {self.number}"

    def next_update(self):
        if spare_builders("main") > 0:
            self.next_build = datetime.now()
        elif self.building:
            goto_list_very_top("main")
            time.sleep(0.2)
            result = build_time.read(BUILDER_LIST_TIMES)
            click_builder()
            self.next_build = text_to_time_2(result)
        else:
            self.next_build = datetime.now()

        pag.click(BOTTOM_LEFT)
        for lab in labs:
            if lab.find():
                lab.click()
                break
        time.sleep(0.2)
        i_research.click()
        time.sleep(0.2)
        result = research_time.read(RESEARCH_TIME)
        result = text_to_time_2(result)
        self.next_research = result
        pag.press("esc")

        if spare_builders("builder") > 0:
            self.next_build_b = datetime.now()
        if self.building_b:
            goto_list_very_top("builder")
            time.sleep(0.2)
            result = build_time.read(BUILDER_LIST_TIMES_B)
            click_builder()
            self.next_build_b = text_to_time_2(result)
        else:
            self.next_build_b = datetime.now()

    def donating(self):
        if self.attacking: return False
        result = True
        for account in accounts:
            if account == account_0: continue
            if account.number < self.number and not account.attacking:
                result = False
            # if result:
            #     db_update(account, "donate", datetime.now() + timedelta(hours=2))
        return result

    def update_resources(self, resources):
        self.gold = resources[0]
        self.elixir = resources[1]
        self.dark = resources[2]
        self.update_attacking()

    def update_attacking(self):
        self.attacking = False
        if self.required_currency == "gold" and self.gold < 0.98 * self.total_gold: self.attacking = True
        if self.required_currency == "dark" and self.dark < 0.98 * self.total_dark: self.attacking = True
        if self.required_currency == "elixir" and self.elixir < 0.98 * self.total_elixir: self.attacking = True
        return

    def war_goals(self):
        total_reward = 500000 ** 2
        if not self.gold or not self.elixir or not self.dark: return [0, 0, 0]
        gold_gap = max(self.total_gold - self.gold, 0)
        elixir_gap = max(self.total_elixir - self.elixir, 0)
        dark_gap = max((self.total_dark - self.dark) * 100, 0)
        total_gap = gold_gap + elixir_gap + dark_gap
        if total_gap == 0: return [0,0,0]
        # print("War goals", gold_gap, total_gap, total_reward)
        gold_goal = int((gold_gap / total_gap * total_reward) ** 0.5)
        elixir_goal = int((elixir_gap / total_gap * total_reward) ** 0.5)
        dark_goal = int((dark_gap / total_gap * total_reward) ** 0.5 / 100)
        return gold_goal, elixir_goal, dark_goal

    def print_info(self):
        text = f"Account {self.number}. Currency {self.required_currency} "
        if self.attacking:    text += "Attacking "
        elif self.donating(): text += "Donating  "
        else:                 text += "          "
        if self.gold: text += f"Gold {int(round(self.gold / self.total_gold, 2) * 100)}% "
        if self.dark: text += f"Dark {int(round(self.dark / self.total_dark, 2) * 100)}% "
        text = extend_string(text, 61)
        text += f"War goals {self.war_goals()} "
        text = extend_string(text, 91)
        if self.building: text += f"Build {time_to_string(self.next_build)} "
        text = extend_string(text, 113)
        if self.building_b: text += f"Build_b {time_to_string(self.next_build_b)} "
        text = extend_string(text, 133)
        text += f"Research {time_to_string(self.next_research)} "
        print(text)

account_data = [
    (0, 13, True, True, False, False, 4, 18000000, 18000000, 300000, BARBS_13, DRAGONS_300, troops1, 1800, "gold"),
    (1, 13, True, True, False, False, 4, 18000000, 18000000, 300000, BARBS_13, DRAGONS_300, troops1, 1800, "gold"),
    (2, 11, False, True, True, False, 4, 10000000, 10000000, 200000, BARBS_11, DRAGONS_260, troops2, 1300, "gold"),
    (3, 10, False, True, True, False, 4, 8500000, 8500000, 200000, GIANT240, DRAGONS_240, troops3, 1100, "gold"),]

for number, th, has_siege, building, building_b, needs_walls, barracks, gold, elixir, dark, army_troops, war_troops, army_troops_b, max_trophies, required_currency in account_data:
    Account(number, th, has_siege, building, building_b, needs_walls, barracks, gold, elixir, dark, army_troops, war_troops, army_troops_b, max_trophies, required_currency)

account_0 = next((x for x in accounts if x.number == 0), None)
account_1 = next((x for x in accounts if x.number == 1), None)
account_2 = next((x for x in accounts if x.number == 2), None)
account_3 = next((x for x in accounts if x.number == 3), None)
accounts.remove(account_0)

current_account = None

