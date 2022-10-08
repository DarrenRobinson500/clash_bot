from image_management import only_colours, see_resources_background
import pytesseract
from number_sets import *

pytesseract.pytesseract.tesseract_cmd = "c:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def read_text(region, text_colours, numbers=False):
    pag.screenshot('temp/temp2.png', region=region)
    i = cv2.imread("temp/temp2.png", 1)

    if text_colours: i = only_colours(i, text_colours)
    result = pytesseract.image_to_string(i)
    if result == "'xl": result = '21'
    # print(f"read_text pre number adj: '{result}'")

    if numbers:
        try:
            result = alpha_to_numbers(result)
            result = get_numbers(result)
        except:
            result = 0
    # print("read_text", result)
    return result

def read_text_image(img, text_colours):
    i = only_colours(img, text_colours)
    result = pytesseract.image_to_string(i)
    return result


def number(str):
    try:
        return int(str)
    except:
        return 0

def read_num(region, colour=WHITE, scale=1, confidence=0.75):
    print("Read num - temp2")
    pag.screenshot('temp/temp2.png', region=region)
    i = cv2.imread(f"temp/temp2.png", 1)
    i = cv2.resize(i, (0,0), fx=scale, fy=scale)
    i = only_colours(i, colour)
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

    found = []
    for y in range(10):
        rects = find_many_image(str(y), i, confidence)
        if len(rects) > 0:
            for rect in rects:
                found.append((str(y), rect[0]))
    result = 0
    # print(found)
    result = ""
    found.sort(key=lambda tup: tup[1])
    for y in found:
        result += y[0]

    #
    #
    # if len(found) == 2:
    #     if found[1][1] > found[0][1]: result = found[0][0] * 10 + found[1][0]
    #     else: result = found[1][0] * 10 + found[0][0]
    # elif len(found) == 1:
    #     result = found[0][0]

    # print(int(result))

    return result

def read_army_time(region, colour=WHITE):
    pag.screenshot('temp/temp2.png', region=region)
    i = cv2.imread(f"temp/temp2.png", 1)
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

    found = []
    for y in [0,1,2,3,4,5,6,7,8,9,"m","s",]:
        rects = find_many_number(str(y), i, 0.80)
        if len(rects) > 0:
            for rect in rects:
                found.append((str(y), rect[0]))
    result = ""
    found.sort(key=lambda tup: tup[1])
    for y in found:
        result += y[0]
    # print("Read army time:", found, "=>", result)
    return result

def read_troop_count(region):
    pag.screenshot('temp/temp2.png', region=region)
    i = cv2.imread(f"temp/temp2.png", 1)
    i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)

    found = []
    for y in [0,1,2,3,4,5,6,7,8,9,]:
        rects = find_many_troop_number(str(y), i, 0.80)
        if len(rects) > 0:
            for rect in rects:
                found.append((str(y), rect[0]))
    result = ""
    found.sort(key=lambda tup: tup[1])
    for y in found:
        result += y[0]
    # print("Read troop count:", found, "=>", result)
    return result

def read_building_level():
    pag.screenshot('temp/building_level.png', region=SELECTED_TOWER)



def read_troop_count_image(i):
    found = []
    for y in [0,1,2,3,4,5,6,7,8,9,]:
        rects = find_many_troop_number(str(y), i, 0.80)
        if len(rects) > 0:
            for rect in rects:
                found.append((str(y), rect[0]))
    result = ""
    found.sort(key=lambda tup: tup[1])
    for y in found:
        result += y[0]
    # print("Read troop count:", found, "=>", result)
    return result

def read_cost(i):
    found = []
    for y in [0,1,2,3,4,5,6,7,8,9,"d","g","e","f","h"]:
        rects = find_many_number_2(i, "numbers_cost", str(y), 0.85)
        if len(rects) > 0:
            for rect in rects:
                found.append((str(y), rect[0]))
    result = ""
    found.sort(key=lambda tup: tup[1])
    for y in found:
        result += y[0]
    print("Read cost:", found, "=>", result)
    return result

def read_resources(i):
    found = []
    for y in [0,1,2,3,4,5,6,7,8,9]:
        rects = find_many_number_2(i, "numbers_resources", str(y), 0.75)
        if len(rects) > 0:
            for rect in rects:
                found.append((str(y), rect[0]))
    result = ""
    found.sort(key=lambda tup: tup[1])
    prev_x = 0
    for y in found:
        # print(prev_x, y[1])
        if y[1] <= prev_x + 3:
            found.remove(y)
        prev_x = y[1]
    for y in found:
        result += y[0]
    # print("Read resources:", found, "=>", result)
    return result

