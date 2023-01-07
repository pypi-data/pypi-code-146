from datetime import datetime, timedelta
import re

def srt_parser(file, text, shift, *kwargs):
    """
    Parser for SubRip (.srt) and WebVTT (.vtt) files.
    """
    for line in text:
        if '-->' in line:
            # remove leading and trailing spaces
            line = line.strip()
            # force period as decimal separator
            line = line.replace(',', '.')
            # extract time stamps
            start, end = line.split('-->')
            start = start.strip()
            end = end.strip()
            # shift
            start_dt = datetime.strptime(start, '%H:%M:%S.%f') + timedelta(seconds=shift)
            end_dt = datetime.strptime(end, '%H:%M:%S.%f') + timedelta(seconds=shift)
            start = start_dt.strftime('%H:%M:%S.%f')[:-3]
            end = end_dt.strftime('%H:%M:%S.%f')[:-3]
            line = f'{start} --> {end}\n'
        # write line
        file.write(line)

def sub_parser(file, text, shift, framerate=24):
    """
    Parser for MicroDVD (.sub) files.
    """
    for line in text:
        regexp = re.search('^\{(\d+)\}\{(\d+)\}(.+)$', line)
        if regexp:
            # decompose line
            start = int(regexp.group(1))
            end = int(regexp.group(2))
            content = regexp.group(3)
            # shift
            start = start + round(shift * framerate)
            end = end + round(shift * framerate)
            line = f'{{{start}}}{{{end}}}{content}\n'
        # write line
        file.write(line)        


# Mapping for the various supported formats
FORMATS = {'srt': srt_parser,
           'vtt': srt_parser,
           'sub': sub_parser}