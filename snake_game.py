import pygame, sys
from pygame.locals import *
from random import randint

# Cores
BLACK = (0, 0, 0)
BLUE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
# Direcoes
UP = 8
DOWN = 2
LEFT = 4
RIGHT = 6


class Game():

    def __init__(self, width, height, fps):
        pygame.init()
        pygame.display.set_caption('Jogo Da Cobrinha') # Nome da janela
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        # Cria o background
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(BLACK)
        self.background.convert()
        self.scorecard = pygame.draw.rect(self.background, RED, Rect([10, 10], [self.width - 20, 100]), 1)# Retangulo da caixa do placar
        # Game area
        self.gamearea = pygame.draw.rect(self.background, BLUE, Rect([10, 120], [self.width - 20, 380]), 1)
        self.points = 0
        # Placar
        self.font = pygame.font.Font(None, 36)
        self.mainClock = pygame.time.Clock()
        self.fps = fps
        self.snake = Snake()
        self.food = Food(self.snake)

    def run(self):
        """Main Loop
        """
        morte = 0


        while not morte:
            # Quit event
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                # <ESC> to quit
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == KEYDOWN:
                    # Verifica se as direcoes sao validas
                    if event.key == K_LEFT and self.snake.direction != RIGHT:
                        self.snake.direction = LEFT
                    elif event.key == K_RIGHT and self.snake.direction != LEFT:
                        self.snake.direction = RIGHT
                    elif event.key == K_UP and self.snake.direction != DOWN:
                        self.snake.direction = UP
                    elif event.key == K_DOWN and self.snake.direction != UP:
                        self.snake.direction = DOWN
                    elif event.key == K_KP_PLUS:
                        self.fps += 5
                    elif event.key == K_KP_PLUS:
                        self.fps -= 5

            # atualiza a cabeca
            morte = self.snake.update(self.snake.direction, self.width, self.height)

            # Checa se a cabeca esta comendo o corpo (colisao)
            if self.snake.corpo.count(self.snake.cabeca) > 0:
                morte = 1

            # Insere uma nova cabeca no corpo (atualiza o corpo)
            self.snake.corpo.insert(0, list(self.snake.cabeca))

            # Come a comida
            if self.snake.cabeca[0] == self.food.foodXY[0] and self.snake.cabeca[1] == self.food.foodXY[1]:
                self.food = Food(self.snake)
                self.incPoints()
            else:
                self.snake.corpo.pop()

            self.mainClock.tick(self.fps)
            self.drawScore()
            self.drawSnake()
            self.drawFood()
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))

        pygame.quit()

    def incPoints(self):
        """Adiciona os pontos a cada vez que a cobrinha come
        """
        self.points = self.points + 100
        if self.points == 300:
            self.fps += 2
        elif self.points == 1000:
            self.fps += 5
        elif self.points == 1500:
            self.fps += 6

    def drawScore(self):
        """Desenha o placar na tela
        """
        surface = self.font.render("Points: " + str(self.points), True, GRAY)
        self.screen.blit(surface, (75, 50))

    def drawSnake(self):
        """Desenha a cobrinha na tela
        """
        for x in self.snake.corpo:
            pygame.draw.rect(self.screen, BLUE, Rect(x, (18, 18)))

    def drawFood(self):
        """Desenha a comida na tela
        """
        pygame.draw.rect(self.screen, RED, Rect(self.food.foodXY, (18, 18)))


class Snake():
    """Snake class
    """

    def __init__(self):
        x1 = randint(0, 18)
        y1 = randint(0, 15)
        x = int(x1 * 20) + 10
        y = int(y1 * 20) + 120
        self.cabeca = [x, y]
        self.corpo = [[x, y], [x - 20, y]]
        self.direction = RIGHT

    def update(self, direction, width, height):
        """Atualiza a cabeca da cobra.
            Retorna 1 se a cabeca sair para fora dos limites do tabuleiro
         """
        if direction == RIGHT:
            self.cabeca[0] += 20
            self.direction = RIGHT
            if self.cabeca[0] > width - 20:
                return 1
            else:
                return 0
        elif direction == LEFT:
            self.cabeca[0] -= 20
            self.direction = LEFT
            if self.cabeca[0] < 10:
                return 1
            else:
                return 0
        elif direction == UP:
            self.cabeca[1] -= 20
            self.direction = UP
            if self.cabeca[1] < 110:
                return 1
            else:
                return 0
        elif direction == DOWN:
            self.cabeca[1] += 20
            self.direction = DOWN
            if self.cabeca[1] > height - 30:
                return 1
            else:
                return 0


class Food():

    def __init__(self, snake):
        while True:
            x1 = randint(0, 20)
            y1 = randint(0, 17)
            self.foodXY = [int(x1 * 20) + 10, int(y1 * 20) + 120]
            if snake.corpo.count(self.foodXY) == 0:
                break


if __name__ == "__main__":
    # call
    Game(440, 510, 8).run()