import random
from copy import copy
from itertools import cycle, repeat
from pathlib import Path

import pygame
from more_itertools import flatten

from creeper_adventure.game import Game

ASSETS = Path(__file__).parent / "assets"


class MouseSprite:
    def __init__(self, game, surf, hotbar):
        self.game = game
        self.surf = surf
        self.hotbar = hotbar

    @property
    def mouse_pos(self):
        return (
            pygame.mouse.get_pos()[0] - 2 - self.game.camera[0],
            pygame.mouse.get_pos()[1] - 2 - self.game.camera[1],
        )

    @property
    def rect(self):
        return pygame.Rect(self.mouse_pos, (4, 4))

    def get_nearest_block_pos(self):
        return (
            [
                self.mouse_pos[0] - (self.mouse_pos[0] % 16),
                self.mouse_pos[1] - (self.mouse_pos[1] % 16),
            ],
        )

    def draw(self):
        if self.hotbar.selected.type is None:
            pygame.draw.rect(self.surf, (255, 0, 0), self.rect)
        else:
            self.img = self.game.get_img(self.hotbar.selected.type).convert()
            self.surf.blit(
                pygame.transform.scale(self.img, (64, 64)),
                self.get_nearest_block_pos(),
            )


class TreeSprite:
    def __init__(self, game, tree, x, y, scale, flip, surf):
        self.game = game
        self.image = tree
        self.health = 100
        self.x = x
        self.y = y
        self.scale = scale
        self.flip = flip
        self.surf = surf
        self.leafs = [Leaf(self.game, self.surf, (x + 25, y + 25)) for i in range(2)]
        self.shaking = 0

    def shake(self):
        if self.shaking == 0:
            self.shaking = 10
            self.shaking_magnitude = random.randint(0, 10)
        self.leafs.extend(
            [
                Leaf(
                    self.game,
                    self.surf,
                    (
                        self.x + 25 + random.randint(-10, 10),
                        self.y + 25 + random.randint(-10, 10),
                    ),
                    lifespan=1,
                )
                for i in range(int(self.shaking_magnitude / 2))
            ]
        )

    @property
    def rotate(self):
        if self.shaking == 0:
            return 0
        self.shaking -= 1
        return random.randint(-self.shaking_magnitude, self.shaking_magnitude)

    @property
    def rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.scale,
            self.scale,
        )

    def draw(self):
        if self.health > 0:
            self.surf.blit(
                pygame.transform.rotate(
                    pygame.transform.flip(
                        pygame.transform.scale(self.image, (self.scale, self.scale)),
                        self.flip,
                        False,
                    ),
                    self.rotate,
                ),
                (self.x, self.y),
            )
            for leaf in self.leafs:
                leaf.draw()


class HotBar:
    def __init__(self, game: Game, scale=32, num=10, margin=None):
        if margin is None:
            margin = scale * 0.1
        self.scale = scale
        self.num = num
        self.margin = margin
        self.ui = pygame.Surface(
            (self.scale * self.num, self.scale), pygame.SRCALPHA, 32
        ).convert_alpha()
        self.game = game
        self.items = [
            HotBarItem(
                game=self.game,
                surf=self.ui,
                pos=pos,
                scale=self.scale,
                margin=self.margin,
            )
            for pos in range(num)
        ]
        self.items[0].selected = True

    @property
    def selected(self):
        return [bar for bar in self.items if bar.selected][0]

    def next(self, step):
        cur_idx = self.items.index(self.selected)
        next_idx = cur_idx + step
        self.items[cur_idx].selected = False
        if next_idx >= len(self.items):
            self.items[0].selected = True
        elif next_idx < 0:
            self.items[-1].selected = True
        else:
            self.items[next_idx].selected = True

    def draw(self):
        self.ui.fill((50, 50, 50))
        for i, item in enumerate(self.game.inventory):
            self.items[i].type = item
        for hot_bar_item in self.items:
            hot_bar_item.draw()

        y = self.game.screen.get_size()[1] - self.scale - self.margin
        x = (self.game.screen.get_size()[0] - self.scale * self.num) / 2
        self.game.screen.blit(
            self.ui,
            (x, y),
        )


