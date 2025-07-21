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

#spawning car
lane_index = random.randint(0, 3)#random lane 
car_x = lane_positions[lane_index] - car_width // 2
car_y = SCREEN_HEIGHT - car_height - 0.1 

#main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(grey)

    #lines inbetween lanes
    for i in range(1, 4):
        x = lane_width * i
        pygame.draw.rect(screen, white, (x - 5, 0, 10, SCREEN_HEIGHT))

    #drawing car
    screen.blit(car_image, (car_x, car_y))

    pygame.display.update()
    clock.tick(60)

pygame.quit()   