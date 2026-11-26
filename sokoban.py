
from collections import deque


LEVELS = [
    [
        "#########",
        "#       #",
        "#  .    #",
        "#  $    #",
        "#  @    #",
        "#       #",
        "#########",
    ],
    [
        "##########",
        "#        #",
        "#  ..    #",
        "#  $$    #",
        "#   @    #",
        "#        #",
        "##########",
    ],
    [
        "###########",
        "#         #",
        "#         #",
        "#    #    #",
        "#    #    #",
        "#  . # $  #",
        "#      @  #",
        "###########",
    ],
    [
        "#########",
        "# .   . #",
        "#       #",
        "# $ # $ #",
        "#   #   #",
        "#   @   #",
        "#########",
    ],
]

DIRECTIONS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}


def load_level(rows):
    walls, goals, boxes = set(), set(), set()
    player = None
    width = len(rows[0])
    if not rows or any(len(row) != width for row in rows):
        raise ValueError("マップの行の長さをそろえてください")
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            pos = (x, y)
            if ch == "#":
                walls.add(pos)
            elif ch in ".+*":
                goals.add(pos)
            if ch in "$*":
                boxes.add(pos)
            if ch in "@+":
                if player is not None:
                    raise ValueError("プレイヤーは1人にしてください")
                player = pos
    if player is None or not boxes or len(boxes) != len(goals):
        raise ValueError("プレイヤー1人、箱とゴールは同じ数が必要です")
    return {"walls": walls, "goals": goals, "boxes": boxes, "player": player,
            "width": width, "height": len(rows), "moves": 0, "pushes": 0, "history": []}


def is_deadlocked(game, box):
    if box in game["goals"]:
        return False
    x, y = box
    blocked_left = not inside(game, (x - 1, y)) or (x - 1, y) in game["walls"]
    blocked_right = not inside(game, (x + 1, y)) or (x + 1, y) in game["walls"]
    blocked_up = not inside(game, (x, y - 1)) or (x, y - 1) in game["walls"]
    blocked_down = not inside(game, (x, y + 1)) or (x, y + 1) in game["walls"]
    return ((blocked_left or blocked_right) and (blocked_up or blocked_down))


def draw_game(game, move_limit=None):
    print("\n" * 2 + "=== SOKOBAN ===")
    print("# 壁   . ゴール   $ 箱   @ プレイヤー   * ゴール上の箱")
    for y in range(game["height"]):
        line = ""
        for x in range(game["width"]):
            pos = (x, y)
            if pos == game["player"]:
                line += "+" if pos in game["goals"] else "@"
            elif pos in game["boxes"]:
                line += "*" if pos in game["goals"] else "$"
            elif pos in game["walls"]:
                line += "#"
            elif pos in game["goals"]:
                line += "."
            else:
                line += " "
        print(line)
    if any(is_deadlocked(game, pos) for pos in game["boxes"]):
        print("警告: ゴール外で箱が角にはまりました。Uで戻すかRで再開できます。")
    print(f"移動回数: {game['moves']} | 押した回数: {game['pushes']}")
    if move_limit is not None:
        print(f"手数上限: {move_limit} | 残り: {max(0, move_limit - game['moves'])}")
    print("WASD: 移動 / U: 一手戻す / H: ヒント / R: リスタート / Q: 終了")


def inside(game, pos):
    return 0 <= pos[0] < game["width"] and 0 <= pos[1] < game["height"]


def move_player(game, key):
    if key not in DIRECTIONS:
        return False
    dx, dy = DIRECTIONS[key]
    x, y = game["player"]
    target = (x + dx, y + dy)
    if not inside(game, target) or target in game["walls"]:
        return False
    pushed_to = None
    if target in game["boxes"]:
        pushed_to = (target[0] + dx, target[1] + dy)
        if (not inside(game, pushed_to) or pushed_to in game["walls"]
                or pushed_to in game["boxes"]):
            return False
    game["history"].append((game["player"], game["boxes"].copy(), game["pushes"]))
    if pushed_to is not None:
        game["boxes"].remove(target)
        game["boxes"].add(pushed_to)
        game["pushes"] += 1
    game["player"] = target
    game["moves"] += 1
    return True


