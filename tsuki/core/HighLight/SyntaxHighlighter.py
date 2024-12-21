from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt5.QtCore import QRegExp,Qt
from PyQt5.QtWidgets import QApplication
import re
class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keyword_patterns = []
        self.comment_pattern = (None, None)
        self.quotation_pattern = (None, None) 
        self.function_pattern = (None, None)

    def highlightBlock(self, text):
        for pattern, format in self.keyword_patterns:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        # 修复多行注释状态
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = self.comment_pattern[0].indexIn(text)

        while start_index >= 0:
            end_index = self.comment_pattern[0].matchedLength()
            self.setFormat(start_index, end_index, self.comment_pattern[1])
            start_index = self.comment_pattern[0].indexIn(text, start_index + end_index)

        # 处理引号字符串
        if self.quotation_pattern[0] is not None:
            expression = QRegExp(self.quotation_pattern[0])
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, self.quotation_pattern[1])
                index = expression.indexIn(text, index + length)

        # 处理函数
        if self.function_pattern[0] is not None:
            expression = QRegExp(self.function_pattern[0])
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, self.function_pattern[1])
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)  # 修复状态重置
        self.highlightMultilineComments(text)

def any(name, alternates):
    """Return a named group pattern matching list of alternates."""
    return "(?P<%s>" % name + "|".join(alternates) + ")"

def make_pat():
    """Generate pattern for Python syntax highlighting.
    
    Adapted from Python IDLE's colorizer.py
    Licensed under the Python Software Foundation License Version 2.
    """
    import keyword
    import builtins
    import re

    kw = r"\b" + any("KEYWORD", keyword.kwlist) + r"\b"
    match_softkw = (
        r"^[ \t]*" +  
        r"(?P<MATCH_SOFTKW>match)\b" +
        r"(?![ \t]*(?:" + "|".join([  
            r"[:,;=^&|@~)\]}]",  
            r"\b(?:" + r"|".join(keyword.kwlist) + r")\b",  
        ]) +
        r"))"
    )
    case_default = (
        r"^[ \t]*" +  
        r"(?P<CASE_SOFTKW>case)" +
        r"[ \t]+(?P<CASE_DEFAULT_UNDERSCORE>_\b)"
    )
    case_softkw_and_pattern = (
        r"^[ \t]*" +  
        r"(?P<CASE_SOFTKW2>case)\b" +
        r"(?![ \t]*(?:" + "|".join([  
            r"_\b",  
            r"[:,;=^&|@~)\]}]",  
            r"\b(?:" + r"|".join(keyword.kwlist) + r")\b",  
        ]) +
        r"))"
    )
    builtinlist = [str(name) for name in dir(builtins)
                   if not name.startswith('_') and
                   name not in keyword.kwlist]
    builtin = r"([^.'\"\\#]\b|^)" + any("BUILTIN", builtinlist) + r"\b"
    comment = any("COMMENT", [r"#[^\n]*"])
    stringprefix = r"(?i:r|u|f|fr|rf|b|br|rb)?"
    sqstring = stringprefix + r"'[^'\\\n]*(\\.[^'\\\n]*)*'?"
    dqstring = stringprefix + r'"[^"\\\n]*(\\.[^"\\\n]*)*"?'
    sq3string = stringprefix + r"'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?"
    dq3string = stringprefix + r'"""[^"\\]*((\\.|"(?!""))[^"\\]*)*(""")?'
    string = any("STRING", [sq3string, dq3string, sqstring, dqstring])
    return re.compile("|".join([
        builtin, comment, string, kw,
        match_softkw, case_default,
        case_softkw_and_pattern,
        any("SYNC", [r"\n"]),
    ]), re.DOTALL | re.MULTILINE)

def matched_named_groups(re_match):
    """Get only the non-empty named groups from an re.Match object."""
    return ((k, v) for (k, v) in re_match.groupdict().items() if v)

