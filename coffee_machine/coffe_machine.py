class CoffeeMachine:
    """
    Class, that implements general coffee machine functionality
    """

    espresso_params = {
        "water": 250,
        "milk": 0,
        "beans": 16,
        "price": 4
    }
    latte_params = {
        "water": 350,
        "milk": 75,
        "beans": 20,
        "price": 7
    }
    cappuccino_params = {
        "water": 200,
        "milk": 100,
        "beans": 12,
        "price": 6
    }

    water_per_cup = None
    milk_per_cup = None
    beans_per_cup = None
    drink_price = None
    welcome_message = '''Please choose an action: 
            1 - buy coffee; 
            2 - fill coffee machine; 
            3 - take the cash; 
            4 - display remaining ingredients; 
            5 - exit '''
    error_message = "Wrong command, please try again"

    def __init__(self, water_total, milk_total, beans_total, empty_cups_total, cash):
        self.water_total = water_total
        self.milk_total = milk_total
        self.beans_total = beans_total
        self.empty_cups_total = empty_cups_total
        self.cash_total = cash

    def start_machine(self, action=None):
        while True:
            if action is None:
                action = self.user_input(self.welcome_message)
            if action == "1":
                while True:
                    drink = self.user_input('''Now please select a drink: 
                    1 - espresso; 
                    2 - latte; 
                    3 - cappuccino. 
                    Press 0 to return to main menu ''')
                    if drink == "1":
                        self.set_resources_needed(self.espresso_params)
                    elif drink == "2":
                        self.set_resources_needed(self.latte_params)
                    elif drink == "3":
                        self.set_resources_needed(self.cappuccino_params)
                    elif drink == "0":
                        action = None
                        break
                    else:
                        print(self.error_message)
                        break
                    self.make_coffee()
                    action = None
                    break
            elif action == "2":
                self.refilling()
                action = None
            elif action == "3":
                self.take_cash()
                action = None
            elif action == "4":
                self.print_current_amounts()
                action = None
            elif action == "5":
                break
            else:
                print(self.error_message)
                action = None

    def user_input(self, message=''):
        command = ''
        while not command:
            command = input(message)
        return command

    def make_coffee(self):
        while True:
            self.print_current_amounts()
            cups = self.user_input("How many cups do you want? Press 0 to return to main menu ")
            cups = int(cups)
            if cups == 0:
                break
            print('''For %d cups of coffee you will need:
            %d ml of water
            %d ml of milk
            %d g of coffee beans
            ''' % (cups, self.water_per_cup * cups, self.milk_per_cup * cups, self.beans_per_cup * cups))
            if self.check_ingredients_amount(cups):
                print("Preparing a coffee...")
                print("Boiling water...")
                print("Adding beans...")
                print("Pouring...")
                print("Adding milk if needed...")
                print("Ready!")
                self.update_ingredients_amount(cups)
                self.print_current_amounts()
                break

    def set_resources_needed(self, drink):
        self.water_per_cup = drink["water"]
        self.milk_per_cup = drink["milk"]
        self.beans_per_cup = drink["beans"]
        self.drink_price = drink["price"]

    def refilling(self):
        self.print_current_amounts()
        water_to_add = self.user_input("How much water do you want to add? ")
        self.water_total += int(water_to_add)
        milk_to_add = self.user_input("How much milk do you want to add? ")
        self.milk_total += int(milk_to_add)
        beans_to_add = self.user_input("How much beans do you want to add? ")
        self.beans_total += int(beans_to_add)
        empty_cups_to_add = self.user_input("How many cups do you want to add? ")
        self.empty_cups_total += int(empty_cups_to_add)
        self.print_current_amounts()

    def take_cash(self):
        self.print_current_amounts()
        print("Please take your money: %f UAH" % self.cash_total)
        self.cash_total = 0
        self.print_current_amounts()

    def print_current_amounts(self):
        print('''
        The coffee machine has: 
            %d ml of water 
            %d ml of milk 
            %d g of coffee beans 
            %d disposable cups 
            %f UAH 
        ''' % (self.water_total, self.milk_total, self.beans_total, self.empty_cups_total, self.cash_total))

    def update_ingredients_amount(self, cups):
        self.water_total -= self.water_per_cup * cups
        self.beans_total -= self.beans_per_cup * cups
        self.milk_total -= self.milk_per_cup * cups
        self.empty_cups_total -= cups
        self.cash_total += self.drink_price

    def check_ingredients_amount(self, cups):
        if cups > self.empty_cups_total:
            print("Not enough cups available. Please add more empty cups and try again")
            return False

        # calculating total amount of resources needed for preparing of specified amount of cups
        water_needed = self.water_per_cup * cups
        milk_needed = self.milk_per_cup * cups
        beans_needed = self.beans_per_cup * cups

        # calculating how many more cups can be prepared with ingredients available
        water_coeff = self.water_total // self.water_per_cup
        if self.milk_per_cup == 0: # in case of espresso
            milk_coeff = 2
        else:
            milk_coeff = self.milk_total // self.milk_per_cup
        beans_coeff = self.beans_total // self.beans_per_cup

        if water_needed == self.water_total and milk_needed == self.milk_total and beans_needed == self.beans_total:
            print("Yes, I can make that amount of coffee")
            return True
        elif water_needed <= self.water_total and milk_needed <= self.milk_total and beans_needed <= self.beans_total:
            if water_coeff > 1 and milk_coeff > 1 and beans_coeff > 1:
                print("Yes, I can make that amount of coffee (and even %d more than that)" % (
                        min(water_coeff, milk_coeff, beans_coeff) - cups))
            else:
                print("Yes, I can make that amount of coffee")
            return True
        else:
            print("No, I can make only %d cups of coffee" % (min(water_coeff, milk_coeff, beans_coeff)))
            return False


coffee = CoffeeMachine(400, 540, 120, 9, 550)
coffee.start_machine()
