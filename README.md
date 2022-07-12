# Chess-Game-with-Animation-and-AI
Created a chess game with Animation

# To run this on your PC, install pygame using the following command 
```
pip install pygame
```
## And now run ChessGame.py


### To play against another person, at line 43 and 44 in file ChessMain.py, make playerOne and playerTwo both to be True
### To play against AI, while playing as white yourself, at line 43 in file ChessMain.py, make playerOne to be True and playerTwo at line 44 in same file to be False
## To just watch AI struggle against itself, at line 43 and 44 in file ChessMain.py, make playerOne and playerTwo both to be False

### To change the difficulty of AI players, change the variable MAX_DEPTH at line6 in file SmartMoveFinder.py file to 1 for least difficulty(greedy algorithm) upto whatever your PC can handle in a reasonable amount of time. Mac M1 with 8 gigs of RAM can usually run upto 3 - 4 move depth in around a minute per move
