import random
import sqlite3


class BankingSystem:

    def __init__(self):
        self.connection = sqlite3.connect('card.s3db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS CARD(
        ID INTEGER PRIMARY KEY,
        NUMBER TEXT,
        PIN TEXT,
        BALANCE INTEGER DEFAULT 0,
        LOGIN_ATTEMPTS INTEGER DEFAULT 0,
        BLOCKED INTEGER DEFAULT 0)
        ''')
        self.connection.commit()

    IIN = "400000"
    current_state = "main_menu"
    current_user = None
    MESSAGES = {
        "main_menu": '''
                Welcome to PyBank!
                Please choose an action: 
                1 - Create an account; 
                2 - Log into account;  
                0 - Exit''',
        "enter_card_number": "Please enter your card number",
        "enter_pin_code": "Please enter your PIN",
        "enter_command": "Your input: ",
        "error": "Wrong command, please try again",
        "logged_in": '''
                    1 - Balance;
                    2 - Add Income;
                    3 - Do Transfer;
                    4 - Close Account;
                    5 - Log out;  
                    0 - Exit''',
        "add_income": "Specify income amount.",
        "transfer_money": '''Specify card number of recipient and amount of money, 
        that you want to transfer, divided by space.''',
        "close_account": '''Your account is about to close and all the data will be lost. 
        Enter your PIN to confirm account removing.'''
    }

    def process_user_command(self):
        if self.current_state == "main_menu":
            command = self.__print_message(self.current_state)
            if command == "0":
                self.connection.close()
                return False
            self.__choose_action(command)
            return True
        elif self.current_state == "enter_card_number":
            card_number = self.__print_message(self.current_state)
            pin_code = self.__print_message("enter_pin_code")
            self.login(card_number, pin_code)
            return True
        elif self.current_state == "logged_in":
            command = self.__print_message(self.current_state)
            self.__user_menu(command)
            return True
        elif self.current_state == "add_income":
            command = self.__print_message(self.current_state)
            self.__add_income(command)
            return True
        elif self.current_state == "transfer_money":
            command = self.__print_message(self.current_state)
            self.__transfer_money(command)
            return True
        elif self.current_state == "close_account":
            command = self.__print_message(self.current_state)
            self.__close_account(command)
            return True

    def __print_message(self, state):
        print(self.MESSAGES[state])
        command = input(self.MESSAGES["enter_command"])
        return command

    def __choose_action(self, action):
        if action == "1":
            self.__create_account()
        elif action == "2":
            self.current_state = "enter_card_number"
        else:
            print(self.MESSAGES["error"])
            self.current_state = "main_menu"

    def __create_account(self):
        account_number = self.__generate_account_number()

        # check for being unique
        account_numbers = self.__get_account_numbers()
        while account_number in account_numbers:
            account_number = self.__generate_account_number()

        card_number = self.IIN + account_number
        check_digit = self.generate_checknumber(card_number)
        card_number = card_number + str(check_digit)
        pin_code = self.__generate_pin_code()

        self.cursor.execute(f'''INSERT INTO CARD 
        (NUMBER, PIN) VALUES ('{card_number}', '{pin_code}')''')
        self.connection.commit()

        print("Your card number: %s" % card_number)
        print("Your PIN code: %s" % pin_code)
        self.current_state = "main_menu"

    def generate_checknumber(self, card_number):
        # remove checknumber if exists
        if len(card_number) == 16:
            card_number = card_number[:-1]

        # split card nubmer to the list of digits
        numbers = [int(d) for d in str(card_number)]

        # getting the sum of digits according to Luhn algorithm
        i = 0
        while i <= 14:
            a = numbers[i] * 2
            if a > 9:
                a = a - 9
            numbers[i] = a
            i = i + 2
        result = sum(numbers)

        # verify and return checknumber
        if result % 10 == 0:
            return 0
        else:
            return 10 - result % 10

    def __generate_account_number(self):
        digits = [str(random.randint(0, 9)) for i in range(9)]
        digit = ""
        for i in digits:
            digit += i
        return digit

    def __generate_pin_code(self):
        digits = [str(random.randint(0, 9)) for i in range(4)]
        digit = ""
        for i in digits:
            digit += i
        return digit

    def __get_account_numbers(self):
        self.cursor.execute('''SELECT NUMBER FROM CARD''')
        result = self.cursor.fetchall()
        account_numbers = []
        for i in result:
            account_numbers.append(i[0][6:15])
        return account_numbers

    # made method public to demonstrate bruteforce attack
    def login(self, card_number, pin_code):
        if self.__check_card_exists(card_number):
            if self.__get_login_attempts(card_number) > 3:
                self.__block_account(card_number)

            if self.__is_account_blocked(card_number):
                print("Your account is blocked. Please contact your manager.")
                self.current_state = "main_menu"
                return False

            if self.__sign_in(card_number, pin_code):
                print("You have successfully logged in!")
                return True
            else:
                print("Your data is incorrect. Please re-check your data and try again")
                self.__change_login_attempt(card_number)
        else:
            print("Card number is incorrect")
            self.current_state = "main_menu"

    def __sign_in(self, card_number, pin_code):
        self.cursor.execute('''SELECT NUMBER,PIN FROM CARD''')
        result = self.cursor.fetchall()
        for i in result:
            if i[0] == card_number and i[1] == pin_code:
                self.current_state = "logged_in"
                self.current_user = i[0]
                self.__change_login_attempt(card_number, 0)
                return True

    def __block_account(self, card_number):
        self.cursor.execute(f'''UPDATE CARD SET BLOCKED = 1 WHERE NUMBER = {card_number}''')
        self.connection.commit()

    def __is_account_blocked(self, card_number):
        result = self.cursor.execute(f'''SELECT BLOCKED FROM CARD WHERE NUMBER = {card_number}''')
        result = result.fetchone()[0]
        if result == 1:
            return True
        else:
            return False

    def __get_login_attempts(self, card_number):
        result = self.cursor.execute(f'''SELECT LOGIN_ATTEMPTS FROM CARD WHERE NUMBER = {card_number}''')
        return result.fetchone()[0]

    def __change_login_attempt(self, card_number, attempt=1):
        current_attempts = self.__get_login_attempts(card_number)
        set_attempt = None
        if attempt == 0:
            set_attempt = 0
        else:
            set_attempt = current_attempts + attempt
        self.cursor.execute(f'''UPDATE CARD SET LOGIN_ATTEMPTS = {set_attempt} WHERE NUMBER = {card_number}''')
        self.connection.commit()

    def __user_menu(self, action):
        balance = self.__get_user_balance()
        if action == "1":
            print("Your balance is: %d" % balance)
        elif action == "2":
            self.current_state = "add_income"
        elif action == "3":
            self.current_state = "transfer_money"
        elif action == "4":
            self.current_state = "close_account"
        elif action == "5":
            self.current_user = None
            self.current_state = "main_menu"
        elif action == "0":
            self.connection.close()
            quit(0)

    def __get_user_balance(self):
        balance = self.cursor.execute(f'''SELECT BALANCE FROM CARD WHERE NUMBER = {self.current_user}''')
        balance = balance.fetchone()[0]
        return balance

    def __add_income(self, amount):
        amount = int(amount) + self.__get_user_balance()
        self.cursor.execute(f"UPDATE CARD SET BALANCE = {amount} WHERE NUMBER = {self.current_user}")
        self.connection.commit()
        print("Your balance was successfully updated. Current balance is %d" % self.__get_user_balance())
        self.current_state = "logged_in"

    def __transfer_money(self, card_and_amount):
        card_and_amount = card_and_amount.split(" ")
        card = card_and_amount[0]
        amount = card_and_amount[1]
        current_balance = self.__get_user_balance()
        invalid_card_message = "Probably you made a mistake in the card number. Please try again!"
        if len(card) != 16:
            print(invalid_card_message)
            self.current_state = "transfer_money"
            return False
        else:
            valid_checknum = self.generate_checknumber(card)

        if int(amount) > int(current_balance):
            print("Not enough money!")
        elif card == self.current_user:
            print("You can't transfer money to the same account!")
        elif card[15] != str(valid_checknum):
            print("Probably you made a mistake in the card number. Please try again!")
        elif not self.__check_card_exists(card):
            print("Such card does not exist.")
        else:
            recipient_amount = self.cursor.execute(f'''SELECT BALANCE FROM CARD WHERE NUMBER = {card}''')
            recipient_amount = recipient_amount.fetchone()[0]
            user_amount = self.__get_user_balance()
            amount_to_transfer = recipient_amount + int(amount)
            new_user_amount = user_amount - int(amount)
            self.cursor.execute(f'''UPDATE CARD SET BALANCE = {amount_to_transfer} WHERE NUMBER = {card}''')
            self.cursor.execute(f'''UPDATE CARD SET BALANCE = {new_user_amount} WHERE NUMBER = {self.current_user}''')
            self.connection.commit()
            print("Money successfully transferred! Your current balance is: %d" % self.__get_user_balance())
            self.current_state = "logged_in"

    def __close_account(self, confirmation):
        user_pin = self.cursor.execute(f'''SELECT PIN FROM CARD WHERE NUMBER = {self.current_user}''')
        user_pin = user_pin.fetchone()[0]
        if confirmation == user_pin:
            self.cursor.execute(f"DELETE FROM CARD WHERE NUMBER = {self.current_user}")
            self.connection.commit()
            self.current_user = None
            print("Your account was successfully deleted!")
            self.current_state = "main_menu"
        else:
            print("Confirmation is not correct.")
            self.current_state = "logged_in"

    def __check_card_exists(self, card_number):
        card = self.cursor.execute(f'''SELECT NUMBER FROM CARD WHERE NUMBER = {card_number}''')
        if len(card.fetchall()) == 0:
            return False
        else:
            return True


# ====================================================================================================================


banking = BankingSystem()


def main():
    while True:
        if not banking.process_user_command():
            break


if __name__ == "__main__":
    main()
