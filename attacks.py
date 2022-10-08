from troops import *

# ================
# === ATTACK_B ===
# ================

barb5 = ("barb_b", 5, 1)
barb_bulk = ("barb_b", 5, 13)
machine = ("machine_b_attacking", 2, 1)
bomb3 = ("bomb_b", 3, 1)
bomb4 = ("bomb_b", 4, 1)
bomb5 = ("bomb_b", 5, 1)
cannon2 = ("cannon_b", 2, 1)
cannon3 = ("cannon_b", 3, 1)
cannon4 = ("cannon_b", 4, 1)
cannon5 = ("cannon_b", 5, 1)
giant4 = ("giant", 4, 1)
pekka1 = ("pekka", 1, 1)

troops3 = [barb5, machine, bomb4, barb5, barb5, cannon5, barb5, barb5, barb5, cannon4, barb5, barb5, ]
troops2 = [barb5, machine, bomb4, barb5, barb5, cannon5, barb5, barb5, barb5, cannon4, barb5, barb5, ]
troops1 = [barb5, bomb5, giant4, barb5, pekka1, barb5, cannon3, machine, cannon3, barb5]

TROOPS_B = ["Fail", troops1, troops2, troops3]

# === ATTACKS ===
war1 = ["edrag",] * 2 + ["dragon"] * 12 + ["freeze"] * 11
war2 = ["dragon"] * 12 + ["lightening"] * 11
war3 = ["dragon"] * 12 + ["bloons"] * 3 + ["lightening"] * 11
war = [None, war1, war2, war3]

GIANT200 = {
            "name": "giant200",
            "resource_objective": [00000,0,2000],
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
            "resource_objective": [400000,0,000],
            "max_th": 10,
            "wizard_check": True,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": True,
            "bomb_target": WIZARDS,
            "bomb_target2": None,
            "lightening": 9,
            "initial_troops": ["king", "queen", ],
            # "initial_troops": ["king", "clan", "clan_ram", "clan_ram2", "queen", "warden"],

            "troop_group": [("giant", 6), ("bomb", 2), ("wizard", 5), ],
            "troop_groups": 4,
            "final_troops": ["wizard", "clan", ],
            # "final_troops": ["wizard", "clan", "giant", "giant", "giant"],
            "troop_pause": 0,
            "drop_points": False,
            "drop_point_troops": ["super_goblin,"],
            "th_gold_adj": True,
        }

GIANT240 = {
            "name": "giant240",
            "resource_objective": [400000,0,2000],
            "max_th": 9,
            "wizard_check": False,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": True,
            "bomb_target": WIZARDS,
            "bomb_target2": None,
            "lightening": 11,
            "spells": [],
            "initial_troops": [king, log_thrower, queen, warden],
            "troop_group": [(giant, 6), (bomber, 2), (wizard, 6), ],
            "troop_groups": 4,
            "final_troops": [wizard, wizard, ],
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

GOLEMS_9 = {
            "name": "golems",
            # "resource_objective": [500000,0,0],
            "resource_objective": [0,0,500],
            "max_th": 11,
            "wizard_check": False,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": False,
            "bomb_target": INFERNOS,
            "bomb_target2": WIZARDS,
            "lightening": 0,
            "initial_troops": ["king", "queen", ],
            "troop_group": [("golem", 3), ("witch", 10), ("bomb", 5), ],
            "troop_groups": 1,
            "final_troops": ["clan", ],
            "troop_pause": 0.45,
            "drop_points": False,
            "drop_point_troops": [],
            "th_gold_adj": False,
        }

GOLEMS_11 = {
            "name": "golems",
            # "resource_objective": [500000,0,0],
            "resource_objective": [0,0,3000],
            "max_th": 11,
            "wizard_check": False,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": False,
            "bomb_target": INFERNOS,
            "bomb_target2": WIZARDS,
            "lightening": 0,
            "initial_troops": ["king", "queen", ],
            "troop_group": [("golem", 3), ("witch", 13), ("bomb", 13), ],
            "troop_groups": 1,
            "final_troops": ["clan", ],
            "troop_pause": 0.45,
            "drop_points": False,
            "drop_point_troops": [],
            "th_gold_adj": False,
        }

GOLEMS_13 = {
            "name": "golems",
            # "resource_objective": [500000,0,0],
            "resource_objective": [0,0,5000],
            "max_th": 11,
            "wizard_check": False,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": False,
            "bomb_target": INFERNOS,
            "bomb_target2": WIZARDS,
            "lightening": 0,
            "initial_troops": ["king", "queen", ],
            "troop_group": [("golem", 3), ("witch", 16), ("bomb", 9), ],
            "troop_groups": 1,
            "final_troops": ["clan", ],
            "troop_pause": 0.45,
            "drop_points": False,
            "drop_point_troops": [],
            "th_gold_adj": False,
        }


BARBS_11 = {
            "name": "barbs",
            # "resource_objective": [500000,0,0],
            "resource_objective": [400000,0,3000],
            "max_th": 11,
            "wizard_check": False,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": False,
            "bomb_target": INFERNOS,
            "bomb_target2": WIZARDS,
            "lightening": 11,
            "spells": [],
            "initial_troops": [king, log_thrower, queen, warden, champ],
            "troop_group": [(super_barb, 52), ],
            "troop_groups": 1,
            "final_troops": [],
            "troop_pause": 0.45,
            "drop_points": False,
            "drop_point_troops": [],
            "th_gold_adj": False,
        }

BARBS_13 = {
            "name": "barbs",
            "resource_objective": [300000,0,5000],
            # "resource_objective": [0,0,5000],
            "max_th": 13,
            "wizard_check": False,
            "towers_to_avoid": INFERNO_HIGH,
            "bomb": True,
            "bomb_target": INFERNOS,
            "bomb_target2": WIZARDS,
            "lightening": 11,
            "spells": [],
            "initial_troops": [king, ram, queen, warden, champ],
            "troop_group": [(super_barb, 60), ],
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
            "towers_to_avoid": [],
            "bomb": False,
            "bomb_target": [],
            "bomb_target2": None,
            "lightening": 0,
            "spells": [],
            "initial_troops": [],
            "troop_group": [("super_goblin", 86), ], # This is used to define the min number required
            "troop_groups": 1,
            "final_troops": [],
            "drop_points": True,
            "drop_point_troops": ["super_goblin",],
            "th_gold_adj": False,
        }

GOBLIN_13 = {
            "name": "goblins",
            "resource_objective": [500000,0,0],
            "max_th": 101,
            "wizard_check": False,
            "towers_to_avoid": [],
            "bomb": False,
            "bomb_target": [],
            "bomb_target2": None,
            "lightening": 0,
            "spells": [],
            "initial_troops": [],
            "troop_group": [("super_goblin", 99), ("bomb", 1),], # This is used to define the min number required
            "troop_groups": 1,
            "final_troops": [],
            "drop_points": True,
            "drop_point_troops": ["super_goblin",],
            "th_gold_adj": False,
        }

DRAGONS_300 = [dragon] * 17 + [balloon] * 6 + [log_thrower] * 2 + [poison, lightening] + [freeze] * 11
DRAGONS_260 = [dragon] * 15 + [balloon] + [poison] + [freeze] * 12
DRAGONS_240 = [dragon] * 12 + [poison] + [lightening] * 10
