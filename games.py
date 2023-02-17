from nav import *
from account import *
from attacks_logic import *
from images import *
from utilities import *
# from run import *
# from account import *
# from bot import *
# from war import *
# from research import *
# from troops import *

games = []

class Game():
    def __init__(self, image, action, preference, min_th=0, extra_troops=[]):
        self.name = image
        self.image = Image(name=image, file=f'images/games/{image}.png', threshold=0.8)
        self.action = action
        self.preference = preference
        self.min_th = min_th
        self.extra_troops = extra_troops
        games.append(self)

    def __str__(self):
        return self.name

    def is_available(self):
        goto(l_games)
        return self.image.find()

    def start(self, account):
        goto(l_games)
        result = self.image.click()
        if result:
            i_start_game.click()
            account.current_game = self
        pag.moveTo(1588, 690)
        pag.dragTo(1000, 336, .2)
        result = self.image.click()
        if result:
            i_start_game.click()
            account.current_game = self
        pag.moveTo(1588, 336)
        pag.dragTo(1000, 690, .2)
        result = self.image.click()
        if result:
            i_start_game.click()
            account.current_game = self

        return result

    def run(self, account):
        if self.action == "attack_builder":
            print("Game run: Attack_b")
            attack_b(account, attack_regardless=True)
        elif self.action == "attack_main":
            print("Game run: Attack", account.games_troops)
            troops_to_use = account.games_troops
            troops_to_use["initial_troops"] = troops_to_use["initial_troops"] + self.extra_troops
            attack(account, troops_to_use, siege_required=False, attack_regardless=True)
        else:
            print("Run: action not coded", self, self.action)

        if not game_active():
            account.current_game = None
            db_games_update(account.number, "")


def game_active():
    # Counter({(128, 128, 0): 1250}) - active game
    goto(l_games)
    time.sleep(0.3)
    region = (960, 395, 50, 25)
    pag.screenshot('temp/games_colour.png', region=region)
    image = cv2.imread('temp/games_colour.png', 1)
    new, counter = simplify(image, gradients=2)
    print(counter)
    result = counter[(128, 128, 0)] > 1000
    print("Game active:", result)
    return result


destroy_builder = Game("destroy_builder", "attack_builder", 1)
giant_builder = Game("giant_builder", "attack_builder", 1)
barb_builder = Game("barb_builder", "attack_builder", 1)
archer_tower_builder = Game("archer_tower_builder", "attack_builder", 1)
destruction_builder = Game("destruction_builder", "attack_builder", 1)
fast_stars_builder = Game("fast_stars_builder", "attack_builder", 1)
firecrackers = Game("firecrackers", "attack_builder", 1)
destroy_lab = Game("destroy_lab", "attack_builder", 1)
crusher_builder = Game("crusher_builder", "attack_builder", 1)
stars_builder = Game("stars_builder", "attack_builder", 1)
clock_builder = Game("clock_builder", "attack_builder", 1)
double_cannon_builder = Game("double_cannon_builder", "attack_builder", 1)
bomber_builder = Game("bomber_builder", "attack_builder", 1)
air_bombs_builder = Game("air_bombs_builder", "attack_builder", 1)

destroy_main = Game("destroy_main", "attack_main", 2)
stars_main = Game("stars_main", "attack_main", 2)
wall_main = Game("wall_main", "attack_main", 2)
elixir_main = Game("elixir_main", "attack_main", 2)
air_sweeper_main = Game("air_sweeper_main", "attack_main", 2, min_th=9)
destroy_wizards = Game("destroy_wizards", "attack_main", 2)
destroy_gold = Game("destroy_gold", "attack_main", 2)
percentage_main = Game("percentage_main", "attack_main", 2)

archer_main = Game("archer_main", "attack_main", 3, extra_troops=[archer] * 30)
wizard_main = Game("archer_main", "attack_main", 3, extra_troops=[wizard] * 7 + [archer] * 2)
giant_main = Game("giant_main", "attack_main", 3, extra_troops=[giant] * 6)
bomber_main = Game("bomber_main", "attack_main", 3, extra_troops=[bomber] * 15)
edrag_main = Game("edrag_main", "attack_main", 3, extra_troops=[edrag])
baby_drag_main = Game("baby_drag_main", "attack_main", 3, extra_troops=[baby_drag] * 3)



def choose_game(account):
    print("Choose game start")
    goto(l_games)
    # print(i_complete.find_detail(fast=False, show_image=True)[0])
    if i_complete.find():
        # print(i_complete.find_detail())
        print("Choose game - complete")
        account.playing_games = False
        return False
    if game_active():
        print("Choose game - game already in progress")
        return False
    available_games = []
    for game in games:
        if game.is_available() and account.th >= game.min_th:
            available_games.append(game)
    pag.moveTo(1588, 690)
    pag.dragTo(1000, 336, .2)
    for game in games:
        if game.is_available():
            available_games.append(game)

    available_games.sort(key=lambda x: x.preference, reverse=False)
    print("Choose game:", objects_to_str(available_games))
    if len(available_games) > 0:
        result = available_games[0]
        account.current_game = result
        db_games_update(account.number, result.name)
        result.start(account)
        return available_games[0]
    return False

# def run_game(account):
#     # change_accounts(account.number, "main")
#     if account.current_game is None:
#         choose_game(account)
#     if account.current_game is None:
#         return
#     account.current_game.run()

def create_combined_games_image(accounts):
    account_images = []
    for account in accounts:
        account_images.append(cv2.imread(f'temp/tracker/games_{account.number}.png', 1))

    header = np.zeros((50, 190, 3), np.uint8)
    x = datetime.now().strftime("%I:%M") + datetime.now().strftime("%p").lower()
    cv2.putText(header, x, (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    images = [header] + account_images
    result = combine_image_vertical(images)
    show(result)
    cv2.imwrite("C:/Users/darre/OneDrive/Darren/clash_bot/tracker/games.png", result)

def get_current_game(account):
    goto(l_games)
    screen = get_screenshot(CURRENT_GAME)
    get_screenshot(GAMES_SCORE, filename=f"tracker/games_{account.number}")
    max_result = 0
    current_game = None
    for game in games:
        result, val = game.image.find_screen(screen, return_result=True)
        print(game, result, val)
        if val > 0.65 and val > max_result:
            max_result = result
            current_game = game
    account.current_game = current_game
    if current_game:
        db_games_update(account.number, current_game.name)
    return current_game

def return_game(name):
    return next((x for x in games if x.name == name), None)

# choose_game()

# db_games_update(3, "wall_main")
# db_games_update(2, "destroy_main")
# db_games_view()

def run_games(accounts):
    for account in accounts:
        if not account.playing_games:
            print("Run games. Not playing:", account)
            continue
        change_accounts_fast(account)
        game = get_current_game(account)
        # print("1", account.current_game)
        if not game:
            # print(account, "No")
            game = choose_game(account)
            # print(account, "No. Chose:", game)
        # print("2", account.current_game)
        if game:
            # print(account, "Yes")
            game.run(account)
        create_combined_games_image(accounts)

# for account in accounts:
#     current_game_name = db_games_read(account.number)
#     current_game = return_game(current_game_name)
#     if current_game:
#         print(account, current_game.name)
#     else:
#         print(account, None)
#     account.current_game = current_game

# for game in games:
#     print(game.name)

# goto(pycharm)