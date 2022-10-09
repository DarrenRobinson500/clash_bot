from member import *
from nav import *

troops = []
troop_files = os.listdir("images/troops_new")
# print("Troop files:", troop_files)

def get_image_from_file(troop, style):
    file = f'{troop}_{style}.png'
    if style == "": file = f'{troop}.png'
    image = None
    if file in troop_files:
        image = cv2.imread('images/troops_new/' + file, 0)
    else:
        print(f"Adding troop image: could not find '{file}'")
    return image

def get_image(troop, style):
    object = next((x for x in troops if x.name == troop), None)
    if style == "army": return object.army
    if style == "train": return object.train
    if style == "donate1": return object.donate1
    if style == "donate2": return object.donate2
    if style == "attack": return object.attack
    return

def get_super_troop(troop):
    goto(main)
    hold_key("a", 0.5)
    hold_key("w", 0.5)
    sequence = ["super_boost/boost", "super_boost/boost_on", f"super_boost/{troop.name}", "super_boost/potion", "super_boost/dark", "super_boost/potion_small", "super_boost/dark2", ]
    for image in sequence:
        time.sleep(0.5)
        val, loc, rect = find_cv2(image)
        print(image, val)
        if val > 0.6:
            print("Click")
            click_rect(rect)
    pag.press("esc")

class Troop():
    def __init__(self, name, type, slide, training_time, donate_bool, donate_preference, donations, donation_count):
        self.name = name
        self.type = type
        self.slide = slide
        self.training_time = training_time
        self.donate_bool = donate_bool
        self.donate_preference = donate_preference
        self.currently_training = False
        if type != "hero":
            self.army = get_image_from_file(name, "army")
            self.train = get_image_from_file(name, "train")
            self.training = get_image_from_file(name, "training")
            self.donate1 = get_image_from_file(name, "donate1")
            self.donate2 = get_image_from_file(name, "donate2")
        else:
            self.army = None
            self.train = None
            self.training = None
            self.donate1 = None
            self.donate2 = None

        self.attack = get_image_from_file(name, "attack")
        self.donations = donations
        self.donation_count = donation_count
        self.super_troop = False
        if "super" in self.name:
            self.super_troop = True

        troops.append(self)

    def __str__(self):
        return self.name

    def in_castle(self):
        val, loc, rect = find(self.army, get_screenshot(CASTLE_TROOPS), show_image=False)
        return val > 0.8

    def start_train(self, count, move_to_start=False):
        print("Start train:", self.name, self.type, count)
        # Set up
        if self.type == "troop":
            goto(troops_tab)
            if self.slide == 2: slide(1, 2)
            else: slide(2, 1)
            make_room(self)
        if self.type == "spell":
            goto(spells_tab)
            make_room(self)
        if self.type == "siege":
            goto(siege_tab)
            # make_room(self)

        # Train
        # for x in range(count):
        val, loc, rect = find(self.train, get_screenshot(TRAIN_RANGE))
        # rect_adj = [rect[0] + TRAIN_RANGE[0], rect[1] + TRAIN_RANGE[1], rect[2], rect[3]]
        if val < 0.8 and self.super_troop:
            get_super_troop(self)
            goto(troops_tab)

        if val > 0.8:
            for x in range(count):
                click_rect(rect, region=TRAIN_RANGE)
        # val, outcome = click(self.train, region=TRAIN_RANGE, show_image=False)
        print("Create troop:", self.name, round(val,2))
        if move_to_start:
            move_to_queue_start(self)

        print("Start train:", self.name, self.training_time, count)
        return self.training_time * count

    def delete(self, count):
        print("Troop delete")
        goto(army_tab)
        click_cv2("edit_army")
        val, loc, rect = find(self.army, get_screenshot(ARMY_EXISTING))
        rect_adj = [rect[0] + ARMY_EXISTING[0], rect[1] + ARMY_EXISTING[1], rect[2], rect[3]]
        spot = pag.center(rect_adj)
        for x in range(count):
            pag.click(spot)
        click_cv2("edit_army_okay")
        click_cv2("surrender_okay")


