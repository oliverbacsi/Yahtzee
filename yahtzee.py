#!/usr/bin/env python3
###############################
# YAHTZEE
# game of dice poker
#
# (c) DickBird Software
#

########## INIT PART ##########

import sys
from time import sleep
from random import randint

DotRelCoords :dict = dict(())
DotRelCoords["1"] = [[2, 2]]
DotRelCoords["2"] = [[1, 1], [3, 3]]
DotRelCoords["3"] = [[1, 1], [2, 2], [3, 3]]
DotRelCoords["4"] = [[1, 1], [1, 3], [3, 1], [3, 3]]
DotRelCoords["5"] = [[1, 1], [1, 3], [2, 2], [3, 1], [3, 3]]
DotRelCoords["6"] = [[1, 1], [2, 1], [3, 1], [1, 3], [2, 3], [3, 3]]
dice :dict = dict(())

if len(sys.argv) < 2:
    print("Usage: yahtzee.py <player1> [player2] [player3] [...]\n")
    exit(1)



########## CLASS PART ##########

class Player:

    def __init__(self, Name: str):
        """Create a new player object and initialize
        Parameters:
            Name (str): The player's short name"""

        self.Name :str = Name
        self.Wins :int = 0
        self.TotWonPoints :int = 0
        self.Points :dict = dict(())
        for i in ["1s", "2s", "3s", "4s", "5s", "6s", "sub", "bon", "dri", "pok", "ful", "sst", "lst", "yah", "cha", "xtr", "TOT"]:
            self.Points[i+",valid"] = False
            self.Points[i+",pts"] = 0
        self.Active :bool = False

    def __repr__(self):
        return repr((self.Name, self.Points["TOT,pts"]))

    def activate(self) -> None:
        """Set the current player status to active"""
        self.Active = True

    def passivate(self) -> None:
        """Set the current player status to not active"""
        self.Active = False

    def dispPlayerName(self, x :int, y :int, l :int, actCol :str, pasCol :str) -> None:
        """Show player name on screen as vertical text
        Parameters:
            x (int): horizontal position on screen
            y (int): vertical starting position on screen
            l (int): maximum length displayed
            actCol (str): complete ANSI escape sequence of color if player is active
            pasCol (str): complete ANSI escape sequence of color if player is not active"""
        if self.Active:
            putBox(x-2, y-1, 5, l+2, actCol)
            print(actCol + "\x1b[" + str(y+1) + ";" + str(x+1) + "H", end="")
        else:
            print(pasCol + "\x1b[" + str(y+1) + ";" + str(x+1) + "H", end="")
        if len(self.Name) < l: l = len(self.Name)
        for i in range(0,l): print(self.Name[i] + "\x1b[B\x1b[D", end="")
        print("\x1b[0m", end="")
        sys.stdout.flush()

    def dispPlayerScore(self, x: int, y:int) -> None:
        """Show the player's score table from a certain starting position
        Parameters:
            x (int): horizontal position on screen
            y (int): vertical starting position on screen"""
        print("\x1b[0m\x1b[" + str(y+1) + ";" + str(x+1) + "H", end="")
        print(str(self.Wins).rjust(3) + "\x1b[2B\x1b[3D", end="")
        if self.Active:
            actCol1 :str = "\x1b[0m\x1b[48;5;22m\x1b[38;5;119m"
            actCol2 :str = "\x1b[0m\x1b[48;5;52m\x1b[38;5;210m"
            pasCol :str = "\x1b[0m\x1b[38;5;178m"
        else:
            actCol :str = "\x1b[0m"
            pasCol :str = "\x1b[0m\x1b[38;5;94m"
        if self.Active:
            for j in ["1s", "2s", "3s", "4s", "5s", "6s"]:
                if self.Points[j+",valid"]:
                    print(pasCol + str(self.Points[j+",pts"]).rjust(3) + "\x1b[0m\x1b[B\x1b[3D", end="")
                else:
                    if game.PointsFor[j] > 0:
                        print(actCol1, end="")
                    else:
                        print(actCol2, end="")
                    print(str(game.PointsFor[j]).rjust(3) + "\x1b[0m\x1b[B\x1b[3D", end="")
        else:
            for j in ["1s", "2s", "3s", "4s", "5s", "6s"]:
                if self.Points[j+",valid"]:
                    print(pasCol + str(self.Points[j+",pts"]).rjust(3) + "\x1b[0m\x1b[B\x1b[3D", end="")
                else:
                    print(actCol + "   \x1b[0m\x1b[B\x1b[3D", end="")
        print("\x1b[B", end="")
        for j in ["sub", "bon"]:
            print(pasCol + str(self.Points[j+",pts"]).rjust(3) + "\x1b[0m\x1b[B\x1b[3D", end="")
        print("\x1b[B", end="")
        if self.Active:
            for j in ["dri", "pok", "ful", "sst", "lst", "yah", "cha"]:
                if self.Points[j+",valid"]:
                    print(pasCol + str(self.Points[j + ",pts"]).rjust(3) + "\x1b[0m\x1b[B\x1b[3D", end="")
                else:
                    if game.PointsFor[j] > 0:
                        print(actCol1, end="")
                    else:
                        print(actCol2, end="")
                    print(str(game.PointsFor[j]).rjust(3) + "\x1b[0m\x1b[B\x1b[3D", end="")
        else:
            for j in ["dri", "pok", "ful", "sst", "lst", "yah", "cha"]:
                if self.Points[j+",valid"]:
                    print(pasCol + str(self.Points[j + ",pts"]).rjust(3) + "\x1b[0m\x1b[B\x1b[3D", end="")
                else:
                    print(actCol + "   \x1b[0m\x1b[B\x1b[3D", end="")
        print("\x1b[B" + pasCol + str(self.Points["xtr,pts"]).rjust(3) + "\x1b[0m\x1b[2B\x1b[3D", end="")
        print(pasCol + str(self.Points["TOT,pts"]).rjust(3) + "\x1b[0m", end="")
        sys.stdout.flush()

    def recalcPoints(self) -> None:
        """Recalculate player's points"""
        self.Points["sub,pts"] = 0
        for i in range(1,7): self.Points["sub,pts"] += self.Points[str(i)+"s,pts"]
        self.Points["bon,pts"] = 35 if self.Points["sub,pts"] > 62 else 0
        self.Points["TOT,pts"] = 0
        for i in ["sub", "dri", "pok", "ful", "sst", "lst", "yah", "cha", "xtr"]:
            self.Points["TOT,pts"] += self.Points[i+",pts"]

    def reset(self) -> None:
        """Reset the in-game scores (except total scores) at the end of a game"""
        for i in ["1s", "2s", "3s", "4s", "5s", "6s", "sub", "bon", "dri", "pok", "ful", "sst", "lst", "yah", "cha", "xtr", "TOT"]:
            self.Points[i+",valid"] = False
            self.Points[i+",pts"] = 0
        self.Active = False

    def addWins(self) -> None:
        """I have won, so increase number of wins"""
        self.Wins += 1


