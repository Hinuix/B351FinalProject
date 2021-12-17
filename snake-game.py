import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
#font = pygame.font.Font('arial.ttf', 25)
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
MAGENTA = (255, 0, 255)

BLOCK_SIZE = 20
SPEED = 20 #origional speed = 20

class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self):        # Using this method will allow the user to controll the snake manually
        #print(self.snake)
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score
    

    def Heuristic1(self, direction): # A heuristic function that will score a move based on the direction you tell it to score. 
        right = 0
        left = 0
        up = 0
        down = 0
        if direction == "RIGHT":
            if((self.head.x + BLOCK_SIZE, self.head.y) in self.snake[1:] or self.head.x + BLOCK_SIZE == self.w): # checks if the snake is going to hit itself or hit a wall
                #print("Moving to the right == danger")
                right -= 10      #score the direction -10 if it is a direction that will result in death
            else:
                right += 1      #if the direction does not result in immediate death then reward the move with +1

            if self.head.x < self.food.x:
                right += 1      #if the direction moves the snake towards the food, the reward the direction with +1  

            return right

        if direction == "LEFT":
            if((self.head.x - BLOCK_SIZE, self.head.y) in self.snake[1:] or self.head.x - BLOCK_SIZE == (-1 * BLOCK_SIZE)): # checks if the snake is going to hit itself or hit a wall
                #print("Moving to the left == danger")
                left -= 10      #score the direction -10 if it is a direction that will result in death
            else:
                left += 1        #if the direction does not result in immediate death then reward the move with +1
            
            if self.head.x > self.food.x:
                left += 1       #if the direction moves the snake towards the food, the reward the direction with +1

            return left

        if direction == "UP":
            if((self.head.x, self.head.y - BLOCK_SIZE) in self.snake[1:] or self.head.y - BLOCK_SIZE == (-1 * BLOCK_SIZE)): # checks if the snake is going to hit itself or hit a wall
                #print("Moving up == danger")
                up -= 10         #score the direction -10 if it is a direction that will result in death
            else:
                up += 1          #if the direction does not result in immediate death then reward the move with +1

            if self.head.y > self.food.y:
                up += 1         #if the direction moves the snake towards the food, the reward the direction with +1

            return up

        if direction == "DOWN":
            if((self.head.x, self.head.y + BLOCK_SIZE) in self.snake[1:] or self.head.y + BLOCK_SIZE == self.h): # checks if the snake is going to hit itself or hit a wall
                #print("Moving Down == danger")
                down -= 10       #score the direction -10 if it is a direction that will result in death
            else:
                down += 1        #if the direction does not result in immediate death then reward the move with +1
            
            if self.head.y < self.food.y:
                down += 1        #if the direction moves the snake towards the food, the reward the direction with +1

            return down
    
    def Heuristic2(self, direction): # A heuristic function that will score a move based on the direction you tell it to score. 
        right = 0
        left = 0
        up = 0
        down = 0
        if direction == "RIGHT":
            if((self.head.x + BLOCK_SIZE, self.head.y) in self.snake[1:] or self.head.x + BLOCK_SIZE == self.w): # checks if the snake is going to hit itself or hit a wall
                #print("Moving to the right == danger")
                right -= 100     #score the direction -10 if it is a direction that will result in death
            else:
                right += 0      #if the direction does not result in immediate death then reward the move with +1

            if self.head.x < self.food.x:
                right += 1      #if the direction moves the snake towards the food, the reward the direction with +1  

            for i in range(2, round(len(self.snake)/4)): #round(len(self.snake)/2)
                if (self.head.x + (i * BLOCK_SIZE), self.head.y) in self.snake[1:]:
                    right -= round(len(self.snake)/4)/i
                
            return right

        if direction == "LEFT":
            if((self.head.x - BLOCK_SIZE, self.head.y) in self.snake[1:] or self.head.x - BLOCK_SIZE == (-1 * BLOCK_SIZE)): # checks if the snake is going to hit itself or hit a wall
                #print("Moving to the left == danger")
                left -= 100      #score the direction -10 if it is a direction that will result in death
            else:
                left += 0       #if the direction does not result in immediate death then reward the move with +1
            
            if self.head.x > self.food.x:
                left += 1       #if the direction moves the snake towards the food, the reward the direction with +1

            for i in range(2, round(len(self.snake)/4)):
                if (self.head.x - (i * BLOCK_SIZE), self.head.y) in self.snake[1:]:
                    left -= round(len(self.snake)/4)/i

            return left

        if direction == "UP":
            if((self.head.x, self.head.y - BLOCK_SIZE) in self.snake[1:] or self.head.y - BLOCK_SIZE == (-1 * BLOCK_SIZE)): # checks if the snake is going to hit itself or hit a wall
                #print("Moving up == danger")
                up -= 100         #score the direction -10 if it is a direction that will result in death
            else:
                up += 0          #if the direction does not result in immediate death then reward the move with +1

            if self.head.y > self.food.y:
                up += 1         #if the direction moves the snake towards the food, the reward the direction with +1

            for i in range(2, round(len(self.snake)/4)):
                if (self.head.x , self.head.y - (i * BLOCK_SIZE)) in self.snake[1:]:
                    up -= round(len(self.snake)/4)/i

            return up

        if direction == "DOWN":
            if((self.head.x, self.head.y + BLOCK_SIZE) in self.snake[1:] or self.head.y + BLOCK_SIZE == self.h): # checks if the snake is going to hit itself or hit a wall
                #print("Moving Down == danger")
                down -= 100       #score the direction -10 if it is a direction that will result in death
            else:
                down += 0       #if the direction does not result in immediate death then reward the move with +1
            
            if self.head.y < self.food.y:
                down += 1        #if the direction moves the snake towards the food, the reward the direction with +1

            for i in range(2, round(len(self.snake)/4)):
                if (self.head.x, self.head.y + (i * BLOCK_SIZE)) in self.snake[1:]:
                    down -= round(len(self.snake)/4)/i

            return down

    def TieBreaker(self, key, moveDirection):
        
        moveDirection2 = key
        moveDirectioncnt = 0
        moveDirectioncnt2 = 0
        while True:
            if moveDirection == "RIGHT":
                moveDirectioncnt += 1
                if (self.head.x + (moveDirectioncnt * BLOCK_SIZE), self.head.y) in self.snake[1:] or self.head.x + (moveDirectioncnt * BLOCK_SIZE) == self.w:
                    break
            
            if moveDirection == "LEFT":
                moveDirectioncnt += 1
                if (self.head.x - (moveDirectioncnt * BLOCK_SIZE), self.head.y) in self.snake[1:] or self.head.x - (moveDirectioncnt * BLOCK_SIZE) == (-1 * BLOCK_SIZE):
                    break
            
            if moveDirection == "UP":
                moveDirectioncnt += 1
                if (self.head.x, self.head.y + (moveDirectioncnt * BLOCK_SIZE)) in self.snake[1:] or self.head.y + (moveDirectioncnt * BLOCK_SIZE) == self.h:
                    break
            
            if moveDirection == "DOWN":
                moveDirectioncnt += 1
                if (self.head.x, self.head.y - (moveDirectioncnt * BLOCK_SIZE)) in self.snake[1:] or self.head.y - (moveDirectioncnt * BLOCK_SIZE) == (-1 *  BLOCK_SIZE):
                    break
        
        while True:
            if moveDirection2 == "RIGHT":
                moveDirectioncnt2 += 1
                if (self.head.x + (moveDirectioncnt2 * BLOCK_SIZE), self.head.y) in self.snake[1:] or self.head.x + (moveDirectioncnt2 * BLOCK_SIZE) == self.w:
                    break
            
            if moveDirection2 == "LEFT":
                moveDirectioncnt2 += 1
                if (self.head.x - (moveDirectioncnt2 * BLOCK_SIZE), self.head.y) in self.snake[1:] or self.head.x - (moveDirectioncnt2 * BLOCK_SIZE) == (-1 * BLOCK_SIZE):
                    break
            
            if moveDirection2 == "UP":
                moveDirectioncnt2 += 1
                if (self.head.x, self.head.y + (moveDirectioncnt2 * BLOCK_SIZE)) in self.snake[1:] or self.head.y + (moveDirectioncnt2 * BLOCK_SIZE) == self.h:
                    break
            
            if moveDirection2 == "DOWN":
                moveDirectioncnt2 += 1
                if (self.head.x, self.head.y - (moveDirectioncnt2 * BLOCK_SIZE)) in self.snake[1:] or self.head.y - (moveDirectioncnt2 * BLOCK_SIZE) == (-1 *  BLOCK_SIZE):
                    break
        if moveDirectioncnt2 > moveDirectioncnt:
            return moveDirection2
        else:
            return moveDirection


    def Get_Best_Move1(self): # a get best move mehtod that uses heuristic1
        directions = {"RIGHT" : 0, "LEFT" : 0, "UP" : 0, "DOWN" : 0}    #A dictionary containing key value pairs of the direction and their given weights. The Weights will be updated through the heuristic function.
        moveScore = -1000   # A variable to keep track of the highest weight
        moveDirection = ""  # A variable to keep track of the best move according to the highest weight
        for key in directions:  #loop through the keys in the dictionarry
            score = self.Heuristic1(key) #Heuristic 1 just tries not to hit itself and move towards the food.
            directions[key] = float(score)     # update the weight of a direction in the dictionary based on the score from the heuristic function
            #print(key + " weight = " + str(directions[key]))
        
        for key in directions: # loop throught the keys in the dictionary again 
            if directions[key] > moveScore:     # decide if the current direction has a larger weight than the current highest recorded weight
                #print(str(directions[key]) + " > movescore = (" + str(moveScore) + ")")
                moveScore = directions[key]     # if a direction has a larger weight, than update the new score
                moveDirection = key             # update the direction to the best option found so far
                #print("Move Directioin = " + moveDirection)
            if directions[key] == moveScore:
                moveDirection = self.TieBreaker(key, moveDirection)

        # Find what direction is the best option so far and update self.direction accordingly
        if moveDirection == "RIGHT":
            #print("Changing direction to " + moveDirection)
            self.direction = Direction.RIGHT       
        
        if moveDirection == "LEFT":
            #print("Changing direction to " + moveDirection)
            self.direction = Direction.LEFT

        if moveDirection == "UP":
            #print("Changing direction to " + moveDirection)
            self.direction = Direction.UP

        if moveDirection == "DOWN":
            #print("Changing direction to " + moveDirection)
            self.direction = Direction.DOWN

    def Get_Best_Move2(self): #same get best move method but it used the heuristic2
        directions = {"RIGHT" : 0, "LEFT" : 0, "UP" : 0, "DOWN" : 0}    #A dictionary containing key value pairs of the direction and their given weights. The Weights will be updated through the heuristic function.
        moveScore = -1000   # A variable to keep track of the highest weight
        moveDirection = ""  # A variable to keep track of the best move according to the highest weight
        for key in directions:  #loop through the keys in the dictionarry
            score = self.Heuristic2(key) # Heuristic2 tries to not box itself in.
            directions[key] = float(score)     # update the weight of a direction in the dictionary based on the score from the heuristic function
            #print(key + " weight = " + str(directions[key]))
        
        for key in directions: # loop throught the keys in the dictionary again 
            if directions[key] > moveScore:     # decide if the current direction has a larger weight than the current highest recorded weight
                #print(str(directions[key]) + " > movescore = (" + str(moveScore) + ")")
                moveScore = directions[key]     # if a direction has a larger weight, than update the new score
                moveDirection = key             # update the direction to the best option found so far
                #print("Move Directioin = " + moveDirection)
            if directions[key] == moveScore:
                moveDirection = self.TieBreaker(key, moveDirection)

        # Find what direction is the best option so far and update self.direction accordingly
        if moveDirection == "RIGHT":
            #print("Changing direction to " + moveDirection)
            self.direction = Direction.RIGHT       
        
        if moveDirection == "LEFT":
            #print("Changing direction to " + moveDirection)
            self.direction = Direction.LEFT

        if moveDirection == "UP":
            #print("Changing direction to " + moveDirection)
            self.direction = Direction.UP

        if moveDirection == "DOWN":
            #print("Changing direction to " + moveDirection)
            self.direction = Direction.DOWN

    def Play_Heuristic1(self): # the method that will play the game hased on the heuristic1 stratagy 
        
        # 1. collect data from heuristic
        self.Get_Best_Move1()

        # 2. move
        self._move(self.direction) # update the head
        #print("Making a move")
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def Play_Heuristic2(self): # the method that will play the game hased on the heuristic1 stratagy 
        
        # 1. collect data from heuristic
        self.Get_Best_Move2()

        # 2. move
        self._move(self.direction) # update the head
        #print("Making a move")
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def DoNotDie(self): # A very simple function that just tries to not make a move that will result in death and tries to move towards the food. 

        if self.head.x + (BLOCK_SIZE) == self.w: # check if it is going to hit the right wall
            if self.head.y > self.food.y:   #check if the snake y coordinate is greater than the food's y coordinate, if it is then move up since the y-axis is inverted (moving up decreases the y coordinate and moveing down increases the y coordinate)
                self.direction = Direction.UP
            if self.head.y < self.food.y:   #check if the snake y coordinate is less than the food's y coordinate, if it is then move down since the y-axis is inverted (moving up decreases the y coordinate and moveing down increases the y coordinate)
                self.direction = Direction.DOWN
            if self.head.y == self.food.y:  #check if the y corrdinate is in line with the food's y coordinate, if it is then move to the left since we know we are near the right wall
                self.direction = Direction.LEFT              

        if self.head.x - BLOCK_SIZE == -20: # check if snake is going to hit the left wall
            if self.head.y > self.food.y:   #check if the snake y coordinate is greater than the food's y coordinate, if it is then move up since the y-axis is inverted (moving up decreases the y coordinate and moveing down increases the y coordinate)
                self.direction = Direction.UP
            if self.head.y < self.food.y:   #check if the snake y coordinate is less than the food's y coordinate, if it is then move down since the y-axis is inverted (moving up decreases the y coordinate and moveing down increases the y coordinate)
                self.direction = Direction.DOWN
            if self.head.y == self.food.y: #check if the y corrdinate is in line with the food's y coordinate, if it is then move to the right since we know we are near the left wall
                self.direction = Direction.RIGHT

        if self.head.y + BLOCK_SIZE == self.h: # check if snake is going to hit the bottom border
            if self.head.x < self.food.x:       #check if the x coordinate is to the left of the food, if it is then move to the right 
                self.direction = Direction.RIGHT
            if self.head.x > self.food.x:       #check if the x coordinate is to the right of the food, if it is then move to the left 
                self.direction = Direction.LEFT
            if self.head.x == self.food.x:      #check if the x coordinate is equal to the food, if it is then move up since we already know we are near the bottom border 
                self.direction = Direction.UP

        if self.head.y - BLOCK_SIZE == -20: # check if the snake is going to hit the top border
            if self.head.x < self.food.x:   #check if the x coordinate is to the left of the food, if it is then move to the right 
                self.direction = Direction.RIGHT
            if self.head.x > self.food.x:       #check if the x coordinate is to the right of the food, if it is then move to the left 
                self.direction = Direction.LEFT
            if self.head.x == self.food.x:      #check if the x coordinate is equal to the food, if it is then move down since we already know we are near the top border 
                self.direction = Direction.DOWN
        

    def Go_Around_Boundry(self): # This function will help the snake go aroung the boundry without dying
        if self.head.x + (BLOCK_SIZE) == self.w: # check if it is going to hit the right wall
            self.direction = Direction.UP
        
        if self.head.x + (BLOCK_SIZE) == self.w and self.head.y == 0: # check if it is going to hit the top right corner
            self.direction = Direction.LEFT
            
        if self.head.x == 0 and self.head.y == 0: # check if it is going to hit the to left corner
            self.direction = Direction.DOWN
            
        if self.head.x == 0 and self.head.y + BLOCK_SIZE == self.h: # check if it is going to hit the bottom left corner
            self.direction = Direction.RIGHT
            
    def is_in_line_with_food(self): # This function will see if the head of the snake is in line with the food's x or y coordinate 
        if self.head.x == self.food.x and self.head.y < self.food.y:
            #print("self.head.x = self.food.x")
            self.direction = Direction.DOWN
        if self.head.x == self.food.x and self.head.y > self.food.y:
            #print("self.head.x = self.food.x")
            self.direction = Direction.UP 
        if self.head.y == self.food.y and self.head.x < self.food.x:
            #print("self.head.x = self.food.x")
            self.direction = Direction.RIGHT
        if self.head.y == self.food.y and self.head.x > self.food.x:
            #print("self.head.x = self.food.x")
            self.direction = Direction.LEFT

    def play_HardCode(self): # This is a simple playing method that used the above three methods to make a decision
        # 1. collect data from heuristic
        #print(self.snake)
        self.is_in_line_with_food()
        
        self.DoNotDie()
        # 2. move
        self._move(self.direction) # update the head
        #print("Making a move")
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
           return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, WHITE, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    counter = 0
   

    
    while True:
        #game_over, score = game.play_step()
        #game_over, score = game.play_HardCode()
        game_over, score = game.Play_Heuristic2()
        if game_over == True:
            break
    
        
    print('Final Score', score)
        
        
    pygame.quit()
    
    #game.heuristic()