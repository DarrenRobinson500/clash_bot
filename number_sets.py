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

    def read(self, region):
        pag.screenshot(f'temp/number_set.png', region=region)
        screen = cv2.imread(f"temp/number_set.png", 0)
        return self.read_screen(screen)

    def read_screen(self, screen):
        found = []
        for number, image in self.numbers:
            h, w = image.shape
            result = cv2.matchTemplate(screen, image, method)
            # show(image)
            # show(screen)
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
        result = ""
        found.sort(key=lambda tup: tup[1])
        # print(found)
        prev_x = 0
        for y in found:
            # print(prev_x, y[1])
            if y[1] <= prev_x + 3:
                found.remove(y)
            prev_x = y[1]
        for y in found:
            result += y[0]
        return result


resource_numbers = Number(name="resource_numbers", directory="numbers_resources")
cost_numbers = Number(name="cost_numbers", directory="numbers_cost", confidence=0.85)
build_time = Number(name="build_time", directory="numbers/time")
research_time = Number(name="research_time", directory="numbers/research")




# screen = cv2.imread(f"temp/mortar.png", 0)
# screen_cost = screen[:,200:]
# screen_count = screen[:,0:200]
# show(screen)
# result = cost_numbers.read_screen(screen_cost)
# print(result)
# result = cost_numbers.read_screen(screen_count)
# print(result)

# for number, image in cost_numbers.numbers:
#         h, w = image.shape
#         print(number)
#         result = cv2.matchTemplate(screen, image, method)
#         # show(image)
#         # show(screen)
#         yloc, xloc = np.where(result >= 0.8)
#         rectangles = []
#         z = zip(xloc, yloc)
#         for (x, y) in z:
#             rectangles.append([int(x), int(y), int(w), int(h)])
#         for x in rectangles:
#             cv2.rectangle(screen, x, (255,255,255), 1)
#
#
# show(screen)
#
