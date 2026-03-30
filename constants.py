"""Sabitler — Irklar, aşı kılavuzu, parazit takvimi, listeler."""

CAT_BREEDS = [
    "Tekir (Tabby)", "Karışık / Melez", "Van Kedisi", "Ankara Kedisi (Angora)",
    "British Shorthair", "British Longhair", "Scottish Fold", "Scottish Straight",
    "Persian (İran)", "Exotic Shorthair", "Siamese (Siyam)", "Maine Coon",
    "Ragdoll", "Bengal", "Russian Blue", "Sphynx", "Norwegian Forest",
    "Birman", "Abyssinian", "Devon Rex", "Cornish Rex", "Burmese",
    "Somali", "Chartreux", "Manx", "Tonkinese", "Ocicat", "Bombay",
    "Himalayan", "Balinese", "Oriental Shorthair", "Singapura",
    "Turkish Van", "Savannah", "Munchkin", "Selkirk Rex", "Korat",
    "Egyptian Mau", "American Shorthair", "Havana Brown", "Diğer",
]
CAT_COLORS = [
    "Siyah", "Beyaz", "Gri", "Turuncu (Sarman)", "Tekir Gri", "Tekir Turuncu",
    "Siyah-Beyaz (Tuxedo)", "Üç Renkli (Calico)", "Kaplumbağa (Tortoiseshell)",
    "Krem", "Mavi (Blue)", "Çikolata", "Lila (Lilac)", "Tarçın",
    "Siyam Deseni (Point)", "Dumanlı (Smoke)", "Gümüş Tabby", "Diğer",
]
CAT_GENDERS = ["Dişi", "Erkek"]
CAT_BLOOD_TYPES = ["A", "B", "AB", "Bilinmiyor"]
FOOD_TYPES = [
    "Kuru Mama", "Yaş Mama", "Ev Yapımı", "Çiğ Et (BARF)", "Diyet Mama",
    "Yavru Mama", "Kısır Mama", "Hassas Mide", "Böbrek Diyeti",
    "Karışık (Kuru + Yaş)", "Diğer",
]
HEALTH_NOTE_TYPES = ["Genel", "Ameliyat", "Acil", "Muayene", "İlaç", "Diğer"]
EXPENSE_CATEGORIES = [
    "Aşı", "Muayene", "Ameliyat", "İlaç", "Mama", "Aksesuar",
    "Bakım / Tıraş", "Acil", "Check-up", "Tahlil / Görüntüleme", "Diğer",
]
MED_FREQUENCIES = [
    "Günde 1", "Günde 2", "Günde 3", "Haftada 1", "Haftada 2",
    "Ayda 1", "Gerektiğinde", "Diğer",
]
MONTHS_TR = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
             "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]

# ── WSAVA 2024 & AAFP 2020 ───────────────────────────────────────────────────
VACCINE_GUIDELINES = {
    "FVRCP": {
        "full_name": "Feline Viral Rhinotracheitis, Calicivirus, Panleukopenia",
        "tr_name": "Karma Aşı (FVRCP)", "category": "core", "category_tr": "Temel",
        "components": "FHV-1 (Herpes), FCV (Calici), FPV (Panleukopeni)",
        "kitten_weeks": [6, 9, 12, 16, 26],
        "adult_interval_days": 1095, "adult_interval_label": "3 yılda bir",
        "notes": "6 haftadan itibaren 3-4 hafta arayla. 26. haftada ek doz. Yetişkin: 3 yılda bir.",
    },
    "Kuduz": {
        "full_name": "Rabies Virus Vaccine",
        "tr_name": "Kuduz Aşısı", "category": "core", "category_tr": "Temel",
        "components": "Rabies virüsü", "kitten_weeks": [12],
        "adult_interval_days": 365, "adult_interval_label": "Yılda bir",
        "notes": "12-16 haftada tek doz. Rapel 1 yıl sonra.",
    },
    "FeLV": {
        "full_name": "Feline Leukemia Virus",
        "tr_name": "Kedi Lösemi (FeLV)", "category": "core",
        "category_tr": "Temel (yavru) / Risk bazlı (yetişkin)",
        "components": "FeLV antijeni", "kitten_weeks": [8, 12],
        "adult_interval_days": 365, "adult_interval_label": "Yılda bir (risk bazlı)",
        "notes": "1 yaş altı tüm kediler için temel. Aşı öncesi FeLV testi önerilir.",
    },
    "Bordetella": {
        "full_name": "Bordetella bronchiseptica",
        "tr_name": "Bordetella", "category": "non-core", "category_tr": "Opsiyonel",
        "components": "Bordetella bronchiseptica", "kitten_weeks": [8],
        "adult_interval_days": 365, "adult_interval_label": "Yılda bir",
        "notes": "Tek intranazal doz. Barınak/pansiyon kedileri için.",
    },
    "Chlamydia": {
        "full_name": "Chlamydia felis",
        "tr_name": "Klamidya", "category": "non-core", "category_tr": "Opsiyonel",
        "components": "Chlamydia felis", "kitten_weeks": [9, 12],
        "adult_interval_days": 365, "adult_interval_label": "Yılda bir",
        "notes": "Çoklu kedi evlerinde klamidya geçmişi varsa önerilir.",
    },
    "FIP": {
        "full_name": "Feline Infectious Peritonitis",
        "tr_name": "FIP Aşısı", "category": "not_recommended", "category_tr": "Önerilmiyor",
        "components": "Feline Coronavirus", "kitten_weeks": [],
        "adult_interval_days": 0, "adult_interval_label": "—",
        "notes": "WSAVA & AAFP: Yeterli kanıt yok, önerilmiyor.",
    },
}

PARASITE_SCHEDULE = {
    "İç Parazit (Yavru)":    {"interval_days": 14, "label": "2 haftada bir"},
    "İç Parazit (Yetişkin)": {"interval_days": 30, "label": "Ayda bir"},
    "Dış Parazit (Pire)":    {"interval_days": 30, "label": "Ayda bir"},
    "Dış Parazit (Kene)":    {"interval_days": 30, "label": "Ayda bir"},
    "Kalp Kurdu":            {"interval_days": 30, "label": "Ayda bir"},
}

KITTEN_SCHEDULE = [
    ("6 hafta", "FVRCP #1"),
    ("8 hafta", "FVRCP #2 + FeLV #1"),
    ("9 hafta", "Chlamydia #1 (gerekirse)"),
    ("12 hafta", "FVRCP #3 + FeLV #2 + Kuduz #1"),
    ("16 hafta", "FVRCP #4 (son yavru doz)"),
    ("26 hafta", "FVRCP ek rapel (WSAVA/AAFP)"),
]

SECTIONS = [
    ("🏠  Pano",              "dashboard"),
    ("👤  Profil",            "profile"),
    ("💉  Aşı Takvimi",       "vaccine"),
    ("📅  Yıllık Takvim",     "calendar"),
    ("📋  Aşı Rehberi",       "guide"),
    ("🐛  Parazit Takvimi",   "parasite"),
    ("💊  İlaç Takibi",       "medications"),
    ("📆  Randevular",        "appointments"),
    ("🍖  Beslenme & Kilo",   "nutrition"),
    ("🏥  Sağlık Notları",    "health"),
    ("💰  Harcamalar",        "expenses"),
    ("📊  İstatistikler",     "stats"),
    ("🏥  Veterinerler",      "vets"),
]
