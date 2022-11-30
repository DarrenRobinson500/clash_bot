from attacks import *
from sql import *
from sql_games import *
# from games import *

accounts = []

def save_tower_details(tower, region):
    get_screenshot(region, filename=tower.name)


def extend_string(string, length):
    extra_spaces = max(length - len(string), 0)
    if extra_spaces > 0:
        string = string + " " * extra_spaces
    return string

class Account():
    def __init__(self, data):
        self.number = data['number']
        self.th = data['th']
        self.has_siege = data['has_siege']
        self.building = data['building']
        self.building_b = data['building_b']
        trophies = [0, 100, 200, 300, 400, 500, 600, 700, 1000, 1200, 1400, 1600, 1800, 2000]
        self.max_trophies = trophies[self.th]
        self.gold = None
        self.elixir = None
        self.dark = None
        self.total_gold = data['total_gold']
        self.total_elixir = data['total_elixir']
        self.total_dark = data['total_dark']
        self.required_currency = data['required_currency']
        self.army_troops = data['army_troops']
        self.war_troops = data['war_troops']
        self.games_troops = data['games_troops']
        self.army_troops_b = data['army_troops_b']
        self.attacking = True
        self.researching = True
        self.next_build = None
        self.next_build_b = None
        self.next_research = None
        self.next_research_b = None
        self.available_upgrades = []
        self.use_suggestion_b = False
        self.clan_troops = None
        self.clan_troops_war = None
        self.current_game = None
        self.playing_games = True
        accounts.append(self)

    def __str__(self):
        return f"Account: {self.number}"

    # def start_game(self):


    def next_update(self):
        if spare_builders(self, "main") > 0:
            self.next_build = datetime.now()
            blank = np.zeros((BUILDER_LIST_TIMES[3], BUILDER_LIST_TIMES[2], 3), np.uint8)
            cv2.imwrite(f'temp/tracker/builder_time{self.number}main.png', blank)
        elif self.building:
            self.update_build_time()
        else:
            self.next_build = datetime.now()

        pag.click(BOTTOM_LEFT)
        self.update_lab_time()

        if spare_builders(self, "builder") > 0:
            self.next_build_b = datetime.now()
            blank = np.zeros((BUILDER_LIST_TIMES_B[3], BUILDER_LIST_TIMES_B[2], 3), np.uint8)
            cv2.imwrite(f'temp/tracker/builder_time{self.number}builder.png', blank)
        else:
            goto_list_very_top("builder")
            get_screenshot(BUILDER_LIST_TIMES_B, filename=f"tracker/builder_time{self.number}builder")
        time.sleep(0.2)
        result = build_time.read(BUILDER_LIST_TIMES_B)
        if self.building_b:
            self.next_build_b = text_to_time_2(result)
        else:
            self.next_build_b = datetime.now() + timedelta(hours=1)
        pag.click(BOTTOM_LEFT)

    def update_build_time(self):
        goto_list_very_top("main")
        get_screenshot(BUILDER_LIST_TIMES, filename=f"tracker/builder_time{self.number}main")
        get_screenshot(NEXT_COMPLETION, filename=f"tracker/next_completion{self.number}main")
        get_screenshot(RESOURCES_G, filename=f"tracker/gold{self.number}")
        time.sleep(0.2)
        result = build_time.read(BUILDER_LIST_TIMES)
        result = text_to_time_2(result)
        if result:
            result += timedelta(minutes=2)
        else:
            result = datetime.now() + timedelta(minutes=10)
        self.next_build = result
        db_update(self, "build", result)

    def update_lab_time(self):
        if not self.researching: return
        goto(lab)
        get_screenshot(RESEARCH_TIME, filename=f"tracker/research_time{self.number}main")
        result = research_time.read(RESEARCH_TIME)
        result = text_to_time_2(result) + timedelta(minutes=1)
        self.next_research = result
        db_update(self, "research", result)
        print("Next research:", result)

    def donating(self):
        if self.attacking: return False
        result = True
        for account in accounts:
            if account.number < self.number and not account.attacking:
                result = False
            # if result:
            #     db_update(account, "donate", datetime.now() + timedelta(hours=2))
        return result

    def update_resources(self, resources):
        if resources[0] > self.total_gold * 2: resources[0] = resources[0] / 10
        self.gold = resources[0]
        self.elixir = resources[1]
        self.dark = resources[2]
        self.update_attacking()

    def update_attacking(self):
        start_mode = True
        if self.attacking is False: start_mode = False
        self.attacking = False
        if self.required_currency == "gold" and self.gold < 0.96 * self.total_gold: self.attacking = True
        if self.required_currency == "dark" and self.dark < 0.96 * self.total_dark: self.attacking = True
        if self.required_currency == "elixir" and self.elixir < 0.9 * self.total_elixir: self.attacking = True
        if start_mode is False and self.attacking:
            db_update(self, "attack", datetime.now() + timedelta(minutes=-20))
        return

    def war_goals(self):
        base_reward = 500000
        if self.th <= 4: base_reward = 5000
        if self.th == 5: base_reward = 25000
        if self.th == 6: base_reward = 100000
        if self.th == 7: base_reward = 200000
        if self.th == 8: base_reward = 300000
        if self.th == 9: base_reward = 400000
        total_reward = base_reward ** 2
        if not self.gold or not self.elixir or not self.dark: return [0, 0, 0]
        gold_gap = max(self.total_gold - self.gold, 0)
        elixir_gap = max(self.total_elixir - self.elixir, 0) * 0
        dark_gap = max((self.total_dark - self.dark) * 100, 0)
        total_gap = gold_gap + elixir_gap + dark_gap
        if total_gap == 0: return [0,0,0]
        # print("War goals", gold_gap, total_gap, total_reward)
        gold_goal = int((gold_gap / total_gap * total_reward) ** 0.5)
        elixir_goal = int((elixir_gap / total_gap * total_reward) ** 0.5)
        dark_goal = int((dark_gap / total_gap * total_reward) ** 0.5 / 100)
        return gold_goal, elixir_goal, dark_goal

    def print_info(self):
        text = f"Account {self.number} "
        if self.attacking:    text += "Attacking "
        elif self.donating(): text += "Donating  "
        else:                 text += "          "
        if self.gold and self.gold > 0: text += f"Gold {int(round(self.gold / self.total_gold, 2) * 100)}% "
        text = extend_string(text, 30)
        if self.dark and self.total_dark > 0: text += f"Dark {int(round(self.dark / self.total_dark, 2) * 100)}% "
        text = extend_string(text, 42)
        text += f"War goals {self.war_goals()} "
        text = extend_string(text, 70)
        if self.building: text += f"Build {time_to_string(self.next_build)} "
        text = extend_string(text, 92)
        if self.building_b: text += f"Build_b {time_to_string(self.next_build_b)} "
        text = extend_string(text, 112)
        text += f"Research {time_to_string(self.next_research)} "
        print(text)

