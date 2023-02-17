from datetime import timedelta
import os

PRINT_CV2 = False
VERBOSE_LOG = False
# current_account = 0

last_move = ["none", 0]
BACKLOG = (160, 190, 1550, 140)

BOTTOM_LEFT = (290, 960)
TOP_RIGHT = (1804, 57)

CURRENCIES = ["elixir1", "dark", "gold", "elixir"]

build_preferences_e1 = [
    "lab", "castle", "army", "workshop", "spell_factory", "barracks", "gold_storage", "warden", "dark_drill",
]

build_preferences_d = [
    "champ", "queen", "king",
]

build_preferences_g = [
    # "wall",
    "elixir_storage",
    "giga_inferno", "eagle", "inferno",
    "air_defence", "x_bow",
    "archer_tower", "cannon", "mortar", "wizard_tower","tesla",
    "air_sweeper",
    "bomb_tower", #"scattershot",
    "air_mine", "giant_bomb", "bomb", "spring_trap","skeleton_trap",
]

build_preferences_e = [
    "dark_storage", "dark_drill",
]

build_b_preferences_e1 = [
    "gold_mine", "gold_storage", "gem", "lab", "machine",
]

build_b_preferences_g = [
    "elixir_collector", "elixir_storage",
    "mega_tesla", "mortar",
    "lava", "roaster", "air_bombs", "giant_cannon", "guard_post", "tesla", "fire_crackers",
    "double_cannon", "cannon", "archer_tower",
    "mega_mine", "mine", "spring_trap", "push_trap",
    "wall",
]

build_b_preferences_e = [
    "barracks",
]


info = {
    "gold": [None,None,None],
    "build": [0,0,0],
    "build_b": [0, 0, 0],
    "coin": [0, 0, 0],
    "clock": [0, 0, 0],
    "trophies": [0, 0, 0],
    "lose_trophies": [0, 0, 0],
}

DP = None
scroll_adj = None

STANDARD_DP = (672, 445)
STANDARD_DP2 = (672, 445)
TROOPS_SLIDE = ["golem", "witch", "minion"]
TROOPS = ["barb", "archer", "giant","bomb", "wizard", "bloons", "healer", "pekka", "dragon", "edrag", "super_barb", "super_goblin", ] + TROOPS_SLIDE
SPELLS = ["lightening", "freeze", "poison"]
SIEGE = ["ram",]
ALL_TROOPS = TROOPS + SPELLS + SIEGE

HEROES_AND_RAMS = ["king", "queen","warden", "champ", "clan", "clan_ram", "clan_ram2", "ram", "ram_empty"]

DONT_DONATE = ["bomb", "super_goblin", ]
TROOP_TRAIN_EXT = ["wizard", "bomb", "super_goblin", "super_barb", "lightening", "freeze", "dragon", "edrag", "witch", "bloons"]
TROOP_ATTACK_EXT = ["super_goblin", "super_barb", ]
TROOP_DONATE_EXT = ["super_barb", "lightening","edrag","bloons","ram",]

# BUSHES = [
#     "trees/bush", "trees/bush2",
#     "trees/tree", "trees/tree2", "trees/tree3", "trees/tree4", "trees/tree5", "trees/tree6", "trees/tree7",
#     "trees/tree8", "trees/tree9", "trees/tree10", "trees/tree11", "trees/tree12", "trees/tree13", "trees/tree14",
#     "trees/tree15", "trees/tree16", #"trees/tree10", "trees/tree11", "trees/tree12", "trees/tree13", "trees/tree14",
#     "trees/stump", "trees/stump2",
#     "trees/trunk",
#     "trees/grove", "trees/grove2", "trees/grove3", "trees/grove4",
#     "trees/gem",
#     "trees/cake",
# ]

RESOURCE_TEMPLATES = ["resources/gold", "resources/gold_b", "resources/elixir", "resources/elixir_b", "resources/dark", "resources/gem", ]

# ==========================
# === LINES FOR RAM RAID ===
# ==========================

x, y = 1089, 159
width, height = 1089-442, 639-159

