
class NumberButton:

    def __init__(self, pygame, font):
        self.pygame = pygame
        self.width = 90
        self.height = 90
        self.my_font = font
        self.selected_num = 0

        self.color_selected = (137, 207, 240)
        self.color_normal = (200, 200, 200)

        '''self.pos = [(840, 390), (930, 390), (1020, 390),
            (840, 480), (930, 480), (1020, 480),
            (840, 570), (930, 570), (1020, 570),
            (930, 660)]'''
        
        self.pos = [(840, 440), (930, 440), (1020, 440),
            (840, 530), (930, 530), (1020, 530),
            (840, 620), (930, 620), (1020, 620),
            (930, 710)]
    
    def draw(self, pygame, surface):
        for idx, pos in enumerate(self.pos):
            pygame.draw.rect(surface, self.color_normal, [pos[0], pos[1], self.width, self.height], 3, 10)
            
            # checking for mouse hover
            if self.button_hover(pos):
                pygame.draw.rect(surface, (112, 128, 144), [pos[0], pos[1], self.width, self.height], 3, 10)
                text_surface = self.my_font.render(str(idx + 1), False, (112, 128, 144))
                if idx >= 9:
                    text_surface = self.my_font.render("x", False, (112, 128, 144))
            else:
                text_surface = self.my_font.render(str(idx + 1), False, self.color_normal)
                if idx >= 9:
                    text_surface = self.my_font.render("x", False, self.color_normal)

            if self.selected_num > 0:
                if self.selected_num - 1 == idx:
                    pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.width, self.height], 3, 10)
                    text_surface = self.my_font.render(str(idx + 1), False, self.color_selected)
                    if idx >= 9:
                        text_surface = self.my_font.render("x", False, self.color_selected)

            surface.blit(text_surface, (pos[0] + 32, pos[1] + 5))

    def button_clicked(self, x: int, y: int) -> None:
        for idx, pos in enumerate(self.pos):
            if self.on_button(x, y, pos):
                self.selected_num = (idx + 1) % 10

    def button_hover(self, pos: tuple) -> bool | None:
        mouse_pos = self.pygame.mouse.get_pos()
        if self.on_button(mouse_pos[0], mouse_pos[1], pos):
            return True
        

    def on_button(self, x: int, y: int, pos: tuple) -> bool:
        return x > pos[0] and x < pos[0] + self.width and y > pos[1] and y < pos[1] + self.height