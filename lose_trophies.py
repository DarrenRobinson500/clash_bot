# from nav import *
from troops import *
from people import *

# ========================
# === 7. LOSE TROPHIES ===
# ========================

def place(troop, count_total, dp=(400,400), troop_pause=0):
    dp1 = (dp[0],min(dp[1],815))
    val, loc, rect = find(troop.i_attack.image, get_screenshot(TROOP_ZONE))
    # print("Place troops:", troop, val, loc)
    if val > 0.63:
        click(troop.i_attack.image, TROOP_ZONE)
        time.sleep(.2)
        count = 0
        pause_dur = 0.2
        while count < count_total:
            pag.click(dp1)
            time.sleep(troop_pause)
            time.sleep(pause_dur)
            prop_troops = int(count / count_total * 100)
            damage = read_text(DAMAGE, WHITE, True)
            if damage > 100: damage = 0
            # print("Place:", prop_troops, damage)
            if damage + 30 > prop_troops and damage > 30:
                pause_dur += 0.1
                pause_dur = min (1.5, pause_dur)
            if damage + 20 > prop_troops and damage > 50:
                reduction = int((1 - prop_troops/damage) * count_total)
                count += reduction * 2
            count += 1


def calc_trophies():
    goto(main)
    time.sleep(1)
    result = trophies.read(TROPHIES, return_number=True, show_image=False)
    return result

def lose_trophies(account):
    global current_location
    current_trophies = calc_trophies()
    print("Lose trophies", account.number, account.max_trophies, current_trophies)
    if current_trophies > account.max_trophies:
        goto(find_a_match)

        hold_key("a", 0.5)
        for _ in range(2): pag.scroll(300)
        # zoom_out()
        dp = STANDARD_DP
        for troop in [king, queen, warden, champ, barb, giant, bomber, super_barb]:
            val, loc, rect = find(troop.i_attack.image, get_screenshot(TROOP_ZONE))
            print("Lose trophies:", troop.name, val)
            if val > 0.65:
                place(troop, 1, dp)
                print("Unleashed", troop)
                break
        click_cv2("surrender")
        click_cv2("surrender_okay")
        current_location = "return_home"
        goto(main)
        invite_latest_attackee()

        # if troop in [barb, giant, bomb, ]:
        #     troop_delete_backlog()
        #     restock([troop], account, extra=False)
        #     attack(account, account.army_troops)

        return True
    return False