class HotBarItem:
    def __init__(self, game: Game, surf, pos=0, scale=24, margin=4):
        self.ui = surf
        self.game = game
        self.scale = scale
        self.margin = margin
        self.surf = pygame.Surface(
            (self.scale - self.margin * 2, self.scale - self.margin * 2)
        ).convert_alpha()
        self.pos = pos
        self.selected = False
        self.surf.fill((0, 0, 0))
        self.type = None

    def draw(self):
        self.surf.fill((0, 0, 0, 60))
        if self.selected:
            self.surf.fill((185, 185, 205, 60))

        if self.type:
            self.img = self.game.get_img(self.type)
            self.ui.blit(
                pygame.transform.scale(
                    self.img,
                    (self.scale - self.margin * 2, self.scale - self.margin * 2),
                ),
                (self.pos * self.scale + self.margin, self.margin),
            )
            font = pygame.font.SysFont(None, self.scale)
            qty = str(self.game.inventory[self.type])
            img = font.render(qty, True, (255, 255, 255))
            self.ui.blit(
                pygame.transform.scale(img, (self.scale * 0.6, self.scale * 0.6)),
                (self.pos * self.scale + self.margin, self.margin),
            )

        self.ui.blit(
            self.surf.convert_alpha(),
            (self.pos * self.scale + self.margin, self.margin),
        )


class Menu:
    def __init__(
        self,
        game: Game,
        title: str = "menu",
        scale: int = 32,
        margin: int = 16,
        alpha=225,
    ):
        self.game = game
        self.is_open = False
        self.title = title
        self.scale = scale
        self.margin = margin
        self.alpha = alpha

    def draw(self):
        if self.is_open:
            self.surf = pygame.Surface(self.game.screen.get_size()).convert_alpha()
            self.surf.fill((0, 0, 0, self.alpha))
            font = pygame.font.SysFont(None, self.scale)
            img = font.render(self.title, True, (255, 255, 255))
            self.surf.blit(
                img,
                (10, 10)
                # (100 * self.scale + self.margin, self.margin),
            )
            self._draw()

            self.game.screen.blit(self.surf, (0, 0))

    def _draw(self):
        ...


class DebugMenu(Menu):
    def __init__(self, game):
        super().__init__(title="Debug Menu", game=game, alpha=0)
        self.font = pygame.font.SysFont(None, 20)

    def _draw(self):
        self.surf.blit(
            self.font.render(
                f"(x, y): ({self.game.x}, {self.game.y})", True, (255, 255, 255)
            ),
            (10, 35),
        )
        self.surf.blit(
            self.font.render(
                f"mouse_pos: {pygame.mouse.get_pos()}", True, (255, 255, 255)
            ),
            (10, 50),
        )
        self.surf.blit(
            self.font.render(
                f"nearest block pos: {self.game.mouse_box.get_nearest_block_pos()}",
                True,
                (255, 255, 255),
            ),
            (10, 65),
        )
        self.surf.blit(
            self.font.render(
                f"walking sound: {self.game.walking_sound_is_playing}",
                True,
                (255, 255, 255),
            ),
            (10, 80),
        )
        self.surf.blit(
            self.font.render(
                f"fps: {round(self.game.clock.get_fps())}",
                True,
                (255, 255, 255),
            ),
            (10, 95),
        )
        self.surf.blit(
            self.font.render(
                f"fullscreen: {pygame.FULLSCREEN}",
                True,
                (255, 255, 255),
            ),
            (10, 110),
        )
        self.surf.blit(
            self.font.render(
                f"elapsed: {self.game.elapsed}",
                True,
                (255, 255, 255),
            ),
            (10, 125),
        )