class Game:

    def __init__(self, PlayerNameList: list):
        """Open a new Game object, and initialize with Players
        Parameters:
            PlayerNameList (list): List of strings (Player's names)"""
        self.Turn :int = 0
        self.Roll :int = 0
        self.CurrPlayerIDX :int = 0
        self.NumPlayers :int = 0
        self.PlayerNameList :list = PlayerNameList
        self.PlayerObjList :list = list(())
        self.ErrorMessage :str = ""
        self.Stay :bool = True
        self.SumDice :int = 0
        self.CountOf :dict = dict(())
        for i in range(1,7): self.CountOf[str(i)] = 0
        for i in self.PlayerNameList:
            self.PlayerObjList.append(Player(i))
        self.PointsFor :dict = dict(())
        for i in ["1s", "2s", "3s", "4s", "5s", "6s", "dri", "pok", "ful", "sst", "lst", "yah", "cha"]:
            self.PointsFor[i] = -1

    def redraw(self) -> None:
        """Redraw the screen according to the current status of the game"""
        global dice

        print("\x1b[0m\x1b[2J\x1b[H\x1b[1;38;5;51m#################### \x1b[1;37mYAHTZEE\x1b[1;38;5;51m #####\x1b[1;38;5;37m=====\x1b[1;38;5;23m-----\x1b[0m")
        for i in range(0,10): print("\x1b[1;38;5;51m#\x1b[0m")
        for i in range(0,6):  print("\x1b[1;38;5;44mI\x1b[0m")
        for i in range(0,6):  print("\x1b[1;38;5;37m!\x1b[0m")
        for i in range(0,6):  print("\x1b[1;38;5;30m:\x1b[0m")
        for i in range(0,7):  print("\x1b[1;38;5;23m.\x1b[0m")
        print("\x1b[5;4H\x1b[38;5;190mROLL\x1b[0m  \x1b[0;32mFIX\x1b[0m", end="")
        print("\x1b[3;6HRolls:    ", end="")
        for i in range(1,4):
            if self.Roll < i:
                print("\x1b[0m\x1b[48;5;31m \x1b[0m  ", end="")
            else:
                print("\x1b[48;5;88m\x1b[38;5;202mX\x1b[0m  ", end="")
        putBox(17,  9, 11, 3, "\x1b[0m")
        putBox(17, 11, 11, 8, "\x1b[0m")
        putBox(17, 18, 11, 4, "\x1b[0m")
        putBox(17, 21, 11, 9, "\x1b[0m")
        putBox(17, 29, 11, 3, "\x1b[0m")
        putBox(17, 31, 11, 3, "\x1b[0m")
        for i in range(0, len(self.PlayerNameList)):
            putBox(27+4*i,  2, 5, 8, "\x1b[0m")
            putBox(27+4*i,  9, 5, 3, "\x1b[0m")
            putBox(27+4*i, 11, 5, 8, "\x1b[0m")
            putBox(27+4*i, 18, 5, 4, "\x1b[0m")
            putBox(27+4*i, 21, 5, 9, "\x1b[0m")
            putBox(27+4*i, 29, 5, 3, "\x1b[0m")
            putBox(27+4*i, 31, 5, 3, "\x1b[0m")

        for i in range(0, len(self.PlayerObjList)):
            obj = self.PlayerObjList[i]
            obj.dispPlayerName(4*i+29, 3, 6, "\x1b[1;37;44m", "\x1b[0m\x1b[1;38;5;143m")

        for y, t in [[10, "Wins"], [12, "1's"], [13, "2's"], [14, "3's"], [15, "4's"], [16, "5's"], [17, "6's"],
                     [19, "SubTotal"], [20, "Bonus"], [22, "Drill"], [23, "Poker"], [24, "FullHouse"],
                     [25, "SmlStrght"], [26, "LrgStrght"], [27, "Yahtzee"], [28, "Chance"], [30, "XtraYhtze"], [32, "TOTAL"]]:
            print("\x1b[0m\x1b[" + str(y+1) + ";19H" + t.rjust(9), end="")

        for i in range(0, len(self.PlayerObjList)):
            obj = self.PlayerObjList[i]
            obj.dispPlayerScore(28+4*i, 10)

        for i in range(1,6):
            dice[i].clearMe()
            dice[i].drawMe()

        print("\x1b[0m\x1b[36;3H\x1b[1;31m" + self.ErrorMessage, end="")
        print("\x1b[0m\x1b[38;1H", end="")

    def recalcDice(self) -> None:
        """Recalculate status variables based on dice standings"""
        self.SumDice = 0
        for i in range(1,7): self.CountOf[str(i)] = 0
        for i in ["1s", "2s", "3s", "4s", "5s", "6s", "dri", "pok", "ful", "sst", "lst", "yah", "cha"]:
            self.PointsFor[i] = 0
        if not dice[1].Value * dice[2].Value * dice[3].Value * dice[4].Value * dice[5].Value : return
        for i in range(1,6):
            self.SumDice += dice[i].Value
            self.CountOf[str(dice[i].Value)] += 1
        for i in range(1,7):
            self.PointsFor[str(i)+"s"] = self.CountOf[str(i)] * i
            if self.CountOf[str(i)] > 2 : self.PointsFor["dri"] = 15
            if self.CountOf[str(i)] > 3 : self.PointsFor["pok"] = 20
            if self.CountOf[str(i)] > 4 : self.PointsFor["yah"] = 50
        if 2 in self.CountOf.values() and 3 in self.CountOf.values() : self.PointsFor["ful"] = 25
        for i in range(1,4):
            if self.CountOf[str(i)] * self.CountOf[str(i+1)] * self.CountOf[str(i+2)] * self.CountOf[str(i+3)] : self.PointsFor["sst"] = 30
        for i in range(1,3):
            if self.CountOf[str(i)] * self.CountOf[str(i+1)] * self.CountOf[str(i+2)] * self.CountOf[str(i+3)] * self.CountOf[str(i+4)] : self.PointsFor["lst"] = 40
        self.PointsFor["cha"] = self.SumDice

    def reset(self) -> None:
        """Reset scores (except total wins and points) at the end of a game"""
        self.Turn = 0
        self.Roll = 0
        self.CurrPlayerIDX = 0
        self.ErrorMessage = ""
        self.SumDice = 0
        for i in range(1,7): self.CountOf[str(i)] = 0
        for i in ["1s", "2s", "3s", "4s", "5s", "6s", "dri", "pok", "ful", "sst", "lst", "yah", "cha"]:
            self.PointsFor[i] = -1
        for obj in self.PlayerObjList: obj.reset()
        self.PlayerObjList[0].activate()

    def showStandings(self) -> None:
        """Display a pop up window with current standings"""
        h :int = len(self.PlayerObjList) + 6
        rank :int = 1
        putBox(10, 5, 34, h, "\x1b[0m")
        plyrlist = list(())
        for obj in self.PlayerObjList:
            plyrlist.append([obj.Name, obj.Points["TOT,pts"]])
        pls = sorted(plyrlist, key= lambda plyr: plyr[1], reverse=True)
        print("\x1b[7;22H\x1b[1mGAME STANDINGS\x1b[9;13H", end="")
        for itm in pls:
            print(str(rank).rjust(2) + ". " + itm[0][:20].ljust(20) + " : " + str(itm[1]).rjust(3) + "\x1b[B\x1b[30D", end="")
            rank += 1
        print("\x1b[0m\x1b[" + str(4+h) + ";21HPress ENTER...", end="")
        input("")


    def whoWon(self) -> Player:
        """Return the player object with the most total points"""
        ret :Player = self.PlayerObjList[0]
        maxPts = -2
        for obj in self.PlayerObjList:
            if obj.Points["TOT,pts"] > maxPts:
                ret = obj
                maxPts = obj.Points["TOT,pts"]
        return ret



