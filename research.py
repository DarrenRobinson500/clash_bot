from troops import *
from time import sleep


def research_slide(direction):
    global current_position
    if direction == "right":
        pag.moveTo(1500, 630, 0.3)
        pag.dragTo(380, 630, 0.5, button="left")
        time.sleep(0.3)
    else:
        pag.moveTo(380, 630, 0.3)
        pag.dragTo(1500, 630, 0.5, button="left")
        time.sleep(0.3)

def next_research(account):
    if account.th <= 10:
        research_preference = [barb, giant, wizard, bomber, lightening, minion, hog, archer, goblin, bloon, heal, rage]
    else:
        research_preference = [barb, ram, log_thrower, golem, witch, minion, clone, skeleton, lava_hound]
    goto(lab)
    if i_research_upgrading.find():
        print("Still research")
        goto(main)
        pag.click(BOTTOM_LEFT)
        account.update_lab_time()
        return
    for troop in research_preference:
        found, count = False, 0
        for slide_direction in ["right", "right", "right", "left", "left", "left"]:
            if troop.i_research.find():
                colour = troop.i_research.colour()
                print("Research", troop, "Found", troop.i_research.colour())
                if colour > 500:
                    troop.i_research.click()
                    sleep(0.1)
                    if i_research_elixir.find():
                        i_research_elixir.click()
                    else:
                        i_research_dark.click()
                    print("Available")
                    pag.press("esc")
                    pag.click(BOTTOM_LEFT)
                    return
            else:
                research_slide(slide_direction)
            count += 1
    account.update_lab_time()

    goto(main)
    pag.click(BOTTOM_LEFT)