def read_build_time(i):
    found = []
    for y in [0,1,2,3,4,5,6,7,8,9,'d','h','m',]:
        rects = find_many_number_2(i, "numbers/time", str(y), 0.8)
        if len(rects) > 0:
            for rect in rects:
                found.append((str(y), rect[0]))
    result = ""
    found.sort(key=lambda tup: tup[1])
    prev_x = 0
    for y in found:
        # print(prev_x, y[1])
        if y[1] <= prev_x + 3:
            found.remove(y)
        prev_x = y[1]
    for y in found:
        result += y[0]
    result = result.replace("hh", "h")
    print("Read build time:", found, "=>", result)
    return result



# def read_army_time_old(region, colour=WHITE):
#     SCALE = 1.29
#     pag.screenshot('temp/temp2.png', region=region)
#     i = cv2.imread(f"temp/temp2.png", 1)
#     i = cv2.resize(i, (0,0), fx=SCALE, fy=SCALE)
#     i = only_colours(i, colour)
#     i = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
#
#     found = []
#     for y in [0,1,2,3,4,5,6,7,8,9,"m","s",]:
#         rects = find_many_image(str(y), i, 0.75)
#         if len(rects) > 0:
#             for rect in rects:
#                 found.append((str(y), rect[0]))
#     result = ""
#     found.sort(key=lambda tup: tup[1])
#     for y in found:
#         result += y[0]
#     # print("Read army time:", found, "=>", result)
#     return result

# def available_gold():
#     wait_cv2("end_battle")
#     time.sleep(1)
#     result = read_text(COIN_REGION, AVAILABLE_GOLD_COLOURS, True)
#     # print("Available Gold:", result)
#     return result

def available_resources():
    wait_cv2("end_battle")
    time.sleep(1)
    gold, elixir, dark = 0,0,0
    result = []

    for name, region in [(gold, AVAILABLE_GOLD), (elixir, AVAILABLE_ELIXIR), (dark, AVAILABLE_DARK)]:
        pag.screenshot(f'temp/available_{name}.png', region=region)
        i = cv2.imread(f"temp/available_{name}.png", 0)
        result_ind = read_resources(i)
        try:
            result_ind = int(result_ind)
        except:
            result_ind = 0
        result.append(result_ind)

    print("Available Resources:", result)
    return result

def current_resources_b():
    time.sleep(1)
    result_array = []
    for x in [RESOURCES_G, RESOURCES_E]:
        pag.screenshot('temp/read_resources.png', region=x)
        i = cv2.imread("temp/read_resources.png", 0)
        result = read_resources(i)
        try:
            result = int(result)
        except:
            result = 0
        result_array.append(result)
    print("Current Resources:", result_array)
    return result_array

def resource_limit():
    time.sleep(1)
    result_array = []
    for x in [RESOURCES_G, RESOURCES_E, RESOURCES_D, ]:
        pag.click(pag.center(x))
        region = x[0]+100, x[1]+70, x[2], x[3]
        result = read_text(region, WHITE, True)
        print(result)
        pag.click(85, 1000)
        time.sleep(0.1)
        result_array.append(result)
    return result_array

def waiting(seconds):
    time.sleep(seconds)

def time_to_army_ready():
    time = army_time()
    print("Time to army ready:", time)
    return time

# def clan_troops():
#     click_cv2("army")
#     wait_cv2("army_tab")
#     time.sleep(3)
#     result = read_text(CLAN_TROOPS, WHITE, False)
#     space = result.find("/")
#     pag.click(85, 1000)
#
#     if space > 0:
#         max_troops = result[space+1:]
#         if max_troops == 0: max_troops = 20
#         current_troops = result[0:space]
#         # print(current_troops, max_troops)
#     try:
#         result = round(int(current_troops) / int(max_troops),2)
#     except:
#         result = 0
#     print("clan_troops", result)
#     return result
#
def army_time():
    result = read_army_time(ARMY_TIME, WHITE)
    try:
        if result[-1] == "s":
            # print("army_time:", 1)
            return 1 # ie 1 minutes
        else:
            result = int(result[0:-1])
            result = min(20, result)
            # print("army_time:", result)
            return result
    except:
        print("army_time: Failed to read screenshot")
        return 0

def capital_coin_time():
    result = read_text(CAPITAL_COIN_TIME, WHITE)
    try:
        result = alpha_to_numbers(result[0][1])
        result = string_to_time(result)
        print("Capital coin time:",result)
    except:
        print("Failed to read screenshot")
        print(result)
    return result

