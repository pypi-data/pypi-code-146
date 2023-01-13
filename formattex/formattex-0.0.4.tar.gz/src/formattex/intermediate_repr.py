from dataclasses import dataclass
from textwrap import TextWrapper

from TexSoup import TexSoup
from TexSoup import data as texsoup_classes

BACKSLASH_SPACE = "__bs__"


def protect_backslash_space(text):
    return text.replace(r"\ ", BACKSLASH_SPACE)


def unprotect_backslash_space(text):
    return text.replace(BACKSLASH_SPACE, r"\ ")


wrapper = TextWrapper(break_long_words=False, width=87, break_on_hyphens=False)


def wrap(text):
    number_newlines_begin = 0
    while text[0] == "\n":
        text = text[1:]
        number_newlines_begin += 1

    number_newlines_end = 0
    while text[-1] == "\n":
        text = text[:-1]
        number_newlines_end += 1

    wrapped = wrapper.fill(text)

    return "\n" * number_newlines_begin + wrapped + "\n" * number_newlines_end


class BaseLatexNode:
    @property
    def code(self):
        return self.text

    @property
    def formatted(self):
        return self.code


@dataclass
class LinesOfText(BaseLatexNode):
    expressions: list

    @property
    def code_protected(self):
        return "".join(str(expr) for expr in self.expressions)

    @property
    def code(self):
        return unprotect_backslash_space(self.code_protected)

    def __repr__(self):
        code = repr(self.code)
        if len(code) > 20:
            code = code[:20] + "[...]"
        return f"LinesOfText(code='{code}')"

    @property
    def formatted(self):
        return unprotect_backslash_space(wrap(self.code_protected))


@dataclass
class CommentLine(BaseLatexNode):
    text: str


@dataclass
class TexCmd(BaseLatexNode):
    name: str
    text: str


class BraceGroup(BaseLatexNode):
    def __init__(self, expr):
        self.content = str(expr).strip()[1:-1]

    @property
    def code(self):
        return "{" + self.content + "}"

    @property
    def formatted(self):
        repr_abstract = InternalRepr(self.content)
        return "{" + repr_abstract.get_formatted() + "}"


@dataclass
class BeginEndBlock(BaseLatexNode):
    kind: str
    content: str

    @property
    def code(self):
        return rf"\begin{{{self.kind}}}{self.content}\end{{{self.kind}}}"

    def __repr__(self):
        if len(self.content) < 10:
            content_repr = self.content.strip()
        else:
            content_repr = self.content[:10].strip() + "[...]"

        return f"BeginEndBlock(kind='{self.kind}', content='{content_repr}'"

    @property
    def formatted(self):
        if self.kind == "figure":
            before_caption, after_caption = self.content.split(r"\caption{")
            after_caption = wrap(r"\caption{" + after_caption)
            content = before_caption + unprotect_backslash_space(after_caption)
        elif self.kind == "abstract":
            repr_abstract = InternalRepr(self.content)
            content = repr_abstract.get_formatted()
        else:
            content = self.content
        return rf"\begin{{{self.kind}}}{content}\end{{{self.kind}}}"


@dataclass
class NewLine(BaseLatexNode):
    code = "\n"


@dataclass
class EmptyLine(BaseLatexNode):
    code = "\n\n"


class InternalRepr:
    def __init__(self, full_code, verbose=False):
        self.full_code = full_code

        if r"\begin{document}" in full_code:
            self.has_document_env = True
            self.before_begin_doc, rest = full_code.split(
                r"\begin{document}", maxsplit=1
            )
            self.code_document_env, self.after_end_doc = rest.split(
                r"\end{document}", maxsplit=1
            )
        else:
            self.has_document_env = False
            self.code_document_env = full_code

        self.things = create_internal_repr_document_env(
            self.code_document_env, verbose=verbose
        )

    def dump(self):

        code_out = "".join(t.code for t in self.things)

        if self.has_document_env:
            code_out = (
                self.before_begin_doc
                + r"\begin{document}"
                + code_out
                + r"\end{document}"
                + self.after_end_doc
            )

        return code_out

    def get_formatted(self, line_length=87):
        wrapper.width = line_length
        code_out = "".join(t.formatted for t in self.things)

        if self.has_document_env:
            code_out = (
                self.before_begin_doc
                + r"\begin{document}"
                + code_out
                + r"\end{document}"
                + self.after_end_doc
            )
        return code_out

    def save_formatted(self, path_output="tmp_formatted.tex", line_length=87):
        code_out = self.get_formatted(line_length)
        if code_out[-1] != "\n":
            code_out += "\n"
        with open(path_output, "w") as file:
            file.write(code_out)
        return code_out


