import os, sys


class GameBoard:
    # set some related constant
    MOVING_SCORE = -1
    WIN_SCORE = 500
    EATEN_SCORE = -500
    FOOD_SCORE = 10

    def __init__(self):
        self.foods_pos = set()      # record the foods position
        self.player_pos = (0, 0)    # the initial position of player
        self.ghosts_name = []       # collect the ghost name
        self.ghosts_pos = dict()    # get the corresponding position of ghosts by the name
        self.player_eaten = False   # the player is live
        self.move_count = 0         # count the total moves
        self.scores = 0             # total scores through the game

        self.width = 0
        self.height = 0
        self.board = []  # basic parameters of game board

    def __str__(self):
        rv = ''
        for line in self.board:
            rv += ''.join(line) + '\n'
        return rv

    def check_won(self):
        return len(self.foods_pos) == 0

    def check_lost(self):
        return self.player_eaten

    @staticmethod
    def generate_board(board):
        # get the board concrete string
        gb = GameBoard()

        # set the basic property of the board
        gb.height = len(board)
        gb.width = len(board[0])
        gb.board = []
        # enumerate each position on the board to check the contents
        for x in range(gb.height):
            line = []
            for y in range(gb.width):
                char = board[x][y]
                if char == 'W' or char == 'X' or char == 'Y' or char == 'Z':
                    # find the ghost
                    gb.ghosts_name.append(char)
                    gb.ghosts_pos[char] = (x, y)
                elif char == 'P':
                    # find the player on the board
                    gb.player_pos = (x, y)
                elif char == '.':
                    # find the new food
                    gb.foods_pos.add((x, y))
                line.append(char)
            gb.board.append(line)
        gb.scores = 0
        gb.move_count = 0
        gb.ghosts_name = sorted(gb.ghosts_name)
        return gb

    # get the next character who need to move
    def next_moving_character(self):
        selected = (['P'] + self.ghosts_name)[self.move_count % (1 + len(self.ghosts_name))]
        return selected

    def next_possible_directions(self, name):
        # get the position of the character
        x, y = self.get_pos_character(name)

        # get the next position of character
        next_pos = [('E', (x, y + 1)), ('N', (x - 1, y)), ('S', (x + 1, y)), ('W', (x, y - 1))]

        # filter the invalid position
        rv = []
        for each in next_pos:
            new_x, new_y = each[1]
            if self.board[new_x][new_y] == '%':
                continue
            elif name in ['X', 'W', 'Y', 'Z']:
                flag = True
                for key, value in self.ghosts_pos.items():
                    if value == each[1]:
                        flag = False
                if not flag:
                    continue
            rv.append(each)
        return rv

    def make_move(self, name, direction):
        if direction is None:
            self.move_count += 1
            return
        if name in self.ghosts_name:
            # update the position of ghost at once
            self.ghosts_pos[name] = direction[1]
            if direction[1] == self.player_pos:
                self.player_eaten = True
                self.scores += self.EATEN_SCORE
        elif name == 'P':
            # the moving character is player
            new_pos = direction[1]
            for key, value in self.ghosts_pos.items():
                if new_pos == value:
                    # encounter a ghost
                    self.player_eaten = True
                    self.scores += self.EATEN_SCORE
            if new_pos in self.foods_pos:
                # encounter a new food
                self.scores += self.FOOD_SCORE
                self.foods_pos.remove(new_pos)

                # check whether food left
                if len(self.foods_pos) == 0:
                    self.scores += self.WIN_SCORE
            # pay for the onestep move
            self.scores += self.MOVING_SCORE
            # update the position of player
            self.player_pos = new_pos
        # update the total count of move
        self.move_count += 1
        self.update_board()

    def update_board(self):
        for x in range(self.height):
            for y in range(self.width):
                if self.board[x][y] != '%':
                    self.board[x][y] = ' '
        # render the player in the board
        self.board[self.player_pos[0]][self.player_pos[1]] = 'P'

        # render the food on the board
        for each in self.foods_pos:
            x, y = each
            self.board[x][y] = '.'

        # render the ghost on the board
        for name, pos in self.ghosts_pos.items():
            x, y = pos
            self.board[x][y] = name

    # according to the name get its corresponding position
    def get_pos_character(self, name):
        if name == 'P':
            return self.player_pos
        elif name in self.ghosts_name:
            return self.ghosts_pos[name]
        else:
            return None


def read_layout_problem(file_path):
    # read the problem from the file
    seed, board, size = 0, [], ()
    with open(file_path, 'r', encoding='utf-8') as file:
        line = file.readline().strip()
        seed = int(line.split(' ')[1])
        height, width = 0, 0
        for line in file:
            board.append(line.strip())
            height += 1
        width = len(board[0])
        size = (height, width)

    # generate the problem in (seed, size, board) format
    prob = (seed, size, board)

    # return back the problem
    return prob


if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases', 'p' + problem_id, test_case_id + '.prob'))
    else:
        print('Error: I need exactly 2 arguments!')
