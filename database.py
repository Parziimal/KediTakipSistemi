"""Veritabanı katmanı — SQLite CRUD işlemleri."""

import os
import sqlite3
from contextlib import contextmanager
from datetime import date

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kedi_bakim.db")


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def transaction():
    """Çok adımlı işlemler için atomik transaction context manager.

    Kullanım::

        with db.transaction() as c:
            c.execute("INSERT INTO cats (name) VALUES (?)", ("Boncuk",))
            c.execute("INSERT INTO health_notes ...")
        # Herhangi bir exception olursa otomatik rollback yapılır.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with _conn() as c:
        c.executescript("""
            CREATE TABLE IF NOT EXISTS cats (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
                breed TEXT DEFAULT '', birthdate TEXT DEFAULT '', color TEXT DEFAULT '',
                gender TEXT DEFAULT '', blood_type TEXT DEFAULT 'Bilinmiyor',
                sterilized INTEGER DEFAULT 0, chip_no TEXT DEFAULT '',
                photo_path TEXT DEFAULT '', notes TEXT DEFAULT '',
                pet_type TEXT DEFAULT 'cat'
            );
            CREATE TABLE IF NOT EXISTS vaccines (
                id INTEGER PRIMARY KEY AUTOINCREMENT, cat_id INTEGER NOT NULL,
                vaccine_key TEXT NOT NULL, vaccine_label TEXT NOT NULL,
                category TEXT DEFAULT 'core', dose_number INTEGER DEFAULT 1,
                applied_date TEXT NOT NULL, next_due_date TEXT DEFAULT '',
                vet_name TEXT DEFAULT '', notes TEXT DEFAULT '',
                FOREIGN KEY (cat_id) REFERENCES cats(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS parasite_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, cat_id INTEGER NOT NULL,
                parasite_type TEXT NOT NULL, applied_date TEXT NOT NULL,
                product_name TEXT DEFAULT '', next_due_date TEXT DEFAULT '',
                notes TEXT DEFAULT '',
                FOREIGN KEY (cat_id) REFERENCES cats(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS weight_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT, cat_id INTEGER NOT NULL,
                log_date TEXT NOT NULL, weight REAL NOT NULL,
                food_type TEXT DEFAULT '', food_amount REAL DEFAULT 0,
                notes TEXT DEFAULT '',
                FOREIGN KEY (cat_id) REFERENCES cats(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS health_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT, cat_id INTEGER NOT NULL,
                note_date TEXT NOT NULL, title TEXT NOT NULL,
                content TEXT DEFAULT '', note_type TEXT DEFAULT 'Genel',
                FOREIGN KEY (cat_id) REFERENCES cats(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT, cat_id INTEGER NOT NULL,
                exp_date TEXT NOT NULL, category TEXT DEFAULT 'Diğer',
                amount REAL NOT NULL, description TEXT DEFAULT '', vet_id INTEGER DEFAULT 0,
                FOREIGN KEY (cat_id) REFERENCES cats(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS vets (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
                clinic TEXT DEFAULT '', phone TEXT DEFAULT '',
                address TEXT DEFAULT '', notes TEXT DEFAULT ''
            );
            CREATE TABLE IF NOT EXISTS medications (
                id INTEGER PRIMARY KEY AUTOINCREMENT, cat_id INTEGER NOT NULL,
                med_name TEXT NOT NULL, dosage TEXT DEFAULT '',
                frequency TEXT DEFAULT '', start_date TEXT DEFAULT '',
                end_date TEXT DEFAULT '', active INTEGER DEFAULT 1,
                notes TEXT DEFAULT '',
                FOREIGN KEY (cat_id) REFERENCES cats(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT, cat_id INTEGER NOT NULL,
                app_date TEXT NOT NULL, app_time TEXT DEFAULT '',
                vet_name TEXT DEFAULT '', reason TEXT DEFAULT '',
                status TEXT DEFAULT 'Planlandı', notes TEXT DEFAULT '',
                FOREIGN KEY (cat_id) REFERENCES cats(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS gallery (
                id INTEGER PRIMARY KEY AUTOINCREMENT, cat_id INTEGER NOT NULL,
                photo_path TEXT NOT NULL, caption TEXT DEFAULT '',
                added_date TEXT DEFAULT '',
                FOREIGN KEY (cat_id) REFERENCES cats(id) ON DELETE CASCADE
            );
        """)
        # Migration: pet_type kolonu yoksa ekle
        try:
            c.execute("ALTER TABLE cats ADD COLUMN pet_type TEXT DEFAULT 'cat'")
            c.commit()
        except sqlite3.OperationalError:
            pass  # Kolon zaten mevcut
        # Performans için indeksler (tekrar çalıştırılabilir)
        c.executescript("""
            CREATE INDEX IF NOT EXISTS idx_vaccines_cat   ON vaccines(cat_id);
            CREATE INDEX IF NOT EXISTS idx_parasite_cat   ON parasite_logs(cat_id);
            CREATE INDEX IF NOT EXISTS idx_weight_cat     ON weight_logs(cat_id);
            CREATE INDEX IF NOT EXISTS idx_health_cat     ON health_notes(cat_id);
            CREATE INDEX IF NOT EXISTS idx_expenses_cat   ON expenses(cat_id);
            CREATE INDEX IF NOT EXISTS idx_meds_cat       ON medications(cat_id);
            CREATE INDEX IF NOT EXISTS idx_appt_cat       ON appointments(cat_id);
            CREATE INDEX IF NOT EXISTS idx_gallery_cat    ON gallery(cat_id);
            CREATE INDEX IF NOT EXISTS idx_vaccines_date  ON vaccines(applied_date);
            CREATE INDEX IF NOT EXISTS idx_appt_date      ON appointments(app_date);
        """)
        c.commit()


# ── Kediler ───────────────────────────────────────────────────────────────────
def get_cats():
    with _conn() as c:
        try:
            return c.execute("SELECT id, name, pet_type FROM cats ORDER BY id").fetchall()
        except Exception:
            return c.execute("SELECT id, name FROM cats ORDER BY id").fetchall()

def get_cat(cid):
    with _conn() as c: return c.execute("SELECT * FROM cats WHERE id=?", (cid,)).fetchone()

def add_cat(name, pet_type="cat"):
    with _conn() as c:
        c.execute("INSERT INTO cats (name, pet_type) VALUES (?, ?)", (name, pet_type))
        return c.execute("SELECT last_insert_rowid()").fetchone()[0]

def get_pet_type(cid):
    with _conn() as c:
        try:
            r = c.execute("SELECT pet_type FROM cats WHERE id=?", (cid,)).fetchone()
            return (r[0] or "cat") if r else "cat"
        except Exception:
            return "cat"

def delete_cat(cid):
    with _conn() as c:
        c.execute("PRAGMA foreign_keys=ON")
        c.execute("DELETE FROM cats WHERE id=?", (cid,))

def save_cat(cid, d):
    with _conn() as c:
        c.execute(
            "UPDATE cats SET name=?,breed=?,birthdate=?,color=?,gender=?,blood_type=?,"
            "sterilized=?,chip_no=?,photo_path=?,notes=?,pet_type=? WHERE id=?",
            (d["name"],d["breed"],d["birthdate"],d["color"],d["gender"],d["blood_type"],
             d["sterilized"],d["chip_no"],d.get("photo_path",""),d["notes"],
             d.get("pet_type","cat"),cid))

# ── Aşılar ────────────────────────────────────────────────────────────────────
def get_vaccines(cid):
    with _conn() as c: return c.execute("SELECT * FROM vaccines WHERE cat_id=? ORDER BY applied_date DESC",(cid,)).fetchall()

def add_vaccine(cid,key,label,cat,dose,applied,nxt,vet,notes):
    with _conn() as c: c.execute("INSERT INTO vaccines(cat_id,vaccine_key,vaccine_label,category,dose_number,applied_date,next_due_date,vet_name,notes)VALUES(?,?,?,?,?,?,?,?,?)",(cid,key,label,cat,dose,applied,nxt,vet,notes))

def delete_vaccine(vid):
    with _conn() as c: c.execute("DELETE FROM vaccines WHERE id=?",(vid,))

# ── Parazit ───────────────────────────────────────────────────────────────────
def get_parasites(cid):
    with _conn() as c: return c.execute("SELECT * FROM parasite_logs WHERE cat_id=? ORDER BY applied_date DESC",(cid,)).fetchall()

def add_parasite(cid,pt,applied,prod,nxt,notes):
    with _conn() as c: c.execute("INSERT INTO parasite_logs(cat_id,parasite_type,applied_date,product_name,next_due_date,notes)VALUES(?,?,?,?,?,?)",(cid,pt,applied,prod,nxt,notes))

def delete_parasite(pid):
    with _conn() as c: c.execute("DELETE FROM parasite_logs WHERE id=?",(pid,))

# ── Kilo ──────────────────────────────────────────────────────────────────────
def get_weights(cid):
    with _conn() as c: return c.execute("SELECT * FROM weight_logs WHERE cat_id=? ORDER BY log_date DESC",(cid,)).fetchall()

def add_weight(cid,ld,w,ft,fa,n):
    with _conn() as c: c.execute("INSERT INTO weight_logs(cat_id,log_date,weight,food_type,food_amount,notes)VALUES(?,?,?,?,?,?)",(cid,ld,w,ft,fa,n))

def delete_weight(lid):
    with _conn() as c: c.execute("DELETE FROM weight_logs WHERE id=?",(lid,))

# ── Sağlık ────────────────────────────────────────────────────────────────────
def get_health(cid):
    with _conn() as c: return c.execute("SELECT * FROM health_notes WHERE cat_id=? ORDER BY note_date DESC",(cid,)).fetchall()

def add_health(cid,nd,t,ct,nt):
    with _conn() as c: c.execute("INSERT INTO health_notes(cat_id,note_date,title,content,note_type)VALUES(?,?,?,?,?)",(cid,nd,t,ct,nt))

def delete_health(nid):
    with _conn() as c: c.execute("DELETE FROM health_notes WHERE id=?",(nid,))

# ── Harcamalar ────────────────────────────────────────────────────────────────
def get_expenses(cid):
    with _conn() as c: return c.execute("SELECT * FROM expenses WHERE cat_id=? ORDER BY exp_date DESC",(cid,)).fetchall()

def add_expense(cid,ed,cat,amt,desc,vid=0):
    with _conn() as c: c.execute("INSERT INTO expenses(cat_id,exp_date,category,amount,description,vet_id)VALUES(?,?,?,?,?,?)",(cid,ed,cat,amt,desc,vid))

def delete_expense(eid):
    with _conn() as c: c.execute("DELETE FROM expenses WHERE id=?",(eid,))

# ── Veterinerler ──────────────────────────────────────────────────────────────
def get_vets():
    with _conn() as c: return c.execute("SELECT * FROM vets ORDER BY name").fetchall()

def add_vet(n,cl,ph,addr,notes):
    with _conn() as c: c.execute("INSERT INTO vets(name,clinic,phone,address,notes)VALUES(?,?,?,?,?)",(n,cl,ph,addr,notes))

def delete_vet(vid):
    with _conn() as c: c.execute("DELETE FROM vets WHERE id=?",(vid,))

# ── İlaçlar ───────────────────────────────────────────────────────────────────
def get_medications(cid):
    with _conn() as c: return c.execute("SELECT * FROM medications WHERE cat_id=? ORDER BY active DESC, start_date DESC",(cid,)).fetchall()

def add_medication(cid,name,dosage,freq,start,end,notes):
    with _conn() as c: c.execute("INSERT INTO medications(cat_id,med_name,dosage,frequency,start_date,end_date,notes)VALUES(?,?,?,?,?,?,?)",(cid,name,dosage,freq,start,end,notes))

def toggle_medication(mid,active):
    with _conn() as c: c.execute("UPDATE medications SET active=? WHERE id=?",(active,mid))

def delete_medication(mid):
    with _conn() as c: c.execute("DELETE FROM medications WHERE id=?",(mid,))

# ── Randevular ────────────────────────────────────────────────────────────────
def get_appointments(cid):
    with _conn() as c: return c.execute("SELECT * FROM appointments WHERE cat_id=? ORDER BY app_date DESC",(cid,)).fetchall()

def add_appointment(cid,ad,at,vet,reason,status,notes):
    with _conn() as c: c.execute("INSERT INTO appointments(cat_id,app_date,app_time,vet_name,reason,status,notes)VALUES(?,?,?,?,?,?,?)",(cid,ad,at,vet,reason,status,notes))

def update_appointment_status(aid,status):
    with _conn() as c: c.execute("UPDATE appointments SET status=? WHERE id=?",(status,aid))

def delete_appointment(aid):
    with _conn() as c: c.execute("DELETE FROM appointments WHERE id=?",(aid,))

# ── Galeri ────────────────────────────────────────────────────────────────────
def get_gallery(cid):
    with _conn() as c: return c.execute("SELECT * FROM gallery WHERE cat_id=? ORDER BY added_date DESC",(cid,)).fetchall()

def add_gallery_photo(cid,path,caption):
    with _conn() as c: c.execute("INSERT INTO gallery(cat_id,photo_path,caption,added_date)VALUES(?,?,?,?)",(cid,path,caption,date.today().isoformat()))

def update_gallery_caption(gid, caption):
    with _conn() as c: c.execute("UPDATE gallery SET caption=? WHERE id=?", (caption, gid))

def delete_gallery_photo(gid):
    with _conn() as c: c.execute("DELETE FROM gallery WHERE id=?",(gid,))

# ── İstatistikler ─────────────────────────────────────────────────────────────
def get_all_stats():
    with _conn() as c:
        cats = c.execute("SELECT COUNT(*) FROM cats").fetchone()[0]
        vaccines = c.execute("SELECT COUNT(*) FROM vaccines").fetchone()[0]
        expenses_total = c.execute("SELECT COALESCE(SUM(amount),0) FROM expenses").fetchone()[0]
        weights = c.execute("SELECT COUNT(*) FROM weight_logs").fetchone()[0]
        health = c.execute("SELECT COUNT(*) FROM health_notes").fetchone()[0]
        meds = c.execute("SELECT COUNT(*) FROM medications WHERE active=1").fetchone()[0]
        apps = c.execute("SELECT COUNT(*) FROM appointments WHERE status='Planlandı'").fetchone()[0]
        exp_by_cat = c.execute(
            "SELECT c.name, COALESCE(SUM(e.amount),0) FROM cats c LEFT JOIN expenses e ON c.id=e.cat_id GROUP BY c.id"
        ).fetchall()
        exp_by_category = c.execute(
            "SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC LIMIT 5"
        ).fetchall()
        return {
            "cats": cats, "vaccines": vaccines, "expenses_total": expenses_total,
            "weights": weights, "health": health, "active_meds": meds,
            "pending_apps": apps, "exp_by_cat": exp_by_cat, "exp_by_category": exp_by_category,
        }


# ── Arama ────────────────────────────────────────────────────────────────────
def search_all(cid, q):
    results = []
    q = f"%{q}%"
    with _conn() as c:
        for r in c.execute("SELECT vaccine_label, applied_date, notes FROM vaccines WHERE cat_id=? AND (vaccine_label LIKE ? OR notes LIKE ?)", (cid, q, q)):
            results.append(("💉 Aşı", r[0], r[1], r[2]))
        for r in c.execute("SELECT med_name, dosage, notes FROM medications WHERE cat_id=? AND (med_name LIKE ? OR notes LIKE ?)", (cid, q, q)):
            results.append(("💊 İlaç", r[0], r[1], r[2]))
        for r in c.execute("SELECT title, note_date, content FROM health_notes WHERE cat_id=? AND (title LIKE ? OR content LIKE ?)", (cid, q, q)):
            results.append(("🏥 Sağlık", r[0], r[1], r[2]))
        for r in c.execute("SELECT reason, app_date, vet_name FROM appointments WHERE cat_id=? AND (reason LIKE ? OR vet_name LIKE ? OR notes LIKE ?)", (cid, q, q, q)):
            results.append(("📆 Randevu", r[0], r[1], r[2]))
        for r in c.execute("SELECT category, exp_date, description FROM expenses WHERE cat_id=? AND (category LIKE ? OR description LIKE ?)", (cid, q, q)):
            results.append(("💰 Harcama", r[0], r[1], r[2]))
        for r in c.execute("SELECT parasite_type, applied_date, product_name FROM parasite_logs WHERE cat_id=? AND (parasite_type LIKE ? OR product_name LIKE ?)", (cid, q, q)):
            results.append(("🐛 Parazit", r[0], r[1], r[2]))
        for r in c.execute("SELECT name, clinic, phone FROM vets WHERE name LIKE ? OR clinic LIKE ?", (q, q)):
            results.append(("🩺 Veteriner", r[0], r[1], r[2]))
    return results