# 定义tag映射
prog_group_name_to_tag = {
    "MATCH_SOFTKW": "KEYWORD",
    "CASE_SOFTKW": "KEYWORD", 
    "CASE_DEFAULT_UNDERSCORE": "KEYWORD",
    "CASE_SOFTKW2": "KEYWORD",
}
class PythonHighlighter(SyntaxHighlighter):
    """Python syntax highlighter based on IDLE's colorizer.
    
    This implementation is adapted from Python IDLE's colorizer.py
    Licensed under the Python Software Foundation License Version 2.
    Original source: https://github.com/python/cpython/blob/main/Lib/idlelib/colorizer.py
    """
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.light = light
        
        # 基于IDLE的配色方案
        self.colors = {
            'COMMENT': "#DD0000",    # 红色注释
            'KEYWORD': "#FF7700",    # 橙色关键字
            'BUILTIN': "#900090",    # 紫色内置函数
            'STRING': "#00AA00",     # 绿色字符串
            'DEFINITION': "#0000FF", # 蓝色定义
            'SYNC': None,            # 同步标记(无颜色)
            'TODO': None,            # 待处理标记(无颜色)
            'ERROR': "#FF0000",      # 错误标记
            'hit': "#HHH"           # 搜索匹配(保持原样)
        }

        # 创建格式
        self.formats = {}
        for tag, color in self.colors.items():
            format = QTextCharFormat()
            if color:
                format.setForeground(QColor(color))
            self.formats[tag] = format

        # 编译正则表达式
        self.prog = make_pat()  # 使用IDLE的pattern生成函数
        self.idprog = re.compile(r"\s+(\w+)")

    def create_format(self, color):
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        format.setFontWeight(QFont.Bold)
        return format

    def highlightBlock(self, text):
        # 清除之前的格式
        self.setFormat(0, len(text), QTextCharFormat())
        
        # 逐个匹配并应用格式
        for match in self.prog.finditer(text):
            for group_name, matched_text in matched_named_groups(match):
                start, end = match.span(group_name)
                # 使用IDLE的tag映射
                tag = prog_group_name_to_tag.get(group_name, group_name)
                if tag in self.formats:
                    self.setFormat(start, end - start, self.formats[tag])
                
                # 处理函数/类定义
                if matched_text in ("def", "class"):
                    if m1 := self.idprog.match(text, end):
                        start, end = m1.span(1)
                        self.setFormat(start, end - start, self.formats['DEFINITION'])

    def highlightMultilineComments(self, text):
        # 处理三引号字符串
        triple_quote_pattern = r'""".*?"""|\'\'\'.*?\'\'\''
        triple_quote_matches = re.finditer(triple_quote_pattern, text, re.DOTALL)
        for match in triple_quote_matches:
            start, end = match.span()
            self.setFormat(start, end - start, self.formats['STRING'])
        
        # 处理多行注释
        comment_start = QRegExp(r'(?<!\"|\'|\w)"""(?!\"|\')')
        comment_end = QRegExp(r'(?<!\"|\'|\w)"""(?!\"|\')')
        self.highlightMultiline(text, comment_start, comment_end, self.formats['COMMENT'])

        comment_start = QRegExp(r"(?<!\"|\'|\w)'''(?!\"|\')")
        comment_end = QRegExp(r"(?<!\"|\'|\w)'''(?!\"|\')")
        self.highlightMultiline(text, comment_start, comment_end, self.formats['COMMENT'])

    def highlightMultiline(self, text, start, end, format):
        if self.previousBlockState() == 1:
            startIndex = 0
            add = 0
        else:
            startIndex = start.indexIn(text)
            add = start.matchedLength()

        while startIndex >= 0:
            endIndex = end.indexIn(text, startIndex + add)
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + end.matchedLength()

            self.setFormat(startIndex, commentLength, format)
            startIndex = start.indexIn(text, startIndex + commentLength)

    def rehighlight(self):
        QApplication.setOverrideCursor(Qt.WaitCursor)
        QSyntaxHighlighter.rehighlight(self)
        QApplication.restoreOverrideCursor()

    def setDocument(self, document):
        super().setDocument(document)
        self.rehighlight()

