import logging
import time


class Logs:
    def __init__(self, filename):
        self.filename = filename
        logging.basicConfig(filename=self.filename,
                            filemode='a',
                            format='%(asctime)s %(levelname)s %(message)s',
                            level=logging.INFO,
                            datefmt='%Y-%m-%d %H:%M:%S')

    @staticmethod
    def write_log(message):
        print(message)
        logging.info(message)

    def read_log(self):
        f = open(self.filename, "r")
        print(f.read())

    def clean_log(self):
        open(self.filename, 'w').close()


class CellNotAvailableEx(Exception):
    def __init__(self):
        self.message = "Cell is not available. Please use another cell."

    def __str__(self):
        return self.message


class WrongCommandEx(Exception):
    def __init__(self):
        self.message = "Wrong command! Please try again."

    def __str__(self):
        return self.message


class TicTacToe:
    current_state = "game_ready"
    first_player_name = None
    second_player_name = None
    battlefield = None
    turns_counter = 0

    def __init__(self):
        self.logger = Logs("games.log")

    MESSAGES = {
        "game_ready": '''
            Welcome to Tic-tac-toe game!
            Please choose an action: 
            1 - Play; 
            2 - Check history; 
            3 - Clean history; 
            0 - Exit''',
        "enter_command": "Your input: ",
        "enter_first_name": "Please enter Player 1 name",
        "enter_second_name": "Please enter Player 2 name",
        "first_player_turn": "%s, your turn. Please enter cell coordinate to set X",
        "second_player_turn": "%s, your turn. Please enter cell coordinate to set O",
        "replay_decision": "Would you like to replay current game (Yes/No)?"
    }

    def process_user_command(self):
        if self.current_state == "game_ready":
            command = self.print_message(self.current_state)
            if command == "0":
                return False
            self.choose_action(command)
            return True

        elif self.current_state == "enter_first_name":
            first_player = self.print_message(self.current_state)
            second_player = self.print_message("enter_second_name")
            self.game_setup(first_player, second_player)
            return True

        elif self.current_state in ("first_player_turn", "second_player_turn"):
            while True:
                command = self.print_message(self.current_state).upper()
                try:
                    self.validate_coordinate(command)
                except WrongCommandEx as ex:
                    print(ex)
                else:
                    self.player_turn(command)
                    return True

        elif self.current_state == "replay_decision":
            command = self.print_message(self.current_state)
            self.replay_game(command)
            return True

    def print_message(self, state):
        if state == "first_player_turn":
            print(self.MESSAGES[state] % self.first_player_name)
        elif state == "second_player_turn":
            print(self.MESSAGES[state] % self.second_player_name)
        else:
            print(self.MESSAGES[state])
        command = input(self.MESSAGES["enter_command"])
        return command

    def choose_action(self, action):
        if action == "1":
            self.current_state = "enter_first_name"
        elif action == "2":
            self.check_history()
            self.current_state = "game_ready"
        elif action == "3":
            self.clean_history()
            self.current_state = "game_ready"
        else:
            print(self.MESSAGES["error"])
            self.current_state = "game_ready"

    def check_history(self):
        print("Here is wins history:")
        self.logger.read_log()

    def clean_history(self):
        self.logger.clean_log()
        print("History was cleared")

    def game_setup(self, first_player_name, second_player_name):
        self.clean_battlefield()
        self.turns_counter = 0
        self.current_state = "first_player_turn"
        self.first_player_name = first_player_name
        self.second_player_name = second_player_name
        self.print_battlefield()
        print("Rules: Player %s uses X, played %s uses O. X goes first!" % (first_player_name, second_player_name))

    def replay_game(self, command):
        if command.lower() == "yes":
            self.game_setup(self.first_player_name, self.second_player_name)
        elif command.lower() == "no":
            self.current_state = "game_ready"

    def player_turn(self, coordinate):
        character = None
        if self.current_state == "first_player_turn":
            character = "X"
        else:
            character = "O"

        # converting user's entered coordinate to list coordinate
        line = coordinate[0]
        cell = coordinate[1]
        if line == "A":
            line = 0
        elif line == "B":
            line = 1
        elif line == "C":
            line = 2
        cell = int(cell) - 1

        try:
            if self.battlefield[line][cell] in ("X", "O"):
                raise CellNotAvailableEx()
            else:
                self.battlefield[line][cell] = character
                if self.current_state == "first_player_turn":
                    self.current_state = "second_player_turn"
                elif self.current_state == "second_player_turn":
                    self.current_state = "first_player_turn"
                self.turns_counter += 1
                self.print_battlefield()
                self.winner_decision()
        except CellNotAvailableEx as ex:
            print(ex)

    # check if entered cell coordinate is valid
    def validate_coordinate(self, command):
        if len(command) != 2:
            raise WrongCommandEx
        elif command[0] not in ("A", "B", "C") or command[1] not in ("1", "2", "3") or len(command) != 2:
            raise WrongCommandEx

    def winner_decision(self):
        is_winner = False
        message = None
        if self.winner_check("X"):
            message = "%s wins!" % self.first_player_name
            is_winner = True
        elif self.winner_check("O"):
            message = "%s wins!" % self.second_player_name
            is_winner = True
        if is_winner:
            self.logger.write_log(message)
            self.clean_battlefield()
            self.current_state = "replay_decision"
        elif self.turns_counter == 9:
            message = "There is a draw"
            self.clean_battlefield()
            self.logger.write_log(message)
            self.current_state = "replay_decision"

    def winner_check(self, character):
        size = len(self.battlefield)
        cells_to_check = []

        # check horizontal lines
        for i in range(size):
            if all([x == character for x in self.battlefield[i]]):
                return True

        # check vertical lines
        for i in range(size):
            for j in range(size):
                cells_to_check.append(self.battlefield[j][i])
            if all([x == character for x in cells_to_check]):
                return True
            cells_to_check.clear()
        cells_to_check.clear()

        # check diagonal line (left to right)
        for i in range(size):
            cells_to_check.append(self.battlefield[i][i])
        if all([x == character for x in cells_to_check]):
            return True
        cells_to_check.clear()

        # check diagonal line (right to left)
        i_start = 0
        j_start = size - 1
        while i_start < size:
            cells_to_check.append(self.battlefield[i_start][j_start])
            i_start += 1
            j_start -= 1
        if all([x == character for x in cells_to_check]):
            cells_to_check.clear()
            return True
        cells_to_check.clear()
        return False

    def clean_battlefield(self):
        self.battlefield = [['A1', 'A2', 'A3'], ['B1', 'B2', 'B3'], ['C1', 'C2', 'C3']]

    def print_battlefield(self):
        array = self.battlefield
        print("Battlefield: ")
        for i in range(len(array)):
            for j in range(len(array[i])):
                print(array[i][j], end=' ')
            print()


# =====================================================================================================================

# created decorator to log total session time
def timer(func):
    def wrapper():
        start = time.time()
        func()
        end = time.time()
        Logs.write_log("Total session time is: %d seconds" % (end - start))

    return wrapper


@timer
def main():
    game = TicTacToe()
    while True:
        if not game.process_user_command():
            break


if __name__ == "__main__":
    main()