class Dice:

    def __init__(self, YPos :int =-1):
        """Create a dice object and initialize
        Parameters:
            YPos (int): vertical position on screen"""
        self.Value :int  = 0
        self.Fixed :bool = False
        self.XPos  :int  = 2
        self.YPos  :int  = YPos

    def putAway(self) -> None:
        """Put the dice away into the fixed location"""
        if not self.Value:
            game.ErrorMessage = "Can not put away a dice not rolled into fixed position"
            self.Fixed = False
        else:
            self.Fixed = True
            while self.XPos < 8:
                self.XPos += 1
                self.clearMe()
                self.drawMe()
                sleep(0.1)

    def takeToRoll(self) -> None:
        """Take the dice back to the rolled ones"""
        self.Fixed = False
        while self.XPos > 2:
            self.XPos -= 1
            self.clearMe()
            self.drawMe()
            sleep(0.1)

    def clearMe(self) -> None:
        """Clear the dice's location"""
        print("\x1b[0m\x1b[" + str(self.YPos+1) + ";3H" + "      \x1b[0;32;42m#####\x1b[0m\x1b[B\x1b[11D"*5, end="")
        sys.stdout.flush()

    def drawMe(self) -> None:
        """Draw the dice onto its current location"""
        global DotRelCoords

        putBox(self.XPos, self.YPos, 5, 5, "\x1b[0m")
        if not self.Value: return
        print("\x1b[1m", end="")
        for coords in DotRelCoords[str(self.Value)]:
            relx, rely = coords
            print("\x1b[" + str(self.YPos+rely+1) + ";" + str(self.XPos+relx+1) + "H*", end="")
        print("\x1b[0m", end="")
        sys.stdout.flush()



