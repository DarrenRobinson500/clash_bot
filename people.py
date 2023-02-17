from nav import *

def invite_latest_attackee():
    goto(main)
    i_mail.click()
    time.sleep(0.2)
    i_attack_log.click()
    rects = i_message.find_many(show_image=False)
    rects = sorted(rects, key=lambda x: x[1])
    if len(rects) > 0:
        click_rect(rects[0])
        time.sleep(0.7)
        i_profile.click()
        time.sleep(0.7)
        i_invite.click()
    time.sleep(0.7)
    i_red_cross.click()

# invite_latest_attackee()

