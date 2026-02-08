import markdown2
from typing import Any


class MaTex:
    def __init__(self, text: str) -> None:
        """
        Initialisiert das MaTex-Objekt.

        Args:
            text (str): Der Markdown/LaTeX-Inhalt der Dokumentation.
        """
        self.text: str = text


def render_matex(obj: Any) -> str:
    """
        Rendert ein MaTex-Objekt oder einen Standardwert als HTML-String für Taipy.

        Args:
            obj (Union[MaTex, Any]): Das zu rendernde Objekt. Falls es MaTex ist, wird Markdown/LaTeX verarbeitet.

        Returns:
            str: Der fertige HTML-Content inklusive Scripts und Styles.
    """
    if not isinstance(obj, MaTex):
        return str(obj)

    html_str: str = markdown2.markdown(obj.text, extras=["latex", "code-friendly", "breaks", "tables"])
    safe_html: str = html_str.replace("{", "{{").replace("}", "}}")

    mathjax_script: str = (
        '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>'
        '<script>window.MathJax = { tex: { inlineMath: [["$", "$"]], displayMath: [["$$", "$$"]] } };</script>'
    )

    style: str = (
        "<style>"
        "body {"
        "  font-family: var(--font-family, 'Lato', Arial, sans-serif) !important;"
        "  color: var(--color-text, #1f1f1f) !important;"
        "  margin: 0; padding: 0;"
        "  display: flex; flex-direction: row; height: 100vh;"
        "  overflow: hidden !important; /* Kein doppelter Scrollbar */"
        "}"
        ".content-area { flex: 1; padding: 40px; overflow-y: auto; scroll-behavior: smooth; }"
        ".sidebar {"
        "  flex: 0 0 20%; min-width: 180px; max-width: 400px;"
        "  border-left: 1px solid var(--color-border, #eee); padding: 25px;"
        "  height: 100vh; overflow-y: auto;"
        "  padding-top: 0px;"
        "}"
        ".sidebar a { text-decoration: none; color: var(--color-primary, #ff6049); font-size: 0.85rem; }"
        ".sidebar ul { list-style: none; padding: 0; margin: 0; }"
        ".sidebar li { margin-bottom: 8px; }"
        ".content-area{"
        "  border: 0px !important;"
        "  padding: 0px !important;"
        "  padding-right: calc(2rem) !important;"
        "  scrollbar-width: thin;"
        "  scrollbar-color: var(--custom-scrollbar-thumb-color) var(--custom-scrollbar-rail-color);"
        "}"
        ".content-area img {"
        "  max-width: 80% !important;"
        "  height: auto !important;"
        "  display: block !important;"
        "  margin: 20px auto !important;"
        "  border-radius: 4px;"
        "}"
        "table { border-collapse: collapse; width: 100%; margin: 20px 0; }"
        "th, td { border: 1px solid var(--color-border, #dfe2e5); padding: 8px 12px; }"
        "</style>"
    )

    sync_script: str = """
    <script>
    function updateTheme() {
        try {
            const parent = window.parent.document;
            const parentHtml = parent.documentElement;
            const parentBody = parent.body;
            const parentStyle = window.parent.getComputedStyle(parentHtml);
            const myRoot = document.documentElement;

            // Prüfen, ob Taipy im Dark Mode ist
            const isDark = parentBody.classList.contains('taipy-dark-mode');
            const suffix = isDark ? '-dark' : '-light';

            // Wir mappen NUR die absolut notwendigen Farben
            // Basierend auf deinem Konsolen-Screenshot:
            myRoot.style.setProperty('--color-paper', parentStyle.getPropertyValue('--color-paper' + suffix));
            myRoot.style.setProperty('--sidebar-bg', parentStyle.getPropertyValue('--color-background' + suffix));
            myRoot.style.setProperty('--color-primary', parentStyle.getPropertyValue('--color-primary'));
            myRoot.style.setProperty('--color-secondary', parentStyle.getPropertyValue('--color-secondary'));
            myRoot.style.setProperty('--color-border', 'gray');
            myRoot.style.setProperty('--custom-scrollbar-thumb-color', parentStyle.getPropertyValue('--custom-scrollbar-thumb-color'));
            myRoot.style.setProperty('--custom-scrollbar-rail-color', parentStyle.getPropertyValue('--custom-scrollbar-rail-color'));

            // Textfarbe: Taipy setzt diese oft direkt im Body
            const textColor = window.parent.getComputedStyle(parentBody).getPropertyValue('color');
            myRoot.style.setProperty('--color-text', textColor);

        } catch (e) { console.error("Theme Sync failed", e); }
    }

    // MutationObserver: Wartet darauf, dass Taipy die Klasse 'taipy-dark-mode' umschaltet
    const observer = new MutationObserver(() => updateTheme());

    function init() {
        updateTheme();
        // Wir beobachten den Body des Elternfensters auf Attribut-Änderungen (Classes)
        observer.observe(window.parent.document.body, { attributes: true });

        // TOC Generierung (wie bisher)
        const sidebarList = document.getElementById('toc-list');
        const headers = document.querySelectorAll('.content-area h1, .content-area h2, .content-area h3');
        headers.forEach((header, index) => {
            const id = 'nav-' + index;
            header.id = id;
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = '#' + id;
            a.innerHTML = header.innerHTML; 
            if(header.tagName === 'H2') li.style.paddingLeft = '10px';
            if(header.tagName === 'H3') li.style.paddingLeft = '20px';
            li.appendChild(a);
            sidebarList.appendChild(li);
        });

        if (window.MathJax && window.MathJax.typeset) window.MathJax.typeset();
    }
    window.addEventListener('load', init);
    </script>
    """

    return (f'{mathjax_script}{style}{sync_script}'
            f'<div class="content-area">{safe_html}</div>'
            f'<div class="sidebar"><h3>Inhalt</h3><ul id="toc-list"></ul></div>')

