"""
The working version of what the reel shows.

The reel's `tour()` fits the panel because two things are named but not written: `free`,
the squares a knight could jump to that it has not stood on, and `ways`, how many onward
moves one of those squares would still have. They are written here, under the same names.

WARNSDORFF'S RULE, 1823, and it is the whole algorithm: at every hop, go to the square
with the FEWEST ways out. That is the opposite of what anyone guesses, and the reason it
works is a counting argument rather than a search. A square with one way in is a square
you will otherwise arrive at last — by which time that one way in has been used by the
route passing through it, and the square is unreachable. Taking the awkward square while
a route to it still exists is what keeps the knight from stranding itself.

There is no backtracking here and no search. Nineteen hops on this board, sixty-three on
a full chessboard, each one decided by counting at most eight squares.

IT IS A HEURISTIC, NOT A THEOREM. It is not guaranteed to complete from every square of
every board — on this 4x5 it completes from ten of the twenty starting squares, and on
4x4 it completes from none, because a 4x4 knight's tour does not exist at all. `tour()`
returns None rather than pretending otherwise, which is the branch on lines 5 and 6 of
the reel.
"""

ROWS = 4
COLS = 5

#: The eight knight moves, and the order matters more than it looks.
#:
#: `min` keeps the FIRST smallest, so when two candidate squares tie on `ways` this list
#: is what breaks the tie. Two of the nineteen hops on the default board are settled this
#: way. Reorder these pairs and you get a different — equally valid — tour, which is why
#: the route below is "a" tour and never "the" tour.
JUMPS = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))


def squares(rows: int = ROWS, cols: int = COLS) -> list[tuple[int, int]]:
    """Every square on the board, row-major."""
    return [(r, c) for r in range(rows) for c in range(cols)]


def jumps_from(sq: tuple[int, int], rows: int = ROWS, cols: int = COLS) -> list[tuple[int, int]]:
    """Every square a knight on `sq` could legally land on, ignoring what is occupied."""
    r, c = sq
    return [
        (r + dr, c + dc)
        for dr, dc in JUMPS
        if 0 <= r + dr < rows and 0 <= c + dc < cols
    ]


def tour(start: tuple[int, int], rows: int = ROWS, cols: int = COLS):
    """
    A knight's tour from `start`, or None if the rule strands the knight.

    Line for line what is on screen, with `free` and `ways` filled in.
    """
    seen = {start}
    path = [start]

    def free(sq):
        """The squares reachable from `sq` that have not been stood on."""
        return [n for n in jumps_from(sq, rows, cols) if n not in seen]

    def ways(sq):
        """How many ways out `sq` would still have once the knight were standing on it."""
        return len([n for n in free(sq) if n != sq])

    while len(path) < rows * cols:
        opts = free(path[-1])
        if not opts:
            return None
        nxt = min(opts, key=ways)
        path.append(nxt)
        seen.add(nxt)

    return path


def is_valid_tour(path, rows: int = ROWS, cols: int = COLS) -> bool:
    """Every square exactly once, and every hop a legal knight move."""
    if path is None:
        return False
    if sorted(path) != sorted(squares(rows, cols)):
        return False
    return all(b in jumps_from(a, rows, cols) for a, b in zip(path, path[1:]))


def starts_that_work(rows: int = ROWS, cols: int = COLS) -> list[tuple[int, int]]:
    """The squares you can set off from and still finish. Not all of them, ever."""
    return [s for s in squares(rows, cols) if is_valid_tour(tour(s, rows, cols), rows, cols)]


def board(path, rows: int = ROWS, cols: int = COLS) -> str:
    """The tour drawn as the order each square was stood on."""
    order = {sq: i + 1 for i, sq in enumerate(path)}
    return '\n'.join(
        '  '.join(f'{order[(r, c)]:>2}' for c in range(cols)) for r in range(rows)
    )