class CppHighlighter(SyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.l = light
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FFD700" if light else "#FFA500"))  # 更鲜艳的颜色
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            # C关键词
            "auto", "break", "case", "char", "const", "continue", "default", "do",
            "double", "else", "enum", "extern", "float", "for", "goto", "if",
            "int", "long", "register", "return", "short", "signed", "sizeof", "static",
            "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while",
            
            # C++额外关键词
            "asm", "bool", "catch", "class", "const_cast", "delete", "dynamic_cast",
            "explicit", "export", "false", "friend", "inline", "mutable", "namespace",
            "new", "operator", "private", "protected", "public", "reinterpret_cast",
            "static_cast", "template", "this", "throw", "true", "try", "typeid",
            "typename", "using", "virtual", "wchar_t",
            
            "alignas", "alignof", "char16_t", "char32_t", "constexpr", "decltype",
            "noexcept", "nullptr", "static_assert", "thread_local",
            
            "abstract", "as", "base", "byte", "checked", "decimal", "delegate", "event",
            "finally", "fixed", "foreach", "in", "interface", "internal", "is", "lock",
            "object", "out", "override", "params", "readonly", "ref", "sbyte", "sealed",
            "stackalloc", "string", "uint", "ulong", "unchecked", "unsafe", "ushort", "var"
        ]
        self.keyword_patterns = [(QRegExp(r"\b" + keyword + r"\b"), keyword_format)
                                 for keyword in keywords]

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor("#32CD32" if light else "#228B22")) 
        self.quotation_pattern = (QRegExp(r"\".*?\"|'.'"), quotation_format) 

        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(QColor("#00BFFF" if light else "#1E90FF"))  
        self.function_pattern = (QRegExp(r"\b[A-Za-z_][A-Za-z0-9_]*(?=\s*\()"), function_format)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#FF4500" if light else "#B22222"))  
        self.comment_pattern = (QRegExp(r"//[^\n]*|/\*[\s\S]*?\*/"), comment_format)  

        preprocessor_format = QTextCharFormat()
        preprocessor_format.setForeground(QColor("#8B008B" if light else "#9370DB")) 
        self.preprocessor_pattern = (QRegExp(r"^\s*#\s*\w+"), preprocessor_format)

    def highlightBlock(self, text):
        for pattern, format in self.keyword_patterns:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.highlightPattern(text, self.quotation_pattern)
        self.highlightPattern(text, self.function_pattern)
        self.highlightPattern(text, self.comment_pattern)
        self.highlightPattern(text, self.preprocessor_pattern)

    def highlightPattern(self, text, pattern):
        expression, format = pattern
        index = expression.indexIn(text)
        while index >= 0:
            length = expression.matchedLength()
            self.setFormat(index, length, format)
            index = expression.indexIn(text, index + length)

class JavaHighlighter(SyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.light = light
        
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FFD700" if light else "#FFA500"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "abstract", "assert", "boolean", "break", "byte", "case",
            "catch", "char", "class", "const", "continue", "default",
            "do", "double", "else", "enum", "extends", "final",
            "finally", "float", "for", "if", "implements",
            "import", "instanceof", "int", "interface", "long",
            "native", "new", "package", "private", "protected",
            "public", "return", "short", "static", "strictfp",
            "super", "switch", "synchronized", "this", "throw", "throws",
            "transient", "try", "void", "volatile", "while",
            "true", "false", "null", "var", "yield", "record", "sealed", "permits"
        ]
        self.keyword_patterns = [(QRegExp(r"\b" + keyword + r"\b"), keyword_format)
                                 for keyword in keywords]

        quotation_format = QTextCharFormat()
        quotation_format.setForeground(QColor("#32CD32" if light else "#228B22"))
        self.quotation_pattern = (QRegExp(r'"(?:\\.|[^"\\])*"'), quotation_format)

        function_format = QTextCharFormat()
        function_format.setFontItalic(True)
        function_format.setForeground(QColor("#00BFFF" if light else "#1E90FF"))
        self.function_pattern = (QRegExp(r"\b[A-Za-z_][A-Za-z0-9_]*(?=\s*\()"), function_format)

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#FF4500" if light else "#B22222"))
        self.single_line_comment_pattern = (QRegExp(r"//[^\n]*"), comment_format)
        self.multi_line_comment_pattern = (QRegExp(r"/\*.*?\*/", QRegExp.DotAll), comment_format)

        annotation_format = QTextCharFormat()
        annotation_format.setForeground(QColor("#8B008B" if light else "#9370DB"))
        self.annotation_pattern = (QRegExp(r"@\w+"), annotation_format)

    def highlightBlock(self, text):
        for pattern, format in self.keyword_patterns:
            self.highlightPattern(text, pattern, format)

        self.highlightPattern(text, *self.quotation_pattern)
        self.highlightPattern(text, *self.function_pattern)
        self.highlightPattern(text, *self.single_line_comment_pattern)
        self.highlightPattern(text, *self.multi_line_comment_pattern)
        self.highlightPattern(text, *self.annotation_pattern)

    def highlightPattern(self, text, pattern, format):
        expression = QRegExp(pattern)
        index = expression.indexIn(text)
        while index >= 0:
            length = expression.matchedLength()
            self.setFormat(index, length, format)
            index = expression.indexIn(text, index + length)


