from .scenes import Scenes 
from src.scenes import SceneBase
import pygame
from pygame.locals import *

class Credits(SceneBase):
    def __init__(self):
        super().__init__()

        if pygame.font:
            title_font = pygame.font.Font(None, 50)
            text_font = pygame.font.Font(None, 36)

            title = title_font.render("Cuatro en Raya", 1, (255, 255, 255))
            title_pos = title.get_rect(centerx=self.background.get_width()/2, centery=self.background.get_height()/2 - 100)

            credits = [
                "Agradecimientos especiales: OpenAI , Claude y GitHub Copilot"
            ]

            for i, line in enumerate(credits):
                text = text_font.render(line, 1, (255, 255, 255))
                text_pos = text.get_rect(centerx=self.background.get_width()/2, centery=self.background.get_height()/2 + 50 + i*40)
                self.background.blit(text, text_pos)

            self.background.blit(title, title_pos)

    def process_input(self, scene_manager):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                scene_manager.update(Scenes.MENU)
                return False
        return False