import random

for _ in range(20):
    uitbarsting_gemeten = random.choices([0, 1], weights=(80, 20))[0]
    print(uitbarsting_gemeten)