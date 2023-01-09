import copy
from typing import Optional
from twothousand_forty_eight.board.tile import Tile
from twothousand_forty_eight.direction import Direction


class Board:
    width: int
    height: int
    tiles: list[list[Tile]]

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.tiles = create_tiles(width, height)

    def __str__(self) -> str:
        out = ""
        for y in range(0, self.height):
            for x in range(0, self.width):
                tile = self.tiles[y][x]
                out += f"{tile.value}\t"
            out += "\n"
        return out

    def set_tile(self, x: int, y: int, val: int):
        self.tiles[y][x] = Tile(x, y, val, None)

    # Get the tiles that exist and which's values are non-zero
    def get_occupied_tiles(self) -> list[Tile]:
        out: list[Tile] = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                tile = self.tiles[y][x]
                if tile.value != 0:
                    out.append(tile)
        return out

    def get_all_tiles(self) -> list[Tile]:
        out: list[Tile] = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                tile = self.tiles[y][x]
                out.append(tile)
        return out


def create_tiles(width: int, height: int) -> list[list[Tile]]:
    tiles = []
    for y in range(0, height):
        col = []
        for x in range(0, width):
            col.append(Tile(x, y, 0, None))
        tiles.append(col)
    return tiles


def get_closest_tile(
    t: Tile,
    viable_tiles: list[Tile],
    dir: Direction,
    mask: int,
) -> Optional[Tile]:
    dir_x = dir.get_x()
    dir_y = dir.get_y()

    closest = None
    closest_dist: int = 99999999999999999

    nearest_block: int = 99999999999999999

    move_is_vertical = dir_y == 0

    for i in viable_tiles:
        condition = t.x < i.x if dir_x > 0 else t.x > i.x if move_is_vertical else t.y < i.y if dir_y > 0 else t.y > i.y

        if (t.y == i.y if move_is_vertical else t.x == i.x) and condition:
            distance = i.x-t.x if dir_x > 0 else t.x - \
                i.x if move_is_vertical else i.y - t.y if dir_y > 0 else t.y - i.y

            if distance != 0 and distance < closest_dist:
                recursed = get_closest_tile(i, viable_tiles, dir, mask)
                r = recursed
                if r != None:
                    if r.value == i.value and r.merged_from == None:
                        # Let this tile merge with the one in the direction of the move
                        nearest_block = distance
                    else:
                        closest = i
                        closest_dist = distance
                else:
                    closest = i
                    closest_dist = distance

    if nearest_block < closest_dist:
        return None

    return closest


def get_farthest_tile(
    t: Tile,
    all_tiles: list[Tile],
    dir: Direction,
    mask: int,
) -> Optional[Tile]:
    dir_x = dir.get_x()
    dir_y = dir.get_y()

    farthest = None
    farthest_dist: int = -99999999999999999

    nearest_block: int = 99999999999999999

    move_is_vertical = dir_y == 0

    for i in all_tiles:
        condition = (t.x < i.x if dir_x > 0 else t.x > i.x) if move_is_vertical else (
            t.y < i.y if dir_y > 0 else t.y > i.y)
        if (t.y == i.y if move_is_vertical else t.x == i.x) and condition:
            distance = i.x-t.x if dir_x > 0 else t.x - \
                i.x if move_is_vertical else i.y - t.y if dir_y > 0 else t.y - i.y

            if distance != 0 and distance > farthest_dist and i.value == mask:
                farthest = i
                farthest_dist = distance
            elif distance != 0 and i.value != mask and distance < nearest_block:
                nearest_block = distance
    if nearest_block < farthest_dist:
        return None
    return farthest


MAX_MOVE_CHECKS = 256


class MoveResult:
    possible: bool
    tiles: list[list[Tile]]
    score_gain: int

    def __init__(self, possible: bool, tiles: list[list[Tile]], score_gain: int) -> None:
        self.possible = possible
        self.tiles = tiles
        self.score_gain = score_gain


def check_move(board: Board, dir: Direction) -> MoveResult:
    global MAX_MOVE_CHECKS
    if dir == Direction.END:
        return MoveResult(
            possible=True,
            tiles=board.tiles,
            score_gain=0,
        )

    was_changed = False

    # copy the current board and unset merged_from
    tiles = copy.deepcopy(board.tiles)
    for t in board.get_occupied_tiles():
        t2 = t
        t2.merged_from = None
        tiles[t.y][t.x] = t2

    score = 0

    # Merge
    ids_checked_for_merge: list[int] = []
    for _ in range(MAX_MOVE_CHECKS):
        b = Board(board.width, board.height)
        b.tiles = tiles
        occupied_tiles = b.get_occupied_tiles()
        viable_tiles: list[Tile] = list(filter(
            lambda t: t.merged_from == None, occupied_tiles))
        t = next((t for t in viable_tiles if not t.id in ids_checked_for_merge), None)
        if t != None:
            closest = get_closest_tile(t, occupied_tiles, dir, t.value)
            if closest != None:
                if t.value == closest.value and closest.merged_from == None:
                    tiles[t.y][t.x] = Tile(t.x, t.y, 0, None)

                    merged = Tile(closest.x, closest.y,
                                  closest.value * 2, None)
                    merged.merged_from = (t.id, closest.id)

                    score += merged.value
                    tiles[closest.y][closest.x] = merged
                    was_changed = True

            ids_checked_for_merge.append(t.id)
        else:
            break

    # Slide
    moved_tiles:  list[int] = []
    for _ in range(MAX_MOVE_CHECKS):
        b = Board(board.width, board.height)
        b.tiles = tiles
        tiles_post = b.get_occupied_tiles()

        t = next((t for t in tiles_post if not t.id in moved_tiles), None)
        if t != None:
            all_tiles = b.get_all_tiles()
            dir_to_use = dir
            farthest_free = get_farthest_tile(t, all_tiles, dir_to_use, 0)

            if farthest_free != None:
                new_tile: Tile = copy.deepcopy(t)
                new_tile.x = farthest_free.x
                new_tile.y = farthest_free.y

                tiles[t.y][t.x] = Tile(t.x, t.y, 0, None)
                tiles[farthest_free.y][farthest_free.x] = new_tile

                was_changed = True
                moved_tiles = []
            else:
                moved_tiles.append(t.id)
        else:
            break

    return MoveResult(
        possible=was_changed,
        tiles=tiles,
        score_gain=score,
    )