def create_internal_repr_texfile(path_in, verbose=False):
    with open(path_in) as file:
        full_code = file.read()

    return InternalRepr(full_code, verbose=verbose)


def remove_double_newline(expressions):
    expressions_cleaned = [expressions[0]]
    for e0, e1 in zip(expressions[:-1], expressions[1:]):
        if e0 == e1 == "\n":
            expressions_cleaned[-1] = texsoup_classes.TexText("\n\n")
        else:
            expressions_cleaned.append(e1)
    return expressions_cleaned


def cleanup_expressions(expressions):
    expressions_cleaned = []
    for expr in expressions:
        if not isinstance(expr, texsoup_classes.TexText) or "\n\n" not in expr:
            expressions_cleaned.append(expr)
            continue

        pieces_without_emptylines = [
            texsoup_classes.TexText(text) for text in expr.split("\n\n")
        ]
        empty_line = texsoup_classes.TexText("\n\n")
        pieces = [empty_line] * (len(pieces_without_emptylines) * 2 - 1)
        pieces[0::2] = pieces_without_emptylines
        expressions_cleaned.extend(piece for piece in pieces if piece)
    return expressions_cleaned


def create_internal_repr_document_env(code_document_env, verbose=False):

    code_document_env = protect_backslash_space(code_document_env)

    things = []

    soup = TexSoup(code_document_env)
    expressions = [node.expr for node in soup.all]
    expressions = cleanup_expressions(expressions)
    expressions = remove_double_newline(expressions)

    in_piece_of_text = False
    exprs_piece_of_text = []

    index = 0
    while index < len(expressions):

        expr = expressions[index]

        if verbose > 1:
            print(f"{repr(expr) = :60}{in_piece_of_text = }")

        try:
            expr_next = expressions[index + 1]
        except IndexError:
            name_next = "text"
            str_next = ""
        else:
            name_next = expr_next.name
            str_next = str(expr_next)

        if expr.name == "text":
            text = str(expr)

            # print(expr.name, repr(text))
            if text.strip().startswith("%"):
                if in_piece_of_text:
                    things.append(LinesOfText(exprs_piece_of_text))
                    in_piece_of_text = False

                things.append(CommentLine(text))
            elif text == "\n\n":
                if in_piece_of_text:
                    things.append(LinesOfText(exprs_piece_of_text))
                    in_piece_of_text = False
                things.append(EmptyLine())

            elif text == "\n":

                if in_piece_of_text:
                    if name_next == "text" and str_next == "\n":
                        things.append(LinesOfText(exprs_piece_of_text))
                        in_piece_of_text = False
                    else:
                        exprs_piece_of_text.append(text)
                else:
                    things.append(NewLine())
            elif not in_piece_of_text and text != "\n":
                in_piece_of_text = True
                exprs_piece_of_text = [text]
            elif in_piece_of_text:
                exprs_piece_of_text.append(text)

            if in_piece_of_text and name_next == "text" and str_next == "\n\n":
                things.append(LinesOfText(exprs_piece_of_text))
                in_piece_of_text = False

        elif isinstance(expr, texsoup_classes.TexMathModeEnv):
            if in_piece_of_text:
                exprs_piece_of_text.append(expr)
            else:
                in_piece_of_text = True
                exprs_piece_of_text = [expr]

        elif isinstance(expr, texsoup_classes.TexCmd):
            if in_piece_of_text:
                exprs_piece_of_text.append(expr)
            else:
                things.append(TexCmd(expr.name, str(expr)))

        elif isinstance(expr, texsoup_classes.TexNamedEnv):

            if in_piece_of_text:
                things.append(LinesOfText(exprs_piece_of_text))
                in_piece_of_text = False

            things.append(BeginEndBlock(expr.name, expr.string))

        elif isinstance(expr, texsoup_classes.BraceGroup):
            if in_piece_of_text:
                exprs_piece_of_text.append(expr)
            else:
                things.append(BraceGroup(expr))

        else:
            raise NotImplementedError

        index += 1

    if in_piece_of_text:
        things.append(LinesOfText(exprs_piece_of_text))

    if verbose > 1:
        print(f"{things = }")

    return things
