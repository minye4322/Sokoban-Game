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
| 1 | 1 move | 2–3 moves |
| 2 | 4 moves | 5–8 moves |
| 3 | Up to 14 moves | 15–21 moves |
| 4 | Up to 13 moves | 14–20 moves |
| 5 | 4 moves | 5–8 moves |
| 6 | Up to 13 moves | 14–20 moves |

Any completed stage earns at least one star. A lower move count earns a higher rating.

## Symbols

- `#` Wall
- `.` Goal
- `$` Box
- `@` Player
- `*` Box on a goal
- `+` Player on a goal

---

# 倉庫番（Sokoban）

Pythonで作成したターミナル用の倉庫番ゲームです。箱を押して、すべてのゴールに置くとステージクリアです。

## 起動方法

```powershell
python sokoban.py
```

外部ライブラリのインストールは不要です。ゲームはステージ1から始まり、全6ステージを順番に進みます。

## 操作方法

| キー | 操作 |
|---|---|
| W / A / S / D | 上 / 左 / 下 / 右へ移動 |
| U | 1手戻す |
| H | 最短クリアルートの次の一手を表示 |
| R | 現在のステージをやり直す |
| Q | ゲームを終了 |

ターミナルでキーを入力し、Enterを押してください。

## ゲームの機能

- 壁、ゴール、箱のある全6ステージ。
- 移動回数と箱を押した回数を表示します。Undoすると箱押し回数も元に戻ります。
- 箱が壁際の角にはまった場合、警告を表示します。
- 任意で手数制限チャレンジを選べます。手数上限はステージごとにあらかじめ設定されています。
  - ステージ1：6手
  - ステージ2：12手
  - ステージ3：32手
  - ステージ4：30手
  - ステージ5：12手
  - ステージ6：30手
- ステージクリア時に、移動回数に応じて1〜3個の星を表示します。

| ステージ | ★★★の条件 | ★★の条件 |
|---|---:|---:|
| 1 | 1手 | 3手以内 |
| 2 | 4手 | 5〜8手 |
| 3 | 14手以内 | 15〜21手 |
| 4 | 13手以内 | 14〜20手 |
| 5 | 4手 | 5〜8手 |
| 6 | 13手以内 | 14〜20手 |

どのステージも、クリアすると最低1個の星を獲得できます。移動回数が少ないほど評価が高くなります。

## 画面の記号

- `#` 壁
- `.` ゴール
- `$` 箱
- `@` プレイヤー
- `*` ゴール上の箱
- `+` ゴール上のプレイヤー
