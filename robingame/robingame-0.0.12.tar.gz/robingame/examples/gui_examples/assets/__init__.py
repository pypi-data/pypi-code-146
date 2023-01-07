from robingame.image import SpriteAnimation, relative_folder

folder = relative_folder(__file__, "")


button_flash = SpriteAnimation.from_spritesheet(
    filename=folder / "flashybutton.png",
    image_size=(32, 16),
    scale=10,
)
