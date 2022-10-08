from bot import *

OBJECTS_B = dir_to_list('attack_b')
print(OBJECTS_B)

def get_screen():
    goto(attacking_b)
    zoom_out()
    hold_key('s', 0.5)
    time.sleep(1)
    pag.screenshot('temp/attacking_b.png')

def for_real():
    start()
    change_accounts(3, "builder")
    goto(builder)
    get_screen()
    loc_th = th_b()
    loc_th = check_loc_th(loc_th)
    a, b = objects_b(loc_th)
    place_troops_b(a, b)
    goto(builder)
    end()

def fake():
    loc_th = th_b()
    loc_th = check_loc_th(loc_th)
    a, b = objects_b(loc_th)

# for_real()
fake()

