from bot import *

path = "C://Users//darre//PycharmProjects//clash_bot//images//attacks1"
dir_list = os.listdir(path)

def list_files():
    count = 1
    for x in dir_list:
        img = cv2.imread(f'images/attacks1/{x}', 1)
        size = img.shape
        if size[0] > 1200 and count <= 100:
            print(f"{count}: {size}")
            count += 1

inferno_high = dir_to_list("towers/inferno_high")
print(inferno_high)


x = 'attack 0112AM.png'
img = cv2.imread(f'images/attacks1/{x}', 1)
found, img = check_towers(inferno_high, img, return_image=True)
print(x, found)
show(img, 20000, x)


count = 0

count_start = 0
cound_end = count_start + 10
for x in dir_list:
    img = cv2.imread(f'attacks1/{x}', 1)
    size = img.shape
    if size[0] > 1200:
        if count_start <= count < cound_end:
            found, img = check_towers(INFERNO_HIGH, img)
            print(x,found)
            scale = 1
            show(cv2.resize(img, (0,0), fx=scale, fy=scale), 5000, f"{x} - {found}")
        count += 1

