import pyautogui as pag
import time


# === CLICKS ===
def wait(image):
    found = False
    count = 0
    while not found:
        image_location = pag.locateCenterOnScreen(f'images/{image}.png', confidence=0.8)
        if image_location:
            found = True
            # print(f"Found {image}")
            return image_location
        else:
            # print(f"{image} {count}")
            time.sleep(1)
            count += 1
        if count > 6:
            count = 0
            timed_click('bluestacks_icon', (0, 0), 2)
            timed_click('reload_game', (0, 0), 2)
    return

def find(image, confidence=0.55):
    result = pag.locateCenterOnScreen(f'images/{image}.png', confidence=confidence)
    # if not result:
    #     try:
    #         result = pag.locateCenterOnScreen(f'images/{image}1.png', confidence=confidence)
    #     except:
    #         pass
    # print(image, result)
    if result:
        result = True
    else:
        result = False
    return result

def wait_and_click(image, confidence=0.6):
    # print("Wait and click:", image)
    found = False
    count = 0
    while not found:
        image_location = pag.locateCenterOnScreen(f'images/{image}.png', confidence=confidence)
        if image_location:
            pag.click(image_location)
            found = True
        else:
            # print(f"{image} {count}")
            time.sleep(1)
            count += 1
        if count == 6:
            wait_and_click('bluestacks_icon')
        if count > 12:
            return
    return

def timed_click(image, offset=(0,0), dur=0, confidence=0.6):
    found = False
    count = 0
    while not found and count <= dur:
        location = pag.locateCenterOnScreen(f'images/{image}.png', confidence=confidence)
        # if not location: # see if there's an alt image
        #     try:
        #         location = pag.locateCenterOnScreen(f'images/{image}1.png', confidence=confidence)
        #     except:
        #         pass
        if location:
            pag.click((location[0] + offset[0], location[1] + offset[1]))
            return True
        # else:
            # print(f"{image} {count}")
        time.sleep(1)
        count += 1
    return False

def intelligent_click(image1, offset1, image2, offset2, confidence=0.6):
    if timed_click(image2, offset2, 0): return
    timed_click(image1, offset1, 3, confidence)
    time.sleep(2)
    timed_click(image2, offset2, 3, confidence)
    return

# def dual_click(image1, image2, confidence=0.6):
#     for x in range(5):
#         if find(image2):
#             click_cv2(image2)
#             time.sleep(0.15)
#             return
#
#         if find(image1):
#             click_cv2(image1)
#             time.sleep(0.15)
#             dual_click(image1, image2, confidence)
#         time.sleep(0.1)
#     return False
