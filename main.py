"""
Kedi Bakım Takip Uygulaması — Loki & Yuumi
Gereksinimler: pip install customtkinter
"""

import os
import sqlite3
from datetime import date, datetime, timedelta

import customtkinter as ctk

# ── Görünüm ───────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kedi_bakim.db")

VACCINE_INTERVALS: dict[str, int] = {
    "İç Parazit": 60,       # 2 ayda bir
    "Karma Aşı": 365,       # 12 ayda bir
    "Kuduz": 365,
    "Dış Parazit": 30,
    "Lösemi": 365,
    "Diğer": 365,
}

SECTIONS = [
    ("👤  Profil",           "profile"),
    ("💉  Aşı Takvimi",      "vaccine"),
    ("🍽️  Beslenme & Kilo",  "nutrition"),
    ("🏥  Sağlık Notları",   "health"),
]

# ── Veritabanı ────────────────────────────────────────────────────────────────

def _conn() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    with _conn() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS cats (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                breed      TEXT    DEFAULT '',
                birthdate  TEXT    DEFAULT '',
                color      TEXT    DEFAULT '',
                sterilized INTEGER DEFAULT 0,
                chip_no    TEXT    DEFAULT '',
                notes      TEXT    DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS vaccines (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                cat_id       INTEGER NOT NULL,
                vaccine_type TEXT    NOT NULL,
                last_date    TEXT    NOT NULL,
                notes        TEXT    DEFAULT '',
                FOREIGN KEY (cat_id) REFERENCES cats(id)
            );
            CREATE TABLE IF NOT EXISTS weight_logs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                cat_id      INTEGER NOT NULL,
                log_date    TEXT    NOT NULL,
                weight      REAL    NOT NULL,
                food_type   TEXT    DEFAULT '',
                food_amount REAL    DEFAULT 0,
                notes       TEXT    DEFAULT '',
                FOREIGN KEY (cat_id) REFERENCES cats(id)
            );
            CREATE TABLE IF NOT EXISTS health_notes (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                cat_id    INTEGER NOT NULL,
                note_date TEXT    NOT NULL,
                title     TEXT    NOT NULL,
                content   TEXT    DEFAULT '',
                note_type TEXT    DEFAULT 'Genel',
                FOREIGN KEY (cat_id) REFERENCES cats(id)
            );
        """)
        # Varsayılan kedileri ekle
        cur = con.execute("SELECT COUNT(*) FROM cats")
        if cur.fetchone()[0] == 0:
            con.executemany("INSERT INTO cats (name) VALUES (?)", [("Loki",), ("Yuumi",)])
        # Yuumi'nin ameliyat notunu ekle (örnek)
        cur2 = con.execute(
            "SELECT id FROM cats WHERE name='Yuumi' LIMIT 1"
        )
        yuumi = cur2.fetchone()
        if yuumi:
            cur3 = con.execute(
                "SELECT COUNT(*) FROM health_notes WHERE cat_id=? AND note_type='Ameliyat'",
                (yuumi[0],),
            )
            if cur3.fetchone()[0] == 0:
                con.execute(
                    """INSERT INTO health_notes (cat_id, note_date, title, content, note_type)
                       VALUES (?, ?, ?, ?, ?)""",
                    (
                        yuumi[0],
                        date.today().strftime("%Y-%m-%d"),
                        "Mide Ameliyatı — Hazırlık Notu",
                        "Yuumi'nin mide ameliyatı geçmişini buraya ekleyin.\n"
                        "Örn: ameliyat tarihi, operatör veteriner, uygulanan işlem, iyileşme süreci...",
                        "Ameliyat",
                    ),
                )
        con.commit()


# ── DB yardımcı fonksiyonlar ──────────────────────────────────────────────────

def get_cats() -> list[tuple]:
    with _conn() as con:
        return con.execute("SELECT id, name FROM cats ORDER BY id").fetchall()


def get_cat(cat_id: int) -> tuple | None:
    with _conn() as con:
        return con.execute("SELECT * FROM cats WHERE id=?", (cat_id,)).fetchone()


def save_cat(cat_id: int, d: dict) -> None:
    with _conn() as con:
        con.execute(
            "UPDATE cats SET name=?,breed=?,birthdate=?,color=?,sterilized=?,chip_no=?,notes=? WHERE id=?",
            (d["name"], d["breed"], d["birthdate"], d["color"],
             d["sterilized"], d["chip_no"], d["notes"], cat_id),
        )


def get_vaccines(cat_id: int) -> list[tuple]:
    with _conn() as con:
        return con.execute(
            "SELECT * FROM vaccines WHERE cat_id=? ORDER BY last_date DESC", (cat_id,)
        ).fetchall()


def add_vaccine(cat_id: int, vtype: str, last_date: str, notes: str) -> None:
    with _conn() as con:
        con.execute(
            "INSERT INTO vaccines (cat_id,vaccine_type,last_date,notes) VALUES (?,?,?,?)",
            (cat_id, vtype, last_date, notes),
        )


def delete_vaccine(vid: int) -> None:
    with _conn() as con:
        con.execute("DELETE FROM vaccines WHERE id=?", (vid,))


def get_weight_logs(cat_id: int) -> list[tuple]:
    with _conn() as con:
        return con.execute(
            "SELECT * FROM weight_logs WHERE cat_id=? ORDER BY log_date DESC", (cat_id,)
        ).fetchall()


def add_weight_log(cat_id, log_date, weight, food_type, food_amount, notes) -> None:
    with _conn() as con:
        con.execute(
            "INSERT INTO weight_logs (cat_id,log_date,weight,food_type,food_amount,notes) VALUES (?,?,?,?,?,?)",
            (cat_id, log_date, weight, food_type, food_amount, notes),
        )


def delete_weight_log(lid: int) -> None:
    with _conn() as con:
        con.execute("DELETE FROM weight_logs WHERE id=?", (lid,))


def get_health_notes(cat_id: int) -> list[tuple]:
    with _conn() as con:
        return con.execute(
            "SELECT * FROM health_notes WHERE cat_id=? ORDER BY note_date DESC", (cat_id,)
        ).fetchall()


def add_health_note(cat_id, note_date, title, content, note_type) -> None:
    with _conn() as con:
        con.execute(
            "INSERT INTO health_notes (cat_id,note_date,title,content,note_type) VALUES (?,?,?,?,?)",
            (cat_id, note_date, title, content, note_type),
        )


def delete_health_note(nid: int) -> None:
    with _conn() as con:
        con.execute("DELETE FROM health_notes WHERE id=?", (nid,))


def days_until_next(last_date_str: str, interval: int) -> tuple[int | None, date | None]:
    try:
        last = datetime.strptime(last_date_str, "%Y-%m-%d").date()
        next_dt = last + timedelta(days=interval)
        return (next_dt - date.today()).days, next_dt
    except ValueError:
        return None, None


# ── Ortak widget'lar ──────────────────────────────────────────────────────────

class SectionTitle(ctk.CTkLabel):
    def __init__(self, parent, text, **kw):
        super().__init__(
            parent, text=text,
            font=ctk.CTkFont(size=21, weight="bold"),
            text_color="#e94560", **kw,
        )


class Card(ctk.CTkFrame):
    def __init__(self, parent, **kw):
        super().__init__(parent, fg_color="#16213e", corner_radius=12, **kw)


def _lbl(parent, text, size=13, bold=False, color=None, **kw):
    font = ctk.CTkFont(size=size, weight="bold" if bold else "normal")
    kwargs = dict(text=text, font=font, **kw)
    if color:
        kwargs["text_color"] = color
    return ctk.CTkLabel(parent, **kwargs)


def _toast(widget, msg: str, color: str = "lightgreen") -> None:
    lbl = ctk.CTkLabel(widget, text=msg, text_color=color,
                       font=ctk.CTkFont(size=13, weight="bold"))
    lbl.pack(pady=(0, 4))
    widget.after(2200, lbl.destroy)


# ── Profil Sekmesi ────────────────────────────────────────────────────────────

class ProfileFrame(ctk.CTkFrame):
    def __init__(self, parent, cat_id: int, cat_name: str, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cat_id = cat_id
        self.cat_name = cat_name
        self._build()

    def _build(self):
        SectionTitle(self, text=f"🐱  {self.cat_name} — Profil").pack(
            anchor="w", padx=24, pady=(22, 10)
        )
        card = Card(self)
        card.pack(fill="x", padx=24, pady=8)
        card.columnconfigure(1, weight=1)

        fields = [
            ("İsim", "name"),
            ("Irk", "breed"),
            ("Doğum Tarihi  (YYYY-MM-DD)", "birthdate"),
            ("Renk / Desen", "color"),
            ("Çip No", "chip_no"),
        ]
        self.vars: dict[str, ctk.StringVar] = {}
        for i, (lbl_text, key) in enumerate(fields):
            ctk.CTkLabel(card, text=lbl_text + ":", anchor="e",
                         font=ctk.CTkFont(size=13)).grid(
                row=i, column=0, sticky="e", padx=(18, 8), pady=9
            )
            var = ctk.StringVar()
            self.vars[key] = var
            ctk.CTkEntry(card, textvariable=var, width=280).grid(
                row=i, column=1, sticky="w", padx=(0, 18), pady=9
            )

        r = len(fields)
        ctk.CTkLabel(card, text="Kısırlaştırıldı:", anchor="e",
                     font=ctk.CTkFont(size=13)).grid(row=r, column=0, sticky="e", padx=(18, 8), pady=9)
        self.steril_var = ctk.BooleanVar()
        ctk.CTkCheckBox(card, text="Evet", variable=self.steril_var).grid(
            row=r, column=1, sticky="w", padx=(0, 18), pady=9
        )

        ctk.CTkLabel(card, text="Notlar:", anchor="ne",
                     font=ctk.CTkFont(size=13)).grid(row=r+1, column=0, sticky="ne", padx=(18, 8), pady=9)
        self.notes_box = ctk.CTkTextbox(card, height=80, width=280)
        self.notes_box.grid(row=r+1, column=1, sticky="w", padx=(0, 18), pady=9)

        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.grid(row=r+2, column=0, columnspan=2, pady=14)
        ctk.CTkButton(btn_row, text="💾  Kaydet", command=self._save,
                      fg_color="#e94560", hover_color="#c73652", width=130).pack(side="left", padx=8)
        ctk.CTkButton(btn_row, text="↺  Yenile", command=self._load, width=110).pack(side="left", padx=8)

        self._load()

    def _load(self):
        row = get_cat(self.cat_id)
        if not row:
            return
        # id, name, breed, birthdate, color, sterilized, chip_no, notes
        keys = ["name", "breed", "birthdate", "color", "chip_no"]
        vals = [row[1], row[2], row[3], row[4], row[6]]
        for k, v in zip(keys, vals):
            self.vars[k].set(v or "")
        self.steril_var.set(bool(row[5]))
        self.notes_box.delete("1.0", "end")
        self.notes_box.insert("1.0", row[7] or "")

    def _save(self):
        data = {k: v.get() for k, v in self.vars.items()}
        data["sterilized"] = int(self.steril_var.get())
        data["notes"] = self.notes_box.get("1.0", "end-1c")
        save_cat(self.cat_id, data)
        _toast(self, "Kaydedildi ✓")


# ── Aşı Takvimi Sekmesi ───────────────────────────────────────────────────────

class VaccineFrame(ctk.CTkFrame):
    def __init__(self, parent, cat_id: int, cat_name: str, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cat_id = cat_id
        self.cat_name = cat_name
        self._build()

    def _build(self):
        SectionTitle(self, text=f"💉  {self.cat_name} — Aşı Takvimi").pack(
            anchor="w", padx=24, pady=(22, 10)
        )

        # Ekleme formu
        form = Card(self)
        form.pack(fill="x", padx=24, pady=(0, 10))
        _lbl(form, "Yeni Aşı Ekle", size=14, bold=True).pack(anchor="w", padx=16, pady=(12, 4))

        r1 = ctk.CTkFrame(form, fg_color="transparent")
        r1.pack(fill="x", padx=16, pady=4)
        _lbl(r1, "Tür:").pack(side="left")
        self.vtype_var = ctk.StringVar(value="İç Parazit")
        ctk.CTkComboBox(r1, variable=self.vtype_var, values=list(VACCINE_INTERVALS.keys()),
                        width=170).pack(side="left", padx=(6, 18))
        _lbl(r1, "Tarih (YYYY-MM-DD):").pack(side="left")
        self.vdate_var = ctk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        ctk.CTkEntry(r1, textvariable=self.vdate_var, width=130).pack(side="left", padx=6)

        r2 = ctk.CTkFrame(form, fg_color="transparent")
        r2.pack(fill="x", padx=16, pady=(4, 12))
        _lbl(r2, "Not:").pack(side="left")
        self.vnotes_var = ctk.StringVar()
        ctk.CTkEntry(r2, textvariable=self.vnotes_var, width=360).pack(side="left", padx=6)
        ctk.CTkButton(r2, text="+ Ekle", command=self._add,
                      fg_color="#e94560", hover_color="#c73652", width=90).pack(side="left", padx=10)

        _lbl(self, "Geçmiş & Planlama", size=15, bold=True).pack(anchor="w", padx=24, pady=(6, 4))
        self.list_frame = ctk.CTkScrollableFrame(self, height=340)
        self.list_frame.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self._refresh()

    def _add(self):
        add_vaccine(self.cat_id, self.vtype_var.get(), self.vdate_var.get(), self.vnotes_var.get())
        self.vnotes_var.set("")
        self._refresh()

    def _refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        rows = get_vaccines(self.cat_id)
        if not rows:
            _lbl(self.list_frame, "Henüz aşı kaydı yok.", color="gray").pack(pady=24)
            return

        # Başlık satırı
        hdr = ctk.CTkFrame(self.list_frame, fg_color="#0f3460")
        hdr.pack(fill="x", pady=(0, 3))
        for col, w in [("Tür", 155), ("Son Tarih", 110), ("Sonraki Tarih", 125),
                       ("Kalan", 120), ("Not", 190), ("", 70)]:
            ctk.CTkLabel(hdr, text=col, width=w, anchor="w",
                         font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5, pady=7)

        # Sıralama: en acil önce (kalan gün artan)
        def sort_key(row):
            remaining, _ = days_until_next(row[3], VACCINE_INTERVALS.get(row[2], 365))
            return remaining if remaining is not None else 9999

        for row in sorted(rows, key=sort_key):
            vid, _, vtype, last_date, notes = row
            interval = VACCINE_INTERVALS.get(vtype, 365)
            remaining, next_dt = days_until_next(last_date, interval)

            if remaining is None:
                badge, tcolor = "?", "gray"
            elif remaining < 0:
                badge, tcolor = f"⚠  {abs(remaining)} gün geçti!", "#ff4444"
            elif remaining <= 7:
                badge, tcolor = f"🔴  {remaining} gün", "#ff6644"
            elif remaining <= 30:
                badge, tcolor = f"🟡  {remaining} gün", "#ffcc00"
            else:
                badge, tcolor = f"🟢  {remaining} gün", "#55ee88"

            card = ctk.CTkFrame(self.list_frame, fg_color="#16213e", corner_radius=8)
            card.pack(fill="x", pady=2)
            for text, w in [
                (vtype, 155), (last_date, 110),
                (str(next_dt) if next_dt else "?", 125),
            ]:
                ctk.CTkLabel(card, text=text, width=w, anchor="w",
                             font=ctk.CTkFont(size=12)).pack(side="left", padx=5, pady=9)
            ctk.CTkLabel(card, text=badge, width=120, anchor="w",
                         text_color=tcolor,
                         font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5)
            ctk.CTkLabel(card, text=notes or "—", width=190, anchor="w",
                         text_color="#999999").pack(side="left", padx=5)
            ctk.CTkButton(card, text="Sil", width=65, fg_color="#2a2a3e",
                          hover_color="#c73652",
                          command=lambda v=vid: self._delete(v)).pack(side="left", padx=5)

    def _delete(self, vid):
        delete_vaccine(vid)
        self._refresh()


# ── Beslenme & Kilo Sekmesi ───────────────────────────────────────────────────

class NutritionFrame(ctk.CTkFrame):
    def __init__(self, parent, cat_id: int, cat_name: str, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cat_id = cat_id
        self.cat_name = cat_name
        self._build()

    def _build(self):
        SectionTitle(self, text=f"🍽️  {self.cat_name} — Beslenme & Kilo").pack(
            anchor="w", padx=24, pady=(22, 10)
        )
        form = Card(self)
        form.pack(fill="x", padx=24, pady=(0, 10))
        _lbl(form, "Yeni Kayıt", size=14, bold=True).pack(anchor="w", padx=16, pady=(12, 4))

        r1 = ctk.CTkFrame(form, fg_color="transparent")
        r1.pack(fill="x", padx=16, pady=4)
        _lbl(r1, "Tarih:").pack(side="left")
        self.date_var = ctk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        ctk.CTkEntry(r1, textvariable=self.date_var, width=130).pack(side="left", padx=(6, 18))
        _lbl(r1, "Kilo (kg):").pack(side="left")
        self.weight_var = ctk.StringVar()
        ctk.CTkEntry(r1, textvariable=self.weight_var, width=80).pack(side="left", padx=(6, 18))
        _lbl(r1, "Mama Türü:").pack(side="left")
        self.food_type_var = ctk.StringVar()
        ctk.CTkEntry(r1, textvariable=self.food_type_var, width=160).pack(side="left", padx=6)

        r2 = ctk.CTkFrame(form, fg_color="transparent")
        r2.pack(fill="x", padx=16, pady=(4, 12))
        _lbl(r2, "Miktar (g):").pack(side="left")
        self.amount_var = ctk.StringVar()
        ctk.CTkEntry(r2, textvariable=self.amount_var, width=80).pack(side="left", padx=(6, 18))
        _lbl(r2, "Not:").pack(side="left")
        self.notes_var = ctk.StringVar()
        ctk.CTkEntry(r2, textvariable=self.notes_var, width=300).pack(side="left", padx=6)
        ctk.CTkButton(r2, text="+ Ekle", command=self._add,
                      fg_color="#e94560", hover_color="#c73652", width=90).pack(side="left", padx=10)

        _lbl(self, "Geçmiş Kayıtlar", size=15, bold=True).pack(anchor="w", padx=24, pady=(6, 4))
        self.list_frame = ctk.CTkScrollableFrame(self, height=320)
        self.list_frame.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self._refresh()

    def _add(self):
        try:
            weight = float(self.weight_var.get()) if self.weight_var.get() else 0.0
            amount = float(self.amount_var.get()) if self.amount_var.get() else 0.0
        except ValueError:
            _toast(self, "Kilo / miktar sayı olmalı!", "#ff6644")
            return
        add_weight_log(self.cat_id, self.date_var.get(), weight,
                       self.food_type_var.get(), amount, self.notes_var.get())
        self.weight_var.set("")
        self.amount_var.set("")
        self.notes_var.set("")
        self._refresh()

    def _delete(self, lid):
        delete_weight_log(lid)
        self._refresh()

    def _refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
        rows = get_weight_logs(self.cat_id)
        if not rows:
            _lbl(self.list_frame, "Henüz kayıt yok.", color="gray").pack(pady=24)
            return

        hdr = ctk.CTkFrame(self.list_frame, fg_color="#0f3460")
        hdr.pack(fill="x", pady=(0, 3))
        for col, w in [("Tarih", 115), ("Kilo", 80), ("Mama Türü", 160),
                       ("Miktar", 90), ("Not", 230), ("", 70)]:
            ctk.CTkLabel(hdr, text=col, width=w, anchor="w",
                         font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=5, pady=7)

        for row in rows:
            lid, _, log_date, weight, food_type, food_amount, notes = row
            card = ctk.CTkFrame(self.list_frame, fg_color="#16213e", corner_radius=8)
            card.pack(fill="x", pady=2)
            for text, w in [
                (log_date, 115),
                (f"{weight} kg" if weight else "—", 80),
                (food_type or "—", 160),
                (f"{food_amount} g" if food_amount else "—", 90),
                (notes or "—", 230),
            ]:
                ctk.CTkLabel(card, text=text, width=w, anchor="w",
                             font=ctk.CTkFont(size=12),
                             text_color="#cccccc").pack(side="left", padx=5, pady=9)
            ctk.CTkButton(card, text="Sil", width=65, fg_color="#2a2a3e",
                          hover_color="#c73652",
                          command=lambda l=lid: self._delete(l)).pack(side="left", padx=5)


# ── Sağlık Notları Sekmesi ────────────────────────────────────────────────────

NOTE_COLORS: dict[str, str] = {
    "Ameliyat":  "#e94560",
    "Acil":      "#ff6600",
    "Muayene":   "#3388ff",
    "İlaç":      "#9944ee",
    "Genel":     "#2299cc",
    "Diğer":     "#555577",
}


class HealthNotesFrame(ctk.CTkFrame):
    def __init__(self, parent, cat_id: int, cat_name: str, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cat_id = cat_id
        self.cat_name = cat_name
        self._build()

    def _build(self):
        SectionTitle(self, text=f"🏥  {self.cat_name} — Sağlık Notları").pack(
            anchor="w", padx=24, pady=(22, 10)
        )
        form = Card(self)
        form.pack(fill="x", padx=24, pady=(0, 10))
        _lbl(form, "Yeni Sağlık Notu", size=14, bold=True).pack(anchor="w", padx=16, pady=(12, 4))

        r1 = ctk.CTkFrame(form, fg_color="transparent")
        r1.pack(fill="x", padx=16, pady=4)
        _lbl(r1, "Tarih:").pack(side="left")
        self.date_var = ctk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        ctk.CTkEntry(r1, textvariable=self.date_var, width=130).pack(side="left", padx=(6, 18))
        _lbl(r1, "Tür:").pack(side="left")
        self.ntype_var = ctk.StringVar(value="Genel")
        ctk.CTkComboBox(r1, variable=self.ntype_var,
                        values=list(NOTE_COLORS.keys()), width=140).pack(side="left", padx=(6, 18))
        _lbl(r1, "Başlık:").pack(side="left")
        self.title_var = ctk.StringVar()
        ctk.CTkEntry(r1, textvariable=self.title_var, width=280).pack(side="left", padx=6)

        r2 = ctk.CTkFrame(form, fg_color="transparent")
        r2.pack(fill="x", padx=16, pady=(4, 12))
        _lbl(r2, "İçerik:").pack(side="left", anchor="n", pady=6)
        self.content_box = ctk.CTkTextbox(r2, height=72, width=500)
        self.content_box.pack(side="left", padx=8)
        ctk.CTkButton(r2, text="+ Ekle", command=self._add,
                      fg_color="#e94560", hover_color="#c73652", width=90).pack(
            side="left", padx=8, anchor="s", pady=4
        )

        _lbl(self, "Sağlık Geçmişi", size=15, bold=True).pack(anchor="w", padx=24, pady=(6, 4))
        self.list_frame = ctk.CTkScrollableFrame(self, height=320)
        self.list_frame.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        self._refresh()

    def _add(self):
        title = self.title_var.get().strip()
        if not title:
            _toast(self, "Başlık boş olamaz!", "#ff6644")
            return
        add_health_note(self.cat_id, self.date_var.get(), title,
                        self.content_box.get("1.0", "end-1c"), self.ntype_var.get())
        self.title_var.set("")
        self.content_box.delete("1.0", "end")
        self._refresh()

    def _delete(self, nid):
        delete_health_note(nid)
        self._refresh()

    def _refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()
        rows = get_health_notes(self.cat_id)
        if not rows:
            _lbl(self.list_frame, "Henüz sağlık notu yok.", color="gray").pack(pady=24)
            return

        for row in rows:
            nid, _, note_date, title, content, note_type = row
            color = NOTE_COLORS.get(note_type, "#555577")

            card = ctk.CTkFrame(self.list_frame, fg_color="#16213e", corner_radius=10)
            card.pack(fill="x", pady=5, padx=2)

            top = ctk.CTkFrame(card, fg_color="transparent")
            top.pack(fill="x", padx=14, pady=(10, 4))
            ctk.CTkLabel(top, text=f"  {note_type}  ",
                         font=ctk.CTkFont(size=11, weight="bold"),
                         fg_color=color, corner_radius=6,
                         text_color="white").pack(side="left")
            ctk.CTkLabel(top, text=f"   {note_date}  —  {title}",
                         font=ctk.CTkFont(size=13, weight="bold")).pack(side="left")
            ctk.CTkButton(top, text="Sil", width=65, fg_color="#2a2a3e",
                          hover_color="#c73652",
                          command=lambda n=nid: self._delete(n)).pack(side="right")

            if content.strip():
                ctk.CTkLabel(card, text=content, anchor="w", justify="left",
                             text_color="#bbbbbb", wraplength=720,
                             font=ctk.CTkFont(size=12)).pack(
                    anchor="w", padx=16, pady=(0, 10)
                )


# ── Ana Uygulama ──────────────────────────────────────────────────────────────

FRAME_CLASSES = {
    "profile":   ProfileFrame,
    "vaccine":   VaccineFrame,
    "nutrition": NutritionFrame,
    "health":    HealthNotesFrame,
}


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🐾  Kedi Bakım Takip — Loki & Yuumi")
        self.geometry("1140x720")
        self.minsize(920, 620)
        self._cats = get_cats()
        self._active_cat = self._cats[0][0]
        self._active_section = "profile"
        self._frames: dict[tuple, ctk.CTkFrame] = {}
        self._cat_btns: dict[int, ctk.CTkButton] = {}
        self._sec_btns: dict[str, ctk.CTkButton] = {}
        self._build_ui()

    # ── UI kurulumu ───────────────────────────────────────────────────────────

    def _build_ui(self):
        # Sidebar
        sidebar = ctk.CTkFrame(self, width=230, corner_radius=0, fg_color="#12122a")
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        ctk.CTkLabel(sidebar, text="🐾  Kedi Bakım",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#e94560").pack(pady=(26, 3), padx=18)
        ctk.CTkLabel(sidebar, text="Loki & Yuumi",
                     font=ctk.CTkFont(size=12),
                     text_color="#888888").pack(pady=(0, 18))
        ctk.CTkFrame(sidebar, height=1, fg_color="#2a2a4a").pack(fill="x", padx=18)

        ctk.CTkLabel(sidebar, text="KED İ SEÇ",
                     font=ctk.CTkFont(size=10),
                     text_color="#666688").pack(pady=(16, 6))
        for cat_id, cat_name in self._cats:
            btn = ctk.CTkButton(
                sidebar, text=cat_name, width=192, height=38,
                fg_color="#0f3460" if cat_id == self._active_cat else "transparent",
                hover_color="#0f3460",
                font=ctk.CTkFont(size=14, weight="bold"),
                command=lambda cid=cat_id: self._select_cat(cid),
            )
            btn.pack(pady=3, padx=18)
            self._cat_btns[cat_id] = btn

        ctk.CTkFrame(sidebar, height=1, fg_color="#2a2a4a").pack(fill="x", padx=18, pady=14)
        ctk.CTkLabel(sidebar, text="BÖLÜMLER",
                     font=ctk.CTkFont(size=10),
                     text_color="#666688").pack(pady=(0, 6))
        for label, key in SECTIONS:
            active = (key == self._active_section)
            btn = ctk.CTkButton(
                sidebar, text=label, width=192, height=40, anchor="w",
                fg_color="#e94560" if active else "transparent",
                hover_color="#c73652" if active else "#1e1e3e",
                font=ctk.CTkFont(size=13),
                command=lambda k=key: self._select_section(k),
            )
            btn.pack(pady=3, padx=18)
            self._sec_btns[key] = btn

        # İçerik alanı
        self.content = ctk.CTkFrame(self, fg_color="#0d0d1e", corner_radius=0)
        self.content.pack(side="left", fill="both", expand=True)
        self._show_frame()

    # ── Navigasyon ────────────────────────────────────────────────────────────

    def _select_cat(self, cat_id: int):
        self._active_cat = cat_id
        for cid, btn in self._cat_btns.items():
            btn.configure(fg_color="#0f3460" if cid == cat_id else "transparent")
        for f in self._frames.values():
            f.destroy()
        self._frames.clear()
        self._show_frame()

    def _select_section(self, key: str):
        self._active_section = key
        for k, btn in self._sec_btns.items():
            active = (k == key)
            btn.configure(
                fg_color="#e94560" if active else "transparent",
                hover_color="#c73652" if active else "#1e1e3e",
            )
        self._show_frame()

    def _show_frame(self):
        cat_id = self._active_cat
        cat_name = next(n for i, n in self._cats if i == cat_id)
        key = (cat_id, self._active_section)

        for w in self.content.winfo_children():
            w.pack_forget()

        if key not in self._frames:
            cls = FRAME_CLASSES[self._active_section]
            self._frames[key] = cls(self.content, cat_id, cat_name)

        self._frames[key].pack(fill="both", expand=True)


# ── Giriş noktası ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    App().mainloop()
