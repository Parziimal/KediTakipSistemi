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

# ── Köpek verileri ────────────────────────────────────────────────────────────
DOG_BREEDS = [
    "Karışık / Melez", "Labrador Retriever", "Golden Retriever", "Alman Çoban Köpeği",
    "Bulldog", "Beagle", "Poodle (Kaniş)", "Rottweiler", "Yorkshire Terrier", "Boxer",
    "Dachshund (Sosis Köpeği)", "Siberian Husky", "Great Dane", "Dobermann", "Shih Tzu",
    "Border Collie", "Australian Shepherd", "Cavalier King Charles Spaniel", "Pomeranian",
    "Maltese", "Chihuahua", "Akita", "Samoyed", "Chow Chow", "Basset Hound",
    "Cocker Spaniel", "Dalmaçyalı", "Jack Russell Terrier", "Weimaraner",
    "Bernese Mountain Dog", "Belçika Malinois", "Irish Setter", "Shar Pei",
    "Kangal", "Anadolu Çoban Köpeği", "Diğer",
]
DOG_COLORS = [
    "Siyah", "Beyaz", "Sarı / Krem", "Kahverengi", "Gri / Gümüş",
    "Turuncu / Kızıl", "Siyah-Beyaz", "Siyah-Kahve (Tan)", "Benekli (Merle)",
    "Alacalı (Brindle)", "Mavi (Blue)", "Çikolata", "Altın (Golden)", "Krem", "Diğer",
]
DOG_GENDERS = ["Dişi", "Erkek"]
DOG_BLOOD_TYPES = ["DEA 1+ (Pozitif)", "DEA 1- (Negatif)", "Bilinmiyor"]

# ── Kuş verileri ──────────────────────────────────────────────────────────────
BIRD_SPECIES = [
    "Muhabbet Kuşu", "Cennet Papağanı (Lovebird)", "Jako Papağanı (African Grey)",
    "Amazon Papağanı", "Kakadu (Cockatoo)", "Macaw (Ara Papağanı)", "Konur (Conure)",
    "Kanarya", "Ispinoz (Finch)", "Hint Bülbülü (Myna)", "Sultan Papağanı (Cockatiel)",
    "Eclectus Papağanı", "Güvercin", "Bıldırcın", "Diğer",
]
BIRD_COLORS = [
    "Yeşil", "Mavi", "Sarı", "Beyaz", "Gri", "Kırmızı", "Mor",
    "Turuncu", "Siyah", "Çok Renkli (Multicolor)", "Diğer",
]
BIRD_GENDERS = ["Dişi", "Erkek", "Belirsiz"]
BIRD_BLOOD_TYPES = ["Bilinmiyor"]

PET_EMOJIS  = {"cat": "🐱", "dog": "🐶", "bird": "🦜"}
PET_LABELS  = {"cat": "Kedi", "dog": "Köpek", "bird": "Kuş"}

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