def change_accounts(account_number, target_base="main"):
    global current_account, current_location
    if current_account:
        print(f"Change accounts from {current_account} to {account_number}")
    if account_number == current_account: return
    goto(change_account)
    time.sleep(0.2)
    loc = [(0,0), (1184, 651), (1184, 524), (1184, 792), (1184, 930),][account_number]
    pag.click(loc)
    time.sleep(0.2)
    # if i_otto.find() or i_master.find():
    #     current_location = builder
    # else:
    #     current_location = main
    if target_base == "main": goto(main)
    else: goto(builder)
    zoom_out()
    current_account = account_number
    try:
        if current_account.gold is None:
            current_account.update_resources(current_resources())
    except:
        pass
    return

def change_accounts_fast(account):
    global current_account
    if current_account:
        print(f"Change accounts from {current_account} to {account}")
    else:
        print(f"Change accounts from None to {account}")
    if account == current_account:
        print("Change accounts fast: Already in account", account)
        return
    goto(change_account)
    time.sleep(0.2)
    loc = [(0,0), (1184, 651), (1184, 524), (1184, 792), (1184, 930),][account.number]
    pag.click(loc)
    found = False
    count = 0
    while not found:
        time.sleep(0.1)
        for image in [i_builder, i_otto, i_master]:
            if image.find():
                if image == i_builder:
                    new_location = main
                else:
                    new_location = builder
                    goto(main)
                change_current_location(new_location)
                found = True
        count += 1
        if count > 30:
            goto(main)
            found = True
    zoom_out()
    print("New account:", account)
    current_account = account

