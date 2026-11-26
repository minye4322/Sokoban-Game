# Sokoban

A terminal-based Sokoban game written in Python. Push every box onto a goal to clear each stage.

## Run

```powershell
python sokoban.py
```

No third-party packages are required. The game starts at Stage 1 and proceeds through all six stages in order.

## Controls

| Key | Action |
|---|---|
| W / A / S / D | Move up / left / down / right |
| U | Undo the previous move |
| H | Show the next move on a shortest solution path |
| R | Restart the current stage |
| Q | Quit |

Enter each move in the terminal and press Enter.

## Features

- Six stages with walls, goals, and boxes.
- Move and box-push counters. Undo also restores the push count.
- A warning when a box is stuck in a wall corner.
- Optional challenge mode with preset move limits:
  - Stage 1: 6 moves
  - Stage 2: 12 moves
  - Stage 3: 32 moves
  - Stage 4: 30 moves
  - Stage 5: 12 moves
  - Stage 6: 30 moves
- A one-to-three-star rating after each cleared stage, based on moves:

| Stage | 3 stars | 2 stars |
|---|---:|---:|
| 1 | 1 move | Up to 3 |
| 2 | 4 moves | Up to 8 |
| 3 | Up to 14 | Up to 21 |
| 4 | Up to 13 | Up to 20 |
| 5 | 4 moves | Up to 8 |
| 6 | Up to 13 | Up to 20 |

Any completed stage earns at least one star. A lower move count earns a higher rating.

## Symbols

- `#` Wall
- `.` Goal
- `$` Box
- `@` Player
- `*` Box on a goal
- `+` Player on a goal
