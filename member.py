from object_recognition import click, find_images_bool, click_cv2, show, wait_cv2
import nav
import os, cv2

member_files = os.listdir("images/members")
members = []

CHAT_NAME = (158, 132, 160, 770)

def get_image_from_file(member, style):
    file = f'{member}_{style}.png'
    if style == "": file = f'{member}.png'
    image = None
    if file in member_files:
        image = cv2.imread('images/members/' + file, 0)
    else:
        print(f"Adding member image: could not find '{file}'")
    return image

class Member():
    def __init__(self, name):
        self.name = name
        self.i_chat = get_image_from_file(name, "chat")
        members.append(self)

member_data = [
    ("benji", 1),
    ("daz", 2),
    ("nero_kyo", 3),
    ("michael_h", 4),
    ("bad_daz", 2),
    ]

# print()
# for name, id in member_data:
#     print("Creating member:", name)
#     Member(name=name, )

