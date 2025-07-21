import pygame, time, random
pygame.init()

#setting the size of the screen
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.RESIZABLE)

#Setting the icon and name for the game
game_icon = pygame.image.load('caricon.jpg')
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Car game")

#colour specifics
grey = (105, 105, 105)
white = (250, 249, 246)

clock = pygame.time.Clock()

#car properties
car_width = 135
car_height = 135

#approaching car properties
car2_width = 170
car2_height = 170

#options for where the car can spawn, in a list
lane_positions = [
    SCREEN_WIDTH // 8 - car_width // 2,            # Lane 1
    SCREEN_WIDTH // 4 + SCREEN_WIDTH // 8 - car_width // 2,  # Lane 2
    SCREEN_WIDTH // 2 + SCREEN_WIDTH // 8 - car_width // 2,  # Lane 3
    SCREEN_WIDTH - SCREEN_WIDTH // 8 - car_width // 2        # Lane 4
]
lane_number = random.randint(0, 3)
car_x = lane_positions[lane_number]
car_y = SCREEN_HEIGHT // 1.22
#options for approaching cars to spawn
lane_positions2 = [
    SCREEN_WIDTH // 8 - car_width // 2 - 15,            # Lane 1
    SCREEN_WIDTH // 4 + SCREEN_WIDTH // 8 - car_width // 2 - 15,  # Lane 2
    SCREEN_WIDTH // 2 + SCREEN_WIDTH // 8 - car_width // 2 - 15,  # Lane 3
    SCREEN_WIDTH - SCREEN_WIDTH // 8 - car_width // 2 - 15        # Lane 4
]
lane_number = random.randint(0, 3)
car2_x = lane_positions2[lane_number]
car2_y = random.randint(-800, -100)
#line/lane variables
lines_width = 10
lines_height = 720
line1_x = SCREEN_WIDTH // 4 - 5
line2_x = SCREEN_WIDTH // 2 - 5
line3_x = 445


#loading sprite for car
car_image = pygame.image.load("silvercar.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (car_width, car_height)) # Resize to fit car dimensions
#sprite for approaching car
crashcar_image = pygame.image.load("opoocar1.png").convert_alpha()
crashcar_image = pygame.transform.scale(crashcar_image, (car2_width, car2_height))

#class for approaching cars
class crashcars:
    def __init__(self, crashcar_image, lane_positions2, car_width, car_height, screen_height):
        self.crashcar_image = crashcar_image
        self.lane_positions2 = lane_positions2
        self.car_width = car2_width
        self.car_height = car2_height
        self.screen_height = screen_height
        self.reset()

    def reset(self):
        self.lane_number = random.randint(0, 3)#picking lane number
        self.x = self.lane_positions2[self.lane_number]
        self.y = random.randint(-800, -100)#starts the cars above the screen

    def update(self):
        self.y += 5#speed of cars coming down screen
        if self.y > self.screen_height:
            self.reset()#resets car back to top when it passes the bottom of screen
    
    #drawing the cars
    def draw(self, screen):
        screen.blit(self.crashcar_image, (self.x, self.y))

#creating the other cars
crash_cars = []
for _ in range(4):
    enemy = crashcars(crashcar_image, lane_positions2, car_width, car_height, SCREEN_HEIGHT)#specifics of the cars
    crash_cars.append(enemy)

#game loop
running = True
while running:
    screen.fill(grey)#filling the background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and lane_number > 0:
                lane_number -= 1
                car_x = lane_positions[lane_number]
            if event.key == pygame.K_RIGHT and lane_number < 3:
                lane_number += 1
                car_x = lane_positions[lane_number]

            
   
    for enemy in crash_cars:
        enemy.update()
        enemy.draw(screen)

    #rectangles for collision detection
    player_rect = pygame.Rect(car_x, car_y, car_width, car_height)
    enemy_rect = pygame.Rect(enemy.x, enemy.y, car_width, car_height)

    for enemy in crash_cars:
        if player_rect.colliderect(enemy_rect):
            running = False
            
    pygame.draw.rect(screen, white, (line1_x, 0, lines_width, lines_height))
    pygame.draw.rect(screen, white, (line2_x, 0, lines_width, lines_height))
    pygame.draw.rect(screen, white, (line3_x, 0, lines_width, lines_height))

    screen.blit(car_image, (car_x, car_y))#making the car image appear

    pygame.display.update()

    clock.tick(60)

pygame.quit()
