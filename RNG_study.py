# FOLLOWING CODE FROM IRGRMI
def upd(rng):
    return (rng * 0x5D588B65 + 1) % 0x100000000

rng = 0x1234567B
#Goomba

item_drop_rate = 3
possible_item_drops = [
    "Dried Shroom",
    "Cake Mix",
    "Big Egg",
    "Honey Jar",
    "Shroom Shake",
    "Catch Card"
]
possible_item_drops_weights = [
    100,
    100,
    100,
    100,
    200,
    50
]

# drop or not
rng = upd(rng)
x = rng // 0x28F5C28
while x >= 100:
    rng = upd(rng)
    x = rng // 0x28F5C28

if x < item_drop_rate:
    # what to drop
    weight_sum = sum(possible_item_drops_weights)
    rng = upd(rng)
    x = 0xFFFFFFFF // weight_sum
    y = rng // x
    while y >= weight_sum:
        rng = upd(rng)
        x = 0xFFFFFFFF // weight_sum
        y = rng // x
    for i in range(len(possible_item_drops)):
        y -= possible_item_drops_weights[i]
        if y < 0:
            print('drop:', possible_item_drops[i])
            break
else:
    print('drop: nothing')