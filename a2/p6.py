import sys, parse
import time, os, copy
import random
from parse import GameBoard

def reflex_function(gm, direction):
    new_pos = direction[1]
    for key, value in gm.ghosts_pos.items():
        if new_pos == value:
            return -1000000000
    if new_pos in gm.foods_pos:
        # encounter a new food
        return 1000000000 + random.randint(1, 10)
    s = gm.scores
    # we think the more closed to ghost is more dangerous
    ghost_distances, food_distances = [], []
    for each in gm.foods_pos:
        food_distances.append(abs(new_pos[0] - each[0]) + abs(new_pos[1] - each[1]))
    for key, each in gm.ghosts_pos.items():
        ghost_distances.append(abs(new_pos[0] - each[0]) + abs(new_pos[1] - each[1]))

    s += random.randint(10, 15) * min(ghost_distances) - random.randint(2, 3) * min(food_distances)
    return s
def expectimax_multiple_ghost(problem, k, verbose):
    #Your p6 code here
    seed, size, board = problem
    solution = ''
    winner = 'Ghost'

    # select the random seed to generate random integer
    # random.seed(seed, version=1)

    gm = GameBoard.generate_board(board)
    # print out some hint message
    solution += f"seed: {seed}\n"
    solution += f"{gm.move_count}\n"
    solution += str(gm)

    # simulate the game
    while True:
        # solution = ''
        moving_figure = gm.next_moving_character()
        possible_directions = gm.next_possible_directions(moving_figure)
        if moving_figure == 'P':
            values = []
            for each in possible_directions:
                values.append((reflex_function(gm, each), each))
            _, picked_direction = max(values, key=lambda x: x[0])
        else:
            if possible_directions:
                picked_direction = random.choice(possible_directions)
            else:
                picked_direction = None
        gm.make_move(moving_figure, picked_direction)

        # add some hint message
        if picked_direction is None:
            solution += f'{gm.move_count}: {moving_figure} moving \n'
        else:
            solution += f'{gm.move_count}: {moving_figure} moving {picked_direction[0]}\n'
        solution += str(gm)
        solution += f'score: {gm.scores}\n'

        # print(solution)

        # check whether the game is over
        if gm.check_won():
            solution += 'WIN: Pacman'
            winner = 'Pacman'
            break
        elif gm.check_lost():
            solution += 'WIN: Ghost'
            break

    return solution, winner

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    file_name_problem = str(test_case_id)+'.prob'
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id))
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:',test_case_id)
    print('k:',k)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = expectimax_multiple_ghost(copy.deepcopy(problem), k, verbose)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)