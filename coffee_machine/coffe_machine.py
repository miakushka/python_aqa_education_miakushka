class CoffeeMachine:
    """
    Class, that implements general coffee machine functionality
    """

    water_per_cup = None
    milk_per_cup = None
    beans_per_cup = None
    drink_price = None
    current_state = "action_required"

    MESSAGES = {
        "action_required": '''Please choose an action: 
            1 - buy coffee; 
            2 - fill coffee machine; 
            3 - take the cash; 
            4 - display remaining ingredients; 
            0 - exit''',

        "enter_drink": '''Now please select a drink: 
                    1 - espresso; 
                    2 - latte; 
                    3 - cappuccino. 
                    Enter 0 to return to main menu ''',

        "enter_cups_amount": "How many cups do you want? Press 0 to return to main menu ",

        "refilling": '''How much ingredients would you like to add (water, milk, beans, cups)?
        Enter needed quantities, divided by space: ''',

        "error": "Wrong command, please try again",

        "enter_command": "Your command: "
    }

    def __init__(self, water_total, milk_total, beans_total, empty_cups_total, cash):
        self.water_total = water_total
        self.milk_total = milk_total
        self.beans_total = beans_total
        self.empty_cups_total = empty_cups_total
        self.cash_total = cash

    def process_user_command(self):
        if self.current_state == "action_required":
            command = self.print_message(self.current_state)
            if command == "0":
                return False
            self.choose_action(command)
            return True

        elif self.current_state == "enter_drink":
            command = self.print_message(self.current_state)
            if command == "0":
                self.current_state = "action_required"
            else:
                self.choose_drink(command)
            return True

        elif self.current_state == "enter_cups_amount":
            command = self.print_message(self.current_state)
            if command == "0":
                self.current_state = "action_required"
            else:
                self.make_drink(command)
            return True

        elif self.current_state == "refilling":
            self.print_current_amounts()
            command = self.print_message(self.current_state)
            self.refilling(command)
            return True

    def print_message(self, state):
        print(self.MESSAGES[state])
        command = input(self.MESSAGES["enter_command"])
        return command

    def choose_action(self, action):
        if action == "1":
            self.current_state = "enter_drink"
        elif action == "2":
            self.current_state = "refilling"
        elif action == "3":
            self.take_cash()
            self.current_state = "action_required"
        elif action == "4":
            self.print_current_amounts()
            self.current_state = "action_required"
        else:
            print(self.MESSAGES["error"])
            self.current_state = "action_required"

    def choose_drink(self, drink):
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

        if drink == "1":
            self.set_resources_needed(espresso_params)
            self.current_state = "enter_cups_amount"
        elif drink == "2":
            self.set_resources_needed(latte_params)
            self.current_state = "enter_cups_amount"
        elif drink == "3":
            self.set_resources_needed(cappuccino_params)
            self.current_state = "enter_cups_amount"
        elif drink == "0":
            self.current_state = "action_required"
        else:
            print(self.MESSAGES["error"])
            self.current_state = "action_required"

    def make_drink(self, cups):
        self.print_current_amounts()
        cups = int(cups)
        if cups == 0:
            self.current_state = "action_required"
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
            self.current_state = "action_required"

    def set_resources_needed(self, drink_params):
        self.water_per_cup = drink_params["water"]
        self.milk_per_cup = drink_params["milk"]
        self.beans_per_cup = drink_params["beans"]
        self.drink_price = drink_params["price"]

    def refilling(self, amounts):
        amounts = amounts.split(" ")
        if len(amounts) < 4:
            print(self.MESSAGES["error"])
            # todo improve validation
        else:
            self.water_total += int(amounts[0])
            self.milk_total += int(amounts[1])
            self.beans_total += int(amounts[2])
            self.empty_cups_total += int(amounts[3])
            self.print_current_amounts()
            self.current_state = "action_required"

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
        possible_cups_amount = self.calculate_possible_cups()

        if possible_cups_amount > cups:
            print("Yes, I can make that amount of coffee (and even %d more than that)" % (possible_cups_amount - cups))
            return True
        elif possible_cups_amount == cups:
            print("Yes, I can make that amount of coffee")
            return True
        else:
            print("No, I can make only %d cup(s) of coffee" % possible_cups_amount)
            return False

    def calculate_possible_cups(self):
        coefficients = [self.water_total // self.water_per_cup, self.beans_total // self.beans_per_cup]
        if self.milk_per_cup > 0:  # in case of espresso
            coefficients.append(self.milk_total // self.milk_per_cup)
        return min(coefficients)


coffee = CoffeeMachine(400, 540, 120, 9, 550)

while True:
    if not coffee.process_user_command():
        break