########## PROC PART ##########

def putBox(x :int, y :int, w :int, h :int, col :str) -> None:
    """Draw a simple rectangle with the specified color
    Parameters:
        x (int): horizontal position on the screen
        y (int): vertical position on the screen
        w (int): width of the box including borders
        h (int): height of the box including borders
        col (str): complete ANSI escape sequence for the color"""

    print(col + "\x1b[" + str(y+1) + ";" + str(x+1) + "H+" + "-"*(w-2) + "+", end="")
    for i in range(0,h-2):
        print("\x1b[B\x1b[" + str(w) + "D|" + " "*(w-2) +"|", end="")
    print("\x1b[B\x1b[" + str(w) + "D+" + "-"*(w-2) + "+", end="")

def playerByWins(plyr) -> int:
    """Return the number of wins of the player
    Parameters:
    plyr : Player() object : the object reference of the player in question"""
    return plyr.Wins

def playerByPts(plyr) -> int:
    """Return the number of total points of the player
    Parameters:
    plyr : Player() object : the object reference of the player in question"""
    return plyr.TotWonPoints

def displayHelp() -> None:
    """Display a help window and return"""
    clist1 = list(("87", "51", "44", "37", "30", "23"))
    print("\x1b[0m\x1b[2J\x1b[H")
    for x1 in range(0,6):
        print("\x1b[1;38;5;"+clist1[x1]+"m"+"#"*10,end="")
    print("\x1b[1;38;5;44m\n#\n#\x1b[0m"+" "*30+"\x1b[1;36mGAME HELP\x1b[0m")
    print("\x1b[1;38;5;44m#\n#\x1b[0m \x1b[1;33mCOMMANDS DURING ROLLING\x1b[0m\n\x1b[1;38;5;44m#")
    print("\x1b[1;38;5;44m#\x1b[0m    \x1b[1;33mF\x1b[0;33m | \x1b[1;33mFIX\x1b[0;33m <dice1> [dice2] ...    -- put down selected dice to the fixed area\x1b[0m")
    print("\x1b[1;38;5;44m#\x1b[0m    \x1b[1;33mT\x1b[0;33m | \x1b[1;33mTAKE\x1b[0;33m <dice1> [dice2] ...   -- take selected dice into hand for rolling\x1b[0m")
    print("\x1b[1;38;5;44m#\x1b[0m    \x1b[1;33mR\x1b[0;33m | \x1b[1;33mROLL\x1b[0;33m                       -- roll dice in hand (not those on the fixed area)\x1b[0m")
    print("\x1b[1;38;5;44m#\n#\n#\x1b[0m \x1b[1;32mCOMMANDS AFTER ROLLING\x1b[0m\n\x1b[1;38;5;44m#")
    print("\x1b[1;38;5;44m#\x1b[0m    \x1b[1;32mW\x1b[0;32m | \x1b[1;32mWRITE\x1b[0;32m <where>              -- write the current points to the score sheet\x1b[0m")
    print("\x1b[1;38;5;44m#\n#\x1b[0m      \x1b[0;32mThe parameter \x1b[1;32m<where>\x1b[0;32m can be one character, meaning:\x1b[0m")
    print("\x1b[1;38;5;44m#\x1b[0m        \x1b[1;32m1 ... 6\x1b[0;32m = sum of 1's ... 6's | \x1b[1;32mD\x1b[0;32m = drill | \x1b[1;32mP\x1b[0;32m = poker | \x1b[1;32mF\x1b[0;32m = full house\x1b[0m")
    print("\x1b[1;38;5;44m#\x1b[0m        \x1b[1;32mS\x1b[0;32m = small straight | \x1b[1;32mL\x1b[0;32m = large straight | \x1b[1;32mY\x1b[0;32m = yahtzee | \x1b[1;32mC\x1b[0;32m = chance\x1b[0m")
    print("\x1b[1;38;5;44m#\n#\n#\x1b[0m \x1b[1;36mOTHER COMMANDS\x1b[0m\n\x1b[1;38;5;44m#")
    print("\x1b[1;38;5;44m#\x1b[0m    \x1b[1;36mS\x1b[0;36m | \x1b[1;36mSHOW\x1b[0;36m                       -- show players rankings in the current game based on points\x1b[0m")
    print("\x1b[1;38;5;44m#\x1b[0m    \x1b[1;36mH\x1b[0;36m | \x1b[1;36mHELP\x1b[0;36m | \x1b[1;36m?\x1b[0;36m                   -- show this help screen\x1b[0m")
    print("\x1b[1;38;5;44m#\x1b[0m    \x1b[1;36mQ\x1b[0;36m | \x1b[1;36mQUIT\x1b[0;36m                       -- quit the game\x1b[0m")
    print("\x1b[1;38;5;44m#\n#\n#\x1b[0m   >>> Hit [ENTER] to continue <<<")

    input("")

