#PONG GAME
import pygame, sys, random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.font.init()


class Player:
    def __init__(self, pos_x, pos_y, img_path, PLAYER_MOV_X):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.PLAYER_MOV_X = PLAYER_MOV_X
        self.img_path = img_path
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x, pos_y)
        self.score = 0

    def update(self):
        print(self.score)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Ball:

    def __init__(self, img_path, x, y):
        self.x = x
        self.y = y
        self.img_path = img_path
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.SPEED_DX = 3 * random.choice([1, -1])
        self.SPEED_DY = 3 * random.choice([1, -1])

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update_ball(self):
        global start_time, GAME_STATE, MAX_GAME_POINT
        self.rect.x += self.SPEED_DX
        self.rect.y += self.SPEED_DY
        if self.rect.top <= 0:
            if player_1.score == MAX_GAME_POINT - 1:
                GAME_STATE = "game_over"
                player_1.score += 1
                game_over(1)
            else:
                print(player_2.score)
                start_time = pygame.time.get_ticks()
                GAME_STATE = 'ready'
                self.rect.y = CANVAS_HEIGHT / 2 -14
                self.rect.x = CANVAS_WIDTH/2
                self.SPEED_DY *= -1
                player_1.score += 1
                pygame.mixer.Sound.play(SCORE_UP)

        if self.rect.bottom >= CANVAS_HEIGHT:
            if player_2.score == MAX_GAME_POINT - 1:
                GAME_STATE = "game_over"
                player_2.score += 1
                game_over(2)
            else:
                self.rect.y = CANVAS_HEIGHT / 2 -14
                self.rect.x = CANVAS_WIDTH / 2
                start_time = pygame.time.get_ticks()
                GAME_STATE = 'ready'
                self.SPEED_DY *= -1
                player_2.score += 1
                pygame.mixer.Sound.play(SCORE_UP)
        if self.rect.left <= 0 or self.rect.right >= CANVAS_WIDTH:
            self.SPEED_DX *= -1

    def collisition_detect(self):
        if pygame.Rect.colliderect(self.rect, player_1.rect) and self.SPEED_DY>0:
            self.SPEED_DY *= -1
            pygame.mixer.Sound.play(PLAYER_1_HIT)
        if pygame.Rect.colliderect(self.rect, player_2.rect) and self.SPEED_DY<0:
            self.SPEED_DY *= -1
            pygame.mixer.Sound.play(PLAYER_2_HIT)


        # if pygame.Rect.colliderect(self.rect, player_1.rect):
        #     self.SPEED_DY *= -1
        #     pygame.mixer.Sound.play(PLAYER_1_HIT)
        # if pygame.Rect.colliderect(self.rect, player_2.rect):
        #     self.SPEED_DY *= -1
        #     pygame.mixer.Sound.play(PLAYER_2_HIT)


def disply_background():
    screen.blit(BACKGROUND, (0, 0))


def count_down(game_stop):
    global GAME_STATE

    if pygame.time.get_ticks() - game_stop < 1500:
        count_time = GAME_FONT.render("READY", False, (127, 235, 191))
        screen.blit(count_time, (CANVAS_WIDTH / 2 - 30, CANVAS_HEIGHT / 2 - 100))
    elif pygame.time.get_ticks() - game_stop < 2500:
        count_time = GAME_FONT.render("1", False, (127, 235, 191))
        screen.blit(count_time, (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 100))
    elif pygame.time.get_ticks() - game_stop < 3500:
        count_time = GAME_FONT.render("2", False, (127, 235, 191))
        screen.blit(count_time, (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 100))
    elif 3501 < pygame.time.get_ticks() - game_stop < 4000:
        count_time = GAME_FONT.render("START", False, (0, 224, 133))
        screen.blit(count_time, (CANVAS_WIDTH / 2 - 25, CANVAS_HEIGHT / 2 - 100))
    else:
        GAME_STATE = 'active'


def game_over(winner):
    global win
    pygame.mixer.Sound.play(WIN)
    win = GAME_FONT.render(f"WINNER : Player {winner}", False, (25, 250, 250))


def restart_game():
    global player_1, player_2, GAME_STATE, SPEED_DY, tennis_ball, start_time
    del player_2
    del player_1
    del tennis_ball
    player_1 = Player(CANVAS_WIDTH / 2, PLAYER_1_Y_POS, "red_player.png", PLAYER_MOV_X)
    player_2 = Player(CANVAS_WIDTH / 2, PLAYER_2_Y_POS, "yellow_player.png", PLAYER_MOV_X)
    tennis_ball = Ball("ball.png", CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
    GAME_STATE = "ready"
    start_time = pygame.time.get_ticks()
    count_down(start_time)


FPS = 120
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 650
PLAYER_1_Y_POS = 600
PLAYER_2_Y_POS = 50
PLAYER_MOV_X = 70
GAME_STATE = 'ready'
MAX_GAME_POINT = 9
GAME_FONT = pygame.font.Font("freesansbold.ttf", 17)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
BACKGROUND = pygame.image.load("pong_bck.png")

PLAYER_1_HIT = pygame.mixer.Sound("p_1.wav")
PLAYER_2_HIT = pygame.mixer.Sound("p_2.wav")
SCORE_UP = pygame.mixer.Sound("add_score.wav")
WIN = pygame.mixer.Sound("win.mp3")

player_1 = Player(CANVAS_WIDTH / 2, PLAYER_1_Y_POS, "red_player.png", PLAYER_MOV_X)
player_2 = Player(CANVAS_WIDTH / 2, PLAYER_2_Y_POS, "yellow_player.png", PLAYER_MOV_X)

tennis_ball = Ball("ball.png", CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2)
start_time = 0

while True:
    clock.tick(FPS)
    player_1_score = GAME_FONT.render(f"Player 1 : {player_1.score}", False, (255, 0, 0))
    player_2_score = GAME_FONT.render(f"Player 2 : {player_2.score}", False, (252, 240, 3))

    disply_background()
    player_1.draw(screen)
    player_2.draw(screen)
    screen.blit(player_1_score, (CANVAS_WIDTH / 2 - 50, CANVAS_HEIGHT - 30))
    screen.blit(player_2_score, (CANVAS_WIDTH / 2 - 50, 10))
    tennis_ball.draw(screen)

    if GAME_STATE == 'active':
        tennis_ball.collisition_detect()
        tennis_ball.update_ball()

    if GAME_STATE == 'ready':
        count_down(start_time)
    if GAME_STATE == 'game_over':
        global win
        restart = GAME_FONT.render(f"  Press space to Restart", False, (250, 250, 250))
        screen.blit(win, (CANVAS_WIDTH / 2 - 80, CANVAS_HEIGHT / 2 - 30))
        screen.blit(restart, (CANVAS_WIDTH / 2 - 100, CANVAS_HEIGHT / 2 + 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and GAME_STATE == 'game_over':
            restart_game()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if player_1.rect.x <= CANVAS_WIDTH - 50:
                player_1.rect.x += PLAYER_MOV_X
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if player_1.rect.x >= 0:
                player_1.rect.x -= PLAYER_MOV_X
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            if player_2.rect.x < CANVAS_WIDTH - 50:
                player_2.rect.x += PLAYER_MOV_X
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if player_2.rect.x >= 0:
                player_2.rect.x -= PLAYER_MOV_X

    pygame.display.update()
