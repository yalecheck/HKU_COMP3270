import sys, random, grader, parse
from parse import GameBoard

def random_play_single_ghost(problem):
    #Your p1 code here
    seed, size, board = problem
    solution = ''

    # select the random seed to generate random integer
    random.seed(seed, version=1)

    gm = GameBoard.generate_board(board)
    # print out some hint message
    solution += f"seed: {seed}\n"
    solution += f"{gm.move_count}\n"
    solution += str(gm)

    # simulate the game
    while True:
        moving_figure = gm.next_moving_character()
        possible_directions = gm.next_possible_directions(moving_figure)
        picked_direction = random.choice(possible_directions)
        gm.make_move(moving_figure, picked_direction)

        # add some hint message
        solution += f'{gm.move_count}: {moving_figure} moving {picked_direction[0]}\n'
        solution += str(gm)
        solution += f'score: {gm.scores}\n'

        # check whether the game is over
        if gm.check_won():
            solution += 'WIN: Pacman'
            break
        elif gm.check_lost():
            solution += 'WIN: Ghost'
            break

    return solution

if __name__ == "__main__":
    try:
        test_case_id = int(sys.argv[1])
    except:
        test_case_id = -6
    problem_id = 1
    grader.grade(problem_id, test_case_id, random_play_single_ghost, parse.read_layout_problem)