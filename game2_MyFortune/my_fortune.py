"""
Module sa son module ki evaluer chans ou chak jou!!!
"""


import random as rdm


def fortune():
    """
    Fonksyon sa a pran yon vale ant 1 e 101,
    epi la banm li kom nonb mwen pou jounen an.
    Apre sa lap banm yon nonb chans, kap ant 1 e 4.
    Si vale li te banm lan te pi gwo ke 50 lap banm opsyon
    chwazi nonb chans mwen an, selman si vale chans lan te
    1 oubyen 2.
    """
    my_number = rdm.randint(1, 101)
    print(my_number)
    lucky_number = rdm.randint(1, 4)
    print(lucky_number)
    if lucky_number in {1, 2}:
        if lucky_number == 1:
            lucky_quotes = "Today is your lucky day!"
        else:
            lucky_quotes = """Today won't be as you expected it, but it'll
            be worth it. You still can choose a brighter path in your life."""
        if my_number in range(50, 101):
            number = int(input("Choose an integer between 1 and 3: "))
            if number == 1:
                print(
                    r"""There's is 70% chance that u meet someone that will
                    please you, and make you smile today! :) """
                )
            elif number == 2:
                print("Today should be a wise day for you!")
            else:
                print(
                    "You have choosen a path were you'll have to work. Be smart today!"
                )
    else:
        lucky_quotes = """You must think about your life, and the choices you are making.
        The day can be tough."""
    print(f"{lucky_quotes}. Your lucky number for today is {lucky_number}")
    return my_number, lucky_number


if __name__ == "__main__":
    fortune()