top = (x, y)
left = (x-width, y+height)
right = (x+width, y+height)
bottom = (x, y + 2* height)
grad = (top[1] - right[1]) / (top[0] - right[0])
lines = [(top[0], top[1], grad),(top[0], top[1], -grad), (bottom[0], bottom[1], grad), (bottom[0], bottom[1], -grad),]

# ===============
# === Regions ===
# ===============

ALL = (0,0,1919,1008)

# Main Screen
BUILDER_REGION = (829, 40, 270, 120)
BUILDER_ZERO_REGION = (888, 109, 100, 50)
BUILDER_B_REGION = (980, 40, 120, 120)
BUILDER_B_ZERO_REGION = (1044, 114, 100, 50)
BUILDER_B_LIST_REGION = (905, 160, 390, 600)
BUILDER_LIST_REGION = (700, 160, 350, 600)
BUILDER_LIST_TIMES = (961, 259, 140, 50)
BUILDER_FIRST_ROW = (680, 219, 490, 60)
BUILDER_BOTTOM = (760, 660, 40, 40)
NEXT_COMPLETION = (749, 227, 370, 50)
RESOURCES_G = (1580, 110, 290, 47)
RESOURCES_E = (1580, 192, 290, 47)
RESOURCES_D = (1580, 281, 290, 47)
RESOURCES = (1620,60, 350, 250)
LEVEL = (315,67, 80, 80)
SELECTED_TOWER = (635, 677, 1000, 70)
SELECTED_TOWER_BUTTONS = (540,758, 1100, 200)
TROPHIES = (395,217, 90, 40)
CHAT_SPOT = (600, 900, 250, 140)
FIND_A_MATCH_SPOT = (1475, 610, 400, 170)
ATTACK_SPOT = (735, 70, 400, 100)
ATTACKING_SPOT = (200, 600, 400, 400)
MAINTENANCE_SPOT = (800, 200, 1400, 400)
SWITCH_ACCOUNT_SPOT = (1486, 366, 350, 100)
FORGE_SPOT = (1010, 150, 250, 100)
FORGE_PATH_SPOT = (850,750, 350, 250)
ATTACK_B_SPOT = (1060, 800, 140, 100)
OKAY_SPOT = (840,330, 600, 650)
OKAY2_SPOT = (930,790, 350, 200)
RETURN_HOME_2_SPOT = (290, 790, 200, 200)
BLUESTACKS_MESSAGE_SPOT = (1610, 750, 250, 150)
ATTACK_BUTTON = (280, 800, 200, 200)
main_regions = [
    BUILDER_REGION, BUILDER_LIST_REGION, BUILDER_LIST_TIMES, RESOURCES_G, RESOURCES_E, RESOURCES_D, RESOURCES, LEVEL,
    SELECTED_TOWER, TROPHIES, CHAT_SPOT, ATTACK_SPOT, ATTACKING_SPOT
                ]

TRADER_TIME = (493,179,190,60)

# LAB
RESEARCH_TIME = (800, 320, 360, 60)

# GAMES
CURRENT_GAME = (920, 195, 200, 210)
GAMES_SCORE = (530, 895, 190, 40)

# NON-DESTINATIONS
SUPERCELL_LOGIN_SPOT = (500, 870, 550, 500)
BLUESTACKS_APP_SPOT = (1500, 120, 200, 200)
PYCHARM_RUNNING_SPOT = (0, 0, 45, 45)
RELOAD_SPOT = (700,575,250,100)
RAID_WEEKEND_NEXT_SPOT = (1300,880,300,100)

# Accounts
ACCOUNT_ICONS = (1136, 467, 110, 420)
change_accounts_regions = [ACCOUNT_ICONS]

# Donations
DONATE_BUTTONS =(720, 100, 230, 800)
DONATE_AREA = (950, 15, 860, 700)

