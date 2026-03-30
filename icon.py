"""Otomatik kedi pati ikonu oluşturucu."""

import os
import sys

ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app_icon.ico")


def create_icon():
    """Pillow ile kedi pati ikonu oluştur ve .ico olarak kaydet."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return None

    if os.path.exists(ICON_PATH):
        return ICON_PATH

    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Meadow green renkler
    pad_color = (76, 175, 80, 255)       # #4CAF50
    pad_dark = (46, 125, 50, 255)        # #2E7D32
    bg_circle = (15, 30, 23, 200)        # koyu yeşil arka plan

    # Arka plan daire
    draw.ellipse([10, 10, 246, 246], fill=bg_circle)

    # Ana pati (büyük oval)
    cx, cy = 128, 160
    draw.ellipse([cx-45, cy-35, cx+45, cy+35], fill=pad_color, outline=pad_dark, width=3)

    # 4 parmak (küçük ovaller)
    toes = [
        (cx-55, cy-75, 30, 26),   # sol dış
        (cx-20, cy-95, 28, 24),   # sol iç
        (cx+20, cy-95, 28, 24),   # sağ iç
        (cx+55, cy-75, 30, 26),   # sağ dış
    ]
    for tx, ty, rw, rh in toes:
        draw.ellipse([tx-rw//2, ty-rh//2, tx+rw//2, ty+rh//2],
                     fill=pad_color, outline=pad_dark, width=2)

    # Çoklu boyut kaydet
    img.save(ICON_PATH, format="ICO", sizes=[(256, 256), (64, 64), (48, 48), (32, 32), (16, 16)])
    return ICON_PATH


def set_app_icon(app):
    """Uygulama ve görev çubuğu ikonunu ayarla."""
    icon_path = create_icon()
    if not icon_path:
        return

    # Windows görev çubuğu için AppUserModelID
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("kedibakimtakip.v4")
        except Exception:
            pass

    # İkonu ayarla (gecikmeyle — customtkinter uyumluluğu)
    try:
        app.after(250, lambda: app.iconbitmap(icon_path))
    except Exception:
        pass
