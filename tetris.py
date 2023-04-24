import pygame
import random
import sys

# Constants
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 480
BLOCK_SIZE = 20
BOARD_WIDTH = 13
BOARD_HEIGHT = 20
BLACK_COLORS = (0, 0, 0)
WHITE_COLORS = (255, 255, 255)
BLOCK_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 165, 0), (57, 137, 47), (46, 46, 132), (120, 37, 111)]
I_BLOCK = [[1, 1, 1, 1]]
J_BLOCK = [[1, 0, 0], [1, 1, 1]]
L_BLOCK = [[0, 0, 1], [1, 1, 1]]
O_BLOCK = [[1, 1], [1, 1]]
S_BLOCK = [[0, 1, 1], [1, 1, 0]]
T_BLOCK = [[0, 1, 0], [1, 1, 1]]
Z_BLOCK = [[1, 1, 0], [0, 1, 1]]

pygame.init()
pygame.font.init() 

class Block:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        self.y = -len(shape)
    
    def move_down(self):
        self.y += 1
    
    def move_left(self):
        self.x -= 1
    
    def move_right(self):
        self.x += 1
    
    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))
    
    def draw(self, screen):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j] == 1:
                    pygame.draw.rect(screen, self.color, ((self.x+j)*BLOCK_SIZE, (self.y+i)*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

class Tetris:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode((BLOCK_SIZE*BOARD_WIDTH, BLOCK_SIZE*BOARD_HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_block = Block(random.choice([I_BLOCK, J_BLOCK, L_BLOCK, O_BLOCK, S_BLOCK, T_BLOCK, Z_BLOCK]), random.choice(BLOCK_COLORS))
        self.next_block = Block(random.choice([I_BLOCK, J_BLOCK, L_BLOCK, O_BLOCK, S_BLOCK, T_BLOCK, Z_BLOCK]), random.choice(BLOCK_COLORS))
        self.score = 0
        self.font = pygame.font.Font(None, 36)

        # load the background
        self.background = pygame.image.load("wallpaper.jpeg")

        # Load the music file
        pygame.mixer.music.load("stranger-things-124008.mp3")
        # Set the volume
        pygame.mixer.music.set_volume(0.5)
        # Start playing the music
        pygame.mixer.music.play(-1)

    def is_game_over(self):
       for j in range(BOARD_WIDTH):
           if self.board[0][j]:
               return True
       return False 

    def run(self):
        game_over = False
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            if self.is_game_over():
                game_over = True 
                self.draw_game_over()
                break

            # Move current block down
            if self.is_valid_position(self.current_block, 0, 1):
                self.current_block.move_down()
            else:
                # Lock block in place
                self.lock_current_block()
                # Check for completed lines
                self.check_lines()
                # Set current block to next block and get a new next block
                self.current_block = self.next_block
                self.next_block = Block(random.choice([I_BLOCK, J_BLOCK, L_BLOCK, O_BLOCK, S_BLOCK, T_BLOCK, Z_BLOCK]), random.choice(BLOCK_COLORS))

                # If the new current block is in an invalid position, game over
                if not self.is_valid_position(self.current_block, 0, 0) or self.current_block.y == 0:
                    # If not, the game is over
                    game_over = True
                    self.draw_game_over()
            
            # Handle user input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.is_valid_position(self.current_block, -1, 0):
                self.current_block.move_left()
            if keys[pygame.K_RIGHT] and self.is_valid_position(self.current_block, 1, 0):
                self.current_block.move_right()
            if keys[pygame.K_DOWN] and self.is_valid_position(self.current_block, 0, 1):
                self.current_block.move_down()
            if keys[pygame.K_UP]:
                self.current_block.rotate()
            
            # Blit the background surface onto the screen
            self.screen.fill(BLACK_COLORS)
            #self.screen.blit(self.background, (0, 0))
            
            # Draw board
            for i in range(BOARD_HEIGHT):
                for j in range(BOARD_WIDTH):
                    if self.board[i][j] != 0:
                        pygame.draw.rect(self.screen, BLOCK_COLORS[self.board[i][j]-1], (j*BLOCK_SIZE, i*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 3)
            pygame.draw.rect(self.screen, BLACK_COLORS, (0, 0, BOARD_WIDTH * BLOCK_SIZE, BOARD_HEIGHT * BLOCK_SIZE), 1)
            
            # Draw current block and next block
            self.current_block.draw(self.screen)
            self.next_block.draw(self.screen)

            # Render score text onto a surface
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))

            # Blit the score surface onto the screen at a specific position
            self.screen.blit(score_text, (10, 10))
            
            # Update screen
            pygame.display.update()
            
            # Tick clock
            self.clock.tick(5)

        # wait for the user to quit the game
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def is_valid_position(self, block, dx, dy):
        for i in range(len(block.shape)):
            for j in range(len(block.shape[0])):
                if block.shape[i][j] == 1:
                    x = block.x + j + dx
                    y = block.y + i + dy
                    if x < 0 or x >= BOARD_WIDTH or y >= BOARD_HEIGHT or (y >= 0 and self.board[y][x] != 0):
                        return False
        return True
    
    def lock_current_block(self):
        for i in range(len(self.current_block.shape)):
            for j in range(len(self.current_block.shape[0])):
                if self.current_block.shape[i][j] == 1:
                    self.board[self.current_block.y+i][self.current_block.x+j] = BLOCK_COLORS.index(self.current_block.color) + 1
    
    def check_lines(self):
        lines_to_remove = []
        for i in range(BOARD_HEIGHT):
            if all([x != 0 for x in self.board[i]]):
                lines_to_remove.append(i)
        for i in reversed(lines_to_remove):
            del self.board[i]
            self.board.insert(0, [0] * BOARD_WIDTH)
            self.score += 10

    def draw_game_over(self):
        #font = pygame.font.SysFont('Arial', 36)
        game_over_text = self.font.render("Game Over", True, (255, 255, 255))
        self.screen.blit(game_over_text, (BOARD_WIDTH*BLOCK_SIZE/2 - game_over_text.get_width()/2, BOARD_HEIGHT*BLOCK_SIZE/2 - game_over_text.get_height()/2))

        # update the display
        pygame.display.update()

if __name__ == "__main__":
    game = Tetris()
    game.run()
    pygame.quit()