########## MAIN PART ##########

game = Game(sys.argv[1:])
game.PlayerObjList[0].activate()
for z in range(1,6): dice[z] = Dice(6*z-1)
while game.Stay:
    game.redraw()
    cmdS = input(">>> ").lower()
    if not len(cmdS): continue
    cmdL = cmdS.split(" ")
    cmd = cmdL[0]
    parm = cmdL[1:]
    game.ErrorMessage = ""

    if cmd in ["q", "quit"]:
        game.Stay = False
        continue

    if cmd in ["r", "roll"]:
        if game.Roll > 2:
            game.ErrorMessage = "No more rolls!"
            continue
        wasRolled :bool = False
        for z in range(1,6):
            if not dice[z].Fixed:
                for q in range(0,10):
                    dice[z].Value = randint(1,6)
                    dice[z].drawMe()
                    sleep(0.1)
                wasRolled = True
        if not wasRolled:
            game.ErrorMessage = "No dice selected to roll!"
            continue
        game.recalcDice()
        game.Roll += 1
        continue

    if cmd in ["t", "take"]:
        if not len(parm):
            game.ErrorMessage = "Specify dice numbers to take!"
            continue
        for zs in parm:
            if zs in ["1", "2", "3", "4", "5"]:
                z = int(zs)
                dice[z].takeToRoll()
        continue

    if cmd in ["f", "fix"]:
        if not len(parm):
            game.ErrorMessage = "Specify dice numbers to fix!"
            continue
        for zs in parm:
            if zs in ["1", "2", "3", "4", "5"]:
                z = int(zs)
                dice[z].putAway()
        continue

    if cmd in ["w", "write"]:
        if not len(parm):
            game.ErrorMessage = "Write points to where?"
            continue
        if parm[0] not in ["1", "2", "3", "4", "5", "6", "d", "p", "f", "s", "l", "y", "c"]:
            game.ErrorMessage = "Write points to where?"
            continue
        idx = "error"
        for k in game.PointsFor.keys():
            if k[0] == parm[0] : idx = k
        plobj = game.PlayerObjList[game.CurrPlayerIDX]
        if plobj.Points[idx+",valid"]:
            game.ErrorMessage = "That score is already taken!"
            continue
        if game.PointsFor[idx] == -1:
            game.ErrorMessage = "Cannot write this value"
            continue
        if game.PointsFor["yah"] == 50 and plobj.Points["yah,valid"] and plobj.Points["yah,pts"] == 50:
            plobj.Points["xtr,pts"] += 100
        plobj.Points[idx+",valid"] = True
        plobj.Points[idx+",pts"] = game.PointsFor[idx]
        plobj.recalcPoints()
        #---------------------------------------------
        game.Roll = 0
        for z in range(1,6):
            dice[z].takeToRoll()
            dice[z].Value = 0
        game.PlayerObjList[game.CurrPlayerIDX].passivate()
        game.CurrPlayerIDX += 1
        if game.CurrPlayerIDX >= len(game.PlayerObjList):
            game.CurrPlayerIDX = 0
            game.Turn += 1
        game.PlayerObjList[game.CurrPlayerIDX].activate()
        for i in ["1s", "2s", "3s", "4s", "5s", "6s", "dri", "pok", "ful", "sst", "lst", "yah", "cha"]:
            game.PointsFor[i] = -1
        if game.Turn == 13:
            game.showStandings()
            for o in game.PlayerObjList:
                o.TotWonPoints += o.Points["TOT,pts"]
            game.whoWon().addWins()
            game.reset()
        continue

    if cmd in ["h", "help", "?"]:
        displayHelp()
        continue

    if cmd in ["s", "show"]:
        game.showStandings()
        continue

