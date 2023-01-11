# Lines automatically build by the following file.
#
#     + ``tools/factory/dsl/build_01_update_specs.py``

ASSOCIATED_EXT = dict()
WITH_UTILS = dict()
JINJA_TAGS = dict()


# -------------- #
# -- ALL TAGS -- #
# -------------- #

ALL_TAGS = [
    (TAG_BLOCK_COMMENT_END:= 'comment_end_string'),
    (TAG_BLOCK_COMMENT_START:= 'comment_start_string'),
    (TAG_BLOCK_INSTR_END:= 'block_end_string'),
    (TAG_BLOCK_INSTR_START:= 'block_start_string'),
    (TAG_INLINE_COMMENT:= 'line_comment_prefix'),
    (TAG_INLINE_INSTR:= 'line_statement_prefix'),
    (TAG_VAR_END:= 'variable_end_string'),
    (TAG_VAR_START:= 'variable_start_string'),
]


# ------------------ #
# -- ALL FLAVOURS -- #
# ------------------ #

ALL_FLAVOURS = [
    (FLAVOUR_ASCII:= 'ascii'),
    (FLAVOUR_HTML:= 'html'),
    (FLAVOUR_LATEX:= 'latex'),
    (FLAVOUR_MD:= 'md'),
]


# ----------- #
# -- ASCII -- #
# ----------- #
#
# Generic behaviour of `jinjaNG`.
#
# Last change: 2023-01-08
# Author     : Christophe Bal

ASSOCIATED_EXT[FLAVOUR_ASCII] = ["*"]

WITH_UTILS[FLAVOUR_ASCII] = False

JINJA_TAGS[FLAVOUR_ASCII] = {
    TAG_VAR_START: "{{",
    TAG_VAR_END: "}}",
    TAG_INLINE_COMMENT: "#_",
    TAG_INLINE_INSTR: "#:",
    TAG_BLOCK_COMMENT_START: "##_",
    TAG_BLOCK_COMMENT_END: "_##",
    TAG_BLOCK_INSTR_START: "##:",
    TAG_BLOCK_INSTR_END: ":##",
}


# ---------- #
# -- HTML -- #
# ---------- #
#
# Useful settings and tools for HTML templating.
#
# Last change: 2023-01-08
# Author     : Christophe Bal

ASSOCIATED_EXT[FLAVOUR_HTML] = ["*.html"]

WITH_UTILS[FLAVOUR_HTML] = True

JINJA_TAGS[FLAVOUR_HTML] = {
    TAG_VAR_START: "{{",
    TAG_VAR_END: "}}",
    TAG_INLINE_COMMENT: None,
    TAG_INLINE_INSTR: None,
    TAG_BLOCK_COMMENT_START: "<!--_",
    TAG_BLOCK_COMMENT_END: "_-->",
    TAG_BLOCK_INSTR_START: "<!--:",
    TAG_BLOCK_INSTR_END: ":-->",
}


# ----------- #
# -- LATEX -- #
# ----------- #
#
# Useful settings and tools for LaTeX templating.
#
# Last change: 2023-01-08
# Author     : Christophe Bal

ASSOCIATED_EXT[FLAVOUR_LATEX] = ["*.tex", "*.sty", "*.tkz"]

WITH_UTILS[FLAVOUR_LATEX] = True

JINJA_TAGS[FLAVOUR_LATEX] = {
    TAG_VAR_START: "\\JNGVALOF{",
    TAG_VAR_END: "}",
    TAG_INLINE_COMMENT: "%_",
    TAG_INLINE_INSTR: "%:",
    TAG_BLOCK_COMMENT_START: "%%_",
    TAG_BLOCK_COMMENT_END: "_%%",
    TAG_BLOCK_INSTR_START: "%%:",
    TAG_BLOCK_INSTR_END: ":%%",
}


# -------- #
# -- MD -- #
# -------- #
#
# Useful settings for Markdown templating.
#
# Last change: 2023-01-09
# Author     : Christophe Bal

ASSOCIATED_EXT[FLAVOUR_MD] = ["*.md"]

WITH_UTILS[FLAVOUR_MD] = False

JINJA_TAGS[FLAVOUR_MD] = {
    TAG_VAR_START: "{{",
    TAG_VAR_END: "}}",
    TAG_INLINE_COMMENT: None,
    TAG_INLINE_INSTR: None,
    TAG_BLOCK_COMMENT_START: "<!--_",
    TAG_BLOCK_COMMENT_END: "_-->",
    TAG_BLOCK_INSTR_START: "<!--:",
    TAG_BLOCK_INSTR_END: ":-->",
}