# Builder Screen
BUILDER_LIST_TIMES_B = (1130, 260, 120, 30)
WIN_ZONE = (869,808, 130, 50)
BOAT_B_SPOT = (1083, 286, 220, 250)
builder_regions = [BUILDER_REGION, BUILDER_LIST_TIMES_B, WIN_ZONE, BOAT_B_SPOT]
REMAINING_ATTACKS = (323, 831, 107, 30)

# Army screen
ARMY_TABS = (320, 50, 1500, 160)
ARMY_TIME = (1120, 188, 110, 40)
ARMY_TIME_B = (919, 919, 154, 40)
ARMY_TROOPS = (518, 168, 150, 45)
CLAN_TROOPS = (731, 706, 75, 45)
CASTLE_REQUEST_AREA_1 = (581, 172, 1350, 200)
CASTLE_REQUEST_AREA_2 = (581, 376, 1350, 400)
TRAIN_RANGE = (345, 535, 1600, 370)
TRAINING_RANGE = (345, 210, 1450, 150)
DELETE_REGION = (1650, 200, 100, 60)
DELETE_2_REGION = (1520, 200, 100, 60)
ARMY_EXISTING = (350,210, 1600, 454)
SPELLS_EXISTING = (350,473, 950, 175)
SIEGE_EXISTING = (1284, 210, 450, 200)
ARMY_CREATE = (345, 534, 1520, 370)
END_ATTACK_SPOT = (275,675,250,150)
ARMY_CLOCK_SPOT = (920,145,100,100)
CASTLE_TROOPS = (347, 753, 1308, 190)
army_regions = [ARMY_TABS, ARMY_TIME, ARMY_TROOPS, CLAN_TROOPS, ARMY_EXISTING, SPELLS_EXISTING, ARMY_CLOCK_SPOT]
troops_regions = [ARMY_TABS, TRAIN_RANGE, DELETE_REGION, ARMY_CREATE, ]
spells_regions = [ARMY_TABS, TRAIN_RANGE, DELETE_REGION, ARMY_CREATE, ]
siege_regions = [ARMY_TABS, TRAIN_RANGE, DELETE_REGION, ARMY_CREATE, ]

# War screen
WAR_DONATION_AREA = (638, 191, 1000, 350)
WAR_BANNER = (935, 145, 300, 140)
WAR_DONATION_COUNT = (968, 751, 80, 24)
WAR_INFO = (1691, 798, 175, 175)

# Trader
CLOCK_POTION = (730, 200, 200, 200)
RESEARCH_POTION = (1070, 600, 200, 200)


# Army screen - builder
ATTACK_B_OKAY_SPOT = (823,828, 250, 100)

# Capital Coin
CAPITAL_COIN_TIME = (506, 340, 150, 40)

# Attacking
TROOP_ZONE = (300, 831, 1350, 200)
DAMAGE = (1650,740, 130, 50)
COIN_REGION = (350, 165, 150, 40)
AVAILABLE_GOLD = (350, 189, 150, 40)
AVAILABLE_ELIXIR = (350, 236, 150, 40)
AVAILABLE_DARK = (350, 284, 150, 40)

# Attacking_b
ATTACKING_B_SPOT = (200,0,300,150)

# === COLOURS ===
AVAILABLE_GOLD_COLOURS = [(204, 251, 255),]
WHITE = [(255, 255, 255),(254, 254, 254),(253, 253, 253),]


# ================
# === DEFENCES ===
# ================

def dir_to_list(dir):
    list = []
    path = "C://Users//darre//PycharmProjects//clash_bot//images//" + dir
    dir_list = os.listdir(path)
    for x in dir_list:
        list.append(dir + "/" + x[:-4])
    return list

TH_B = dir_to_list("attack_b/th_b")
WALL_B = ["wallb1", ]
EXTRAS_B = ['attack_b/mine_b', 'attack_b/mine_b2', 'attack_b/mine_b3', 'attack_b/lab_b', 'attack_b/lab_b2', 'attack_b/lab_b3', 'attack_b/camp_b', 'attack_b/camp_b2', 'attack_b/gold_storage_b', 'attack_b/gold_storage_b2', 'attack_b/elixir_storage_b', 'attack_b/elixir_storage_b2', 'attack_b/barracks_b', 'attack_b/gem_mine_b', 'attack_b/elixir_pump_b', 'attack_b/elixir_pump_b2', 'attack_b/elixir_pump_b3', 'attack_b/clock_b', 'attack_b/clock_b2', 'attack_b/machine_b', 'attack_b/machine_b2']
WALLS_B = ['attack_b/w1', ]