# ── WSAVA 2024 & AAHA 2022 — Köpek aşı kılavuzu ─────────────────────────────
DOG_VACCINE_GUIDELINES = {
    "DA2PP": {
        "full_name": "Canine Distemper + Adenovirus-2 + Parvovirus + Parainfluenza (DA2PP / DHPPi)",
        "tr_name": "Kombine Aşı (DA2PP)", "category": "core", "category_tr": "Temel",
        "components": "CDV (Distemper), CAV-2 (Adenovirüs), CPV-2 (Parvovirus), CPiV (Parainfluenza)",
        "kitten_weeks": [7, 10, 14, 17],
        "adult_interval_days": 1095, "adult_interval_label": "3 yılda bir",
        "notes": "Yavru seri: 6–8. haftadan başla, 2–4 haftada bir, 16–18. haftaya kadar "
                 "(yüksek riskli bölgelerde 18–20. hafta önerilir). 26. haftada opsiyonel booster. "
                 "1. yılda rapel; ardından her 3 yılda bir. Kaynak: WSAVA 2024, AAHA 2022.",
    },
    "Kuduz_K": {
        "full_name": "Kuduz Virüsü (Rabies) — İnaktive; 1 yıllık ve 3 yıllık formülasyonlar mevcut",
        "tr_name": "Kuduz Aşısı", "category": "core", "category_tr": "Temel",
        "components": "İnaktive Kuduz virüsü",
        "kitten_weeks": [14],
        "adult_interval_days": 365, "adult_interval_label": "Yılda bir (1 yıllık) / 3 yılda bir (3 yıllık ürün)",
        "notes": "Minimum ≥12. haftada tek doz. İlk dozdan tam 1 yıl sonra zorunlu rapel "
                 "(tüm ürünler için geçerli). Sonraki rapeller ürün etiketine ve yerel yasal "
                 "zorunluluğa göre belirlenir. Kaynak: WSAVA 2024, AAHA 2022.",
    },
    "Leptospirosis": {
        "full_name": "Leptospira interrogans — Dörtlü serovar (L4: Canicola, Icterohaemorrhagiae, Pomona, Grippotyphosa)",
        "tr_name": "Leptospiroz (L4)", "category": "core", "category_tr": "Temel",
        "components": "İnaktive Leptospira bacterin — 4 serovar",
        "kitten_weeks": [14, 16],
        "adult_interval_days": 365, "adult_interval_label": "Yılda bir",
        "notes": "AAHA 2024: Tüm köpekler için TEMEL olarak güncellendi. "
                 "Minimum ≥12. haftada başla; ikinci doz 2–4 hafta sonra (2 dozluk başlangıç serisi zorunlu). "
                 "Tek doz tam koruma sağlamaz. Kaynak: AAHA 2022/2024, WSAVA 2024.",
    },
    "Bordetella_K": {
        "full_name": "Bordetella bronchiseptica (tercihen CPiV ve CAV-2 ile kombine ürün)",
        "tr_name": "Kennel Cough / Bordetella", "category": "non-core", "category_tr": "Opsiyonel",
        "components": "Bordetella bronchiseptica — intranasal/oral canlı veya enjektabl inaktive",
        "kitten_weeks": [8],
        "adult_interval_days": 365, "adult_interval_label": "Yılda bir (yüksek riskli ortam: 6 ayda bir)",
        "notes": "Pansiyon, barınak, köpek parkı, gösteri gibi sosyal ortamlardaki köpekler için. "
                 "İntranasal/oral: tek doz (≥3–4 hafta); enjektabl: 2 doz (2–4 hafta arayla, ≥8 hafta). "
                 "AAHA: Kombine ürün (Bb+CPiV±CAV-2) tek bileşenli ürünlere tercih edilmeli. "
                 "Kaynak: AAHA 2022.",
    },
    "Lyme": {
        "full_name": "Borrelia burgdorferi — Lyme Hastalığı (Rekombinant OspA veya tam hücreli bacterin)",
        "tr_name": "Lyme Hastalığı (Borrelia)", "category": "non-core", "category_tr": "Opsiyonel",
        "components": "Rekombinant OspA proteini veya tam hücreli Borrelia bacterin",
        "kitten_weeks": [10, 14],
        "adult_interval_days": 365, "adult_interval_label": "Yılda bir",
        "notes": "Kene açısından endemik bölgelerde (Kuzey Amerika, Kuzey Avrupa) veya bu bölgelere "
                 "seyahat eden köpekler için. 2 dozluk başlangıç serisi (2–4 hafta arayla). "
                 "Endemik alana girmeden ≥2–4 hafta önce tamamlanmalı. "
                 "Kene önleme programıyla birlikte kullanılmalı. Kaynak: AAHA 2022.",
    },
    "CanineInfluenza": {
        "full_name": "Canine Influenza Virus H3N8 + H3N2 — Bivalent İnaktive",
        "tr_name": "Köpek Gribi (CIV Bivalent)", "category": "non-core", "category_tr": "Opsiyonel",
        "components": "İnaktive bivalent CIV (H3N8 + H3N2)",
        "kitten_weeks": [10, 13],
        "adult_interval_days": 365, "adult_interval_label": "Yılda bir",
        "notes": "2 dozluk başlangıç serisi (2–4 hafta arayla). Pansiyon, köpek okulu, gösteri gibi "
                 "yoğun sosyal ortamlardaki köpekler için risk-bazlı yaklaşımla önerilir. "
                 "Tüm köpeklere rutin olarak önerilmez. Kaynak: AAHA 2022.",
    },
    "CCV_K": {
        "full_name": "Canine Coronavirus (CCV) — Bağırsak Tipi",
        "tr_name": "Köpek Coronavirüsü (CCV)", "category": "not_recommended", "category_tr": "Önerilmiyor",
        "components": "İnaktive CCV",
        "kitten_weeks": [],
        "adult_interval_days": 0, "adult_interval_label": "—",
        "notes": "WSAVA 2024: CCV'nin doğrulanmış hastalık prevalansı mevcut aşıların kullanımını "
                 "haklı kılmamaktadır. İmmünkompetan köpeklerde yalnızca hafif, kendi kendini "
                 "sınırlayan gastroenterit yapar. Klinik fayda kanıtı yetersiz. Kaynak: WSAVA 2024.",
    },
}

