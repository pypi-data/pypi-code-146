import os
import subprocess
import shlex
import json
from shutil import which
from warnings import warn


class AVFile:
    def __init__(self, filename=None):
        if type(filename) != str:
            raise TypeError('filename must be a string.')
        self.filename = filename

    def get_chapters(self, force_generated_titles=False):
        """Get a list of chapters.  Each chapter is a dict with a title, start
        time, and end time.  Titles will be automatically generated as
        'Chapter 1', 'Chapter 2', etc. if they aren't available in the
        metadata, or if force_generated_titles is set to True.
        """
        check_file(self.filename)
        ffprobe_path = get_bin_path('ffprobe')
        command = "ffprobe -loglevel error -i %s -print_format json -show_chapters" % (
            shlex.quote(self.filename)
        )
        try:
            output = subprocess.check_output(
                command,
                shell=True,
                # stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError:
            warn(
                "Couldn't process %s.  Will assume it has no chapters." % self.filename
            )
            return []
        results = []
        for chapnum, c in enumerate(json.loads(output)['chapters']):
            if force_generated_titles or ('title' not in c['tags']):
                title = 'Chapter ' + str(chapnum + 1)
            else:
                title = c['tags']['title']
            results.append(
                {
                    'title': title,
                    'start_time': c['start_time'],
                    'end_time': c['end_time'],
                }
            )
        return results

    def extract_audio(self, output_filename, chapter=None, stream=0, overwrite=False):
        """Extracts audio from a single chapter of the input file.  The output
        is encoded using '-q:a 0', which should give high quality.

        Keyword arguments:
        output_filename -- where the output should be saved, e.g. '/tmp/out.mp3'
        chapter -- either None to grab the entire file, or a single chapter dict from the get_chapters() list (default None)
        stream -- which audio stream to use (0-indexed) (default 0)
        overwrite -- overwrite output_filename if it already exists (default False)
        """
        check_file(self.filename)
        ffmpeg_path = get_bin_path('ffmpeg')
        overwrite_flag = '-y' if overwrite else ''
        if chapter is None:
            time_flags = ''
        else:
            time_flags = '-ss %s ' % (
                chapter['start_time']
                if chapter['start_time'] is not None
                else '00:00:00.000'
            )
            # TODO: could time_flags just be '' if chapter['start_time'] is None?  or would that mess up the -to flag?
            if chapter['end_time'] is not None:
                time_flags += '-to %s' % (chapter['end_time'])
        command = "ffmpeg -i %s %s -q:a 0 -map 0:a:%d %s %s" % (
            shlex.quote(self.filename),
            time_flags,
            stream,
            overwrite_flag,
            shlex.quote(output_filename),
        )
        # TODO: allow other quality options, e.g. copying original without re-encoding
        output = subprocess.check_output(
            command,
            shell=True,
            # stderr=subprocess.STDOUT,
        )
        # TODO: (option to) squelch output?

    def extract_all_chapters_audio(
        self, output_dir, output_filenames=None, stream=0, overwrite=False
    ):
        """Extract audio from each chapter into separate mp3 files, which will
        be saved in output_dir.  Filenames will be 'Chapter 1.mp3',
        'Chapter 2.mp3', etc., unless a list of output_filenames is
        given (including extensions).  The `stream` and `overwrite`
        parameters are the same as in extract_audio().
        """
        chapters = self.get_chapters(force_generated_titles=True)
        expected_num_filenames = 1 if len(chapters) < 1 else len(chapters)
        if (
            output_filenames is not None
            and len(output_filenames) != expected_num_filenames
        ):
            raise RuntimeError(
                "%d output filenames were specified, but input file seems have %d chapters."
                % (len(output_filenames), expected_num_filenames)
            )
        if len(chapters) < 1:
            warn(
                "%s doesn't appear to have chapters.  Will output a single file."
                % self.filename
            )
            chapters = [
                {
                    'title': 'Chapter 1',
                    'start_time': None,
                    'end_time': None,
                }
            ]
        for chapnum, chapter in enumerate(chapters):
            if output_filenames is not None:
                output_filename = output_filenames[chapnum]
            else:
                output_filename = chapter['title'] + '.mp3'
            self.extract_audio(
                os.path.join(output_dir, output_filename),
                chapter=chapter,
                stream=stream,
                overwrite=overwrite,
            )


def check_file(filename):
    if filename is None:
        raise ValueError('No filename was given.')
    if not os.path.isfile(filename):
        raise FileNotFoundError("Couldn't find %s" % filename)
    # TODO: try ffprobe here too?


def get_bin_path(binfile):
    """binfile is a command like 'ls' or 'ffmpeg'.  The full path to the
    actual binary is returned.  This function can also be used to make
    sure a binary exists on the system, since it will raise a
    RuntimeError if it isn't.
    """
    bin_path = which(binfile)
    if bin_path is None:
        raise RuntimeError("Couldn't find the %s binary." % binfile)
    return bin_path
