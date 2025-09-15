# AnkiThemeTwin/__init__.py — Anki 25.x (Qt6/PyQt6)
# 7 themes with high-contrast, readability-first palettes.
# Switch from Tools > Theme: AnkiThemeTwin

from aqt import mw, gui_hooks
from aqt.qt import QAction, QApplication
from typing import Literal

Theme = Literal[
    "sepia_word", "sepia_paper", "gray_word", "gray_paper",
    "sepia_special", "dark_warm_soft", "dark_neutral_soft"
]

def get_config():
    return mw.addonManager.getConfig(__name__) or {}

def write_config(cfg: dict):
    mw.addonManager.writeConfig(__name__, cfg)

# ---------------- Palettes (readability-first; tuned for AA contrast) ----------------
# Word-like variants (baseline)
SEPIA_WORD = {
    "bg": "#F9F5E9", "fg": "#2A2420",  # darker text than before for stronger contrast
    "muted": "#5C524A", "border": "#D9D0C2",
    "accent": "#7B5F4B",  # link (warm, still readable)
    "button": "#EDE5D6", "buttonText": "#2A2420",
    "input": "#FCF9F1", "inputText": "#2A2420",
    "hover": "#E6DECF", "selection": "#DACCB7",
}

SEPIA_PAPER = {  # a bit darker to damp reflections in brighter rooms
    "bg": "#F3E7D3", "fg": "#29231F",
    "muted": "#5B4E44", "border": "#CFBEA7",
    "accent": "#715843",
    "button": "#E9DFC9", "buttonText": "#29231F",
    "input": "#FBF4E8", "inputText": "#29231F",
    "hover": "#E2D5BF", "selection": "#D7C6AC",
}

GRAY_WORD = {
    "bg": "#E6E6E6", "fg": "#1E1E1E",
    "muted": "#454545", "border": "#CFCFCF",
    "accent": "#0F5AA6",
    "button": "#F2F2F2", "buttonText": "#1E1E1E",
    "input": "#FFFFFF", "inputText": "#1E1E1E",
    "hover": "#E0E0E0", "selection": "#CFCFCF",
}

GRAY_PAPER = {  # darker neutral gray "paper"
    "bg": "#D9D9D9", "fg": "#1C1C1C",
    "muted": "#3F3F3F", "border": "#BFBFBF",
    "accent": "#0F5AA6",
    "button": "#E9E9E9", "buttonText": "#1C1C1C",
    "input": "#F7F7F7", "inputText": "#1C1C1C",
    "hover": "#D2D2D2", "selection": "#C5C5C5",
}

# NEW — your special sepia: warmer, slightly darker paper tone for anti-glare
SEPIA_SPECIAL = {
    "bg": "#EEDFC6", "fg": "#201A16",            # very dark text for crisp edges
    "muted": "#54483F", "border": "#CDB99F",
    "accent": "#6D523F",
    "button": "#E6D3B7", "buttonText": "#201A16",
    "input": "#FAF2E4", "inputText": "#201A16",
    "hover": "#DFC9A9", "selection": "#D2BC9C",
}

# NEW — soft dark (NOT pure black) with warm foreground
DARK_WARM_SOFT = {
    "bg": "#2F2A27", "fg": "#F5F2ED",           # near-white text for high contrast
    "muted": "#D1C7BC", "border": "#6B5E55",
    "accent": "#FFD8A0",                        # warm links
    "button": "#3A332F", "buttonText": "#F5F2ED",
    "input": "#3A332F", "inputText": "#F5F2ED",
    "hover": "#3F3833", "selection": "#5A5048",
}

# NEW — soft dark neutral (cooler link; still not pitch black)
DARK_NEUTRAL_SOFT = {
    "bg": "#303030", "fg": "#F2F2F2",
    "muted": "#CFCFCF", "border": "#5A5A5A",
    "accent": "#80B9FF",                        # accessible cool blue
    "button": "#3A3A3A", "buttonText": "#F2F2F2",
    "input": "#3A3A3A", "inputText": "#F2F2F2",
    "hover": "#404040", "selection": "#5A5A5A",
}

PALETTES = {
    "sepia_word": SEPIA_WORD,
    "sepia_paper": SEPIA_PAPER,
    "gray_word": GRAY_WORD,
    "gray_paper": GRAY_PAPER,
    "sepia_special": SEPIA_SPECIAL,
    "dark_warm_soft": DARK_WARM_SOFT,
    "dark_neutral_soft": DARK_NEUTRAL_SOFT,
}

def palette_for(theme: Theme):
    return PALETTES[theme]

# Backward compatibility for older config values
def normalize_theme(t: str) -> Theme:
    legacy = {"sepia": "sepia_word", "gray": "gray_word", "dark": "dark_neutral_soft"}
    v = legacy.get(t, t)
    return v if v in PALETTES else "sepia_special"