class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, light=True, parent=None):
        super().__init__(parent)
        self.light = light
        # 格式
        self.basic_formatting()
        # 标题
        self.header_format = QTextCharFormat()
        self.header_format.setFontWeight(QFont.Bold)
        self.header_format.setForeground(QColor("#0000FF" if light else "#4169E1"))
        
        self.emphasis_format = QTextCharFormat()
        self.emphasis_format.setFontItalic(True)
        self.emphasis_format.setForeground(QColor("#008000" if light else "#32CD32"))
        
        self.strong_format = QTextCharFormat()
        self.strong_format.setFontWeight(QFont.Bold)
        self.strong_format.setForeground(QColor("#800000" if light else "#CD5C5C"))

        self.link_format = QTextCharFormat()
        self.link_format.setForeground(QColor("#1E90FF" if light else "#87CEFA"))
        self.link_format.setFontUnderline(True)

        self.code_block_format = QTextCharFormat()
        self.code_block_format.setForeground(QColor("#808080" if light else "#A9A9A9"))
        self.code_block_format.setBackground(QColor("#F0F0F0" if light else "#2F4F4F"))

        self.list_format = QTextCharFormat()
        self.list_format.setForeground(QColor("#FF8C00" if light else "#FFA500"))

    def basic_formatting(self):
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FFD700" if self.light else "#FFA500"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "#", "##", "###", "####", "#####", "######", "*", "_", ">", "-",
            "1.", "2.", "3.", "4.", "5.", "6.", "```", "[", "]", "(", ")",
            "!", "!!", "!!!", "!!!!", "!!!!!", "!!!!!!", "~~"
        ]
        self.keyword_patterns = [(QRegExp(re.escape(keyword)), keyword_format)
                                 for keyword in keywords]

        self.quotation_format = QTextCharFormat()
        self.quotation_format.setForeground(QColor("#32CD32" if self.light else "#228B22"))
        self.quotation_pattern = QRegExp(r"`.*`")

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#FF4500" if self.light else "#B22222"))
        self.comment_pattern = QRegExp(r"<!--.*-->")

    def highlightBlock(self, text):
        for pattern, format in self.keyword_patterns:
            self.highlight_pattern(text, pattern, format)
        self.highlight_pattern(text, self.quotation_pattern, self.quotation_format)
        self.highlight_pattern(text, self.comment_pattern, self.comment_format)
        self.highlight_headers(text)
        self.highlight_emphasis_and_strong(text)
        self.highlight_links(text)
        self.highlight_code_blocks(text)
        self.highlight_lists(text)

    def highlight_pattern(self, text, pattern, format):
        expression = QRegExp(pattern)
        index = expression.indexIn(text)
        while index >= 0:
            length = expression.matchedLength()
            self.setFormat(index, length, format)
            index = expression.indexIn(text, index + length)

    def highlight_headers(self, text):
        expression = QRegExp(r"^#{1,6}\s.*$")
        self.highlight_pattern(text, expression, self.header_format)

    def highlight_emphasis_and_strong(self, text):
        self.highlight_pattern(text, r"\*[^\*]+\*", self.emphasis_format)
        self.highlight_pattern(text, r"_[^_]+_", self.emphasis_format)
        self.highlight_pattern(text, r"\*\*[^\*]+\*\*", self.strong_format)
        self.highlight_pattern(text, r"__[^_]+__", self.strong_format)

    def highlight_links(self, text):
        expression = QRegExp(r"\[([^\]]+)\]\(([^\)]+)\)")
        self.highlight_pattern(text, expression, self.link_format)

    def highlight_code_blocks(self, text):
        expression = QRegExp(r"```[\s\S]*?```")
        self.highlight_pattern(text, expression, self.code_block_format)

    def highlight_lists(self, text):
        expression = QRegExp(r"^\s*[\*\+\-]\s")
        self.highlight_pattern(text, expression, self.list_format)
        expression = QRegExp(r"^\s*\d+\.\s")
        self.highlight_pattern(text, expression, self.list_format)
