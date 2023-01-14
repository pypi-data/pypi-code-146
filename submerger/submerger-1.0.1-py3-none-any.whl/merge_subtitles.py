from typing import List

from submerger.subtitle import Subtitle
from submerger.subtitle_format import SubtitleFormat


def merge_subtitles(
        base_srt: str,
        base_srt_tags: SubtitleFormat,
        secondary_srt: str,
        secondary_srt_tags: SubtitleFormat,
) -> str:
    subtitle_list: List[Subtitle] = []

    for subtitle in Subtitle.from_srt(base_srt):
        subtitle_list.append(Subtitle(
            subtitle.start_time,
            subtitle.end_time,
            base_srt_tags.format(subtitle.text),
        ))

    for subtitle in Subtitle.from_srt(secondary_srt):
        subtitle_list.append(Subtitle(
            subtitle.start_time,
            subtitle.end_time,
            secondary_srt_tags.format(subtitle.text),
        ))

    return Subtitle.to_srt(subtitle_list)
