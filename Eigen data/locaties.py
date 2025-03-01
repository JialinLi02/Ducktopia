import itertools
import string

import string

letters = string.ascii_uppercase[:25]  # 'A' to 'Y'
numbers = range(1, 51)  # 1 to 50

string_list = [f"{letter}{num}" for letter in letters for num in numbers]

print(string_list)

a = ("John", "Charles", "Mike")
b = ("Jenny", "Christy", "Monica")

x = zip(a, b)

print(list(x))