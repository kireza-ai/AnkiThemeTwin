# AnkiThemeTwin/__init__.py  — Anki 25.x (Qt6/PyQt6)
# Global themes for Anki: Sepia (Word/Paper) and Gray (Word/Paper),
# with safe switching + legacy config compatibility.

from aqt import mw, gui_hooks
from aqt.qt import QAction, QApplication
from typing import Literal

Theme = Literal["sepia_word", "sepia_paper", "gray_word", "gray_paper"]

def get_config():
    return mw.addonManager.getConfig(__name__) or {}

def write_config(cfg: dict):
    mw.addonManager.writeConfig(__name__, cfg)

# ---------- Palettes ----------
SEPIA_WORD = {  # close to Word Immersive Reader "Sepia"
    "bg": "#F9F5E9", "fg": "#3B2F2A", "muted": "#6B5B4E", "border": "#D9D0C2",
    "accent": "#8C6F5A", "button": "#EDE5D6", "buttonText": "#3B2F2A",
    "input": "#FCF9F1", "inputText": "#3B2F2A", "hover": "#E6DECF", "selection": "#E6D9C5",
}
SEPIA_PAPER = {  # slightly darker "paper" sepia to damp reflections
    "bg": "#F3E7D3", "fg": "#3A2E29", "muted": "#6A5B4E", "border": "#CFBEA7",
    "accent": "#7C634F", "button": "#E9DFC9", "buttonText": "#3A2E29",
    "input": "#FBF4E8", "inputText": "#3A2E29", "hover": "#E2D5BF", "selection": "#DBCBB3",
}
GRAY_WORD = {  # close to Word Immersive Reader "Grey"
    "bg": "#E6E6E6", "fg": "#222222", "muted": "#4A4A4A", "border": "#CFCFCF",
    "accent": "#1F66B3", "button": "#F2F2F2", "buttonText": "#222222",
    "input": "#FFFFFF", "inputText": "#222222", "hover": "#E0E0E0", "selection": "#D0D0D0",
}
GRAY_PAPER = {  # darker neutral gray ("paper") for bright rooms
    "bg": "#D9D9D9", "fg": "#202020", "muted": "#454545", "border": "#BFBFBF",
    "accent": "#1F66B3", "button": "#E9E9E9", "buttonText": "#202020",
    "input": "#F7F7F7", "inputText": "#202020", "hover": "#D2D2D2", "selection": "#C7C7C7",
}

def palette_for(theme: Theme):
    return {
        "sepia_word": SEPIA_WORD,
        "sepia_paper": SEPIA_PAPER,
        "gray_word": GRAY_WORD,
        "gray_paper": GRAY_PAPER,
    }[theme]

# Support old config values automatically
def normalize_theme(t: str) -> Theme:
    legacy = {"sepia": "sepia_word", "gray": "gray_word"}
    v = legacy.get(t, t)
    return v if v in {"sepia_word","sepia_paper","gray_word","gray_paper"} else "sepia_word"

# ---------- WebView CSS (cards/editor/browser/toolbar HTML) ----------
def css_vars(p):
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
      line-height: 1.55;
    }}
    a, a:visited {{ color: var(--atk-accent) !important; }}
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
    """

def inject_css(web_content, ctx):
    theme = normalize_theme(get_config().get("currentTheme", "sepia_word"))
    web_content.head += f"<style>{css_vars(palette_for(theme))}</style>"

# ---------- Qt Widgets stylesheet (menus, buttons, inputs, tabs...) ----------
def qss(p):
    return f"""
    QWidget {{ background:{p['bg']}; color:{p['fg']}; }}
    QToolTip {{ background:{p['hover']}; color:{p['fg']}; border:1px solid {p['border']}; }}
    QMenu, QMenuBar, QStatusBar, QDialog, QFrame, QDockWidget {{ background:{p['bg']}; color:{p['fg']}; }}
    QPushButton {{ background:{p['button']}; color:{p['buttonText']}; border:1px solid {p['border']}; padding:6px 10px; }}
    QPushButton:hover {{ background:{p['hover']}; }}
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox, QAbstractSpinBox {{
        background:{p['input']}; color:{p['inputText']}; border:1px solid {p['border']};
        selection-background-color:{p['selection']}; selection-color:{p['fg']};
    }}
    QTreeView, QListView, QTableView {{
        background:{p['bg']}; alternate-background-color:{p['input']};
        color:{p['fg']}; gridline-color:{p['border']};
    }}
    QHeaderView::section {{ background:{p['button']}; color:{p['buttonText']}; border:1px solid {p['border']}; padding:4px 6px; }}
    QTabBar::tab {{ background:{p['button']}; color:{p['buttonText']}; border:1px solid {p['border']}; padding:6px 10px; margin:1px; }}
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

# ---------- Switch + Menu ----------
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
        ("Gray (Word-like)", "gray_word"),
        ("Gray (Paper)", "gray_paper"),
    ]
    for label, key in options:
        act = QAction(label, mw)
        act.triggered.connect(lambda _, k=key: set_theme(k))
        m.addAction(act)

def on_profile_open():
    if not getattr(mw, "_ankitwin_menu", False):
        add_menu()
        mw._ankitwin_menu = True
    apply_qt_styles(normalize_theme(get_config().get("currentTheme", "sepia_word")))

# Hooks (per Anki add-on docs)
gui_hooks.profile_did_open.append(on_profile_open)
gui_hooks.webview_will_set_content.append(inject_css)
