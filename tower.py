import os, cv2
from datetime import datetime, timedelta

files = os.listdir("images/towers") + os.listdir("images/towers_b")
towers = []

def get_image_from_file(object, village, style):
    file = f'{object}_{style}.png'
    if style == "": file = f'{object}.png'
    if village == "main": directory = 'images/towers/'
    else: directory = 'images/towers_b/'
    image = None
    if file in files:
        image = cv2.imread(directory + file, 0)
    else:
        print(f"Adding image: could not find '{directory + file}'")
    return image

class Tower():
    def __init__(self, name, village, category, resource, priority):
        self.name = name
        self.village = village
        self.category = category
        self.resource = resource
        self.priority = priority
        self.i_text = get_image_from_file(name, village, "text")
        self.levels = []
        towers.append(self)

    def __str__(self):
        return f"{self.name}"

    def print_tower(self):
        print("Tower:", self.name)
        for x in self.levels:
            print(" -", x)

    def add_level(self, tower, level, th, gold, elixir, dark, days):
        self.Level(tower=tower, level=level, th=th, gold=gold, elixir=elixir, dark=dark, days=days)

    class Level():
        def __init__(self, tower, level, th, gold, elixir, dark, days):
            self.tower = tower
            self.level = level
            self.th = th
            self.gold = gold
            self.elixir = elixir
            self.dark = dark
            self.days = timedelta(days=days)
            tower.levels.append(self)

        def __str__(self):
            return f"Level: {self.level}. Time: {self.days}"

