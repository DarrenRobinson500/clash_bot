from collections import Counter

my_list = ["a", "a", "a", "b", "b"]

string = ""
troops_counter = Counter(my_list)

for t in troops_counter:
    string += f"{t}: {troops_counter[t]}, "
print("Troops:", string[:-2])

