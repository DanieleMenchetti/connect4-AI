# connect4-AI
AI BOT for Connect 4 game with Mini-Max algorithm and alpha-beta pruning.

## Info
The heuristic choosen makes this BOT a defensive player rather than an aggressive one.

In fact, as soon as the BOT notices a line made up of two adjacent opponent tokens, \
he attributes a high value to the insertion of his own token capable of countering the opponent's line.

## Usage
**CLI**: run .py in a terminal.

**AI-only**:
1. Create a file named 'input.txt' with the following data:\
player_turn\
tree_depth\
board

    * player_turn is a char ('X', 'O').
    * tree_depth is an int (0, ..., 42).
    * board is a the board structure that must be in this format:\
    .|.|.|.|.|.|.|\
    .|.|.|.|.|.|.|\
    .|.|.|.|.|.|.|\
    .|.|.|.|.|.|.|\
    .|.|X|.|.|.|.|\
    .|X|X|O|O|O|.|



2. run .py

3. The output will show:
* N={0, ..., 6}: it means that the player choosen should put the token in the column N.
* E: error found with the input file, with message related.
* X: victory for the X player.
* O: victory for the O player.
* .: tie.

## Author
[Daniele Menchetti](https://github.com/danielemenchetti)
