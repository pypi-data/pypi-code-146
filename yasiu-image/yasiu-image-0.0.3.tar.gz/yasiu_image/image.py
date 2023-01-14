import numpy as np

from PIL import Image


def read_gif_frames(path):
    img = Image.open(path, )
    ind = 0
    # sequence = []
    # img = img.convert("RGBA")
    img.seek(0)
    # fr = np.array(img, dtype=np.uint8)
    while True:
        fr = np.array(img, dtype=np.uint8).copy()
        # print(f"Read shape: {fr.shape}")
        # sequence.append(fr)
        yield fr

        ind += 1
        try:
            img.seek(ind)
        except EOFError:
            # print(f"Breaking at: {ind}")
            break


def read_webp_frames(path):
    img = Image.open(path)
    ind = 0

    img.seek(0)
    # fr = np.array(img, dtype=np.uint8)
    while True:
        fr = np.array(img, dtype=np.uint8).copy()
        yield fr

        ind += 1
        try:
            img.seek(ind)
        except EOFError:
            # print(f"Breaking at: {ind}")
            break


def save_image_list_to_gif(frames, exp_path, use_rgba=False, duration=40, quality=100, disposal=2):
    """

    Args:
        frames:
        exp_path: path to export file with ".gif" ending
        use_rgba: bool,
        duration: int, default 40, [ms], preferable in range <20, 80>
        quality: 100
        disposal: int, default 2 = clear

    Returns:

    """

    if not (exp_path.endswith("gif") or exp_path.endswith("GIF")):
        exp_path += ".gif"

    if use_rgba:
        for img in frames:
            print(img.shape)
            assert img.shape[2] == 3, f"Image must have alpha channel! But has: {img.shape}"

        pil_frames = [Image.fromarray(fr).convert("RGBA") for fr in frames]

        for pil_fr, fr in zip(pil_frames, frames):
            alpha_pil = Image.fromarray(fr[:, :, 3])
            pil_fr.putalpha(alpha_pil)

    else:
        pil_frames = [Image.fromarray(fr).convert("RGB") for fr in frames]

    pil_frames[0].save(
            exp_path, save_all=True, append_images=pil_frames[1:],
            optimize=False, loop=0,
            # background=(0, 0, 0, 255),
            quality=quality, duration=duration,
            disposal=disposal,
    )
    return 0


__all__ = ['read_webp_frames', 'read_gif_frames', 'save_image_list_to_gif']

if __name__ == "__main__":
    gen = read_gif_frames("kycu_faja.gif")
    # for i, frame in enumerate(gen):
    #     print(i)
    frames = list(gen)

    save_image_list_to_gif(frames, "kycu-alfa", use_rgba=False)