# print(TH_B)

ATTACK_B_TROOPS = ["barb_b", "machine_b_attacking", "bomb_b", "cannon_b", "giant", "pekka"]

ARCHER_TOWERS = ["archer_t", "archer_t2", "archer_t3", ]
WIZARD_LOW = ["wizard1", "wizard3"]
WIZARD_MED = ["wizard_med", "wizard5", ]
WIZARD_HIGH = ["wizard2", "wizard4", "wizard8", "wizard10"]
INFERNO_LOW = ["inferno_low", "inferno_low2", "inferno_low3", "inferno_low4", "inferno_low5"]
INFERNO_HIGH = ["inferno_high", "inferno_high2", "inferno_high3", "inferno_high4", "inferno_high5", "inferno_high6", "inferno_high7", "inferno_high8", "inferno_high9", "inferno_high10", "inferno_high11", "inferno_high12" ]
CROSS_LOW = ["cross_low", "cross_low2", "cross_low3", "cross_low4", "cross_low5",]
CROSS_HIGH = ["cross_high", "cross_high2"]
EAGLE = ["eagle", "eagle2", "eagle3", "eagle4", "eagle5", "eagle6", "eagle7"]
# TH6 = ["th6"]
TH7 = ["th7", "th7b", "th7c", "th7d",]
TH8 = ["th8", "th8b", "th8c", "th8d",]
TH9 = ["th9", "th9b", "th9c"]
TH10 = ["th10", "th10b"]
TH11 = ["th11","th11b","th11c","th11d",]
TH12 = ["th12", "th12b", "th12c", "th12d", "th12e", "th12f", "th12g", "th12h", "th12i"]
TH13 = ["th13", "th13b"]
TH14 = ["th14", "th14b", "th14c"]
WIZARDS = WIZARD_HIGH + WIZARD_MED + WIZARD_LOW
INFERNOS = INFERNO_HIGH + INFERNO_LOW
TH = TH7 + TH8 + TH9 + TH10 + TH11 + TH12 + TH13 + TH14
LABS = ["lab7", "lab9",]

TOWERS_ASSESSMENT = [
    ("Low Wizards", WIZARD_LOW, 2, "Wizard"),
    ("Med Wizards", WIZARD_MED, 3, "Wizard"),
    ("High Wizards", WIZARD_HIGH, 4, "Wizard"),
    ("Low Inferno", INFERNO_LOW, 6, "Inferno"),
    ("High Inferno", INFERNO_HIGH, 8, "Inferno"),
    ("Low Cross", CROSS_LOW, 5, "Cross"),
    ("High Cross", CROSS_HIGH, 7, "Cross"),
    ("Eagle", EAGLE, 14, "Inferno"),
    # ("TH6", TH6, 1, "TH"),
    ("TH7", TH7, 2, "TH"),
    ("TH8", TH8, 3, "TH"),
    ("TH9", TH9, 5, "TH"),
    ("TH10", TH10, 7, "TH"),
    ("TH11", TH11, 10, "TH"),
    ("TH12", TH12, 13, "TH"),
    ("TH13", TH13, 17, "TH"),
    ("Lab", LABS, 0, "Labs"),
]

TOWERS = []
for x in ["archer", "dark_barracks", "elixir_storage", "gold_mine", "town_hall", "wall", "lab",]:
    TOWERS.append((f"tower_{x}", x))

LEVELS = []
for x in [2,7,9,10,13,15,17]: LEVELS.append((f"level{x}", x))

OBSTACLES = ["bush", ]

def objects_to_str(objects):
    string = ""
    for x in objects:
        try:
            string += x.name + ", "
        except:
            pass
    return string[0:-1]