def get_numbers(string):
    new_string = "0"
    for x in string:
        if x.isdigit():
            new_string += x
    return int(new_string)

def alpha_to_numbers(string):
    if len(string) == 0: return ""
    if VERBOSE_LOG: print("alpha_to_numbers Pre:", string)
    string = string.replace("xl", "21")
    string = string.replace("xs", "20")
    string = string.replace("[", "0")
    # string = string.replace("d", "0")
    string = string.replace("I", "1")
    string = string.replace("T", "1")
    string = string.replace("t", "1")
    string = string.replace("l", "1")
    string = string.replace("i", "1")
    string = string.replace("J", "1")
    string = string.replace("e", "2")
    string = string.replace("é", "2")
    string = string.replace("Z", "2")
    string = string.replace("z", "2")
    string = string.replace("A", "4")
    string = string.replace("S", "5")
    string = string.replace("Q", "4")
    string = string.replace("B", "8")
    string = string.replace("g", "9")
    string = string.replace("O", "0")
    string = string.replace("o", "0")
    string = string.replace("u", "H")
    string = string.replace("q ", " ")
    string = string.replace("-", "")
    string = string.replace("~", "")
    string = string.replace("//", "/")
    string = string.replace("/p", "/")
    if string[-1] == "5": string = string[0:-2] + "s"
    if VERBOSE_LOG: print("alpha_to_numbers Post:", string)
    return string

def text_to_time(string):
    print(f"text_to_time:{string}")
    space = string.find(" ")

    if space == -1: return
    if string[space-1].isdigit():
        if string[-1] == "M":
            string = string.replace(" ", "H ")
            space = string.find(" ")
        if string[-1] == "s":
            string = string.replace(" ", "M ")
            space = string.find(" ")

    days, hours, minutes, seconds = 0,0,0,0
    mode = string[space-1]
    print("Mode:", mode)
    if mode == "t": mode = "H"
    if mode == "M":
        minutes = string[0:space-1]
        seconds = string[space+1:-2]
    if mode.lower() == "h":
        hours = string[0:space-1]
        minutes = string[space+1:-2]
    if mode == "d":
        days = string[0:space-1]
        hours = string[space+1:-2]

    try:
        days = int(days)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
    except:
        return None
    if days == 0 and hours == 0 and minutes == 0 and seconds == 0: return None
    print("Clean time", days, hours, minutes, seconds)
    finish = datetime.now() + timedelta(days=days) + timedelta(hours=hours) + timedelta(minutes=minutes) + timedelta(seconds=seconds)
    print("Finish time", finish)

    return finish

def text_to_time_2(string):
    # print(f"text_to_time_2: {string}")
    string = string.replace("hh", "h")
    days_x = string.find("d")
    hours_x = string.find("h")
    minutes_x = string.find("m")
    seconds_x = string.find("s")
    # print(days_x, hours_x, minutes_x)

    days, hours, minutes, seconds = 0,0,0,0
    if days_x != -1:
        days = string[0:days_x]
        hours = string[days_x+1:-1]
        # print("Days")
    elif hours_x != -1:
        hours = string[:hours_x]
        minutes = string[hours_x+1:-1]
        # print("Hours")
    elif minutes_x != -1:
        minutes = string[0:minutes_x]
        seconds = string[minutes_x+1:-1]
        # print("Minutes")
    elif seconds_x != -1:
        seconds = string[0:seconds_x-1]
    else:
        return

    try:
        days = int(days)
        days = min(7, days)
    except:
        days = 0
    try:
        hours = int(hours)
        hours = min(24, hours)
    except:
        hours = 0
    try:
        minutes = int(minutes)
        minutes = min(60, minutes)
    except:
        minutes = 0
    try:
        seconds = int(seconds)
        seconds = min(60, seconds)
    except:
        seconds = 0

    # print(days, hours, minutes)

    if days == 0 and hours == 0 and minutes == 0 and seconds == 0: return None
    # print("Clean time", days, hours, minutes, seconds)
    finish = datetime.now() + timedelta(days=days) + timedelta(hours=hours) + timedelta(minutes=minutes) + timedelta(seconds=seconds)
    # print("Finish time", finish)

    return finish

def string_to_time(time):
    try:
        return datetime.fromisoformat(time)
    except:
        return datetime.now()

def time_to_string(time):
    if time is None: return "Now"
    if time <= datetime.now():
        return "Now"
    elif time <= datetime.now() + timedelta(hours=24):
        return time.strftime('%I:%M%p')
    elif time <= datetime.now() + timedelta(hours=48):
        return time.strftime('%d %b %I:%M%p')
    else:
        return time.strftime('%d %b')

