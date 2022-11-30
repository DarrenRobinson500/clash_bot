from object_recognition import *
from constants import *
method = cv2.TM_CCOEFF_NORMED

number_sets = []

class Number():
    def __init__(self, name, directory, confidence=0.75):
        print("Creating number set:", name)
        self.name = name
        self.numbers = []
        self.confidence = confidence
        files = os.listdir(directory)
        for file in files:
            image = cv2.imread(f'{directory}/{file}', 0)
            x = file[0:-4]
            self.numbers.append((x, image))
        number_sets.append(self)

    # def __init__(self, name, directory, number_array):
    #     self.name = name
    #     self.numbers = []
    #
    #     files = os.listdir(directory)
    #     print("Creating number set:", name)
    #     for x in number_array:
    #         file = f'{x}.png'
    #         if file in files:
    #             image = cv2.imread(f'{directory}/{x}.png', 0)
    #             self.numbers.append((x, image))
    #         else:
    #             print(f"Adding number image: could not find f'{directory}/{x}.png'")
    #     number_sets.append(self)

    def show_numbers(self):
        for x, i in self.numbers:
            show(i, label=str(x))

    def read(self, region, show_image=False, return_number=False):
        pag.screenshot(f'temp/number_set.png', region=region)
        screen = cv2.imread(f"temp/number_set.png", 0)
        return self.read_screen(screen, show_image=show_image, return_number=return_number)

    def read_screen(self, screen, show_image=False, return_number=False, show_rectangles=False):
        found = []
        for number, image in self.numbers:
            h, w = image.shape
            # print(image.shape)
            result = cv2.matchTemplate(screen, image, method)

            if show_image:
                min_val, val, min_loc, loc = cv2.minMaxLoc(result)
                show(image)
                show(screen, label=str(round(val,2)))
            yloc, xloc = np.where(result >= self.confidence)
            z = zip(xloc, yloc)
            rectangles = []
            for (x, y) in z:
                rectangles.append([int(x), int(y), int(w), int(h)])
                rectangles.append([int(x), int(y), int(w), int(h)])
            rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

            if len(rectangles) > 0:
                for rectangle in rectangles:
                    found.append((str(number), rectangle[0]))
        # print("Number set - read screen (found variable):", found)
        result = ""
        found.sort(key=lambda tup: tup[1])
        # print("Number set - read screen (found variable sorted):", found)
        prev_x = -4
        for y in found:
            # print(prev_x, y[1])
            if y[1] <= prev_x + 3:
                found.remove(y)
                # print("Number set - read screen - removed", y[0])
            prev_x = y[1]
        for y in found:
            result += y[0]
        # print("Number set - read screen (result):", result)
        if return_number:
            result = result.replace("e", "")
            result = result.replace("g", "")
            result = result.replace("h", "")

            try:
                result = int(result)
            except:
                result = 0


        return result


resource_numbers = Number(name="resource_numbers", directory="numbers/resources")
cost_numbers = Number(name="cost_numbers", directory="numbers_cost", confidence=0.85)
tower_count = Number(name="tower_count", directory="numbers/tower_count", confidence=0.85)
build_time = Number(name="build_time", directory="numbers/time")
research_time = Number(name="research_time", directory="numbers/research", confidence=0.85)
troop_numbers = Number(name="troop_numbers", directory="numbers/troop_count")
selected_level = Number(name="selected_level", directory="numbers/levels", confidence=0.9)
selected_tower = Number(name="selected_tower", directory="numbers/towers", confidence=0.9)
trophies = Number(name="trophies", directory="numbers/trophies", confidence=0.85)
coin_time = Number(name="coin_time", directory="numbers/coin")
war_donation_count = Number(name="war_donation_count", directory="numbers/war_donation_count", confidence=0.85)
