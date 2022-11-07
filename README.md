# YAHTZEE
---

> The dice poker game in Python for ANSI terminals

![Screenshot](https://github.com/oliverbacsi/Yahtzee/blob/main/images/0-main.png)

**Usage**:
```
yahtzee.py
```

* All graphics are ANSI powered and controls are read from command line with "input"
* The game is turn based, players can make their scores sequentially
* active player is highlighted
* Each player has 3 possibilities to roll the dice
* In the first roll all dice have to be rolled, in the next 2 it's possible to keep some
* Dice in the "ROLL" area will be rolled, and in the "KEEP" area they are kept fixed
* After rolling the results can be written in any unoccupied cell of the score board
* If the score board is full, the game ends. Whoever has the most points wins the game

![Screenshot](https://github.com/oliverbacsi/Yahtzee/blob/main/images/1-help.png)

**Game Rules**:

Any achieved combination (which are similar to those of Poker) can be written in any cell of the score board.
If the numbers of the dice do not match the combination, zero points are added to the scoreboard (value is indicated with red).
If the dice fulfill the necessary combination, the value displayed in green will be added to the scoreboard.
The combination "Yahtzee" does not exist in Poker, as it means five equal numbers.
if the player already has a Yahtzee, and any other combination is achieved by five equal numbers, then Extra Yahtzee's are added automatically.
Extra Yahtzee does not apply if the player does not have a Yahtzee yet.
If the subtotal score of the first 6 rows of the scoreboard (number of 1's to number of 6's) adds up to at least 63, then a bonus of 35 points is added.
At the end of the playing there is a statistics shown from all the games, based on the number of won games and number of total collected points.

![Screenshot](https://github.com/oliverbacsi/Yahtzee/blob/main/images/2-scores.png)

**Known Bugs**:

* [ ] If the last player achieves the Subtotal Bonus (35pts if the sum of the first 6 rows is > 62) in the last ever round of a game, then by some stupid reason only the collected points are added to his/her score, but not the 35pts extra bonus. So the guy in the rightmost column might get 35pts less than deserved...
