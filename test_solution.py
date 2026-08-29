"""
Run it: python3 test_solution.py   (or: pytest)
"""

from main import REEL_TOUR, START
from solution import COLS, ROWS, is_valid_tour, jumps_from, squares, starts_that_work, tour


def test_it_finds_a_real_tour():
    path = tour(START)
    assert is_valid_tour(path)
    assert len(path) == ROWS * COLS == 20
    assert len(set(path)) == 20


def test_every_hop_is_a_legal_knight_move():
    path = tour(START)
    assert all(b in jumps_from(a) for a, b in zip(path, path[1:]))


def test_it_is_the_tour_the_reel_animates():
    # The tie-break order in JUMPS decides which of several valid tours comes out. If it
    # ever changes, the video and the repo would show different routes without saying so.
    assert tour(START) == REEL_TOUR


def test_warnsdorff_is_a_heuristic_not_a_guarantee():
    # Half the starting squares strand the knight. The rule is a very good guess, not a
    # proof, and `tour` returns None rather than pretending otherwise.
    works = starts_that_work()
    assert 0 < len(works) < ROWS * COLS
    assert START in works
    assert len(works) == 10


def test_a_four_by_four_board_has_no_tour_from_anywhere():
    # Not a failure of the rule — a knight's tour on 4x4 does not exist at all.
    assert all(tour(s, 4, 4) is None for s in squares(4, 4))


def test_it_is_deterministic():
    assert tour(START) == tour(START)


if __name__ == '__main__':
    passed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith('test_'):
            fn()
            print(f'  ok  {name}')
            passed += 1
    print(f'\n{passed} tests passed\n')
