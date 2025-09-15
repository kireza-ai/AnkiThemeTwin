# AnkiThemeTwin/__init__.py — Anki 25.x (Qt6/PyQt6)
# 7 high-readability themes + About dialog + GitHub link
# Tools > Theme: AnkiThemeTwin  |  Help > About AnkiThemeTwin

from aqt import mw, gui_hooks
from aqt.qt import (
    QAction, QApplication,
    QDialog, QVBoxLayout, QLabel, QPushButton,
)
from aqt.utils import openLink
from typing import Literal

Theme = Literal[
    "sepia_word", "sepia_paper", "gray_word", "gray_paper",
    "sepia_special", "dark_warm_soft", "dark_neutral_soft"
]

def get_config():
    return mw.addonManager.getConfig(__name__) or {}

def write_config(cfg: dict):
    mw.addonManager.writeConfig(__name__, cfg)

# ---------------- Palettes (readability-first) ----------------
SEPIA_WORD = {"bg":"#F9F5E9","fg":"#2A2420","muted":"#5C524A","border":"#D9D0C2",
    "accent":"#7B5F4B","button":"#EDE5D6","buttonText":"#2A2420",
    "input":"#FCF9F1","inputText":"#2A2420","hover":"#E6DECF","selection":"#DACCB7"}
SEPIA_PAPER = {"bg":"#F3E7D3","fg":"#29231F","muted":"#5B4E44","border":"#CFBEA7",
    "accent":"#715843","button":"#E9DFC9","buttonText":"#29231F",
    "input":"#FBF4E8","inputText":"#29231F","hover":"#E2D5BF","selection":"#D7C6AC"}
GRAY_WORD = {"bg":"#E6E6E6","fg":"#1E1E1E","muted":"#454545","border":"#CFCFCF",
    "accent":"#0F5AA6","button":"#F2F2F2","buttonText":"#1E1E1E",
    "input":"#FFFFFF","inputText":"#1E1E1E","hover":"#E0E0E0","selection":"#CFCFCF"}
GRAY_PAPER = {"bg":"#D9D9D9","fg":"#1C1C1C","muted":"#3F3F3F","border":"#BFBFBF",
    "accent":"#0F5AA6","button":"#E9E9E9","buttonText":"#1C1C1C",
    "input":"#F7F7F7","inputText":"#1C1C1C","hover":"#D2D2D2","selection":"#C5C5C5"}
SEPIA_SPECIAL = {"bg":"#EEDFC6","fg":"#201A16","muted":"#54483F","border":"#CDB99F",
    "accent":"#6D523F","button":"#E6D3B7","buttonText":"#201A16",
    "input":"#FAF2E4","inputText":"#201A16","hover":"#DFC9A9","selection":"#D2BC9C"}
DARK_WARM_SOFT = {"bg":"#2F2A27","fg":"#F5F2ED","muted":"#D1C7BC","border":"#6B5E55",
    "accent":"#FFD8A0","button":"#3A332F","buttonText":"#F5F2ED",
    "input":"#3A332F","inputText":"#F5F2ED","hover":"#3F3833","selection":"#5A5048"}
DARK_NEUTRAL_SOFT = {"bg":"#303030","fg":"#F2F2F2","muted":"#CFCFCF","border":"#5A5A5A",
    "accent":"#80B9FF","button":"#3A3A3A","buttonText":"#F2F2F2",
    "input":"#3A3A3A","inputText":"#F2F2F2","hover":"#404040","selection":"#5A5A5A"}

PALETTES = {
    "sepia_word": SEPIA_WORD,
    "sepia_paper": SEPIA_PAPER,
    "gray_word": GRAY_WORD,
    "gray_paper": GRAY_PAPER,
    "sepia_special": SEPIA_SPECIAL,
    "dark_warm_soft": DARK_WARM_SOFT,
    "dark_neutral_soft": DARK_NEUTRAL_SOFT,
}

def palette_for(theme: Theme): return PALETTES[theme]

def normalize_theme(t: str) -> Theme:
    legacy = {"sepia":"sepia_word","gray":"gray_word","dark":"dark_neutral_soft"}
    v = legacy.get(t, t)
    return v if v in PALETTES else "sepia_special"

