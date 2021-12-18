# B351FinalProject

The method Play_Step() is a stand alone method that allowes the user to manually controll the snake to get a fell for the game. 

The Methods play_Heuristic1 and Play_Heuristic2 are the same except for the get_best_move that those methods call. The diference is which heuristic function you would like to run. 
You can change which Heuristic method is called in the init by commenting out one function and un-commenting the other. 

The game works by calling one of the Play_Heuristic methods, that method will that call it's designated get_best_move method to collect data from the heuristic and return the best move based on that data. Next the Play_Heuristic method will update the snake to move to whatever direction the get_best_move method returned. After that it checks if the game is over by a collision and if it is not a game over, the init will continue to call the Play_heurisc method untill the variable game_over is returned as False.