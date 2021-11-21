"""
This module simulates bruteforce attack on PyBank. To run bruteforce attack simply run this script.
To check the bruteforce account protection, you have to do the following steps manually:
1. Run banking.py
2. Create an account
3. Try to log into created account 4 times in a row with wrong PIN
4. Your account will be blocked and you want be able to sign in even with valid credentials
"""
import banking

bank = banking.BankingSystem()


def cards(base, number):
    i = 0
    while i <= number:
        yield base + i
        i += 1


def pins(base, number):
    i = 0
    while i <= number:
        yield base + i
        i += 1


card_generator = cards(400000000000000, 999999999)
pin_generator = pins(0, 9999)

while True:
    card = str(next(card_generator))
    card = card + str(bank.generate_checknumber(card))
    while True:
        pin = str(next(pin_generator, "end"))
        if pin == "end":
            pin_generator = pins(0, 9999)
            break
        if len(pin) == 1:
            pin = "000" + pin
        elif len(pin) == 2:
            pin = "00" + pin
        elif len(pin) == 3:
            pin = "0" + pin
        print("Card number: %s" % card)
        print("Pin: %s" % pin)
        if bank.login(card, pin):
            quit(0)