# Make troop objects
# Name, Type, Time, Donate
troop_data = [
    ("barb", "troop", 1, 5, False, 5, 0, 10),
    ("archer", "troop", 1, 6, True, 5, 1, 10),
    ("giant", "troop", 1, 30, True, 5, 0, 5),
    ("wizard", "troop", 1, 30, True, 5, 0, 5),
    ("bomber", "troop", 1, 15, False, 5, 0, 2),
    ("goblin", "troop", 1, 7, False, 5, 0, 1),
    ("bloon", "troop", 1, 30, True, 5, 0, 8),
    ("healer", "troop", 1, 120, False, 5, 0, 1),
    ("dragon", "troop", 1, 180, True, 2, 1, 1),
    ("baby_drag", "troop", 1, 90, True, 5, 0, 1),
    ("edrag", "troop", 1, 360, True, 3, 1, 1),
    ("pekka", "troop", 1, 180, True, 4, 1, 1),
    ("miner", "troop", 1, 40, True, 4, 0, 1),
    ("yeti", "troop", 1, 240, True, 4, 0, 1),
    ("bowler", "troop", 2, 60, True, 4, 0, 1),
    ("super_barb", "troop", 1, 25, True, 1, 1, 20),
    ("minion", "troop", 1, 15, False, 5, 0, 10),
    ("super_minion", "troop", 10, 108, False, 10, 0, 1),
    ("hog", "troop", 2, 45, True, 5, 0, 7),
    ("lightening", "spell", 1, 180, True, 6, 0, 5),
    ("freeze", "spell", 1, 180, True, 6, 0, 1),
    ("poison", "spell", 1, 180, True, 7, 0, 2),
    ("skeleton", "spell", 1, 180, True, 8, 0, 2),
    ("rage", "spell", 1, 360, True, 6, 1, 1),
    ("ram", "siege", 1, 20 * 60, True, 7, 1, 6),
    ("slammer", "siege", 1, 20 * 60, True, 7, 0, 1),
    ("log_thrower", "siege", 1, 20 * 60, True, 7, 0, 1),
    ("siege", "siege", 1, 20 * 60, True, 7, 0, 1),
    ("king", "hero", 1, 0, False, 8, 0, 0),
    ("queen", "hero", 1, 0, False, 8, 0, 0),
    ("warden", "hero", 1, 0, False, 8, 0, 0),
    ("champ", "hero", 1, 0, False, 8, 0, 0),
]
print()
for name, type, slide, training_time, donate_bool, donate_preference, donations, donation_count in troop_data:
    print("Creating troop:", name)
    Troop(name=name, type=type, slide=slide, training_time=training_time, donate_bool=donate_bool,
          donate_preference=donate_preference, donations=donations, donation_count=donation_count)

barb = next((x for x in troops if x.name == 'barb'), None)
giant = next((x for x in troops if x.name == 'giant'), None)
wizard = next((x for x in troops if x.name == 'wizard'), None)
bomber = next((x for x in troops if x.name == 'bomber'), None)
balloon = next((x for x in troops if x.name == 'balloon'), None)
dragon = next((x for x in troops if x.name == 'dragon'), None)
edrag = next((x for x in troops if x.name == 'edrag'), None)
super_barb = next((x for x in troops if x.name == 'super_barb'), None)

lightening = next((x for x in troops if x.name == 'lightening'), None)
freeze = next((x for x in troops if x.name == 'freeze'), None)
poison = next((x for x in troops if x.name == 'poison'), None)

queen = next((x for x in troops if x.name == 'queen'), None)
king = next((x for x in troops if x.name == 'king'), None)
warden = next((x for x in troops if x.name == 'warden'), None)
champ = next((x for x in troops if x.name == 'champ'), None)

ram = next((x for x in troops if x.name == 'ram'), None)
log_thrower = next((x for x in troops if x.name == 'log_thrower'), None)

troops.sort(key=lambda x: x.donate_preference, reverse=False)


def troop_str(required_troops):
    string = ""
    for x in required_troops:
        try:
            string += x.name + ", "
        except:
            pass
    return string[0:-1]


def delete_a_troop():
    val, loc, rect = find_cv2("remove_troops", DELETE_2_REGION)
    center = pag.center(rect)
    pag.click(center)

def make_room(troop):
    count = 0
    colour = check_troop_colour_train(troop)
    print("Make room:", colour)
    while not colour and count < 6:
        delete_a_troop()
        colour = check_troop_colour_train(troop)
        count += 1

def check_troop_colour_train(troop):
    if troop.train is None:
        print("No training image")
        return False
    val, loc, rect = find(troop.train, get_screenshot(TRAIN_RANGE), troop.name)
    rect_adj = [rect[0] + TRAIN_RANGE[0], rect[1] + TRAIN_RANGE[1], rect[2], rect[3], ]
    colour = check_colour_rect(rect_adj, show_image=False)
    return colour

def move_to_queue_start(troop):
    print("Moving to queue start")
    for _ in range(2):
        val, loc, rect = find(troop.training, get_screenshot(BACKLOG))
        if val > 0.70:
            a = BACKLOG[0] + pag.center(rect)[0], BACKLOG[1] + pag.center(rect)[1] + 10
            b = BACKLOG[0] + BACKLOG[2] + 10, a[1] + 10
            if a[0] < 1600: drag(a, b)

def drag(a, b):
    x0, y0 = a
    x1, y1 = b
    pag.moveTo(x0, y0, 0.3)
    pag.dragTo(x1, y1, 1, button="left")
    time.sleep(1)

def slide(slide_pos, slide_pos_target):
    time.sleep(0.2)
    print(f"Slide from {slide_pos} to {slide_pos_target}")
    if slide_pos == slide_pos_target:
        return slide_pos

    if slide_pos < slide_pos_target:
        start_x = 1650
        end_x = 250
        slide_pos = min(slide_pos + 1, 2)
    else:
        start_x = 250
        end_x = 1650
        slide_pos = min(slide_pos - 1, 1)

    dur = 0.3
    pag.moveTo(start_x, 600, dur)
    pag.dragTo(end_x, 600, dur)
    time.sleep(1)
    return slide_pos

