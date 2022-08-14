from bot import *

path = "C://Users//darre//PycharmProjects//clash_bot//attacks1"
dir_list = os.listdir(path)

# print(dir_list)

# x = 'attack 0117AM.png'
# img = cv2.imread(f'attacks1/{x}', 1)
# found, img = check_towers(INFERNO_HIGH, img)
# print(x, found)
# show(img, 20000, x)

# count = 0
#
# count_start = 70
# cound_end = count_start + 10
# for x in dir_list:
#     if count_start <= count < cound_end:
#         img = cv2.imread(f'attacks1/{x}', 1)
#         found, img = check_towers(INFERNO_HIGH, img)
#         print(x,found)
#         scale = 0.7
#         show(cv2.resize(img, (0,0), fx=scale, fy=scale), 5000, f"{x} - {found}")
#     count += 1


list = [('2', 70), ('d', 84), ('1', 90), ('1', 107), ('h', 109), ('8', 116), ('1', 124), ('h', 127)]
print(list)
prev_x = 0
for y in list:
    print(prev_x, y[1])
    if y[1] <= prev_x + 3:
        list.remove(y)
    prev_x = y[1]

print(list)