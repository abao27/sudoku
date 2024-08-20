
class GameModes:

    def __init__(self, pygame, font):
        self.pygame = pygame
        self.width = 180
        self.height = 60
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.selected_difficulty = "Easy"

        self.color_selected = (137, 207, 240)
        self.color_normal = (200, 200, 200)
        
        self.pos = [(840, 150), (840, 220), (840, 290)]
        self.gamemodes = ["Easy", "Medium", "Hard"]
    
    def draw(self, pygame, surface):
        for idx, pos in enumerate(self.pos):
            pygame.draw.rect(surface, self.color_normal, [pos[0], pos[1], self.width, self.height], 3, 10)
            
            # checking for mouse hover
            if self.button_hover(pos):
                pygame.draw.rect(surface, (112, 128, 144), [pos[0], pos[1], self.width, self.height], 3, 10)
                text_surface = self.my_font.render(self.gamemodes[idx], False, (112, 128, 144))
            else:
                text_surface = self.my_font.render(self.gamemodes[idx], False, self.color_normal)

            if self.gamemodes[idx] == self.selected_difficulty:
                pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.width, self.height], 3, 10)
                text_surface = self.my_font.render(self.gamemodes[idx], False, self.color_selected)

            surface.blit(text_surface, (pos[0] + 32, pos[1] + 5))

    def button_clicked(self, x: int, y: int) -> None:
        for idx, pos in enumerate(self.pos):
            if self.on_button(x, y, pos):
                self.selected_difficulty = self.gamemodes[idx]

    def button_hover(self, pos: tuple) -> bool | None:
        mouse_pos = self.pygame.mouse.get_pos()
        if self.on_button(mouse_pos[0], mouse_pos[1], pos):
            return True
        

    def on_button(self, x: int, y: int, pos: tuple) -> bool:
        return x > pos[0] and x < pos[0] + self.width and y > pos[1] and y < pos[1] + self.height