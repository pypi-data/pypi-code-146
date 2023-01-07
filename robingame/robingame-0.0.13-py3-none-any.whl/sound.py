from pathlib import Path

import pygame


def init_sound(
    frequency=44100,
    size=-16,
    channels=2,
    buffer=0,
):
    if not pygame.mixer.get_init():
        pygame.mixer.pre_init(frequency, size, channels, buffer)
        pygame.mixer.init()


def load_sound(filename: str | Path, volume=0.5, **sound_kwargs):
    filename = Path(filename)
    if not filename.exists():
        raise FileNotFoundError(filename.as_posix())

    init_sound(**sound_kwargs)
    sound = pygame.mixer.Sound(filename.as_posix())
    sound.set_volume(volume)
    return sound