class LightSource:
    def __init__(self, game: Game, surf, img, center):
        self.surf = surf
        self.game = game
        self.img = img
        self.center = center
        self.sx, self.sy = center
        self.spot = self.game.get_img("spotlight")


class Leaf:
    def __init__(self, game: Game, surf, center, lifespan=None):
        self.surf = surf
        self.game = game
        self.center = center
        self.sx, self.sy = center
        self.img = pygame.transform.scale(
            self.game.get_img("leaf"), (4, 4)
        )  # .convert_alpha()
        self.lifespan = lifespan
        self.r = random.randint(0, 360)
        self.x, self.y = [int(i) + random.randint(-8, 8) for i in self.center]
        self.speed = 3
        self.restart()

    def restart(self):
        if self.lifespan is not None:
            self.lifespan -= 1
        if self.lifespan is None or self.lifespan > 0:
            self.r = random.randint(0, 360)
            self.x, self.y = [int(i) + random.randint(-8, 8) for i in self.center]

    def draw(self):
        self.surf.blit(
            pygame.transform.rotate(self.img, self.r), (int(self.x), int(self.y))
        )

        if self.y < self.sy + 40:
            self.y += random.randint(0, 5) / 4 * self.speed * self.game.elapsed
            self.x += random.randint(-15, 5) / 10 * self.speed * self.game.elapsed
            self.r += random.randint(-10, 10) * self.speed / 3 * self.game.elapsed
        elif self.y < self.sy + 45:
            self.y += random.randint(-2, 5) / 10 * self.speed * self.game.elapsed
            self.x += random.randint(-18, 2) / 10 * self.speed * self.game.elapsed
            self.r += random.randint(-10, 25) * self.speed * self.game.elapsed
        else:
            self.restart()
        if self.x > self.sx + 100:
            self.restart()


class Bee:
    def __init__(self):
        self.bee = pygame.image.load(ASSETS / "bee/idle/1.png")
        self.x = 0
        self.y = 0

    def draw(self, screen, x, y):
        self.x += random.randint(-2, 2)
        self.y += random.randint(-2, 2)
        screen.blit(
            self.bee,
            (
                x + self.x - self.bee.get_size()[0] / 2,
                y + self.y - self.bee.get_size()[1] / 2,
            ),
        )