DOG_PUPPY_SCHEDULE = [
    ("6–8 hafta",        "DA2PP #1 — İlk doz"),
    ("9–11 hafta",       "DA2PP #2"),
    ("12–16 hafta",      "DA2PP #3 + Kuduz #1 (≥12. hafta) + Leptospiroz #1 (≥12. hafta)"),
    ("14–16 hafta",      "Leptospiroz #2 (ilkten 2–4 hafta sonra) ± Lyme #1 (endemik bölgeyse)"),
    ("16–18 hafta",      "DA2PP #4 — yüksek riskli bölgelerde 18–20. haftaya kadar uzat"),
    ("26 hafta",         "DA2PP opsiyonel booster — anne antikoru girişimini kapatır (WSAVA öneri)"),
    ("52 hafta (1 yıl)", "Tüm aşı boosterleri + Kuduz zorunlu ilk rapeli"),
]

DOG_PARASITE_SCHEDULE = {
    "İç Parazit (Standart)":    {"interval_days": 90,  "label": "3 ayda bir (yılda 4×)"},
    "İç Parazit (Yüksek Risk)": {"interval_days": 30,  "label": "Ayda bir (ham et/avcı köpek)"},
    "Dış Parazit (Pire)":       {"interval_days": 30,  "label": "Ayda bir — yıl boyu"},
    "Dış Parazit (Kene)":       {"interval_days": 30,  "label": "Ayda bir — yıl boyu"},
    "Kalp Kurdu (Aylık ürün)":  {"interval_days": 30,  "label": "Ayda bir — yıl boyu"},
    "Kalp Kurdu (ProHeart 6)":  {"interval_days": 180, "label": "6 ayda bir"},
    "Kalp Kurdu (ProHeart 12)": {"interval_days": 365, "label": "Yılda bir"},
}

