import random


async def use(qty: int) -> int:
    total = 0
    for i in range(qty):
        total += _amount()

    return -1


def _amount():
    # gets a random amount between 1 and 50
    p1 = random.randrange(1, 22)
    p2 = random.randrange(1, 22)

    return p1 * p2 / 100  # a number between 1 and 3.7^3
