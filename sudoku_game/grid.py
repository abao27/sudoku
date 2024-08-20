from random import sample
from number_button import NumberButton
from gamemodes import GameModes
import pygame
from copy import deepcopy

def create_line_coordinates(size: int) -> list[list[tuple]]:
    pts = []
    for y in range(1, 11):
        pts.append([(75, y * size), (750, y * size)])
    for x in range(1, 11):
        pts.append([(x * size, 75), (x * size, 750)])
    #print(pts)
    return pts


SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE ** 2


def pattern(row: int, col: int) -> int:
    return (SUB_GRID_SIZE * (row % SUB_GRID_SIZE) + row // SUB_GRID_SIZE + col) % GRID_SIZE

def shuffle(sample_range: range) -> list:
    return sample(sample_range, len(sample_range))

def create_grid(subgrid: int) -> list[list]:
    # Creates the 9x9 grid filled with random numbers
    row_base = range(subgrid)
    rows = [g * subgrid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * subgrid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, subgrid ** 2 + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]

def remove_numbers(grid: list[list]) -> None:
    # randomly sets numbers to 0 on the grid
    num_cells = GRID_SIZE ** 2
    empties = num_cells * 3 // 7     # 5
    for i in sample(range(num_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0

def remove_numbers1(grid: list[list], difficulty: str) -> None:
    # randomly sets numbers to 0 on the grid
    num_cells = GRID_SIZE ** 2
    n = 7
    if difficulty == "Medium":
        n = 5
    elif difficulty == "Hard":
        n = 4
    empties = num_cells * 3 // n      # 5
    for i in sample(range(num_cells), empties):
        grid[i // GRID_SIZE][i % GRID_SIZE] = 0

class Grid:
    def __init__(self, font):
        self.win = False
        self.cell_size = 75
        self.x_offset = 25
        self.y_offset = 0
        self.line_coordinates = create_line_coordinates(self.cell_size)
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__testgrid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.unplayable = self.unplayable_cells()
        #print(self.unplayable)

        self.game_font = font
        self.difficulty = "Easy"

        self.number_buttons = NumberButton(pygame, self.game_font)
        self.gamemode = GameModes(pygame, self.game_font)
    
    def get_mouse_click(self, x: int, y: int) -> None:
        if x <= 750 and y <= 750:
            grid_x, grid_y = x // 75 - 1, y // 75 - 1
            print(grid_x, grid_y)
            if self.is_playable(grid_x, grid_y):
                #print("played")
                self.set_cell(grid_x, grid_y, self.number_buttons.selected_num)
        self.number_buttons.button_clicked(x, y)
        self.gamemode.button_clicked(x, y)

        if self.gamemode.selected_difficulty != self.difficulty:
            self.difficulty = self.gamemode.selected_difficulty
            self.restart1(self.gamemode.selected_difficulty)

        if self.check_grids():
            print("You win!")
            self.win = True

    def restart(self) -> None:
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__testgrid = deepcopy(self.grid)
        remove_numbers(self.grid)
        self.unplayable = self.unplayable_cells()
        self.win = False
    
    def restart1(self, difficulty: str) -> None:
        self.grid = create_grid(SUB_GRID_SIZE)
        self.__testgrid = deepcopy(self.grid)
        remove_numbers1(self.grid, difficulty)
        self.unplayable = self.unplayable_cells()
        self.win = False
    
    def check_grids(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if self.grid[y][x] != self.__testgrid[y][x]:
                    return False
        return True

    def unplayable_cells(self) -> list[tuple]:
        # gather y, x coordinates for all pre-filled cells
        filled = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.get_cell(y, x) != 0:
                    filled.append((y, x))
        return filled
    
    def is_playable(self, x: int, y: int):
        return (x, y) not in self.unplayable

    def __draw_lines(self, pg, surface) -> None:
        # draws grid lines
        for idx, line in enumerate(self.line_coordinates):
            if idx in [0, 3, 6, 9, 10, 13, 16, 19]:
                pg.draw.line(surface, (0, 0, 0), line[0], line[1], 4)
            else:
                pg.draw.line(surface, (137, 207, 240), line[0], line[1], 2)
        
    def __draw_numbers(self, surface) -> None:
        # draw the grid numbers
        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                if self.get_cell(x, y) != 0:
                    if (x, y) in self.unplayable:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (105, 105, 105))
                    else:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (100,149,237))

                    if self.get_cell(x, y) != self.__testgrid[y][x]:
                        text_surface = self.game_font.render(str(self.get_cell(x, y)), False, (255, 0, 0))
                    surface.blit(text_surface, ((x + 1) * self.cell_size + self.x_offset, (y + 1) * self.cell_size + self.y_offset))

    def draw_all(self, pg, surface):
        self.__draw_lines(pg, surface)
        self.__draw_numbers(surface)
        self.number_buttons.draw(pg, surface)
        self.gamemode.draw(pg, surface)

    def get_cell(self, x: int, y: int) -> int:
        # get a cell value at y, x coordinate
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, value: int) -> int:
        # set cell value at y, x coordinate
        self.grid[y][x] = value

    def show(self):
        # prints the grid row by row to the output
        for cell in self.grid:
            print(cell)


if __name__ == "__main__":
    grid = Grid("Comic Sans MS")
    grid.show()