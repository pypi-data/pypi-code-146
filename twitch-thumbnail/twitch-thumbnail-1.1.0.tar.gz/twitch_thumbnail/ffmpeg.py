def _make_ffmpeg_args(url: str, path: str, join: bool = False):
    args = [
        "ffmpeg",
        "-i",
        url,
        "-f",
        "image2",
        "-update",
        "1",
        "-vframes",
        "1",
        path,
        "-y",
    ]

    if join:
        args = " ".join(args)

    return args
