import markdown2
from pathlib import Path

class MaTex:
    def __init__(self, text):
        self.text = text

def render_matex(obj):
    if isinstance(obj, MaTex):
        html_str = markdown2.markdown(obj.text, extras=["latex", "code-friendly", "breaks"])
        safe_html = html_str.replace("{", "{{").replace("}", "}}")
        mathjax_script = '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'
        body_style = (
            "<style>"
            "body {"
            "font-family: var(--font-family, Lato, Arial, sans-serif) !important;"
            "font-size: 1rem !important;"
            "line-height: 1.5 !important;"
            "color: var(--color-text, #1f1f1f) !important;"
            "background: var(--color-paper, #ffffff) !important;"
            "margin: 0 !important;"
            "padding: 0 !important;"
            "border: none !important;"
            "}"
            "</style>"
        )
        return f'{mathjax_script}{body_style}<div class="taipy-text">{safe_html}</div>'
    return str(obj)

