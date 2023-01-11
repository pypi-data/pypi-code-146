#!/usr/bin/env python3
import pygame

def main():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load('./sounds/complete.wav')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.music.load('./sounds/one_hour')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.music.load('./sounds/30_minutes.wav')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.music.load('./sounds/15_minutes.wav')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.music.load('./sounds/5_minutes.wav')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.music.load('./sounds/closed.wav')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

    except Exception as e:
        print(f'Error initializing Announcer.\n   {e}')
        raise

if __name__ == "__main__":
    main()
