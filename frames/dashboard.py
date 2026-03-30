import os, customtkinter as ctk
import theme as T, database as db
from utils import _title, _subtitle, _lbl, _card, _empty, calc_age, days_remaining, remaining_badge
try:
    from PIL import Image; HAS_PIL = True
except ImportError: HAS_PIL = False


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, cid, cname, app=None, **kw):
        super().__init__(parent, fg_color="transparent", **kw)
        self.cid, self.cname = cid, cname; self._build()

    def _build(self):
        sc = ctk.CTkScrollableFrame(self, fg_color="transparent")
        sc.pack(fill="both", expand=True)
        cat = db.get_cat(self.cid); age = calc_age(cat[3]) if cat else "—"

        # Başlık kartı
        hdr = _card(sc, hover=False); hdr.pack(fill="x", padx=20, pady=(16, 10))
        hi = ctk.CTkFrame(hdr, fg_color="transparent"); hi.pack(fill="x", padx=20, pady=16)
        photo = cat[9] if cat and len(cat) > 9 else ""
        if HAS_PIL and photo and os.path.exists(photo):
            img = Image.open(photo).resize((72, 72))
            self._img = ctk.CTkImage(light_image=img, dark_image=img, size=(72, 72))
            ctk.CTkLabel(hi, image=self._img, text="").pack(side="left", padx=(0, 16))
        else:
            icon_f = ctk.CTkFrame(hi, fg_color=T.SIDEBAR_ACTIVE, width=72, height=72, corner_radius=36)
            icon_f.pack(side="left", padx=(0, 16))
            icon_f.pack_propagate(False)
            ctk.CTkLabel(icon_f, text="🐱", font=ctk.CTkFont(size=32)).place(relx=0.5, rely=0.5, anchor="center")

        info = ctk.CTkFrame(hi, fg_color="transparent"); info.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(info, text=self.cname, font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=T.TEXT_PRIMARY).pack(anchor="w")
        breed = cat[2] if cat and cat[2] else "Irk belirtilmemiş"
        gender = cat[5] if cat and len(cat) > 5 and cat[5] else ""
        sub = f"{gender}  ·  {breed}  ·  {age}" if gender else f"{breed}  ·  {age}"
        ctk.CTkLabel(info, text=sub, font=ctk.CTkFont(size=12), text_color=T.TEXT_MUTED).pack(anchor="w", pady=(2, 0))

        # Bildirim banner'ı — yaklaşan 7 gün içi
        urgent = []
        for v in db.get_vaccines(self.cid):
            if v[7]:
                r = days_remaining(v[7])
                if r is not None and r <= 7: urgent.append((v[3], v[7], r))
        for p in db.get_parasites(self.cid):
            if p[5]:
                r = days_remaining(p[5])
                if r is not None and r <= 7: urgent.append((p[2], p[5], r))
        if urgent:
            banner = ctk.CTkFrame(sc, fg_color=T.ERROR, corner_radius=8)
            banner.pack(fill="x", padx=20, pady=(0, 8))
            _lbl(banner, f"⚠  {len(urgent)} acil hatırlatma", size=13, bold=True, color="white").pack(
                side="left", padx=14, pady=8)
            for u in sorted(urgent, key=lambda x: x[2])[:3]:
                bt, _ = remaining_badge(u[2])
                _lbl(banner, f"{u[0]}: {bt}", size=11, color="white").pack(side="left", padx=8)

        # Özet kartları satırı
        stats = db.get_all_stats()
        summary_row = ctk.CTkFrame(sc, fg_color="transparent")
        summary_row.pack(fill="x", padx=20, pady=(4, 8))
        vaccine_count = len(db.get_vaccines(self.cid))
        med_count = len([m for m in db.get_medications(self.cid) if m[7] == 1])
        app_count = len([a for a in db.get_appointments(self.cid) if a[6] == "Planlandı"])
        exp_total = sum(e[4] for e in db.get_expenses(self.cid))

        for i, (icon, label, value, color) in enumerate([
            ("💉", "Aşı", str(vaccine_count), T.BADGE_BLUE),
            ("💊", "Aktif İlaç", str(med_count), T.BADGE_PURPLE),
            ("📆", "Randevu", str(app_count), T.ACCENT_SECONDARY),
            ("💰", "Harcama", f"{exp_total:,.0f} ₺", T.BADGE_YELLOW),
        ]):
            sc_card = _card(summary_row, hover=True)
            sc_card.pack(side="left", fill="both", expand=True,
                         padx=(0 if i == 0 else 3, 3 if i < 3 else 0))
            ctk.CTkLabel(sc_card, text=icon, font=ctk.CTkFont(size=20)).pack(anchor="w", padx=12, pady=(10, 0))
            _lbl(sc_card, value, size=18, bold=True, color=color).pack(anchor="w", padx=12, pady=(2, 0))
            _lbl(sc_card, label, size=10, color=T.TEXT_MUTED).pack(anchor="w", padx=12, pady=(0, 10))

        # Bölümler
        self._section(sc, "Yaklaşan Aşılar", self._items(db.get_vaccines, 7), "💉", "Henüz aşı kaydı yok", "Aşı Takvimi bölümünden ilk kaydı ekleyin")
        self._section(sc, "Parazit Takvimi", self._items(db.get_parasites, 5), "🐛", "Parazit kaydı yok", "Parazit Takvimi bölümünden takip başlatın")
        self._weight_summary(sc)
        self._appointments(sc)
        self._expense_summary(sc)

    def _items(self, fn, due_idx):
        items = []
        for r in fn(self.cid):
            if r[due_idx]:
                rem = days_remaining(r[due_idx])
                if rem is not None:
                    lbl = r[3] if due_idx == 7 else r[2]
                    items.append((lbl, r[due_idx], rem))
        return sorted(items, key=lambda x: x[2])

    def _section(self, sc, title, items, empty_icon, empty_title, empty_sub):
        _title(sc, text=title).pack(anchor="w", padx=24, pady=(14, 4))
        if not items:
            _empty(sc, empty_icon, empty_title, empty_sub)
            return
        for label, due, rem in items[:5]:
            bt, bc = remaining_badge(rem)
            row = _card(sc); row.pack(fill="x", padx=24, pady=2)
            _lbl(row, label, size=13, bold=True, color=T.TEXT_PRIMARY).pack(side="left", padx=14, pady=10)
            _lbl(row, f"→ {due}", size=12, color=T.TEXT_SECONDARY).pack(side="left", padx=8)
            _lbl(row, bt, size=12, bold=True, color=bc).pack(side="right", padx=14)

    def _weight_summary(self, sc):
        _title(sc, text="Son Kilo").pack(anchor="w", padx=24, pady=(14, 4))
        ws = db.get_weights(self.cid)
        if not ws:
            _empty(sc, "⚖️", "Kilo kaydı yok", "Beslenme & Kilo bölümünden kayıt ekleyin")
            return
        w = ws[0]; row = _card(sc); row.pack(fill="x", padx=24, pady=2)
        _lbl(row, f"{w[3]} kg", size=16, bold=True, color=T.TEXT_PRIMARY).pack(side="left", padx=14, pady=10)
        _lbl(row, f"Tarih: {w[2]}", size=12, color=T.TEXT_SECONDARY).pack(side="left", padx=8)
        if len(ws) >= 2:
            diff = w[3] - ws[1][3]; s = "+" if diff > 0 else ""
            _lbl(row, f"{s}{diff:.2f} kg", size=12, bold=True,
                 color=T.ERROR if abs(diff) > 0.5 else T.ACCENT).pack(side="right", padx=14)

    def _appointments(self, sc):
        _title(sc, text="Yaklaşan Randevular").pack(anchor="w", padx=24, pady=(14, 4))
        apps = [a for a in db.get_appointments(self.cid) if a[6] == "Planlandı"]
        if not apps:
            _empty(sc, "📆", "Planlanmış randevu yok", "Randevular bölümünden yeni randevu ekleyin")
            return
        for a in sorted(apps, key=lambda x: x[2])[:3]:
            row = _card(sc); row.pack(fill="x", padx=24, pady=2)
            rem = days_remaining(a[2]); bt, bc = remaining_badge(rem)
            _lbl(row, f"{a[2]} {a[3]}", size=13, bold=True, color=T.TEXT_PRIMARY).pack(side="left", padx=14, pady=10)
            _lbl(row, a[5] or "Randevu", size=12, color=T.TEXT_SECONDARY).pack(side="left", padx=8)
            _lbl(row, bt, size=12, bold=True, color=bc).pack(side="right", padx=14)

    def _expense_summary(self, sc):
        _title(sc, text="Harcama Özeti").pack(anchor="w", padx=24, pady=(14, 4))
        es = db.get_expenses(self.cid)
        if not es:
            _empty(sc, "💰", "Harcama kaydı yok", "Harcamalar bölümünden masrafları takip edin")
            return
        total = sum(e[4] for e in es)
        row = _card(sc); row.pack(fill="x", padx=24, pady=2)
        _lbl(row, f"Toplam: {total:,.2f} ₺", size=16, bold=True, color=T.TEXT_PRIMARY).pack(side="left", padx=14, pady=10)
        _lbl(row, f"{len(es)} kayıt", size=12, color=T.TEXT_SECONDARY).pack(side="left", padx=8)
