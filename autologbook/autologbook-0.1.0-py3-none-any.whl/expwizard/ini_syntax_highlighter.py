#  Copyright (c) 2022. Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#  and associated documentation files (the "Software"), to deal in the Software without restriction, including without
#  limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
#  Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
#  Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from PyQt5.QtCore import QRegularExpression, Qt
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QTextDocument


class SHRule:
    def __init__(self, regexp: QRegularExpression, form: QTextCharFormat):
        self._regexp = regexp
        self._format = form

    @property
    def regexp(self) -> QRegularExpression:
        return self._regexp

    @regexp.setter
    def regexp(self, regexp: QRegularExpression):
        self._regexp = regexp

    @property
    def format(self) -> QTextCharFormat:
        return self._format

    @format.setter
    def format(self, formatting: QTextCharFormat):
        self._format = formatting


class IniSyntaxHighlighter(QSyntaxHighlighter):

    def __init__(self, text_document: QTextDocument):
        super().__init__(text_document)
        self.rules = list()

        # comment formatting
        comment_format = QTextCharFormat()
        comment_format.setForeground(Qt.darkGreen)
        comment_format.setFontItalic(True)
        comment_pattern = QRegularExpression('#[^\\n]*')
        self.rules.append(SHRule(comment_pattern, comment_format))

        # section formatting
        section_format = QTextCharFormat()
        section_format.setForeground(Qt.darkBlue)
        section_format.setFontWeight(QFont.Bold)
        section_pattern = QRegularExpression(r'\[.*\]')
        self.rules.append(SHRule(section_pattern, section_format))

        key_format = QTextCharFormat()
        key_format.setForeground(Qt.red)
        key_format.setFontWeight(QFont.Bold)
        key_pattern = QRegularExpression('.*=')
        self.rules.append(SHRule(key_pattern, key_format))

        value_format = QTextCharFormat()
        value_format.setForeground(Qt.darkBlue)
        value_pattern = QRegularExpression('=(.*)')
        self.rules.append(SHRule(value_pattern, value_format))

        equal_format = QTextCharFormat()
        equal_format.setForeground(Qt.darkCyan)
        equal_pattern = QRegularExpression('=')
        self.rules.append(SHRule(equal_pattern, equal_format))

    def highlightBlock(self, text: str) -> None:

        for rule in self.rules:
            match_iterator = rule.regexp.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)
