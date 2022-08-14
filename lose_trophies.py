from bot import *

def lose_trophies():
    start()
    goto("attacking")
    place("king", 1)
    goto("main")

def calc_trophies():
    goto("main")
    time.sleep(1)
    result = read_num(TROPHIES, WHITE, 1.00)
    if result < 200: result = result * 10
    return result


start()
print(read_num(TROPHIES, WHITE, 0.98))
print(read_num(TROPHIES, WHITE, 1.00))
end()

# lose_trophies