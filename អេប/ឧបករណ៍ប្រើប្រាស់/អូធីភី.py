import random
import string


def បង្កើត_អូធីភី(length: int = 6) -> str:
    return "".join(random.choices(string.digits, k=length))
