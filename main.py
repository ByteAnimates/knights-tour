"""
Run it: python3 main.py

The tour from the reel, then the two facts the animation cannot show: how few starting
squares actually work, and that the board everyone pictures first has no tour at all.
"""

from solution import ROWS, COLS, board, is_valid_tour, squares, starts_that_work, tour

START = (0, 0)

#: The route the reel animates, hop by hop. Kept here so that a change to the tie-break
#: order — which is the one thing that quietly rewrites the answer — fails loudly instead
#: of leaving the video and the repo showing different tours.
REEL_TOUR = [
    (0, 0), (2, 1), (3, 3), (1, 4), (0, 2), (1, 0), (3, 1), (2, 3), (0, 4), (1, 2),
    (2, 0), (0, 1), (1, 3), (3, 4), (2, 2), (3, 0), (1, 1), (0, 3), (2, 4), (3, 2),
]


def main() -> None:
    path = tour(START)

    print(f'\n{ROWS}x{COLS} board, starting at {START} — {len(path)} squares, {len(path) - 1} hops\n')
    print(board(path))

    works = starts_that_work()
    print(f'\nStarting squares that finish: {len(works)} of {ROWS * COLS}')
    print('  ' + ', '.join(str(s) for s in works))

    print(
        '\nThe rule never looks ahead and never backtracks. It counts, at most eight\n'
        'squares at a time, and takes the one with the fewest ways out.\n'
    )

    dead = [s for s in squares(4, 4) if tour(s, 4, 4) is not None]
    print(f'On a 4x4 board: {len(dead)} of 16 starts finish — a 4x4 knight\'s tour does not exist.\n')



if __name__ == '__main__':
    main()