# ---------------- CSS/QSS ----------------
def css_vars(p):
    return f"""
    html, body {{
      background:{p['bg']} !important; color:{p['fg']} !important;
      font-family:"Segoe UI","Amiri","Arial",sans-serif !important;
      line-height:1.58; font-size:16px;
      -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
    }}
    a {{ color:{p['accent']} !important; text-decoration:underline; }}
    ::selection {{ background:{p['selection']}; color:{p['fg']}; }}
    """

def inject_css(web_content, ctx):
    theme = normalize_theme(get_config().get("currentTheme","sepia_special"))
    web_content.head += f"<style>{css_vars(palette_for(theme))}</style>"

def qss(p):
    return f"QWidget {{ background:{p['bg']}; color:{p['fg']}; }}"

def apply_qt_styles(theme: Theme):
    app = QApplication.instance()
    if app: app.setStyleSheet(qss(palette_for(theme)))

# ---------------- About Dialog ----------------
def show_about_dialog():
    dlg = QDialog(mw); dlg.setWindowTitle("About — AnkiThemeTwin")
    layout = QVBoxLayout(dlg)
    lbl = QLabel(
        '<div style="font-size:14px;">'
        '<b>AnkiThemeTwin</b><br>'
        'Eye-comfort themes with high readability.<br><br>'
        'Author: <b>Dr. Mohammed</b><br>'
        '<a href="https://github.com/MohammedTsmu/AnkiThemeTwin">'
        'GitHub: MohammedTsmu/AnkiThemeTwin</a>'
        '</div>'
    )
    lbl.setOpenExternalLinks(True); layout.addWidget(lbl)
    btn = QPushButton("Open GitHub")
    btn.clicked.connect(lambda: openLink("https://github.com/MohammedTsmu/AnkiThemeTwin"))
    layout.addWidget(btn)
    closeBtn = QPushButton("Close"); closeBtn.clicked.connect(dlg.accept)
    layout.addWidget(closeBtn)
    dlg.setLayout(layout); dlg.resize(520,240); dlg.exec()

# ---------------- Menu ----------------
def set_theme(theme: Theme):
    theme = normalize_theme(theme); cfg = get_config()
    if cfg.get("currentTheme")!=theme:
        cfg["currentTheme"]=theme; write_config(cfg)
    apply_qt_styles(theme)

def add_menu():
    m = mw.form.menuTools.addMenu("Theme: AnkiThemeTwin")
    options = [
        ("Sepia (Word-like)","sepia_word"),
        ("Sepia (Paper)","sepia_paper"),
        ("Sepia (Special • Dr. M)","sepia_special"),
        ("Gray (Word-like)","gray_word"),
        ("Gray (Paper)","gray_paper"),
        ("Dark • Warm (Soft)","dark_warm_soft"),
        ("Dark • Neutral (Soft)","dark_neutral_soft"),
    ]
    for label,key in options:
        act=QAction(label,mw); act.triggered.connect(lambda _,k=key:set_theme(k))
        m.addAction(act)
    m.addSeparator()
    actGitHub=QAction("Visit Project GitHub",mw)
    actGitHub.triggered.connect(lambda: openLink("https://github.com/MohammedTsmu/AnkiThemeTwin"))
    m.addAction(actGitHub)
    actAbout=QAction("About AnkiThemeTwin",mw)
    actAbout.triggered.connect(show_about_dialog)
    m.addAction(actAbout)
    help_menu=mw.form.menuHelp
    actAboutHelp=QAction("About AnkiThemeTwin",mw)
    actAboutHelp.triggered.connect(show_about_dialog)
    help_menu.addAction(actAboutHelp)

def on_profile_open():
    if not getattr(mw,"_ankitwin_menu",False):
        add_menu(); mw._ankitwin_menu=True
    apply_qt_styles(normalize_theme(get_config().get("currentTheme","sepia_special")))

gui_hooks.profile_did_open.append(on_profile_open)
gui_hooks.webview_will_set_content.append(inject_css)