class Creeper(Game):
    def __init__(self, debug=False):
        super().__init__()
        pygame.mouse.set_visible(False)
        self.inventory = {"plank-bottom": 1, "plank-top": 1}
        self._imgs = {}
        self.blocks = {}
        self.camera = (0, 0)
        self.day_len = 1000 * 60
        self.background = pygame.Surface(self.screen.get_size())
        self.foreground = pygame.Surface(self.screen.get_size())
        self.build = pygame.Surface(self.screen.get_size())
        # self.darkness = pygame.Surface(self.screen.get_size())
        self.axe_sound = pygame.mixer.Sound(ASSETS / "sounds/axe.mp3")
        self.walking_sound = pygame.mixer.Sound(ASSETS / "sounds/walking.mp3")
        self.walking_sound_is_playing = False
        self.speed = 5

        self.background.fill((0, 255, 247))
        self.x, self.y = [i / 2 for i in self.screen.get_size()]
        self.spot = pygame.image.load(ASSETS / "spotlight.png")
        self.light_power = 1.1
        self.leaf = pygame.transform.scale(
            pygame.image.load(ASSETS / "leaf.png"), (4, 4)
        ).convert_alpha()
        self.creepers = cycle(
            flatten(
                [
                    repeat(pygame.image.load(img), 5)
                    for img in Path(ASSETS / "stev/idle/").glob("*.png")
                ]
            )
        )
        self.tree_imgs = [
            pygame.image.load(img) for img in Path(ASSETS / "oak_trees/").glob("*.png")
        ]
        # self.creeper = pygame.image.load(ASSETS/"creeper/idle/1.png")
        self.creeper = next(self.creepers)
        self.bee = Bee()
        x = 0
        self.hotbar = HotBar(game=self)
        self.leafs = []
        self.trees = []

        x_range = [
            0,
            self.screen.get_size()[0],
        ]
        y_range = [
            self.screen.get_size()[1] * 0.35,
            self.screen.get_size()[1] * 0.5,
        ]
        for i in range(30):
            x = random.randint(*x_range)
            y = random.randint(*y_range)

            scale = random.randint(42, 86)
            self.trees.append(
                TreeSprite(
                    game=self,
                    tree=random.choice(self.tree_imgs),
                    x=x,
                    y=y,
                    scale=scale,
                    flip=random.randint(0, 1),
                    surf=self.background,
                )
            )

        self.mouse_box = MouseSprite(self, self.background, hotbar=self.hotbar)
        self.joysticks = {}

        self.hotbar_back_debounce = 1
        self.hotbar_forward_debounce = 1
        self.inventory_open_debounce = 1
        self.debug_open_debounce = 1
        self.main_open_debounce = 1

        self.controller_hotbar_back_debounce = 1
        self.controller_hotbar_forward_debounce = 1
        self.controller_inventory_open_debounce = 1
        self.controller_debug_open_debounce = 1
        self.controller_main_open_debounce = 1

        self.debounce_walk_img = 0

        self.inventory_menu = Menu(self, title="inventory")
        self.debug_menu = DebugMenu(self)
        self.debug_menu.is_open = debug
        self.main_menu = Menu(self, title="main menu")

    def get_img(self, img):
        try:
            return self._imgs[img]
        except KeyError:
            self._imgs[img] = pygame.image.load(ASSETS / f"{img}.png")
            return self._imgs[img]

    def attack(self):

        collisions = self.mouse_box.rect.collidedictall(
            {tree: tree.rect for tree in self.trees}
        )
        if not collisions:
            return False
        for collision in collisions:
            tree = collision[0]
            tree.health -= 10
            tree.hit = True
            tree.shake()
        self.axe_sound.play()
        return True

    def place_block(self):
        # if self.hotbar.selected.type is None:
        #     return False
        self.blocks[str(self.mouse_box.get_nearest_block_pos())] = Block(
            self.hotbar.selected.type, self.mouse_box.get_nearest_block_pos()
        )
        print(self.blocks)

    def process_deaths(self):
        for i, tree in enumerate(copy(self.trees)):
            if tree.health <= 0:
                self.inventory["log"] = self.inventory.get("log", 0) + 10
                try:
                    del self.trees[i]
                except IndexError:
                    # get this one on the next pass
                    # killing two items in the same frame will error
                    ...

    def normal_keys(self):
        keys = self.keys
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= 10 * self.speed * self.elapsed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += 10 * self.speed * self.elapsed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= 10 * self.speed * self.elapsed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += 10 * self.speed * self.elapsed
        if keys[pygame.K_k]:
            self.hotbar.next(1)
        if keys[pygame.K_j]:
            self.hotbar.next(-1)

        for event in self.events:
            if event.type == pygame.MOUSEWHEEL:
                self.hotbar.next(event.y)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    did_attack = self.attack()
                if pygame.mouse.get_pressed()[2]:
                    did_place = self.place_block()

            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                self.joysticks[joy.get_instance_id()] = joy
            if event.type == pygame.JOYDEVICEREMOVED:
                del self.joysticks[event.instance_id]

        if not self.joysticks:
            if (keys[pygame.K_ESCAPE]) and self.main_open_debounce:
                print("opens")
                self.main_menu.is_open = not self.main_menu.is_open
                self.main_open_debounce = 0
            elif not keys[pygame.K_ESCAPE]:
                self.main_open_debounce = 1

            if keys[pygame.K_e] and self.inventory_open_debounce:
                self.inventory_menu.is_open = not self.inventory_menu.is_open
                self.inventory_open_debounce = 0
            elif not keys[pygame.K_e]:
                self.inventory_open_debounce = 1

        for joystick in self.joysticks.values():
            if joystick.get_axis(5) > 0:
                if self.attack():
                    joystick.rumble(0.1, 0.0, 100)

            if joystick.get_button(4) and self.controller_hotbar_back_debounce:
                print(self.controller_hotbar_back_debounce)
                self.hotbar.next(-1)
                self.controller_hotbar_back_debounce = 0
                print(self.hotbar_back_debounce)
            if not joystick.get_button(4):
                self.controller_hotbar_back_debounce = 1

            if joystick.get_button(5) and self.controller_hotbar_forward_debounce:
                self.hotbar.next(1)
                self.controller_hotbar_forward_debounce = 0
            elif not joystick.get_button(5):
                self.controller_hotbar_forward_debounce = 1

            if (
                keys[pygame.K_e] or joystick.get_button(2)
            ) and self.controller_inventory_open_debounce:
                self.inventory_menu.is_open = not self.inventory_menu.is_open
                self.controller_inventory_open_debounce = 0
            elif not keys[pygame.K_e] and not joystick.get_button(2):
                self.controller_inventory_open_debounce = 1

            if (
                keys[pygame.K_ESCAPE] or joystick.get_button(9)
            ) and self.controller_main_open_debounce:
                self.main_menu.is_open = not self.main_menu.is_open
                self.controller_main_open_debounce = 0
            elif not (keys[pygame.K_ESCAPE] or joystick.get_button(9)):
                self.controller_main_open_debounce = 1

            if keys[pygame.K_F3] and self.controller_debug_open_debounce:
                self.debug_menu.is_open = not self.debug_menu.is_open
                self.controller_debug_open_debounce = 0
            elif not keys[pygame.K_F3]:
                self.controller_debug_open_debounce = 1

            hats = joystick.get_numhats()
            for i in range(hats):
                hat = joystick.get_hat(i)
                if hat[0] == 1:
                    self.x += 10 * self.speed * self.elapsed
                if hat[0] == -1:
                    self.x -= 10 * self.speed * self.elapsed
                if hat[1] == -1:
                    self.y += 10 * self.speed * self.elapsed
                if hat[1] == 1:
                    self.y -= 10 * self.speed * self.elapsed

            if abs(joystick.get_axis(0)) > 0.2:
                self.x += joystick.get_axis(0) * 10 * self.speed * self.elapsed
            if abs(joystick.get_axis(1)) > 0.2:
                self.y += joystick.get_axis(1) * 10 * self.speed * self.elapsed

            if abs(joystick.get_axis(3)) > 0.2 and abs(joystick.get_axis(4)) > 0.2:
                pygame.mouse.set_pos(
                    (
                        pygame.mouse.get_pos()[0] + joystick.get_axis(3) * 32,
                        pygame.mouse.get_pos()[1] + joystick.get_axis(4) * 32,
                    )
                )
            elif abs(joystick.get_axis(3)) > 0.2:
                pygame.mouse.set_pos(
                    (
                        pygame.mouse.get_pos()[0] + joystick.get_axis(3) * 32,
                        pygame.mouse.get_pos()[1],
                    )
                )
            elif abs(joystick.get_axis(4)) > 0.2:
                pygame.mouse.set_pos(
                    (
                        pygame.mouse.get_pos()[0],
                        pygame.mouse.get_pos()[1] + joystick.get_axis(4) * 32,
                    )
                )

    def inventory_keys(self):
        keys = self.keys
        if not self.joysticks:
            if keys[pygame.K_e] and self.inventory_open_debounce:
                self.inventory_menu.is_open = not self.inventory_menu.is_open
                self.inventory_open_debounce = 0
            elif not keys[pygame.K_e]:
                self.inventory_open_debounce = 1

        for joystick in self.joysticks.values():
            if (
                keys[pygame.K_e] or joystick.get_button(2)
            ) and self.controller_inventory_open_debounce:
                self.inventory_menu.is_open = not self.inventory_menu.is_open
                self.controller_inventory_open_debounce = 0
            elif not keys[pygame.K_e] and not joystick.get_button(2):
                self.controller_inventory_open_debounce = 1

    def main_keys(self):
        keys = self.keys

        if not self.joysticks:
            if (keys[pygame.K_ESCAPE]) and self.main_open_debounce:
                print("opens")
                self.main_menu.is_open = not self.main_menu.is_open
                self.main_open_debounce = 0
            elif not keys[pygame.K_ESCAPE]:
                self.main_open_debounce = 1

        for joystick in self.joysticks.values():
            if (
                keys[pygame.K_ESCAPE] or joystick.get_button(9)
            ) and self.controller_main_open_debounce:
                self.main_menu.is_open = not self.main_menu.is_open
                self.controller_main_open_debounce = 0
            elif not (keys[pygame.K_ESCAPE] or joystick.get_button(9)):
                self.controller_main_open_debounce = 1

    def make_sound(self):
        if not hasattr(self, "last_x"):
            self.last_x = self.x
        if not hasattr(self, "last_y"):
            self.last_y = self.y
        if (
            self.last_x == self.x and self.last_y == self.y
        ) and self.walking_sound_is_playing:
            self.walking_sound.stop()
            self.walking_sound_is_playing = False

        if (
            self.last_x != self.x or self.last_y != self.y
        ) and not self.walking_sound_is_playing:
            self.walking_sound.play()
            self.walking_sound_is_playing = True
        if (
            self.last_x != self.x or self.last_y != self.y
        ) and self.debounce_walk_img < 0:
            self.creeper = next(self.creepers)
            self.debounce_walk_img = 0.15
        self.last_x = self.x
        self.last_y = self.y

    def game(self):
        # self.camera = (self.camera[0] + 1, self.camera[1])

        self.debounce_walk_img -= self.elapsed
        self.screen.blit(self.background, self.camera)
        for block in self.blocks.values():
            self.screen.blit(block.img, block.pos)

        self.background.fill((0, 255, 247))
        self.process_deaths()
        for tree in self.trees:
            tree.draw()

        self.screen.blit(
            self.creeper,
            (
                self.x - self.creeper.get_size()[0] / 2,
                self.y - self.creeper.get_size()[1] / 2,
            ),
        )
        self.bee.draw(self.screen, self.x, self.y)
        for leaf in self.leafs:
            leaf.draw()

        light_level = pygame.time.get_ticks() % self.day_len
        light_level = abs(light_level * (255 * 2 / self.day_len) - 255)

        # self.darkness.fill((light_level, light_level, light_level))
        # if self.light_power < 500:
        #     self.light_power = min(self.light_power**1.1, 500)
        # self.darkness.blit(
        #     pygame.transform.smoothscale(
        #         self.spot, [self.light_power, self.light_power]
        #     ),
        #     (self.x - self.light_power / 2, self.y - self.light_power / 2),
        # )
        # self.screen.blit(
        #     pygame.transform.scale(self.darkness, self.screen.get_size()).convert(),
        #     (0, 0),
        #     special_flags=pygame.BLEND_MULT,
        # )

        self.hotbar.draw()
        self.debug_menu.draw()
        self.inventory_menu.draw()
        self.main_menu.draw()

        self.mouse_box = MouseSprite(self, self.background, hotbar=self.hotbar)

        self.make_sound()

        if self.inventory_menu.is_open:
            self.inventory_keys()
        elif self.main_menu.is_open:
            self.main_keys()
        else:
            self.normal_keys()
            self.mouse_box.draw()


def main(debug=False):
    creeper = Creeper(debug=debug)
    creeper.run()


if __name__ == "__main__":
    main()
