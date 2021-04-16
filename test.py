import random


def main():
    # Def input
    sum_elements = 100

    this_values = [5, 10, 20, 5, 0, 30, 5, 10, 15]
    moves = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, 10000):
        ind_move = test_once(sum_elements, this_values)
        moves[ind_move] += 1

    r = ""
    for move in moves:
        r += str(move / 100) + ", "

    print(r)


def test_once(sum_elements, this_values):
    rand_int = random.randint(0, sum_elements - 1)

    ind_move = 0
    sum_not_chosen = 0
    chosen = sum_not_chosen > rand_int
    while ind_move < len(this_values) and not chosen:
        sum_not_chosen += this_values[ind_move]
        chosen = sum_not_chosen > rand_int
        ind_move += 1

    ind_move -= 1
    return ind_move


if __name__ == '__main__':
    main()
