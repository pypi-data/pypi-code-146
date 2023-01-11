def chunkify(lst: list, max_chunk_size: int) -> list[list]:
    """Split list into n lists that does not exceed max_chunk_size.

    Args:
        lst (typing.List): Initial list of things.
        max_chunk_size (int): The maximum size of the chunks.

    Returns:
        list[list]: List of lists.
    """
    if max_chunk_size <= 0:
        raise ValueError("max_chunk_size must be greater than 0.")

    if not lst:
        return []

    n = len(lst) // max_chunk_size + 1

    return [lst[i::n] for i in range(n)]