def undo(game):
    if game["history"]:
        game["player"], game["boxes"], game["pushes"] = game["history"].pop()
        game["moves"] -= 1


def is_cleared(game):
    return game["boxes"] == game["goals"]


def is_move_limit_reached(game, move_limit):
    return move_limit is not None and game["moves"] >= move_limit


def find_hint(game):
    if is_cleared(game):
        return None
    initial_state = (game["player"], frozenset(game["boxes"]))
    queue = deque([(initial_state, None)])
    visited = {initial_state}
    while queue:
        (player, boxes), first_move = queue.popleft()
        for key, (dx, dy) in DIRECTIONS.items():
            target = (player[0] + dx, player[1] + dy)
            if not inside(game, target) or target in game["walls"]:
                continue
            next_boxes = boxes
            if target in boxes:
                pushed_to = (target[0] + dx, target[1] + dy)
                if (not inside(game, pushed_to) or pushed_to in game["walls"]
                        or pushed_to in boxes):
                    continue
                next_boxes = frozenset((boxes - {target}) | {pushed_to})
            state = (target, next_boxes)
            if state in visited:
                continue
            if next_boxes == game["goals"]:
                return first_move or key
            visited.add(state)
            queue.append((state, first_move or key))
    return None


def choose_start_level():
    while True:
        print("開始するステージを選んでください:")
        for index in range(len(LEVELS)):
            print(f"{index + 1}: ステージ {index + 1}")
        choice = input("番号を入力 (Q: 終了) > ").strip().lower()
        if choice == "q":
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(LEVELS):
            return int(choice) - 1
        print("有効なステージ番号を入力してください。")


def choose_move_limit():
    while True:
        choice = input("手数上限チャレンジを有効にしますか？ (Y/N) > ").strip().lower()
        if choice in ("n", "no"):
            return None
        if choice in ("y", "yes"):
            break
        print("YまたはNを入力してください。")
    while True:
        limit = input("このステージの手数上限を入力してください > ").strip()
        if limit.isdigit() and int(limit) > 0:
            return int(limit)
        print("1以上の整数を入力してください。")


def format_level_summary(level_number, game):
    return (
        f"ステージ{level_number}の結果: "
        f"移動回数 {game['moves']}回 / 押した回数 {game['pushes']}回"
    )


def main():
    level_index = choose_start_level()
    if level_index is None:
        return
    move_limit = choose_move_limit()
    game = load_level(LEVELS[level_index])
    while True:
        draw_game(game, move_limit)
        if is_cleared(game):
            print("クリア！")
            print(format_level_summary(level_index + 1, game))
            level_index += 1
            if level_index == len(LEVELS):
                print("全ステージクリア！")
                break
            input("Enterを押して次へ...")
            game = load_level(LEVELS[level_index])
            continue
        if is_move_limit_reached(game, move_limit):
            print("手数上限に達しました。Uで一手戻すか、Rでやり直してください。")
        key = input("操作 > ").strip().lower()[:1]
        if key == "q":
            break
        if key == "r":
            game = load_level(LEVELS[level_index])
        elif key == "u":
            undo(game)
        elif key == "h":
            hint = find_hint(game)
            if hint is None:
                message = "この盤面はすでにクリア済みです。" if is_cleared(game) else "解けるルートが見つかりません。"
                print(message)
            else:
                directions = {"w": "上", "a": "左", "s": "下", "d": "右"}
                print(f"ヒント: {hint.upper()} ({directions[hint]}) へ進んでください。")
        elif not is_move_limit_reached(game, move_limit):
            move_player(game, key)


if __name__ == "__main__":
    main()