# ---------------- WebView CSS (cards/editor/browser/toolbar HTML) ----------------
def css_vars(p):
    # Extra readability tweaks:
    # - stronger defaults for text, headings and links
    # - underlines on links to avoid color-only reliance
    # - slightly larger base size for comfort; adjust if you prefer
    return f"""
    :root {{
      --atk-bg:{p['bg']}; --atk-fg:{p['fg']}; --atk-muted:{p['muted']}; --atk-border:{p['border']};
      --atk-accent:{p['accent']}; --atk-btn:{p['button']}; --atk-btn-text:{p['buttonText']};
      --atk-input:{p['input']}; --atk-input-text:{p['inputText']};
      --atk-hover:{p['hover']}; --atk-selection:{p['selection']};
    }}
    html, body {{
      background: var(--atk-bg) !important;
      color: var(--atk-fg) !important;
      font-family: "Segoe UI", "Amiri", "Arial", sans-serif !important;
      line-height: 1.58;
      font-size: 16px;
      -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility;
    }}
    a, a:visited {{
      color: var(--atk-accent) !important; text-decoration: underline;
      text-underline-offset: 2px;
    }}
    ::selection {{ background: var(--atk-selection); color: var(--atk-fg); }}
    .card, .content, .row {{ background: var(--atk-bg) !important; color: var(--atk-fg) !important; }}
    input, textarea, select {{
      background: var(--atk-input) !important; color: var(--atk-input-text) !important;
      border: 1px solid var(--atk-border) !important;
    }}
    button, .btn, .md-button {{
      background: var(--atk-btn) !important; color: var(--atk-btn-text) !important;
      border: 1px solid var(--atk-border) !important;
    }}
    .is-muted, .hint, .field, .tags {{ color: var(--atk-muted) !important; }}
    hr {{ border-color: var(--atk-border) !important; }}
    h1,h2,h3 {{ color: var(--atk-fg) !important; font-weight: 700; }}
    strong,b {{ color: var(--atk-fg) !important; font-weight: 700; }}
    """

def inject_css(web_content, ctx):
    theme = normalize_theme(get_config().get("currentTheme", "sepia_special"))
    web_content.head += f"<style>{css_vars(palette_for(theme))}</style>"

# ---------------- Qt Widgets stylesheet (menus, buttons, inputs, tabs...) ----------------
def qss(p):
    # Keep high contrast for text; avoid over-styling layouts.
    return f"""
    QWidget {{ background:{p['bg']}; color:{p['fg']}; }}
    QToolTip {{ background:{p['hover']}; color:{p['fg']}; border:1px solid {p['border']}; }}
    QMenu, QMenuBar, QStatusBar, QDialog, QFrame, QDockWidget {{ background:{p['bg']}; color:{p['fg']}; }}
    QPushButton {{
        background:{p['button']}; color:{p['buttonText']};
        border:1px solid {p['border']}; padding:6px 10px; font-weight:600;
    }}
    QPushButton:hover {{ background:{p['hover']}; }}
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox, QAbstractSpinBox {{
        background:{p['input']}; color:{p['inputText']};
        border:1px solid {p['border']};
        selection-background-color:{p['selection']}; selection-color:{p['fg']};
    }}
    QTreeView, QListView, QTableView {{
        background:{p['bg']}; alternate-background-color:{p['input']};
        color:{p['fg']}; gridline-color:{p['border']};
    }}
    QHeaderView::section {{
        background:{p['button']}; color:{p['buttonText']};
        border:1px solid {p['border']}; padding:4px 6px; font-weight:600;
    }}
    QTabBar::tab {{
        background:{p['button']}; color:{p['buttonText']};
        border:1px solid {p['border']}; padding:6px 10px; margin:1px;
    }}
    QTabBar::tab:selected {{ background:{p['hover']}; }}
    QScrollBar:vertical {{ background:{p['bg']}; width:12px; margin:0; }}
    QScrollBar::handle:vertical {{ background:{p['border']}; min-height:20px; border-radius:6px; }}
    QScrollBar:horizontal {{ background:{p['bg']}; height:12px; margin:0; }}
    QScrollBar::handle:horizontal {{ background:{p['border']}; min-width:20px; border-radius:6px; }}
    a, QLabel#linkLabel {{ color:{p['accent']}; }}
    """

def apply_qt_styles(theme: Theme):
    app = QApplication.instance()
    if app:
        app.setStyleSheet(qss(palette_for(theme)))

# ---------------- Switch + Menu ----------------
def set_theme(theme: Theme):
    theme = normalize_theme(theme)
    cfg = get_config()
    if cfg.get("currentTheme") != theme:
        cfg["currentTheme"] = theme
        write_config(cfg)
    apply_qt_styles(theme)

def add_menu():
    m = mw.form.menuTools.addMenu("Theme: AnkiThemeTwin")
    options = [
        ("Sepia (Word-like)", "sepia_word"),
        ("Sepia (Paper)", "sepia_paper"),
        ("Sepia (Special • Dr. M)", "sepia_special"),
        ("Gray (Word-like)", "gray_word"),
        ("Gray (Paper)", "gray_paper"),
        ("Dark • Warm (Soft)", "dark_warm_soft"),
        ("Dark • Neutral (Soft)", "dark_neutral_soft"),
    ]
    for label, key in options:
        act = QAction(label, mw)
        act.triggered.connect(lambda _, k=key: set_theme(k))
        m.addAction(act)

def on_profile_open():
    if not getattr(mw, "_ankitwin_menu", False):
        add_menu(); mw._ankitwin_menu = True
    apply_qt_styles(normalize_theme(get_config().get("currentTheme", "sepia_special")))

# Hooks
gui_hooks.profile_did_open.append(on_profile_open)
gui_hooks.webview_will_set_content.append(inject_css)
