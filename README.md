# Dou Shou Qi (Jungle Chess) AI
> By Yoav Amitai
> 

<img style="float: left" src="https://ancientchess.com/graphics-rules/dou_shou_qi_jungle_game-board.jpg">
This projects aims to implement the traditional Chinese game *Dou Shou Qi* (鬥獸棋, or Jungle Chess) using python, and adding a minimax algorithm as a basis for a computer-based opponent.

The project uses python libraries, such as:
 1. numPy
 2. pygame

___

The game utilizes an MVC software design pattern:
 1. **model.py** stores, modifies and uses the data structures of the game - a 2D array representing the rank of the game pieces and their position on the board.
 2. **view.py** implements the visual representation of the game, using _pygame_ as a graphic library.
 3. **controller.py** manages the flow of the game, communications between the view and the model.

