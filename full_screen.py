from bot import *

def create_double_screen(account):
    x_end = 1600
    y1_end = 600
    y2_end = 900

    # read screenshots
    img0 = cv2.imread('temp/attacking1.png', 1)
    img2 = cv2.imread('temp/attacking2.png', 1)

    # find TH for alignment
    val, rect1 = find_tower(img0, TH)
    val, rect2 = find_tower(img2, TH)
    y_adj = rect1[1] - rect2[1]
    y2_start = y1_end - y_adj

    # crop and combine images
    img1 = img0[0:        y1_end, 0: x_end]
    img2 = img2[y2_start: y2_end, 0: x_end]
    img = np.concatenate((img1, img2), axis=0)

    # save the image
    post = datetime.now().strftime('%I%M%p')
    x = f'images/attacks{account}/attack {post}.png'
    cv2.imwrite(x, img)
    return img

def get_double_screen():
    for _ in range(2): pag.scroll(300)
    pag.screenshot('temp/attacking1.png')
    for _ in range(3): pag.scroll(-300)
    pag.screenshot('temp/attacking2.png')

def get_double_screen_full():
    start()
    goto(find_a_match)
    time.sleep(1)
    for _ in range(2): pag.scroll(300)
    pag.screenshot('temp/attacking1.png')
    time.sleep(1)
    for _ in range(4): pag.scroll(-300)
    pag.screenshot('temp/attacking2.png')
    goto(main)
    end()

# account = 1
# get_double_screen_full()
# create_double_screen(account)

start()
goto(find_a_match)

img1 = cv2.imread('temp/attacking.png', 1)
result = ram_drop_point(img1)
print(result)
goto(main)
end()
time.sleep(1.3)
click_cv2('image')
img = cv2.imread('temp/attack.png', 1)

show(img)