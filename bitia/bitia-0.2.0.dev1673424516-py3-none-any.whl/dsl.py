__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import typing as T
from urllib.parse import urlparse

import pyparsing as pp

ppc = pp.pyparsing_common


class FileWithLocation:
    def __init__(self, filename: str, location: T.Optional[str] = None):
        self.filename = filename
        self.location = location

    def __repr__(self):
        return str((self.filename, self.location))

    def url(self):
        return self.location.geturl()

    @staticmethod
    def from_tokens(_s, _loc, toks):
        loc = toks[-1]
        assert 1 <= len(toks) <= 2, f"Either 1 or 2 tokens, got {toks}"
        filename = loc.path if len(toks) == 1 else str(toks[0])
        return FileWithLocation(filename, loc)


p_start = pp.Literal("<").suppress()
p_end = pp.Literal(">").suppress()
p_pipe = pp.Literal("|").suppress()

# fixme: filename can have no-printables?
p_filepath = pp.Word(pp.printables.translate({ord(i): None for i in r"|"})).set_name(
    "filepath"
)

p_url = pp.Word(pp.printables.translate({ord(i): None for i in r"<>"})).set_name("url")
p_url.setParseAction(lambda xs: list(map(urlparse, xs)))

p_file_with_url = p_start + pp.Optional(p_filepath + p_pipe) + p_url + p_end
p_file_with_url.set_name("file_with_location")
p_file_with_url.set_parse_action(FileWithLocation.from_tokens)
#  p_file_with_url.set_debug()


class DSL:
    """Domain Spefic Langauge for BiTIA"""

    def __init__(self):
        pass

    @staticmethod
    def transform_line(line: str) -> str:
        """Transform a simple line"""
        # rule 1: search for p_file_with_url and replace those.
        to_replace: T.Dict[str, str] = {}
        download_lines = set()
        for tokens, start, end in p_file_with_url.scan_string(line):
            download_lines.add(f"bitia-runner tools make-available {tokens[0].url()}")
            to_replace[line[start:end]] = tokens[0].filename
        for k, v in to_replace.items():
            line = line.replace(k, v)
        return "\n".join(download_lines) + "\n" + line


def test_simple_cli_with_dsl():
    """Test the full dsl"""
    lines = [
        "# samtools sort -n Col0_C1.100k.bam -o out.sort.bam",
        "samtools sort -n <Col0_C1.100k.bam|https://figshare.com/ndownloader/files/2133244> -o out.sort.bam",
        "# samtools fastq Col0_C1.100k.bam",
        "samtools fastq <Col0_C1.100k.bam|https://figshare.com/ndownloader/files/2133244>",
        "# fastqc SRR20076358_1.fastq.gz",
        "fastqc <ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR200/058/SRR20076358/SRR20076358_1.fastq.gz>",
    ]
    for line in lines:
        newline = DSL.transform_line(line)
        print("\n--")
        print(f"\told={line}\n\tnew={newline}")


def test_parser():
    """tests"""
    assert not p_start.parse_string("<")
    assert not p_end.parse_string(">")
    a = p_url.parse_string("https://subcom.tech/a.txt#sha256=3319eqeqda")
    print(11, a)
    assert a
    assert a[0].scheme == "https"
    assert a[0].fragment == "sha256=3319eqeqda"
    assert a[0].path == "/a.txt"

    a = p_file_with_url.parse_string("<foo.txt|http://example.com/foo.txt>")
    print(12, a)
    assert a

    a = p_file_with_url.parse_string("<http://example.com/foo.txt>")
    assert a
    print(a)


if __name__ == "__main__":
    test_simple_cli_with_dsl()
    test_parser()