# ── AAV — Kuş aşı kılavuzu ───────────────────────────────────────────────────
BIRD_VACCINE_GUIDELINES = {
    "Polyomavirus": {
        "full_name": "Avian Polyomavirus (APV) — Psittimune APV",
        "tr_name": "Polyomavirus Aşısı (APV)", "category": "core",
        "category_tr": "Temel (Psittasin Papağanlar)",
        "components": "İnaktive Avian Polyomavirus — subkutan enjeksiyon",
        "kitten_weeks": [5, 7],
        "adult_interval_days": 365, "adult_interval_label": "Yılda bir",
        "notes": "Jako, kakadu, macaw, kakariki, konur, sultan papağanı ve benzerlerine uygulanır. "
                 "⚠ Muhabbet kuşunda (Melopsittacus undulatus) KESİNLİKLE KONTRENDİKE. "
                 "İlk doz: ≥5 hafta (35 gün); ikinci doz 2–3 hafta sonra. "
                 "Yetişkin yıllık rapel özellikle çoklu kuş ortamlarında önerilir. "
                 "Kaynak: AAV — Association of Avian Veterinarians.",
    },
    "NewcastleDisease": {
        "full_name": "Avian Paramyxovirus Type 1 (APMV-1) / Newcastle Hastalığı — LaSota suşu",
        "tr_name": "Newcastle Hastalığı (NDV)", "category": "non-core",
        "category_tr": "Opsiyonel (Güvercin / Kümes)",
        "components": "LaSota suşu — canlı attenüe veya inaktive",
        "kitten_weeks": [],
        "adult_interval_days": 365, "adult_interval_label": "Yılda bir",
        "notes": "Yalnızca yarışmacı güvercinler ve açık hava kümes hayvanları için. "
                 "Psittasin papağanlarda KESİNLİKLE ÖNERİLMEZ — MLV suşları hastalığa yol açabilir. "
                 "Kaynak: AAV.",
    },
    "WestNile": {
        "full_name": "West Nile Virüsü — At kökenli aşı, etiket dışı kullanım",
        "tr_name": "West Nile Virüsü", "category": "not_recommended",
        "category_tr": "Yalnızca Zoo / Koleksiyon",
        "components": "İnaktive WNV (etiket dışı at aşısı)",
        "kitten_weeks": [],
        "adult_interval_days": 0, "adult_interval_label": "—",
        "notes": "Yalnızca zoo koleksiyonlarında (turna, flamingo, karga türleri) değerlendirilir. "
                 "Ev papağanları ve standart evcil kuşlar için lisanslı ürün mevcut değil. "
                 "Rutin kullanım önerilmez. Kaynak: AAV.",
    },
}

BIRD_CARE_SCHEDULE = [
    ("6–12 ay",                 "Rutin veteriner kontrolü — genel sağlık, kilo, tüy ve gaga muayenesi"),
    ("6–12 ay",                 "Dışkı testi — Gram lekesi + parazit taraması (yeni kuş: edinimden 2–3 gün içinde)"),
    ("12–24 ay",                "Kan tahlili — CBC + kimyasal panel (5 yaş üstü kuşlarda yıllık önerilir)"),
    ("1–3 ay",                  "Tırnak bakımı — türe, tünek yüzeyine ve bireysel aşınmaya göre değişir"),
    ("Tüy dökümü döneminde",    "Vitamin A takviyesi + misting (ıslatma) sıklığını artır; diyet optimizasyonu öncelikli"),
    ("Gerektiğinde",            "Gaga bakımı — SADECE aşırı büyüme veya hastalık belirtisi varsa; rutin tıraş yapılmaz"),
    ("Her veteriner ziyaretinde", "Dış parazit kontrolü — kırmızı akar (Dermanyssus), tüy akarı, kaşıntılı bit"),
]

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
    ("🖼  Galeri",            "gallery"),
    ("⚙  Ayarlar",           "settings"),
]

# Sidebar menü gruplandırması
SECTION_MAP = {
    "dashboard":    ("🏠", "Pano"),
    "profile":      ("👤", "Profil"),
    "gallery":      ("🖼", "Galeri"),
    "vaccine":      ("💉", "Aşı Takvimi"),
    "parasite":     ("🐛", "Parazit Takvimi"),
    "medications":  ("💊", "İlaç Takibi"),
    "appointments": ("📆", "Randevular"),
    "health":       ("🏥", "Sağlık Notları"),
    "nutrition":    ("🍖", "Beslenme & Kilo"),
    "expenses":     ("💰", "Harcamalar"),
    "calendar":     ("📅", "Yıllık Takvim"),
    "guide":        ("📋", "Aşı Rehberi"),
    "stats":        ("📊", "İstatistikler"),
    "vets":         ("🩺", "Veterinerler"),
    "settings":     ("⚙", "Ayarlar"),
}

SECTION_GROUPS = [
    ("Hayvan",  ["dashboard", "profile", "gallery"]),
    ("Sağlık",  ["vaccine", "parasite", "medications", "appointments", "health"]),
    ("Takip",   ["nutrition", "expenses", "calendar"]),
    ("Bilgi",   ["guide", "stats", "vets", "settings"]),
]