#--- CUT THIS DEBUG BULLSHIT FROM HERE
#game.PlayerObjList[0].Wins = 7
#game.PlayerObjList[1].Wins = 11
#game.PlayerObjList[2].Wins = 2
#game.PlayerObjList[0].TotWonPoints = 280
#game.PlayerObjList[1].TotWonPoints = 520
#game.PlayerObjList[2].TotWonPoints = 975
#***

LW = game.PlayerObjList.copy()
LW.sort(key=playerByWins, reverse=True)
LP = game.PlayerObjList.copy()
LP.sort(key=playerByPts, reverse=True)

print("\n")
clist = list(("87","51","44","37","30","23"))
for x in range(0,6):
    print("\x1b[1;38;5;"+clist[x]+"m"+"#"*10,end="")
print("\x1b[1;38;5;18m##\n#\x1b[0m"+" "*20+"\x1b[1;36mTOURNAMENT STATISTICS\x1b[0m")
print("\x1b[1;38;5;18m#\n#\x1b[0m \x1b[1;33mRANKING BY WINS\x1b[0m                   \x1b[1;32mRANKING BY POINTS\x1b[0m\n\x1b[1;38;5;18m# "+"="*60)
for x in range(0,len(LW)):
    print("\x1b[1;38;5;18m#\x1b[0m \x1b[0;33m"+str(x+1)+". \x1b[1m"+str(LW[x].Wins).rjust(3)+"\x1b[0;33m wins: "+LW[x].Name,end="\x1b[0m")
    print(" "*(22-len(str(x+1))-len(LW[x].Name)),end="\x1b[0;32m")
    print(str(x+1)+". \x1b[1m"+str(LP[x].TotWonPoints)+"\x1b[0;32m pts: "+LP[x].Name+"\x1b[0m")
print("\n")
exit(0)
