class RegexsResult:
    def __init__(self, text: str, start: int, end: int, add_extra=True) -> None:
        if len(text) < end:
            raise ValueError(
                f"{__file__}: ERROR: end of matching is out of range ({end} > {len(text)})"  # noqa: E501
            )
        if len(text) < start:
            raise ValueError(
                f"{__file__}: ERROR: start of matching is out of range ({start} > {len(text)})"  # noqa: E501
            )
        if end < 0:
            raise ValueError(
                f"{__file__}: ERROR: end of matching is out of range ({end})"
            )
        if start < 0:
            raise ValueError(
                f"{__file__}: ERROR: end of matching is out of range ({start})"
            )
        self.text = text
        if len(text) > end + 1 and text[end + 1] == "\n" and add_extra:
            end += 1
            self.extra_end_line = True
        else:
            self.extra_end_line = False
        self.start = start
        self.end = end
        self.matching = text[start : (end + 1)]

    def __str__(self):
        return self.matching
