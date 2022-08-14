from datetime import timedelta
import os

PRINT_CV2 = False
VERBOSE_LOG = False
current_account = 0
sweep_period = timedelta(minutes=20)
ACCOUNT_NEEDS_WALLS = [1,]

BOTTOM_LEFT = (75, 1005)
TOP_RIGHT = (1804, 57)

CURRENCIES = ["elixir1", "dark", "gold", "elixir"]

build_preferences_e1 = [
    "lab", "army", "workshop", "spell_factory", "castle", "barracks", "gold_storage", "warden",
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

MAX_TROPHIES = [0, 1500, 1400, 1000]
STANDARD_DP = (540, 360)
STANDARD_DP2 = (540, 360)
TROOPS = ["barb", "archer", "giant","bomb", "wizard", "bloons", "healer", "pekka", "dragon", "edrag", "super_barb", "super_goblin",]
SPELLS = ["lightening", "freeze", "poison"]
SIEGE = ["ram",]
MINES = ["gold1", "gold2", "gold3"]
ALL_TROOPS = TROOPS + SPELLS + SIEGE

HEROES_AND_RAMS = ["king", "queen","warden", "champ", "clan", "clan_ram", "clan_ram2", "ram", "ram_empty"]

DONT_DONATE = ["bomb", "super_goblin", ]
TROOP_TRAIN_EXT = ["wizard", "bomb", "super_goblin", "super_barb", "lightening", "freeze", "dragon", ]
TROOP_ATTACK_EXT = ["super_goblin", "super_barb", ]
TROOP_DONATE_EXT = ["super_barb", "lightening","edrag"]

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

x, y = 930, 120
width, height = 680, 525

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
BUILDER_REGION = (629, 40, 120, 120)
BUILDER_ZERO_REGION = (720, 70, 100, 50)
BUILDER_B_REGION = (780, 40, 120, 120)
BUILDER_B_ZERO_REGION = (903, 70, 100, 50)
BUILDER_B_LIST_REGION = (705, 170, 290, 550)
BUILDER_LIST_REGION = (550, 160, 300, 600)
BUILDER_LIST_TIMES = (800, 239, 160, 50)
RESOURCES_G = (1426,80, 290, 47)
RESOURCES_E = (1426,172, 290, 47)
RESOURCES_D = (1514,261, 200, 47)
RESOURCES = (1420,60, 350, 250)
LEVEL = (115,67, 80, 80)
SELECTED_TOWER = (435, 677, 1000, 60)
TROPHIES = (190,190, 80, 40)
CHAT_SPOT = (400, 900, 250, 140)
FIND_A_MATCH_SPOT = (1475, 610, 400, 170)
ATTACK_SPOT = (535, 70, 400, 100)
ATTACKING_SPOT = (0, 600, 400, 400)
MAINTENANCE_SPOT = (600, 200, 1400, 400)
SWITCH_ACCOUNT_SPOT = (1286, 366, 350, 100)
FORGE_SPOT = (810, 150, 250, 100)
ATTACK_B_SPOT = (860, 800, 140, 100)
OKAY_SPOT = (640,330, 600, 650)
RETURN_HOME_2_SPOT = (90, 790, 200, 200)
BLUESTACKS_MESSAGE_SPOT = (1410, 750, 250, 150)

# NON-DESTINATIONS
SUPERCELL_LOGIN_SPOT = (300, 870, 550, 500)
BLUESTACKS_APP_SPOT = (1500, 120, 200, 200)
PYCHARM_RUNNING_SPOT = (0, 0, 45, 45)
RELOAD_SPOT = (500,575,250,100)
RAID_WEEKEND_NEXT_SPOT = (1300,880,300,100)

# Accounts
ACCOUNT_ICONS = (1136, 467, 110, 420)

# Donations
DONATE_BUTTONS =(520, 140, 205, 760)
DONATE_AREA = (795, 15, 860, 700)

# Builder Screen
BUILDER_LIST_TIMES_B = (1000, 240, 100, 30)
WIN_ZONE = (869,808, 130, 50)
BOAT_B_SPOT = (1083, 286, 220, 250)

# Army screen
ARMY_TABS = (120, 50, 1500, 160)
ARMY_TIME = (1018, 165, 90, 40)
ARMY_TIME_B = (919, 919, 154, 40)
ARMY_TROOPS = (318, 168, 150, 45)
CLAN_TROOPS = (631, 706, 75, 45)
TRAIN_RANGE = (145, 535, 1520, 370)
DELETE_REGION = (1650, 200, 100, 60)
ARMY_EXISTING = (150,210, 1040, 175)
SPELLS_EXISTING = (150,473, 950, 165)
ARMY_CREATE = (145, 534, 1520, 370)
END_ATTACK_SPOT = (75,675,250,150)
ARMY_CLOCK_SPOT = (920,145,100,100)

# Army screen - builder
ATTACK_B_OKAY_SPOT = (823,828, 250, 100)

# Capital Coin
CAPITAL_COIN_TIME = (250,270, 175,50)

# Attacking
TROOP_ZONE = (259, 831, 1350, 200)
DAMAGE = (1650,740, 130, 50)
COIN_REGION = (150, 165, 150, 40)
AVAILABLE_GOLD = (150, 165, 150, 40)
AVAILABLE_ELIXIR = (150, 215, 150, 40)
AVAILABLE_DARK = (150, 265, 150, 40)

# Attacking_b
ATTACKING_B_SPOT = (0,0,300,150)

# === COLOURS ===
AVAILABLE_GOLD_COLOURS = [(204, 251, 255),]
WHITE = [(255, 255, 255),(254, 254, 254),(253, 253, 253),]


# ================
# === DEFENCES ===
# ================

TH_B = ["thb7", "thb8", "thb8b",]
WALL_B = ["wallb1", ]
EXTRAS_B = ['attack_b/mine_b', 'attack_b/mine_b2', 'attack_b/mine_b3', 'attack_b/lab_b', 'attack_b/lab_b2', 'attack_b/lab_b3', 'attack_b/camp_b', 'attack_b/camp_b2', 'attack_b/gold_storage_b', 'attack_b/gold_storage_b2', 'attack_b/elixir_storage_b', 'attack_b/elixir_storage_b2', 'attack_b/barracks_b', 'attack_b/gem_mine_b', 'attack_b/elixir_pump_b', 'attack_b/elixir_pump_b2', 'attack_b/elixir_pump_b3', 'attack_b/clock_b', 'attack_b/clock_b2', 'attack_b/machine_b', 'attack_b/machine_b2']
WALLS_B = ['attack_b/w1', ]

def dir_to_list(dir):
    list = []
    path = "C://Users//darre//PycharmProjects//clash_bot//images//" + dir
    dir_list = os.listdir(path)
    for x in dir_list:
        list.append(dir + "/" + x[:-4])
    return list

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