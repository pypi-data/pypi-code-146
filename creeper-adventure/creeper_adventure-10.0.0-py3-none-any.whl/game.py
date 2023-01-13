import pygame


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(__file__)

        self.screen_size = (854, 480)
        self.screen_size = (1280, 800)
        self.screen_size = (1920, 1080)
        # pygame.display.set_mode(resolution, flags, bpp)
        flags = pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode(self.screen_size, flags)
        self.clock = pygame.time.Clock()

        self.running = True
        self.surfs = []
        self.elapsed = 0

    def should_quit(self):
        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

    def game(self):
        ...

    def reset_screen(self):
        ...
        # self.screen.fill((0, 0, 0))

    def run(self):
        while self.running:
            self.events = pygame.event.get()
            self.should_quit()
            self.reset_screen()
            self.keys = pygame.key.get_pressed()
            self.game()
            for surf in self.surfs:
                pygame.blit(surf)
            pygame.display.update()
            self.elapsed = self.clock.tick(60) / 100
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