# account_data = [
#     (0, 13, True, True, False, False, 4, 18000000, 18000000, 300000, BARBS_60, DRAGONS_300, troops1, 0, "gold"),
#     (1, 13, True, True, False, False, 4, 18000000, 18000000, 300000, BARBS_60, DRAGONS_300, troops1, 2000, "gold"),
#     (2, 11, False, True, True, False, 4, 10000000, 10000000, 200000, BARBS_52, DRAGONS_260, troops2, 1500, "gold"),
#     (3, 10, False, True, False, False, 4, 8500000, 8500000, 200000, GIANT240, DRAGONS_240, troops2, 1300, "gold"),
#     (4, 7, False, True, False, True, 4, 4000000, 10000, 0, GIANT200, DRAGONS_240, troops3, 750, "gold"),
# ]
#
account_data_0 = {
    'number': 0,
    'th': 0,
    'has_siege': False,
    'building': False,
    'building_b': False,
    'total_gold': 0,
    'total_elixir': 0,
    'total_dark': 0,
    'army_troops': None,
    'war_troops': None,
    'games_troops': None,
    'army_troops_b': None,
    'required_currency': None,
}

account_data_1 = {
    'number': 1,
    'th': 13,
    'has_siege': True,
    'building': True,
    'building_b': False,
    'total_gold': 18000000,
    'total_elixir': 18000000,
    'total_dark': 300000,
    'army_troops': BARBS_60,
    'war_troops': DRAGONS_300,
    'games_troops': BARBS_60_GAMES,
    'army_troops_b': troops1,
    'required_currency': "gold",
}

account_data_2 = {
    'number': 2,
    'th': 12,
    'has_siege': False,
    'building': True,
    'building_b': True,
    'total_gold': 10000000,
    'total_elixir': 10000000,
    'total_dark': 240000,
    'army_troops': BARBS_52,
    'war_troops': DRAGONS_260,
    'games_troops': BARBS_52_GAMES,
    'army_troops_b': troops2,
    'required_currency': "gold",
}

account_data_3 = {
    'number': 3,
    'th': 11,
    'has_siege': False,
    'building': True,
    'building_b': False,
    'total_gold': 8500000,
    'total_elixir': 8500000,
    'total_dark': 200000,
    'army_troops': GIANT240,
    'war_troops': DRAGONS_260,
    'games_troops': GIANT240_GAMES,
    'army_troops_b': troops2,
    'required_currency': "gold",
}

account_data_4 = {
    'number': 4,
    'th': 8,
    'has_siege': False,
    'building': True,
    'building_b': False,
    'total_gold': 6000000,
    'total_elixir': 6000000,
    'total_dark': 80000,
    'army_troops': GIANT200,
    'war_troops': DRAGONS_240,
    'games_troops': GIANT200_GAMES,
    'army_troops_b': troops3,
    'required_currency': "gold",
}

for data in [account_data_0, account_data_1, account_data_2, account_data_3, account_data_4]:
    Account(data)

def return_account(number):
    return next((x for x in accounts if x.number == number), None)

account_0 = next((x for x in accounts if x.number == 0), None)
account_1 = next((x for x in accounts if x.number == 1), None)
account_2 = next((x for x in accounts if x.number == 2), None)
account_3 = next((x for x in accounts if x.number == 3), None)
account_4 = next((x for x in accounts if x.number == 4), None)
accounts.remove(account_0)

account_1.use_suggestion_b = True
account_1.clan_troops = [super_barb] * 9
account_1.clan_troops_war = [dragon, dragon, bloon]
account_2.clan_troops = [super_barb] * 7
account_2.clan_troops_war = [dragon, bloon, bloon, bloon]

current_account = None



