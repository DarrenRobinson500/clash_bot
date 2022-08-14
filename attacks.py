from constants import *

# ================
# === ATTACK_B ===
# ================

barb = ("barb_b", 5, 1)
barb_bulk = ("barb_b", 5, 13)
machine = ("machine_b_attacking", 2, 1)
bomb3 = ("bomb_b", 3, 1)
bomb4 = ("bomb_b", 4, 1)
bomb5 = ("bomb_b", 5, 1)
cannon2 = ("cannon_b", 2, 1)
cannon3 = ("cannon_b", 3, 1)
cannon4 = ("cannon_b", 4, 1)
cannon5 = ("cannon_b", 5, 1)
giant = ("giant", 4, 1)
pekka = ("pekka", 1, 1)

troops3 = [barb, machine, bomb3, barb_bulk, cannon2]
troops2 = [barb, machine, bomb4, barb, barb, cannon5, barb, barb, barb, cannon4, barb, barb, ]
troops1 = [barb, bomb5, giant, barb, pekka, barb, cannon3, machine, cannon3, barb]

TROOPS_B = ["Fail", troops1, troops2, troops3]

# === ATTACKS ===
GIANT200 = {
            "name": "giant200",
            "resource_objective": [300000,0,0],
            "max_th": 8,
            "wizard_check": True,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": True,
            "bomb_target": WIZARDS,
            "bomb_target2": None,
            "lightening": 7,
            "initial_troops": ["king", "queen", "clan",],
            "troop_group": [("giant", 5), ("bomb", 2), ("wizard", 5), ],
            "troop_groups": 4,
            "final_troops": ["wizard",],
            "troop_pause": 0,
            "drop_points": False,
            "drop_point_troops": ["super_goblin,"],
            "th_gold_adj": True,
        }

GIANT220 = {
            "name": "giant220",
            "resource_objective": [450000,0,0],
            "max_th": 9,
            "wizard_check": True,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": True,
            "bomb_target": WIZARDS,
            "bomb_target2": None,
            "lightening": 9,
            "initial_troops": ["king", "queen", ],
            "troop_group": [("giant", 6), ("bomb", 2), ("wizard", 5), ],
            "troop_groups": 4,
            "final_troops": ["wizard", "clan", ],
            "troop_pause": 0,
            "drop_points": False,
            "drop_point_troops": ["super_goblin,"],
            "th_gold_adj": True,
        }

GIANT240_TH9 = {
            "name": "giant240",
            "resource_objective": [400000,0,0],
            "max_th": 9,
            "wizard_check": False,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": True,
            "bomb_target": WIZARDS,
            "bomb_target2": None,
            "lightening": 11,
            "initial_troops": ["king", "clan", "clan_ram", "clan_ram2", "queen", "warden"],
            "troop_group": [("giant", 6), ("bomb", 2), ("wizard", 6), ],
            "troop_groups": 4,
            "final_troops": ["wizard", "wizard", ],
            "troop_pause": 0,
            "drop_points": False,
            "drop_point_troops": [],
            "th_gold_adj": False,
        }

GIANT260 = {
            "name": "giant260",
            "resource_objective": [400000,0,0],
            "max_th": 11,
            "wizard_check": False,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": True,
            "bomb_target": EAGLE,
            "bomb_target2": INFERNOS,
            "lightening": 11,
            "initial_troops": ["king", "clan", "clan_ram", "clan_ram2", "queen", "warden", "giant"],
            "troop_group": [("giant", 6), ("bomb", 2), ("wizard", 6), ],
            "troop_groups": 4,
            "final_troops": ["wizard", "wizard", ],
            "troop_pause": 0,
            "drop_points": False,
            "drop_point_troops": [],
            "th_gold_adj": False,
        }

BARBS_11 = {
            "name": "barbs",
            "resource_objective": [500000,0,0],
            "max_th": 11,
            "wizard_check": False,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": False,
            "bomb_target": INFERNOS,
            "bomb_target2": WIZARDS,
            "lightening": 11,
            "initial_troops": ["king", "clan_ram", "clan_ram2", "queen", "warden", ],
            "troop_group": [("super_barb", 52), ],
            "troop_groups": 1,
            "final_troops": [],
            "troop_pause": 0.45,
            "drop_points": False,
            "drop_point_troops": [],
            "th_gold_adj": False,
        }

BARBS_13 = {
            "name": "barbs",
            "resource_objective": [800000,0,0],
            # "resource_objective": [0,0,5000],
            "max_th": 13,
            "wizard_check": False,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": True,
            "bomb_target": INFERNOS,
            "bomb_target2": WIZARDS,
            "lightening": 11,
            "initial_troops": ["king", "ram_empty", "clan_ram", "clan_ram2", "queen", "warden", "champ"],
            "troop_group": [("super_barb", 60), ],
            "troop_groups": 1,
            "final_troops": [],
            "troop_pause": 0.45,
            "drop_points": False,
            "drop_point_troops": [],
            "th_gold_adj": False,
        }

GOBLIN = {
            "name": "goblins",
            "resource_objective": [500000,0,0],
            "max_th": 101,
            "wizard_check": False,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": False,
            "bomb_target": [],
            "bomb_target2": None,
            "lightening": 0,
            "initial_troops": [],
            "troop_group": [("super_goblin", 12), ("edrag", 2), ("dragon", 2), ("giant", 15)], # This is used to define the min number required
            "troop_groups": 1,
            "final_troops": [],
            "drop_points": True,
            "drop_point_troops": ["super_goblin",],
            "th_gold_adj": False,
        }

FAV_ATTACK = [None, BARBS_13, BARBS_11, GIANT220]
