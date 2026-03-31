"""Çoklu Tema Sistemi — Yeşil, Gri, Pembe."""

# ── Tema Paletleri ───────────────────────────────────────────────────────────

THEMES = {
    "green": {
        "name": "Teal", "orb": "#00FFFF",
        "SIDEBAR_BG": "#0A0A0A", "SIDEBAR_HOVER": "#1A1A1A", "SIDEBAR_ACTIVE": "#252525",
        "MAIN_BG": "#121212", "CARD_BG": "#1E1E1E", "BORDER": "#333333",
        "ACCENT": "#00FFFF", "ACCENT_HOVER": "#66FFFF", "ACCENT_DARK": "#00CCCC",
        "TEXT_PRIMARY": "#FFFFFF", "TEXT_SECONDARY": "#B0B0B0", "TEXT_MUTED": "#666666",
        "BADGE_GREEN": "#00E676", "BADGE_TEAL": "#00FFFF",
        "BTN_TEXT": "#0A0A0A",
    },
    "gray": {
        "name": "Gece", "orb": "#FFD700",
        "SIDEBAR_BG": "#000D22", "SIDEBAR_HOVER": "#001844", "SIDEBAR_ACTIVE": "#002266",
        "MAIN_BG": "#001133", "CARD_BG": "#002266", "BORDER": "#003399",
        "ACCENT": "#FFD700", "ACCENT_HOVER": "#FFE44D", "ACCENT_DARK": "#CCB000",
        "TEXT_PRIMARY": "#FFFFFF", "TEXT_SECONDARY": "#AAC4E8", "TEXT_MUTED": "#5577AA",
        "BADGE_GREEN": "#66FF88", "BADGE_TEAL": "#66DDEE",
        "BTN_TEXT": "#001133",
    },
    "pink": {
        "name": "Pastel", "orb": "#FFB6C1",
        "SIDEBAR_BG": "#ECECEC", "SIDEBAR_HOVER": "#DEDEDE", "SIDEBAR_ACTIVE": "#D0D0D0",
        "MAIN_BG": "#F8F8F8", "CARD_BG": "#FFFFFF", "BORDER": "#E0E0E0",
        "ACCENT": "#FF8FAB", "ACCENT_HOVER": "#FFB6C1", "ACCENT_DARK": "#E0708A",
        "TEXT_PRIMARY": "#333333", "TEXT_SECONDARY": "#666666", "TEXT_MUTED": "#999999",
        "BADGE_GREEN": "#66BB6A", "BADGE_TEAL": "#4DB6AC",
        "BTN_TEXT": "#FFFFFF",
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
        # Kedi
        "FVRCP": BADGE_BLUE, "Kuduz": ERROR, "FeLV": BADGE_ORANGE,
        "Bordetella": BADGE_PURPLE, "Chlamydia": BADGE_TEAL, "FIP": TEXT_MUTED,
        # Köpek
        "DA2PP": BADGE_BLUE, "Kuduz_K": ERROR, "Leptospirosis": BADGE_TEAL,
        "Bordetella_K": BADGE_PURPLE, "Lyme": BADGE_GREEN,
        "CanineInfluenza": BADGE_ORANGE, "CCV_K": TEXT_MUTED,
        # Kuş
        "Polyomavirus": BADGE_PINK, "NewcastleDisease": BADGE_YELLOW,
        "WestNile": TEXT_MUTED,
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
