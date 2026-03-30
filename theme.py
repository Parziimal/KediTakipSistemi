"""Çoklu Tema Sistemi — Yeşil, Gri, Pembe."""

# ── Tema Paletleri ───────────────────────────────────────────────────────────

THEMES = {
    "green": {
        "name": "Mint", "orb": "#7DFFB3",
        "SIDEBAR_BG": "#0E1F18", "SIDEBAR_HOVER": "#183D2C", "SIDEBAR_ACTIVE": "#20523A",
        "MAIN_BG": "#111C16", "CARD_BG": "#1A3025",  "BORDER": "#2C5A40",
        "ACCENT": "#7DFFB3", "ACCENT_HOVER": "#A8FFD0", "ACCENT_DARK": "#4CE89A",
        "TEXT_PRIMARY": "#E0FFF0", "TEXT_SECONDARY": "#9CD4B5", "TEXT_MUTED": "#5A9E76",
        "BADGE_GREEN": "#7DFFB3", "BADGE_TEAL": "#6EE7D4",
        "BTN_TEXT": "#0A1F12",
    },
    "gray": {
        "name": "Lavanta", "orb": "#B8A9E8",
        "SIDEBAR_BG": "#171428", "SIDEBAR_HOVER": "#252040", "SIDEBAR_ACTIVE": "#342E58",
        "MAIN_BG": "#141224", "CARD_BG": "#1E1A35", "BORDER": "#3D3668",
        "ACCENT": "#B8A9E8", "ACCENT_HOVER": "#D1C4FF", "ACCENT_DARK": "#9B87DB",
        "TEXT_PRIMARY": "#EDE7FF", "TEXT_SECONDARY": "#B8A9E8", "TEXT_MUTED": "#6E5FAA",
        "BADGE_GREEN": "#81E6A0", "BADGE_TEAL": "#80D8E0",
        "BTN_TEXT": "#141224",
    },
    "pink": {
        "name": "Sakura", "orb": "#FFB2D1",
        "SIDEBAR_BG": "#1E0F18", "SIDEBAR_HOVER": "#38192E", "SIDEBAR_ACTIVE": "#4A2240",
        "MAIN_BG": "#1A0D15", "CARD_BG": "#291420", "BORDER": "#502A40",
        "ACCENT": "#FFB2D1", "ACCENT_HOVER": "#FFD4E8", "ACCENT_DARK": "#FF8AB8",
        "TEXT_PRIMARY": "#FFF0F5", "TEXT_SECONDARY": "#F5A3C7", "TEXT_MUTED": "#9A5070",
        "BADGE_GREEN": "#88E8A8", "BADGE_TEAL": "#88D8E8",
        "BTN_TEXT": "#1E0F18",
    },
}

# ── Aktif tema (varsayılan: yeşil) ───────────────────────────────────────────
_current = "green"

def _apply(t):
    global SIDEBAR_BG, SIDEBAR_HOVER, SIDEBAR_ACTIVE, MAIN_BG, CARD_BG, BORDER
    global ACCENT, ACCENT_HOVER, ACCENT_DARK, ACCENT_SECONDARY
    global TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED
    global SUCCESS, WARNING, ERROR
    global BADGE_GREEN, BADGE_TEAL, BADGE_BLUE, BADGE_PURPLE, BADGE_ORANGE, BADGE_YELLOW, BADGE_PINK
    global VACCINE_COLORS, NOTE_COLORS, PARASITE_COLORS, EXPENSE_COLORS
    global BTN_TEXT

    p = THEMES[t]
    SIDEBAR_BG    = p["SIDEBAR_BG"]
    SIDEBAR_HOVER = p["SIDEBAR_HOVER"]
    SIDEBAR_ACTIVE = p["SIDEBAR_ACTIVE"]
    MAIN_BG       = p["MAIN_BG"]
    CARD_BG       = p["CARD_BG"]
    BORDER        = p["BORDER"]
    ACCENT        = p["ACCENT"]
    ACCENT_HOVER  = p["ACCENT_HOVER"]
    ACCENT_DARK   = p["ACCENT_DARK"]
    ACCENT_SECONDARY = "#FF9800"
    TEXT_PRIMARY   = p["TEXT_PRIMARY"]
    TEXT_SECONDARY = p["TEXT_SECONDARY"]
    TEXT_MUTED     = p["TEXT_MUTED"]
    BTN_TEXT       = p["BTN_TEXT"]

    SUCCESS = p["ACCENT"]
    WARNING = "#FFA726"
    ERROR   = "#EF5350"

    BADGE_GREEN  = p["BADGE_GREEN"]
    BADGE_TEAL   = p["BADGE_TEAL"]
    BADGE_BLUE   = "#42A5F5"
    BADGE_PURPLE = "#CE93D8"
    BADGE_ORANGE = "#FF7043"
    BADGE_YELLOW = "#FFD54F"
    BADGE_PINK   = "#F48FB1"

    VACCINE_COLORS = {
        "FVRCP": BADGE_BLUE, "Kuduz": ERROR, "FeLV": BADGE_ORANGE,
        "Bordetella": BADGE_PURPLE, "Chlamydia": BADGE_TEAL, "FIP": TEXT_MUTED,
    }
    NOTE_COLORS = {
        "Ameliyat": ERROR, "Acil": BADGE_ORANGE, "Muayene": BADGE_BLUE,
        "İlaç": BADGE_PURPLE, "Genel": BADGE_TEAL, "Diğer": TEXT_MUTED,
    }
    PARASITE_COLORS = {
        "İç Parazit (Yavru)": BADGE_ORANGE, "İç Parazit (Yetişkin)": "#ee8844",
        "Dış Parazit (Pire)": "#cc6633", "Dış Parazit (Kene)": "#aa5533",
        "Kalp Kurdu": BADGE_PINK,
    }
    EXPENSE_COLORS = {
        "Aşı": BADGE_GREEN, "Muayene": BADGE_BLUE, "Ameliyat": ERROR,
        "İlaç": BADGE_PURPLE, "Mama": BADGE_YELLOW, "Aksesuar": BADGE_TEAL,
        "Bakım / Tıraş": ACCENT, "Acil": BADGE_ORANGE,
        "Check-up": BADGE_BLUE, "Tahlil / Görüntüleme": "#78909C", "Diğer": TEXT_MUTED,
    }


def set_theme(name):
    global _current
    if name in THEMES:
        _current = name
        _apply(name)


def get_current():
    return _current


# İlk yükleme
_apply(_current)
