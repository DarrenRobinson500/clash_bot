from attacks import *
from sql import *
from sql_games import *
# from games import *

trophy_limits = {0: 0, 1: 100, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600, 7: 700, 8: 1000, 9: 1200, 10: 1400, 11: 1600, 12: 1800, 13: 2000}

accounts = []

def save_tower_details(tower, region):
    get_screenshot(region, filename=tower.name)


def extend_string(string, length):
    extra_spaces = max(length - len(string), 0)
    if extra_spaces > 0:
        string = string + " " * extra_spaces
    return string

def get_donation_troops():
    donation_troops = []
    for troop in troops:
        if troop.donations > 0 and troop.type != "siege":
            for x in range(troop.donation_count):
                donation_troops.append(troop)
    donation_siege = [x for x in troops if x.type == 'siege' and x.donations > 0]
    if len(donation_siege) < 6:
        for _ in range(6 - len(donation_siege)):
            donation_siege.append(log_thrower)
    return donation_troops, donation_siege

def get_donation_troops_min():
    donation_troops = []
    for troop in troops:
        if troop.donations > 0 and troop.type != "siege":
            donation_troops.append(troop)
    donation_siege = [x for x in troops if x.type == 'siege' and x.donations > 0]
    if len(donation_siege) < 6:
        for _ in range(6 - len(donation_siege)):
            donation_siege.append(log_thrower)
    return donation_troops, donation_siege

class Account():
    def __init__(self, data):
        self.number = data['number']
        self.th = data['th']
        self.has_siege = data['has_siege']
        self.requires_siege = data['requires_siege']
        self.building = data['building']
        self.building_b = data['building_b']
        self.max_trophies = trophy_limits[self.th]
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
        icon = data['icon']
        self.icon = Image(icon, f"images/accounts/{icon}.png")
        self.troops_to_build = None
        self.attacking = True
        self.researching = True
        self.next_build = db_read(self.number, "build")
        self.next_build_b = db_read(self.number, "build_b")
        self.next_research = db_read(self.number, "research")
        self.build_cycle = 0
        self.needs_walls = data['needs_walls']
        self.next_research_b = None
        self.available_upgrades = []
        self.use_suggestion_b = False
        self.clan_troops = None
        self.clan_troops_war = None
        self.current_game = None
        self.playing_games = True
        self.cwl_attacks_left = False
        self.cwl_donations_left = True
        self.mode = None
        if self.number in [1,2]:
            self.cwl_donations_left = True
        accounts.append(self)

    def __str__(self):
        return f"Account {self.number}:"

    def set_mode(self):
        if account_0.mode == "cwl":
            if self in war_participants:
                if self.cwl_donations_left:
                    self.mode = "Donating CWL"
                    self.update_troops_to_build()
                    return
                elif self.attacking:
                    self.mode = "Attacking"
                    self.update_troops_to_build()
                    return
                elif self.donating():
                    self.mode = "Donating"
                    self.update_troops_to_build()
                    return
                elif self.cwl_attacks_left:
                    self.mode = "War troops"
                    self.update_troops_to_build()
                    return
        if account_0.mode == "preparation":
            if self in war_participants:
                if self.cwl_donations_left:
                    self.mode = "Donating War"
                    self.update_troops_to_build()
                    return
                elif self.attacking:
                    self.mode = "Attacking"
                    self.update_troops_to_build()
                    return
                elif self.donating():
                    self.mode = "Donating"
                    self.update_troops_to_build()
                    return
        if account_0.mode == "battle_day":
            if self in war_participants:
                if self.attacking:
                    self.mode = "Attacking"
                    self.update_troops_to_build()
                    return
                elif self.donating():
                    self.mode = "Donating"
                    self.update_troops_to_build()
                    return
                elif self.cwl_attacks_left:
                    self.mode = "War Troops"
                    self.update_troops_to_build()
                    return
        if self.attacking:
            self.mode = "Attacking"
            self.update_troops_to_build()
            return
        if self.donating():
            self.mode = "Donating"
            self.update_troops_to_build()
            return
        self.mode = ""

    def update_troops_to_build(self):
        # if self.mode in ["Donating CWL", "Donating War", "War troops"]:
        #     donation_troops, donation_siege = get_donation_troops_min()
        # else:
        donation_troops, donation_siege = get_donation_troops()

        if self.has_siege:
            donation_troops += donation_siege
        war_troops = [dragon] * 5 + [super_barb] * 10 + [lightening, freeze] * 7 + [poison]
        war_donation = [super_minion] * 20 + [minion] * 20 + [archer] * 5 + [super_barb] * 5
        self.troops_to_build = self.convert_attack_to_troops(self.army_troops)

        if self.mode in ["Donating CWL", "Donating War"]: self.troops_to_build = war_donation
        if self.mode in ["War Troops"]: self.troops_to_build = war_troops
        if self.mode in ["Donating"]:
            self.troops_to_build = donation_troops
            if account_0.mode == "cwl": self.troops_to_build += war_troops
        if self.mode in ["Attacking"]: self.troops_to_build = self.convert_attack_to_troops(self.army_troops)

        for troop in self.troops_to_build:
            if type(troop) != type(super_barb):
                self.troops_to_build.remove(troop)
        # self.troops_to_build.sort(key=lambda x: x.type, reverse=True)
        # print("Troops to build:", self, self.mode, objects_to_str(self.troops_to_build))

    def convert_attack_to_troops(self, data):
        troops_required = data['initial_troops'] + data['final_troops']
        for x, no in data['troop_group']:
            troops_required += [x] * no * data['troop_groups']

        troops_required += [lightening] * data['lightening']
        if self.has_siege:
            troops_required += [log_thrower] * 5

        return troops_required

    def print_troops(self):
        print("Print troops")

        troops_counter = Counter(self.troops_to_build)
        string = ""
        for t in troops_counter:
            string += f"{t}: {troops_counter[t]}, "
        print(self, string[:-2])

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
        builder_list_times = get_screenshot(BUILDER_LIST_TIMES, filename=f"tracker/builder_time{self.number}main")
        get_screenshot(RESOURCES_G, filename=f"tracker/gold{self.number}")
        time.sleep(0.2)
        result = build_time.read_screen(builder_list_times, show_image=False)
        result = text_to_time_2(result)
        if result:
            result += timedelta(minutes=2)
        else:
            result = datetime.now() + timedelta(minutes=10)
        self.next_build = result
        db_update(self, "build", result)

    def update_build_b_time(self):
        goto_list_very_top("builder")
        builder_list_times = get_screenshot(BUILDER_LIST_TIMES_B, filename=f"tracker/builder_time{self.number}builder")
        time.sleep(0.2)
        result = build_time.read_screen(builder_list_times, show_image=False)
        print("Raw result:", result)
        result = text_to_time_2(result)
        print(result)
        if result:
            result += timedelta(minutes=2)
        else:
            result = datetime.now() + timedelta(minutes=10)
        self.next_build_b = result
        db_update(self, "build_b", result)

    def update_lab_time(self):
        if not self.researching: return
        goto(l_lab)
        screen = get_screenshot(RESEARCH_TIME, filename=f"tracker/research_time{self.number}main")
        result = research_time.read_screen(screen, show_image=False)
        result = text_to_time_3(result)
        if result:
            result = result + timedelta(minutes=1)
        else:
            result = datetime.now() + timedelta(minutes=120)
        self.next_research = result
        db_update(self, "research", result)
        print("Next research:", result)

    def donating(self):
        if self.attacking: return False
        result = True
        for account in accounts:
            if account.number == 3 and not account.attacking:
                result = True
            if account.number < self.number and not account.attacking:
                result = False
        if result:
            self.mode = "Donating"
            # self.update_troops_to_build()
            db_update(self, "donate", datetime.now() + timedelta(minutes=20))
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
        base_reward = 600000
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
        text = f"Account {self.number}: "
        text += self.mode
        text = extend_string(text, 30)
        if self.gold and self.gold > 0: text += f"Gold {int(round(self.gold / self.total_gold, 2) * 100)}% "
        text = extend_string(text, 40)
        if self.dark and self.total_dark > 0: text += f"Dark {int(round(self.dark / self.total_dark, 2) * 100)}% "
        text = extend_string(text, 52)
        text += f"War goals {self.war_goals()} "
        text = extend_string(text, 80)
        if self.building: text += f"Build {time_to_string(self.next_build)} "
        text = extend_string(text, 102)
        if self.building_b: text += f"Build_b {time_to_string(self.next_build_b)} "
        text = extend_string(text, 122)
        text += f"Research {time_to_string(self.next_research)} "
        print(text)

