from bot import *
from object_recognition import *
from constants import *
from sandpit.quantify import *


TOWERS = []
for x in ["archer", "dark_barracks", "elixir_storage", "gold_mine", "town_hall", "wall"]:
    TOWERS.append((f"tower_{x}", x))


def main():
    click_cv2('bluestacks_icon')
    time.sleep(.2)

    print("ARCHERS: ", get_tower_levels(ARCHER_TOWERS))
    print("WIZARDS: ", get_tower_levels(WIZARDS))
    print("TOWN HALL: ", get_tower_levels(TH))

def get_tower_levels(tower_type):
    pag.click(95, 985)
    time.sleep(0.5)
    pag.screenshot(f"own/main_village.png")
    i = cv2.imread(f"own/main_village.png")

    # Find Towers
    rects = find_tower_many(i, tower_type, 0.55)
    levels = []

    # Select Towers
    for x in rects:
        pag.click(pag.center(x))
        time.sleep(.5)

        max_val = 0
        max_level = None
        for img, level in LEVELS:
            val, loc, rect = find_cv2(img, SELECTED_TOWER)
            # print(val, loc, rect)
            if val > max_val:
                max_val = val
                max_level = level
        levels.append(max_level)
    return levels

def find_best(images, screen):
    val_max = 0
    val_name = None
    for image_str,image_name in images:
        template = cv2.imread(f'images/{image_str}.png', 0)
        if template is None:
            print("click_cv2: couldn't find file:", image_str)

        # cv2.imshow('Screen', screen)
        # cv2.imshow('Template', template)
        # cv2.waitKey(0)
        # print("Screen", screen.shape)
        # print("Template", template.shape)

        result = cv2.matchTemplate(screen, template, method)
        _, val, _, _ = cv2.minMaxLoc(result)
        if val > val_max:
            val_max = val
            val_name = image_name
    return val_name, val_max

def click_all():
    towers = []
    start_x = 1050
    end_x = 900
    step_y = 40
    step_x = int(step_y / 0.82)
    for y in range(100, 600, step_y):
        for x in range(start_x, end_x, step_x):
            tower = read_tower(x,y)
            if tower: towers.append(tower)
        start_x -= step_x
        end_x += step_x
    pag.click(95, 985)
    pag.scroll(-300)
    for y in range(300, 1000, step_y):
        for x in range(start_x, end_x, step_x):
            tower = read_tower(x,y)
            if tower: towers.append(tower)
        start_x += step_x
        end_x -= step_x
    print_towers(towers)

def print_towers(towers):
    for x in towers:
        if x[0] != "wall": print(x)

def click_one():
    x, y = 1005, 430
    pag.click(x,y)

def read_tower(x, y):
    pag.click(x,y)
    time.sleep(0.5)
    pag.screenshot('temp/temp.png', region=SELECTED_TOWER)
    screen = cv2.imread('temp/temp.png', 0)
    level = find_best(LEVELS, screen)
    tower = find_best(TOWERS, screen)
    if level[1] > 0.7 and tower[1] > 0.7:
        # print(tower, level)
        return tower[0], level[0], (x, y)
    if tower[0] in OBSTACLES:
        # print(tower, level)
        return tower[0], 0, (x, y)
    return

start()
pag.click(1400, 110)
pag.drag(-100, 300, 0.25, button='left')
pag.drag(80, 0, 0.25, button='left')

click_all()
end()

# click_cv2("pycharm")

