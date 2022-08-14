import bot
from bot import *


def create_war_troops(troops):
    troop_delete_backlog()
    for x in TROOPS:
        actual = troop_count(x)
        print("Create war troops", x, actual)
        troop_delete(x, actual)
    restock(troops)
    restock(troops)


troops1 = ["edrag"] * 8 + ["dragon"] * 2 + ["lightening"] * 11
troops2 = ["dragon"] * 12 + ["balloon"] + ["lightening"] * 11
data = [(1, troops1), (2, troops2)]

# for account, troops in data:
#     change_accounts(1, "main")
#     create_war_troops(troops)

start()
for account, troops in [(1, troops1), (2, troops2), ]:
    change_accounts(account)
    create_war_troops(troops)
    request(account)
end()