def get_account(account_number):
    for account in accounts + [account_0, ]:
        if account_number == account.number: return account

def change_accounts(account_number, target_base="main"):
    global current_account, current_location
    if current_account:
        print(f"Change accounts from {current_account} to {account_number}")
    if account_number == current_account: return
    account = get_account(account_number)
    goto(change_account)
    time.sleep(0.2)
    account.icon.click()
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
    account.icon.click()
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
                    # goto(main)
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
    'requires_siege': False,
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
    'icon': None,
    'needs_walls': False
}

account_data_1 = {
    'number': 1,
    'th': 13,
    'has_siege': True,
    'requires_siege': False,
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
    'icon': "bad_daz",
    'needs_walls': False
}

account_data_2 = {
    'number': 2,
    'th': 11,
    'has_siege': False,
    'requires_siege': True,
    'building': True,
    'building_b': True,
    'total_gold': 10000000,
    'total_elixir': 10000000,
    'total_dark': 200000,
    'army_troops': BARBS_52,
    'war_troops': DRAGONS_260,
    'games_troops': GIANT240_GAMES,
    'army_troops_b': troops2,
    'required_currency': "gold",
    'icon': "daz",
    'needs_walls': False
}

account_data_3 = {
    'number': 3,
    'th': 10,
    'has_siege': False,
    'requires_siege': False,
    'building': True,
    'needs_walls': False,
    'building_b': True,
    'total_gold': 8500000,
    'total_elixir': 6000000,
    'total_dark': 200000,
    'army_troops': GIANT240,
    'war_troops': DRAGONS_240,
    'games_troops': GIANT200_GAMES,
    'army_troops_b': troops3,
    'required_currency': "gold",
    'icon': "bob",
}

for data in [account_data_0, account_data_1, account_data_2, account_data_3]:
# for data in [account_data_0, account_data_1, account_data_2]:
    Account(data)

def return_account(number):
    return next((x for x in accounts if x.number == number), None)

account_0 = next((x for x in accounts if x.number == 0), None)
account_1 = next((x for x in accounts if x.number == 1), None)
account_2 = next((x for x in accounts if x.number == 2), None)
account_3 = next((x for x in accounts if x.number == 3), None)
accounts.remove(account_0)

war_participants = [account_1, ]
# war_participants = []

# account_1.use_suggestion_b = True
# account_1.clan_troops = [super_barb] * 9
# account_1.clan_troops_war = [dragon, dragon, bloon]
# account_2.clan_troops = [super_barb] * 7
# account_2.clan_troops_war = [dragon, bloon, bloon, bloon]

current_account = None



