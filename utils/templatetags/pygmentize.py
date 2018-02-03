from django import template
import re
from pygments import highlight
from pygments.lexers import PythonLexer, guess_lexer
from pygments.formatters import HtmlFormatter 

register = template.Library()

regex = re.compile(r'<code>(.*?)</code>', re.DOTALL)

@register.filter(name='pygmentize')
def pygmentize(value):
        last_end = 0
        to_return = ''
        found = 0
        for match_obj in regex.finditer(value):
            code_string = match_obj.group(1)
            try:
                lexer = guess_lexer(code_string)
            except ValueError:
                lexer = PythonLexer()
            pygmented_string = highlight(code_string, lexer, HtmlFormatter())
            to_return = to_return + value[last_end:match_obj.start(1)] + pygmented_string
            last_end = match_obj.end(1)
            found = found + 1
        to_return = to_return + value[last_end:]
        return to_return
