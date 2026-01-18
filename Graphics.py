import pygame


class Button:
    def __init__(self, image: pygame.Surface, x: int = 0, y: int = 0, scale: float = 1):
        img_width, img_hight = image.get_width(), image.get_height()
        self._image = pygame.transform.scale(
            image, (int(img_width * scale), int(img_hight * scale)))

        self._scale = scale
        self._rect = self._image.get_rect()
        self._rect.topleft = (x, y)
        self._clicked = False

    @property
    def image(self) -> pygame.Surface:
        return self._image

    @image.setter
    def image(self, new_image: pygame.image):
        img_width, img_hight = new_image.get_width(), new_image.get_height()
        self._image = pygame.transform.scale(
            new_image, (int(img_width * self._scale), int(img_hight * self._scale)))

    def is_clicked(self) -> bool:
        been_clicked = False

        mouse_pos = pygame.mouse.get_pos()

        if self._rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self._clicked:
                self._clicked = True
                been_clicked = True

        # if pygame.mouse.get_pressed()[0] == 0:
        #   self._clicked = False

        return been_clicked

    def draw(self, screen: pygame.Surface):
        screen.blit(self._image, (self._rect.x, self._rect.y))


def display_text(text: str, screen: pygame.Surface, x: int = 0, y: int = 0):
    font = pygame.font.Font("PressStart2P-Regular.ttf", 32)
    message = font.render(text, True)
    message_rect = message.get_rect()
    message_rect.topleft = (x, y)

    screen.blit(message, message_rect)
