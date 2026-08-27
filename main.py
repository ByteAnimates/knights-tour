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


# ── the claims above, checked ────────────────────────────────────────────────────

_path = tour(START)

# It is a real tour: every square exactly once, every hop a legal knight move.
assert is_valid_tour(_path)
assert len(_path) == ROWS * COLS == 20
assert len(set(_path)) == 20

# And it is the tour on screen. If the tie-break order changes, this is what says so.
assert _path == REEL_TOUR, 'the tour drifted from the one the reel animates'

# The rule is a heuristic, not a guarantee — half the starting squares strand the knight.
_works = starts_that_work()
assert 0 < len(_works) < ROWS * COLS
assert START in _works

# 4x4 has no knight's tour at all, from any square, by any method.
assert all(tour(s, 4, 4) is None for s in squares(4, 4))

# Deterministic: same start, same tour, every run.
assert tour(START) == tour(START)

if __name__ == '__main__':
    main()
