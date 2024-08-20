import pygame
import os
from grid import Grid

# set the window position relative to the screen upper left corner
os.environ['SOL_VIDEO_WINDOW_POS'] = "%d,%d" % (400, 100)

# create the window surface and set the window caption
surface = pygame.display.set_mode((1200, 825))
pygame.display.set_caption('Sudoku')

pygame.font.init()
game_font = pygame.font.SysFont('Comic Sans MS', 50)

grid = Grid(game_font)
running = True

# the game loop
while running:
    
    # check for input events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.win:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                grid.get_mouse_click(pos[0], pos[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.win:
                grid.restart()
    
    # clear window surface to black
    surface.fill((255, 255, 255))

    # draw grid lines
    grid.draw_all(pygame, surface)

    if grid.win:
        win_surface = game_font.render("You won!", False, (0, 255, 0))
        surface.blit(win_surface, (250, 200))

        restart_surface = game_font.render("Press space to restart!", False, (0, 255, 200))
        surface.blit(restart_surface, (220, 300))

    # update window surface
    pygame.display.flip()