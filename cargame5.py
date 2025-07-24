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
car_speed = 8

#lanesetup
lane_width = SCREEN_WIDTH // 4
lane_positions = [
    lane_width * 0 + lane_width // 2,
    lane_width * 1 + lane_width // 2,
    lane_width * 2 + lane_width // 2,
    lane_width * 3 + lane_width // 2
]#lanes in a list

#car setup
car_image = pygame.image.load("silvercar.png").convert_alpha()
car_image = pygame.transform.scale(car_image, (car_width, car_height))

opposing_car_image = pygame.image.load("yellowcar.png").convert_alpha()
opposing_car_image = pygame.transform.scale(opposing_car_image, (car_width, car_height))

#spawning car
lane_index = random.randint(0, 3)#random lane 
car_x = lane_positions[lane_index] - car_width // 2
car_y = SCREEN_HEIGHT - car_height - 0.1 


#class for opposing cars
class EnemyCar:
    def __init__(self, image, lane_positions, car_width, car_height, screen_height):#setup
        self.image = image
        self.lane_positions = lane_positions
        self.car_width = car_width
        self.car_height = car_height
        self.screen_height = screen_height
        self.reset()
    
    def reset(self):#reset to top of screen
        self.lane_index = random.randint(0, 3) #choosing lane to spawn in randomly
        self.x = self.lane_positions[self.lane_index] - self.car_width // 2 
        self.y = random.randint(-800, -100) #positioning at top of screen
    
    def update(self):
        self.y += 5
        if self.y > self.screen_height:
            self.reset()#resets to new random lane

    #drawing the car on the screen
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

opposing_cars = []
for _ in range(4):  #creating opposing cars
    enemy = EnemyCar(opposing_car_image, lane_positions, car_width, car_height, SCREEN_HEIGHT)
    opposing_cars.append(enemy)

#options after dying
def game_over_screen():
    font_1 = pygame.font.SysFont(None, 72)
    font_2 = pygame.font.SysFont(None, 48)

    game_over_text = font_1.render("Game Over", True, white)
    restart_text = font_2.render("Press R to Restart or Q to Quit", True, white)

    #where on the screen the message shows
    while True:
        screen.fill(grey)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return#go back and restart the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()#quit the game

#main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over_screen()

    
    #checking which keys getting pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        car_x -= car_speed #move left
    if keys[pygame.K_RIGHT]:
        car_x += car_speed #move right

    screen.fill(grey)

    #lines inbetween lanes
    for i in range(1, 4):
        x = lane_width * i
        pygame.draw.rect(screen, white, (x - 5, 0, 10, SCREEN_HEIGHT))

    #drawing car
    screen.blit(car_image, (car_x, car_y))

    #drawing enemy cars
    for enemy in opposing_cars:
        enemy.update()
        enemy.draw(screen)
    
    #rectangle for user car
    player_rect = pygame.Rect(car_x, car_y, car_width, car_height)

    #check for collision with each enemy car
    for enemy in opposing_cars:
        enemy_rect = pygame.Rect(enemy.x, enemy.y, car_width, car_height)
        if player_rect.colliderect(enemy_rect):
            running = False  #end the game when collision detected
            game_over_screen()
            
            #reseting cars
            lane_index= random.randint(0,3)
            car_x = lane_positions[random.randint(0, 3)] - car_width // 2
            for enemy in opposing_cars:
                enemy.reset()  
            break#exits loop so it doesnt trigger again

    pygame.display.update()
    clock.tick(60)

pygame.quit() 