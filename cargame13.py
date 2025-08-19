import pygame, time, random, os
pygame.init()

# setting the size of the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 
                                 pygame.RESIZABLE)

# setting the icon and name for the game
game_icon = pygame.image.load('caricon.jpg')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Car game")

# colour specifics
grey = (105, 105, 105)
white = (250, 249, 246)

clock = pygame.time.Clock()

# car properties
car_width = 135
car_height = 135
car_speed = 8

# lanesetup
lane_width = SCREEN_WIDTH // 4
lane_positions = [
    lane_width * 0 + lane_width // 2,
    lane_width * 1 + lane_width // 2,
    lane_width * 2 + lane_width // 2,
    lane_width * 3 + lane_width // 2
]  # lanes in a list

# car setup
car_image = pygame.image.load("silvercar.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (car_width, car_height))

opposing_car_image = pygame.image.load("yellowcar.png").convert_alpha()
opposing_car_image = pygame.transform.scale(opposing_car_image, 
                                            (car_width, car_height))

# spawning car
lane_index = random.randint(0, 3)  # random lane 
car_x = lane_positions[lane_index] - car_width // 2
car_y = SCREEN_HEIGHT - car_height - 0.1 


# class for opposing cars
class EnemyCar:
    """represents the cars the the user has to dodge"""
    def __init__(self, 
                 image, 
                 lane_index, 
                 lane_positions, 
                 car_width, 
                 car_height, 
                 screen_height
    ): 
        self.image = image
        self.lane_positions = lane_positions
        self.lane_index = lane_index
        self.car_width = car_width
        self.car_height = car_height
        self.screen_height = screen_height
        self.reset()

    def reset(self):

        """reseting the car at the top of the screen"""
        self.x = self.lane_positions[self.lane_index] - self.car_width // 2 
        self.y = random.randint(-800, -100)  # positioning at top of screen
        self.speed = random.randint(4,8)

    
    def update(self):

        """moving the car down the screen by its speed"""
        self.y += self.speed
        if self.y > self.screen_height:
            self.reset()  # resets to new random lane
            return True
        return False

    def draw(self, screen):

        """drawing car on the screen"""
        screen.blit(self.image, (self.x, self.y))

opposing_cars = []


for lane_index in range(4):  # creating opposing cars
    enemy = EnemyCar(opposing_car_image, 
                     lane_index, 
                     lane_positions, 
                     car_width, 
                     car_height, 
                     SCREEN_HEIGHT
                     )
    opposing_cars.append(enemy)


def start_screen():
    """start screen"""
    font_1 = pygame.font.SysFont(None, 72)
    font_2 = pygame.font.SysFont(None, 48)

    title_text = font_1.render("Car Game", True, white)
    start_text = font_2.render("Press S to Start", True, white)

    while True:
        screen.fill(grey)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 
                                 SCREEN_HEIGHT // 3))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 
                                 SCREEN_HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return  # exit the start screen loop

def game_over_screen(score):
    """options after dying"""
    font_1 = pygame.font.SysFont(None, 72)
    font_2 = pygame.font.SysFont(None, 48)

    # texts showing on screen
    game_over_text = font_1.render("Game Over", True, white)
    restart_text = font_2.render(
        "Press R to Restart or Q to Quit", 
                                 True, 
                                 white)
    high_score_text = font_2.render(f"High Score: {high_score}", True, white)
    score_text = font_2.render(f"Your Score: {score}", True, white)

    # where on the screen the message shows
    while True:
        screen.fill(grey)
        screen.blit(game_over_text, (
            SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
            SCREEN_HEIGHT // 3.5))
        screen.blit(restart_text, (
            SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
            SCREEN_HEIGHT // 1.7))
        screen.blit(score_text, (
            SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
            SCREEN_HEIGHT // 2.5))
        screen.blit(high_score_text, (
            SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 
            SCREEN_HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return  # go back and restart the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()  # quit the game


# score
score = 0
score_font = pygame.font.SysFont(None, 48)
high_score = 0

def load_high_score():


    """load high score from file"""
    if os.path.exists("high_score.txt"):  # checking if file exists
        with open("high_score.txt", "r") as file:
            return int(file.read().strip())  # reading and cleaning text
    return 0  # if no filem then high score = 0

def save_high_score(score):


    """save high score to file"""
    with open("high_score.txt", "w") as file:  
        # replacing or creating file for high score
        file.write(str(score))  # writing new high score

high_score = load_high_score()


start_screen()

# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # checking which keys getting pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= car_speed  # move left
    if keys[pygame.K_RIGHT]:
        car_x += car_speed  # move right

    screen.fill(grey)

    # lines inbetween lanes
    for i in range(1, 4):
        x = lane_width * i
        pygame.draw.rect(screen, white, (x - 5, 0, 10, SCREEN_HEIGHT))

    # drawing car
    screen.blit(car_image, (car_x, car_y))

    # drawing enemy cars
    for enemy in opposing_cars:
        if enemy.update():
            score += 1
        enemy.draw(screen)
    
    # drawing score
    score_text = score_font.render(f"Score: {score}", True, white)  # message
    screen.blit(score_text, (20, 20))  # where on screen

    # rectangle for user car
    player_rect = pygame.Rect(
        car_x + 30, 
        car_y + 7, 
        car_width - 59, 
        car_height - 9)

    # check for collision with each enemy car
    for enemy in opposing_cars:
        enemy_rect = pygame.Rect(
            enemy.x + 33, 
            enemy.y + 7, 
            car_width - 62.5, 
            car_height - 9)  # plus and minus to shrink hitboxes
        if player_rect.colliderect(enemy_rect):
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            game_over_screen(score)
        
            score = 0
            score_timer = pygame.time.get_ticks()

            # reseting cars
            lane_index = random.randint(0, 3)
            car_x = lane_positions[random.randint(0, 3)] - car_width // 2
            for enemy in opposing_cars:
                enemy.reset()  
            break  # exits loop so it doesnt trigger again

    pygame.display.update()
    clock.tick(60)

pygame.quit()